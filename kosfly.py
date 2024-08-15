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

day = 1
def random_sleep(min_seconds=1, max_seconds=5):
    time.sleep(random.uniform(min_seconds, max_seconds))

def extract_flight_info(page_html, target_date):
    soup = BeautifulSoup(page_html, 'html.parser')
    flights = []


    # Select all rows in the table
    rows = soup.select('table.flug_auswahl tr.flugzeile, table.flug_auswahl tr.ausgewaehlterFlug')
    print(f"Found {len(rows)} rows in the flight table.")

    for row in rows:
        # Extract date from the row
        date_cell = row.select_one('td.ab_datum')
        if date_cell:
            flight_date = date_cell.get_text(strip=True)
            print(flight_date)
            print(f"Checking flight date: {flight_date}")
            flight_date_part = flight_date.split(' ')[1]
            # Check if this is the desired date
            if target_date == flight_date_part:
                print(f"Match found for date: {target_date}")
                # Extract flight details
                time_cell = row.select_one('td.ab_an')
                flight_number_cell = row.select_one('td.carrier_flugnr')
                price_cell = row.select_one('td.b_ges_preis')

                price_text = price_cell.get_text(strip=True) if price_cell else 'N/A'
                price_text = price_text.replace('€', '').replace(',', '.').strip()
                price_text = price_cell.get_text(strip=True) if price_cell else 'N/A'
                if price_text.lower() == 'sold out':
                    price = None
                else:
                    price_text = price_text.replace('€', '').replace(',', '.').strip()
                    price = float(price_text) if price_text != 'N/A' else 'N/A'

                flight = {
                    'date': flight_date,
                    'time': time_cell.get_text(strip=True) if time_cell else 'N/A',
                    'flight_number': flight_number_cell.get_text(strip=True) if flight_number_cell else 'N/A',
                    'price': price
                }
                flights.append(flight)
    
    return flights

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set to True to run headlessly
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            extra_http_headers={
                'Accept-Language': 'en-US,en;q=0.9',
                'Connection': 'keep-alive',
                'DNT': '1',
            }
        )
        page = context.new_page()

        url = 'https://www.kosova-fly.de/'
        page.goto(url)
        random_sleep(2, 3)

        # Click the "Njëdrejtimshe" (one-way) radio button
        page.click('input[value="ow"]')

        # Select the "Nisja nga" (Departure from) dropdown
        page.select_option('select[name="VON"]', value='PRN')

        # Select the "Kthimi" (Return to) dropdown
        page.select_option('select[name="NACH"]', value='DUS')

        # Set the departure date to 03.08
           # Set the departure date to 03.08
        target_date = (datetime.now() + timedelta(day)).strftime('%d.%m')
        page.fill('input[name="DATUM_HIN"]', target_date)

        # Click the search button
        button_selector = 'a#buchen_aktion'

        # Wait for the button to be visible
        page.wait_for_selector(button_selector, state='visible')
        
        # Click the search button
        page.click(button_selector)
        
        # Wait for the page to load or content to update
        page.wait_for_load_state('networkidle')

        random_sleep(2, 3)

        page_html = page.content()
        flights = extract_flight_info(page_html, target_date)

        if flights:
            print("Flight information extracted:")
            for flight in flights:
                 print(f"Date: {flight['date']}, Time: {flight['time']}, Flight Number: {flight['flight_number']}, Price: {flight['price']}")
        else:
            print("No flights found for the specified date.")

        # Save the flight information to a JSON file
        with open('flights.json', 'w') as json_file:
            json.dump(flights, json_file, indent=4)
            print("Flight information saved to flights.json")

        save_flights(flights, "Prishtina", "Düsseldorf" , day ,url)
        print("Flight information saved to flights.db")
        
        time.sleep(5)
        browser.close()

if __name__ == "__main__":
    main()
