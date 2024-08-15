from datetime import datetime, timedelta
import json
import os
import random
import time
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from database import save_flights

load_dotenv()

def random_sleep(min_seconds=1, max_seconds=2):
    time.sleep(random.uniform(min_seconds, max_seconds))

def extract_flight_info(page_html):
    soup = BeautifulSoup(page_html, 'html.parser')
    flights = []

    flight_rows = soup.select('label.flight_info_content')
    for flight_row in flight_rows:
        price_div = flight_row.select_one('div.price_content h2')
        airline_div = flight_row.select_one('div.airlines_company')
        departure_time_div = flight_row.select('div.flight_time_content div.time_content h5')
        date_div = soup.select_one('div.swiper-slide.swiper-slide-active')

    if price_div and airline_div and departure_time_div and date_div:
        price_text = price_div.get_text(strip=True) if price_div else 'N/A'
        price_text = price_text.replace('€', '').replace(',', '.').strip()
        if price_text.lower() == 'sold out':
            price = 'N/A'
        else:
            price = price_text if price_text != 'N/A' else 'N/A'
        
        flight_date = date_div['data-date'] if date_div else 'N/A'
        departure_time = departure_time_div[0].get_text(strip=True) if len(departure_time_div) > 0 else 'N/A'
        arrival_time = departure_time_div[1].get_text(strip=True) if len(departure_time_div) > 1 else 'N/A'
        flight_time = f"{departure_time} - {arrival_time}"

        flights.append({
            'price': price,
            'flight_number': airline_div.get_text(strip=True),
            'time': flight_time,
            'date': flight_date
        })

    return flights

def run_flyska_ticket_script():
    airport_pairs = [
        ('PRN', 'DUS'),
        ('PRN', 'MUC'),
        ('DUS', 'PRN'),
        ('MUC', 'PRN')
    ]

    for departure, arrival in airport_pairs:
        for day in range(1, 8):
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)  # Set to True to run headlessly
                context = browser.new_context(
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    extra_http_headers={
                        'Accept-Language': 'en-US,en;q=0.9',
                        'Connection': 'keep-alive',
                        'DNT': '1',
                    }
                )
                page = context.new_page()

                url = 'https://prod.flyksa.com/sq'
                page.goto(url)
                random_sleep(1, 2)

                # Click on the "One Way" option
                page.click('input#oneWay')

                page.click('div.from_holder.choose_directions .choices')

                # Click on the departure option
                page.click(f'div.choices__item[data-value="{departure}"]')

                # Select arrival
                page.click('div.to_holder.choose_directions .choices')
                page.click(f'div.to_holder div.choices__item[data-value="{arrival}"]', timeout=10000)

                # Get the target date in the required format
                page.click('#outdate')
                time.sleep(1)

                target_date = datetime.now() + timedelta(days=day)
                target_date_str = target_date.strftime('%Y-%m-%d')
                target_date_obj = datetime.strptime(target_date_str, '%Y-%m-%d')

                day_selector = f'div.day.unit[data-time="{int(target_date_obj.timestamp()) * 1000}"]'
                page.click(day_selector)
                time.sleep(1)

                # Click the search button        
                page.click('button:has-text("Kërko fluturim")')

                random_sleep(3, 6)

                page_html = page.content()
                flights = extract_flight_info(page_html)
                # Save the flight information to the database
                save_flights(flights, departure, arrival, day, url)
                print(f"Flight information saved for {departure} to {arrival} on day {day}")

                browser.close()

if __name__ == "__main__":
    flights = run_flyska_ticket_script()
