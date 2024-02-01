import customtkinter as ctk
from tkinter import messagebox
from widgets import OptionMenu, EntryBox, Frame
from settings import *
import requests
from currency_symbols import CurrencySymbols
from time import sleep
import sys
import os
from PIL import Image, ImageTk


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# This class handles real-time currency conversion
class RealTimeCurrencyConverter:
    def __init__(self, api_url, max_retries=3, retry_delay=1):
        self.api_url = api_url
        self.max_retries = max_retries
        self.retry_delay = retry_delay

        for tries in range(self.max_retries):
            try:
                response = requests.get(f"{api_url}/rates", timeout=10)
                response.raise_for_status()
                data = response.json()
                self.currencies = data["rates"]
                self.currency_list = list(self.currencies.keys())
                break
            except Exception as e:
                # messagebox.showerror("Error", f"Attempt {tries+1} api request failed")
                sleep(self.retry_delay)
        else:
            messagebox.showerror(
                "Error", "API is not responding. Please try again later."
            )
            self.currencies = {}
            self.currency_list = []

    def convert(self, from_currency, to_currency, amount):
        try:
            response = requests.get(
                f"{self.api_url}/convert",
                params={"from": from_currency, "to": to_currency, "amount": amount},
            )
            response.raise_for_status()
            data = response.json()
            return data["converted_amount"]
        except Exception as e:
            print(e)
            return None


# This class represents the main application
class App(ctk.CTk):
    def __init__(self, converter):
        super().__init__()
        self.currency_converter = converter
        self.setup_ui()
        self.perform_conversion()
        self.mainloop()

    # Set up the user interface
    def setup_ui(self):
        self.setup_window()
        self.create_widgets()
        self.bind_events()

    # Configure the main application window
    def setup_window(self):
        self.title("Currency Converter")
        SCREEN_WIDTH, SCREEN_HEIGHT = (
            self.winfo_screenwidth(),
            self.winfo_screenheight(),
        )
        x = (SCREEN_WIDTH / 2) - (APP_WIDTH / 2)
        y = (SCREEN_HEIGHT / 2) - (APP_HEIGHT / 2)
        self.geometry(f"{APP_WIDTH}x{APP_HEIGHT}+{int(x)}+{int(y)}")
        self.minsize(MIN_WIDTH, MIN_HEIGHT)
        self.resizable(False, False)

        # Use resource_path to get the correct path for the icon
        icon_path = resource_path("dollar note.ico")

        try:
            # mac's ):
            if sys.platform == "darwin":
                img = Image.open(icon_path)
                photo = ImageTk.PhotoImage(img)
                self.tk.call("wm", "iconphoto", self._w, photo)

            else:
                self.iconbitmap("dollar note.ico")

        except Exception as e:
            print(f"Error loading icon: {e}")

    # Create the UI widgets
    def create_widgets(self):
        self.heading_font = ctk.CTkFont(
            family=HEADING_FONT, size=HEADING_FONT_SIZE, weight=HEADING_FONT_WEIGHT
        )
        self.currency_font = ctk.CTkFont(family=CURRENCY_FONT, size=CURRENCY_FONT_SIZE)

        ctk.CTkLabel(self, text="Currency Converter", font=self.heading_font).place(
            relx=0.5, y=30, anchor="center"
        )
        self.main_frame = Frame(self, width=350)
        self.main_frame.place(relx=0.5, y=100, anchor="n")

        self.options_boxes()
        self.entry_boxes()

        # Initialize and place the currency icon labels
        self.from_currency_icon = ctk.CTkLabel(self.main_frame, font=self.currency_font)
        self.from_currency_icon.place(x=5, y=70)

        self.to_currency_icon = ctk.CTkLabel(self.main_frame, font=self.currency_font)
        self.to_currency_icon.place(x=185, y=70)

        self.update_currency_icon(
            self.from_variable, self.from_currency_icon, self.from_entry_box
        )
        self.update_currency_icon(
            self.to_variable, self.to_currency_icon, self.to_entry_box
        )

    # Create option selection boxes for currency conversion
    def options_boxes(self):
        self.from_variable = ctk.StringVar(self, "GBP")
        self.to_variable = ctk.StringVar(self, "USD")
        self.currency_list = sorted(
            [
                "GBP",
                "INR",
                "TRY",
                "USD",
                "AUD",
                "JPY",
                "EUR",
                "CZK",
                "UAH",
                "BRL",
                "ARS",
                "RUB",
            ]
        )

        self.from_options_box = OptionMenu(
            self.main_frame,
            values=self.currency_list,
            font=self.currency_font,
            variable=self.from_variable,
            fg_color=FG_COLOUR,
            button_color=BUTTON_COLOR,
            button_hover_color=BUTTON_COLOR_HOVER,
        )
        self.from_options_box.place(x=20)

        self.to_options_box = OptionMenu(
            self.main_frame,
            values=self.currency_list,
            font=self.currency_font,
            variable=self.to_variable,
            fg_color=FG_COLOUR,
            button_color=BUTTON_COLOR,
            button_hover_color=BUTTON_COLOR_HOVER,
        )
        self.to_options_box.place(x=200)

    # Create entry boxes for entering currency amounts
    def entry_boxes(self):
        validate_num = (self.register(self.validate_float), "%P", "%d")
        self.from_amount = ctk.StringVar(self, "1")
        self.to_amount = ctk.DoubleVar(self)

        self.from_entry_box = EntryBox(
            self.main_frame,
            font=self.currency_font,
            validate="key",
            validatecommand=validate_num,
            textvariable=self.from_amount,
        )
        self.from_entry_box.place(x=20, y=70)

        try:
            self.from_amount.trace("w", lambda *args: self.perform_conversion())
        except Exception as e:
            print(e)

        self.to_entry_box = EntryBox(
            self.main_frame,
            state="disabled",
            font=self.currency_font,
            textvariable=self.to_amount,
        )
        self.to_entry_box.place(x=200, y=70)

    # Bind events to update currency icons and perform conversions
    def bind_events(self):
        self.from_variable.trace(
            "w",
            lambda *args: self.update_currency_icon(
                self.from_variable, self.from_currency_icon, self.from_entry_box
            ),
        )
        self.to_variable.trace(
            "w",
            lambda *args: self.update_currency_icon(
                self.to_variable, self.to_currency_icon, self.to_entry_box
            ),
        )

    # Update currency icons based on selected currencies
    def update_currency_icon(self, currency_variable, label_widget, entry_box):
        currency_code = currency_variable.get()
        currency_symbol = self.get_currency_symbol(currency_code)

        label_widget.configure(text=currency_symbol, width=10, anchor="e")

        place_info = entry_box.place_info()

        if currency_code == "BRL" or currency_code == "CZK":
            entry_box.place_configure(x=int(place_info["x"]) + 10)
        else:
            if entry_box is self.to_entry_box:
                entry_box.place_configure(x=200)
            else:
                entry_box.place_configure(x=20)

        label_widget.configure(text=currency_symbol)
        self.perform_conversion()

    # Get the currency symbol based on the currency code
    def get_currency_symbol(self, currency_code):
        c = CurrencySymbols()
        symbol = c.get_symbol(currency_code)
        return symbol

    # Validate input to allow only numeric values
    def validate_float(self, value, action_type):
        if action_type == "1":  # insertion
            try:
                float(value)
                return True
            except ValueError:
                messagebox.showerror("Error", "Only numbers are allowed")
                return False
        return True

    # Perform currency conversion when the input changes
    def perform_conversion(self):
        try:
            amount = float(self.from_amount.get())
        except ValueError:
            amount = 0

        from_currency = self.from_variable.get()
        to_currency = self.to_variable.get()
        converted_amount = self.currency_converter.convert(
            from_currency, to_currency, amount
        )
        self.to_amount.set(converted_amount)


# Entry point of the application
if __name__ == "__main__":
    api_url = "https://salty-hollows-99370-c2cc07dd6680.herokuapp.com/"
    converter = RealTimeCurrencyConverter(api_url)
    App(converter)
