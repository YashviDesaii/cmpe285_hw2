from flask import Flask, render_template, request
from alpha_vantage.timeseries import TimeSeries
import datetime
import pytz
import requests

app = Flask(__name__)
def get_company_name(symbol, api_key):
    try:
        # Make an API call to get the full company name based on the symbol
        url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={symbol}&apikey={api_key}"
        response = requests.get(url)
        data = response.json()
        
        if 'bestMatches' in data:
            matches = data['bestMatches']
            if matches:
                # Use the first match's name
                return matches[0]['2. name']
        return "Company Name Not Found"

    except Exception as e:
        return f"Error: {e}"

def get_stock_info(symbol, api_key):
    try:
        # Initialize the Alpha Vantage API client
        ts = TimeSeries(key=api_key, output_format='pandas')

        # Retrieve stock data
        data, _ = ts.get_quote_endpoint(symbol=symbol)

        # Extract relevant information
        current_time = datetime.datetime.now(pytz.timezone('US/Pacific'))
        formatted_time = current_time.strftime('%a %b %d %H:%M:%S PDT %Y')

        #company_name = data['01. symbol'].values[0]
        company_name = get_company_name(symbol, api_key)
        stock_price = float(data['05. price'].values[0])
        value_change = float(data['09. change'].values[0])
        percentage_change = float(data['10. change percent'].values[0].replace('%', ''))
        output = "{}\n{}\n{:.2f} {:.2f} ({:.2f}%)".format(formatted_time, company_name + " " "(" + symbol + ")", stock_price, value_change, percentage_change)

        return output

    except Exception as e:
        return f"An error occurred: {e}"

@app.route('/', methods=['GET', 'POST'])
def stock_info():
    if request.method == 'POST':
        symbol = request.form['symbol']
        api_key = "64ASG3BHV8WFGY68"  
        stock_info = get_stock_info(symbol, api_key)
        return render_template('stock_info.html', stock_info=stock_info)

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
