# Currency Converter (Python, Tkinter, APIs)

![Screenshot (106)](https://github.com/jaydeep080805/Currency-Converter/assets/64449369/68471a72-c673-4121-8dd9-4b129a5bc55f)

A real-time currency converter GUI application built using Python and the Tkinter library. The application fetches currency conversion rates from an external API and allows users to convert an amount from one currency to another. Users can select the source currency, target currency, and enter the amount to be converted. The converted amount is displayed instantly on the screen. The application supports a range of currencies and ensures error handling for invalid input.

### Technologies and Libraries:
- Python
- Tkinter (GUI framework)
- requests (HTTP library for API calls)
- forex_python.converter (Currency conversion library)
- currency_symbols (Library to fetch currency symbols)

### Features:
- Fetches real-time currency conversion rates from an external API.
- Provides a user-friendly GUI interface for currency conversion.
- Supports a variety of currencies, including GBP, INR, TRY, USD, AUD, JPY, EUR, CZK, UAH, BRL, ARS, RUB.
- Validates user input to ensure proper conversion.
- Automatically updates currency symbols in the GUI based on the selected currencies.

### How To Run Locally:
- navigate to the directory you would like to use the app in
- setup a virtual environment: 
  - ```python -m venv venv```
- activate the virtual environment:
- on windows:
  - ```venv/Scripts/activate```
- on mac:
  - ```source venv/bin/activate```
- install the dependencies ```pip install -r requirements.txt```
- create a .env file with one variable "ACCESS_KEY" which is needed for http://api.exchangeratesapi.io/
- run the app ```python main.py```
