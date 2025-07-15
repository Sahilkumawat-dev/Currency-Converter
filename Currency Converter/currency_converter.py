import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# using API
API_URL = "https://api.exchangerate-api.com/v4/latest/USD"

# NotesSociety

def get_exchange_rates():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            return response.json()['rates']
        else:
            return None
    except Exception as e:
        print(f"Error fetching exchange rates: {e}")
        return None

@app.route('/')
def index():
    rates = get_exchange_rates()
    if not rates:
        return "Error fetching exchange rates. Please try again later."
    return render_template('index.html', currencies=rates.keys())
    # NotesSociety

@app.route('/convert', methods=['POST'])
def convert():
    try:
        rates = get_exchange_rates()
        if not rates:
            return jsonify({"error": "Error fetching exchange rates"}), 500

        amount = request.form['amount']
        from_currency = request.form['from_currency'].upper()
        to_currency = request.form['to_currency'].upper()

        # check if number is valid
        try:
            amount = float(amount)
        except ValueError:
            return jsonify({"error": "Invalid amount entered"}), 400
            # NotesSociety

        if from_currency not in rates or to_currency not in rates:
            return jsonify({"error": "Invalid currency code"}), 400

        # Conversion logic
        converted_amount = round(amount * rates[to_currency] / rates[from_currency], 2)
        return jsonify({"converted_amount": converted_amount})

    except Exception as e:
        print(f"Error during conversion: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500
    # NotesSociety
if __name__ == '__main__':
    app.run(debug=True)
