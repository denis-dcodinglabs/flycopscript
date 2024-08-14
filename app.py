from flask import Flask, jsonify
from rfly import scrape_flights

app = Flask(__name__)

@app.route('/scrape_flights', methods=['GET'])
def scrape_flights_endpoint():
    flights = scrape_flights()
    return jsonify(flights)

if __name__ == '__main__':
    app.run(debug=True)