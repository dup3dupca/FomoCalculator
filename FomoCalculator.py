import requests
import pandas as pd
import numpy as np
import yfinance as yf
import datetime
import decimal
import time
import sys 
import select
from pandas import Timestamp
import pytz
import matplotlib.pyplot as plt
import os

#Dates
def get_first_trade_date(ticker):
    ticker_obj = yf.Ticker(ticker)
    hist = ticker_obj.history(period="max")
    return hist.index[0].date()

def set_start_date(first_trade_date):
    if start_date := input(f"Enter a start date (yyyy-mm-dd) since {first_trade_date} or press enter to use first trade date: "):
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
    else:
        start_date=first_trade_date
    return start_date

def set_end_date():
    if end_date := input(f"Enter an end date to calculate from (yyyy-mm-dd) or press enter to use yesterday's date {datetime.date.today()- datetime.timedelta(days=1)}: "):
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
    else:
        end_date=datetime.date.today()
    return end_date

def set_date_format(date):
    return date.strftime('%Y-%m-%d')

def get_lowest_date_price(data):
    low_price = data['Low'].min()
    low_date = data['Low'].idxmin().date()
    return round(low_price,2), set_date_format(low_date)

def get_highest_date_price(data,low_date):
    low_date = datetime.datetime.strptime(str(low_date), "%Y-%m-%d").date()
    subset_data = data.loc[low_date:]
    high_price = subset_data['High'].max()
    high_date = subset_data['High'].idxmax().date()
    return round(high_price,2), set_date_format(high_date)

def set_date_timestamp(date,div):
    timezone = pytz.timezone(str(get_timezone(div)))
    date = Timestamp(date, tz=timezone)
    return date

def get_timezone(div):
    for dividend_date,dividend_amnt in div.items():
        return dividend_date.tzinfo

#Ticker Data
def get_ticker_input():
    while True:
        try:
            ticker = input("Enter Ticker Symbol or 'exit' to return to menu:")
            if ticker == "exit":
                print("\nReturning to main menu...\n")
                main()
            return SearchStock(ticker)
        except Exception:
            continue

def get_ticker_data(ticker,start_date,end_date):
    return yf.download(ticker, start=start_date, end=end_date)

def get_ticker_data_no_progressbar(ticker,start_date,end_date):
    return yf.download(ticker, start=start_date, end=end_date, progress=False)

def get_ticker_long_name(ticker):
    ticker_obj = yf.Ticker(ticker)
    info = ticker_obj.info
    return info['longName']

def get_ticker_currency(ticker):
    ticker_obj = yf.Ticker(ticker)
    info=ticker_obj.info
    return info['currency']

def get_ticker_div_bool(ticker,low_date,high_date):
    ticker_obj=yf.Ticker(ticker)
    div=ticker_obj.dividends
    if div.empty:
        return False
    low_date = set_date_timestamp(low_date,div)
    high_date = set_date_timestamp(high_date,div)
    return any(low_date <= date <= high_date for date in div.index)

#Calculations
def get_multiplier(low_price,high_price):
    multiplier = (decimal.Decimal(high_price) - decimal.Decimal(low_price))/decimal.Decimal(low_price)
    return round(multiplier,3)

def get_percentage(multiplier):
    return round(multiplier*100,2)

# Regular print statements and dividend print statements
def get_print_statements(ticker,div_check,low_price,high_price,currency,longname,low_date,high_date):
    get_lowest_highest_prints(low_price,high_price,currency,low_date,high_date)
    get_div_check(ticker,div_check,low_date,high_date,longname,low_price,high_price)

def get_lowest_highest_prints(low_price,high_price,currency,low_date,high_date):
    print(f"\nThe Lowest price in this stock's history was: ${low_price:,.2f} {currency} on {low_date}")
    print(f"The Highest price in this stock's history was: ${high_price:,.2f} {currency} on {high_date}\n")

def get_div_check(ticker,div_check,low_date,high_date,longname,low_price,high_price):
    if div_check:
        print(f"{longname} did have a dividend during this period\n")
        check_div_low_high_dates(ticker,longname,low_date,high_date,low_price,high_price)
    else:
        print(f"{longname} did not have a dividend during this period\n")
        check_low_high_dates(longname,low_price,high_price) 

def check_low_high_dates(longname,low_price,high_price):
    multiplier=get_multiplier(low_price,high_price)
    percentage=get_percentage(multiplier)
    get_positive_print_statements(longname,multiplier,percentage)

def check_div_low_high_dates(ticker,longname,low_date,high_date,low_price,high_price):
    multiplier=get_multiplier(low_price,high_price)
    payout_multiplier=get_payout_multiplier(ticker,low_date,high_date,low_price,multiplier)
    shares=get_div_reinvest_shares(ticker,low_date,high_date)
    reinvest_multiplier=round(decimal.Decimal(shares)*multiplier,2)
    get_positive_div_print(longname,payout_multiplier,reinvest_multiplier)
 
def get_positive_print_statements(longname,multiplier,percentage):
    print(f"You could have made: {multiplier:,.2f}x times your investment or a {percentage:,.2f}% increase in your capital with {longname}\n")

def get_positive_div_print(longname,payout_multiplier,reinvest_multiplier):
    print(f"You could have made: {payout_multiplier:,.2f}x times your investment or a {payout_multiplier*100:,.2f}% increase in your capital with {longname} including dividend payouts\n")
    print(f"You could have made: {reinvest_multiplier:,.2f}x times your investment or a {reinvest_multiplier*100:,.2f}% increase in your capital with {longname} including dividend reinvestment\n")
    
#Div calculations

def get_payout_multiplier(ticker,low_date,high_date,low_price,multiplier):
    payout=get_div_payout(ticker,low_date,high_date)
    payout_mult=round(payout/low_price,2)
    return decimal.Decimal(payout_mult)+multiplier

def get_div_reinvest_shares(ticker,low_date,high_date):
    ticker_obj = yf.Ticker(ticker)
    hist_data = ticker_obj.history(start=low_date, end=high_date)
    shares = 1 
    div = ticker_obj.dividends
    for dividend_date, dividend_amount in div.items():
        dividend_date = dividend_date.strftime('%Y-%m-%d')
        if low_date <= dividend_date <= high_date:
            close_price = hist_data.loc[dividend_date, "Close"]
            shares_purchased = dividend_amount / close_price
            shares += shares_purchased
    return round(shares,2)

def get_div_payout(ticker, low_date, high_date):
    ticker_obj = yf.Ticker(ticker)
    div = ticker_obj.dividends
    low_date = set_date_timestamp(low_date,div)
    high_date = set_date_timestamp(high_date,div)
    div_sum = sum(dividend_amount for dividend_date, dividend_amount in div.items() if low_date <= dividend_date <= high_date)
    return round(div_sum, 2)

def calculate_best_percentage(ticker,div_check,low_price,high_price,low_date,high_date):
    if not div_check:
        return get_percentage(get_multiplier(low_price,high_price))
    multiplier=get_multiplier(low_price,high_price)
    payout_multiplier=get_payout_multiplier(ticker,low_date,high_date,low_price,multiplier)
    shares=get_div_reinvest_shares(ticker,low_date,high_date)
    reinvest_multiplier=round(decimal.Decimal(shares)*multiplier,2)
    return max(payout_multiplier*100, reinvest_multiplier*100)

#Search Functions 
def SearchStock(ticker):
    try:
        first_trade_date=get_first_trade_date(ticker)
        name=get_ticker_long_name(ticker)
        print(f"\nThe first tradeable date for {name} was {first_trade_date}")
        start_date=set_start_date(first_trade_date)
        end_date=set_end_date()
        data = get_ticker_data(ticker,start_date,end_date)
        low_price, low_date = get_lowest_date_price(data)
        high_price,high_date = get_highest_date_price(data,low_date)
        currency=get_ticker_currency(ticker)
        div_check=get_ticker_div_bool(ticker,low_date,high_date)
        get_print_statements(ticker,div_check,low_price,high_price,currency,name,low_date,high_date)      
    except Exception:
        print("Error Processing Ticker Symbol, please try again...\n")
        get_ticker_input()

#compare_sp500 functions

#Main function
def compare_sp500():
# Get the tickers for the S&P 500 and create a dictionary with all S&P500 tickers and their data
    sp500_tickers=read_tickers()
    percentage_list=[]
    print("\nPlease wait, calculating historical data and dividend information for all S&P 500 stocks, this may take a while...\n ")
# Loop through all tickers in the S&P 500
    percentage_list=search_sp500(sp500_tickers,percentage_list)
    df=sort_dataframe(percentage_list)
    print(f"\n{df}\n")
    to_csv(df)

def read_tickers():
    while True:
        option=input("Input 1 if you would like to read tickers from web or 2 to read from our database:")
        if option=="1":
            table=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
            df = table[0]
            return df['Symbol'].tolist()
        elif option=="2":
            script_directory = os.path.dirname(os.path.abspath(__file__))
            relative_path = 'CSVDataFiles/SP500.csv'
            absolute_path = os.path.join(script_directory, relative_path)
            df=pd.read_csv(absolute_path)
            return df['Symbol']
        else:
            print("Please input again\n")

def search_sp500(sp500_tickers,percentage_list):
    total_tickers = len(sp500_tickers)
    start_time=time.time()
    for i, ticker in enumerate(sp500_tickers):
        ticker = ticker.replace('.','-')
        try:
            first_trade_date=get_first_trade_date(ticker)
            data=get_ticker_data_no_progressbar(ticker,first_trade_date,datetime.date.today())
            low_price, low_date = get_lowest_date_price(data)
            high_price,high_date = get_highest_date_price(data,low_date)
            if not low_price or not high_price:
                raise ValueError(f"\nNo data found for {ticker} or symbol may be delisted")
            multiplier=get_multiplier(low_price,high_price)
            percentage=get_percentage(multiplier)
            div_check=get_ticker_div_bool(ticker,low_date,high_date)
            if div_check:
                append_divs(ticker,low_date,high_date,low_price,high_price,percentage_list)
            else:
                percentage_list.append([ticker,multiplier,percentage,low_date,low_price,high_date,high_price])
            progress = (i+1)/total_tickers*100
            elapsed_time = time.time() - start_time
            eta = (elapsed_time / progress) * (100 - progress)
            eta_str = time.strftime('%H:%M:%S', time.gmtime(eta))
            print(f"\rProgress: '${ticker}' {progress:.2f}% ETA: {eta_str} or press 'q' then 'enter' to return to menu: ", end='', flush=True)
            if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                line = input()
                if line.lower() == 'q':
                    print("\nReturning to main menu...\n")
                    main()
        except Exception as e:
            print(f"\rError processing {ticker}: {str(e)}\n", end='', flush=False)
            continue
    elapsed_time=time.time()-start_time
    elapsed_time = time.strftime('%H:%M:%S', time.gmtime(elapsed_time))
    print(f"\nTime taken to complete: {elapsed_time}")
    return percentage_list
   
def append_divs(ticker,low_date,high_date,low_price,high_price,percentage_list):
    payout_multiplier,reinvest_multiplier=get_div_multipliers(ticker,low_date,high_date,low_price,high_price)
    if payout_multiplier > reinvest_multiplier:
        percentage_list.append([ticker,payout_multiplier,payout_multiplier*100,low_date,low_price,high_date,high_price])
    else:
        percentage_list.append([ticker,reinvest_multiplier,reinvest_multiplier*100,low_date,low_price,high_date,high_price])

def get_div_multipliers(ticker,low_date,high_date,low_price,high_price):
    multiplier=get_multiplier(low_price,high_price)
    payout_multiplier=get_payout_multiplier(ticker,low_date,high_date,low_price,multiplier)
    shares=get_div_reinvest_shares(ticker,low_date,high_date)
    reinvest_multiplier=round(decimal.Decimal(shares)*multiplier,2)
    return payout_multiplier,reinvest_multiplier

def sort_dataframe(percentage_list):
    df = pd.DataFrame(percentage_list, columns=['Ticker', 'Multiplier', 'Percentage', 'ATL Date', 'ATL Price', 'ATH Date', 'ATH Price'])
    df = df.sort_values('Percentage', ascending=False)
    df['Ranks'] = range(1, len(df) + 1)
    df['Multiplier'] = df['Multiplier'].apply(lambda x: '{:,.2f}x'.format(x) if x is not None else 'N/A')
    df['Percentage'] = df['Percentage'].apply(lambda x: '{:,.0f}%'.format(x))
    df['ATL Price'] = df['ATL Price'].apply(lambda x: '${:,.2f}'.format(float(x)))
    df['ATH Price'] = df['ATH Price'].apply(lambda x: '${:,.2f}'.format(float(x)))
    return df[['Ranks', 'Ticker', 'Multiplier', 'Percentage', 'ATL Date', 'ATL Price', 'ATH Date', 'ATH Price']]

def to_csv(df):
    csv = input("Would you like to turn this into a .CSV file? (Y/N)")
    if csv.upper()=="Y":
        if name := input("Please input a name for your file, or press enter to use the default 'BestPerformers.csv': "):
            df.to_csv(f'{name}.csv', index=False)
            print(f"Saved as {name}.csv\n")
        else:
            df.to_csv('BestPerformers.csv', index=False)
            print(f"Saved as BestPerformers.csv\n")

#Compare Functions
def compare_stocks():
    while True:
        amnt_stocks = input("Select a number of stocks to compare (1-10): ")
        try:
            amnt_stocks = int(amnt_stocks)
            if 1 <= amnt_stocks <= 10:
                stock_list=pick_stocks(amnt_stocks)
                operations(stock_list)
                break  # Exit the loop if a valid number of stocks is selected
            else:
                print("Invalid input. Please enter a number between 1 and 10.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def pick_stocks(amnt_stocks):
    stock_list = []
    i = 1
    while len(stock_list) < amnt_stocks:
        try:
            ticker = input(f"Enter {get_ordinal_number(i)} ticker symbol or 'exit' to return to menu:")
            if ticker == "exit":
                print("\nReturning to main menu...\n")
                main()
            elif ticker=="":
                print("No input was detected, ",end='')
            else:
                stock_list.append(ticker)
                i += 1
        except Exception:
            continue
    return stock_list

def get_ordinal_number(number):
    suffixes = ['th', 'st', 'nd', 'rd', 'th', 'th', 'th', 'th', 'th', 'th']
    suffix = 'th' if 10 <= number % 100 <= 20 else suffixes[number % 10]
    return f"{number}{suffix}"
       
def operations(stock_list):
    compare_list=[]
    for ticker in stock_list:
        try:
            first_trade_date=get_first_trade_date(ticker)
            data = get_ticker_data_no_progressbar(ticker,first_trade_date,datetime.date.today())
            low_price, low_date = get_lowest_date_price(data)
            high_price,high_date = get_highest_date_price(data,low_date)
            div_check=get_ticker_div_bool(ticker,low_date,high_date)
            percentage=calculate_best_percentage(ticker,div_check,low_price,high_price,low_date,high_date) 
            multiplier=percentage/100
            compare_list.append([ticker,multiplier,percentage,low_date,low_price,high_date,high_price])
            print(f"\rCalculating {ticker}... Please wait ", end='', flush=True)
        except Exception:
            print(f"\nTicker {ticker} not found... Please try again\n")
            stock_list=pick_stocks(len(stock_list))
            operations(stock_list)
            return
    print(f"\n{sort_dataframe(compare_list)}\n")
  
#Dev
def dev_mode():
    ticker="tsla"
    ticker_obj=yf.Ticker(ticker)
    print(ticker_obj.splits)

#Main Menu
def main():
    while True:
        option = input(f"""\
Enter:
1 to search the performance of a stock,
2 to compare each stock in the S&P 500,
3 to compare the performance of stocks,
or 'exit' to quit.
""")
        if option=='1':
            get_ticker_input()
        elif option=='2':
            compare_sp500()
        elif option=='3':
            compare_stocks()
        elif option=='4':
            dev_mode()
        elif option =="exit":
            exit()
        else:
            print("Try a valid option")
            
main()