from currency_symbols import CurrencySymbols
from settings import URL
import requests
from forex_python.converter import CurrencyCodes

data = requests.get(URL).json()
poop = data["rates"]

currencies = [cur for cur in poop.keys()]

c = CurrencySymbols()
for i in currencies:
    print(f"{i} = {c.get_symbol(i)}")
    # print(f"{i} = {c.get_currency_name(i)}")

print(CurrencySymbols.get_symbol("UAH"))
