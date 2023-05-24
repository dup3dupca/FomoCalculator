import requests
import pandas as pd
import numpy as np
import yfinance as yf
import datetime
import decimal
import time
import sys 
import select

#Get Date and Prices functions
def get_first_trade_date_end_date(ticker):
    data=get_ticker_data_no_progressbar(ticker)
    first_trade_date = data.index[1].date()
    current_date = datetime.date.today()
    return first_trade_date,current_date
    
def get_lowest_date_price(data, start_date, end_date):
    lowest_price = float('inf')
    low_date = start_date
    for date, price in data.loc[low_date:end_date, 'Low'].items():
        if price < lowest_price:
            lowest_price = price
            low_date = date
    low_date=low_date.strftime('%Y-%m-%d')
    return lowest_price, low_date

def get_highest_date_price(data, start_date, end_date):
    highest_price = 0
    high_date = end_date
    for date, price in data.loc[start_date:high_date, 'High'].items():
        if price > highest_price:
            highest_price = price
            high_date = date
    high_date=high_date.strftime('%Y-%m-%d')
    return highest_price, high_date

def get_lowest_date_price_entirety(data):
    lowest_price = float('inf')
    low_date = None
    for date, price in data['Low'].items():
        if price < lowest_price:
            lowest_price = price
            low_date = date
    low_date=low_date.strftime('%Y-%m-%d')
    return lowest_price, low_date
    
def get_highest_date_price_entirety(data):
    highest_price = 0
    high_date = None
    for date, price in data['High'].items():
        if price > highest_price:
            highest_price = price
            high_date = date
    high_date=high_date.strftime('%Y-%m-%d')
    return highest_price, high_date

#Get Data Functions
def get_ticker_data(ticker):
    ticker_obj = yf.Ticker(ticker)
# Retrieve the historical price data for the stock
    hist = ticker_obj.history(period="max")
# Extract the date of the first available data point
    first_trade_date = hist.index[0].date()
    current_date = datetime.date.today()
    return yf.download(ticker, start=first_trade_date, end=current_date)

def get_ticker_data_no_progressbar(ticker):
    ticker_obj = yf.Ticker(ticker)
    hist = ticker_obj.history(period="max")
    first_trade_date = hist.index[0].date()
    current_date = datetime.date.today()
    return yf.download(ticker, start=first_trade_date, end=current_date, progress=False)

#Calculate multipliers and percentages
def get_multiplier_percentage_both_divs(ticker,lowest_price, highest_price):
    ticker_obj = yf.Ticker(ticker)
    div=ticker_obj.dividends
    start_date,end_date=get_first_trade_date_end_date(ticker)
    lowest_price=round(lowest_price,2)
    highest_price=round(highest_price,2)
    multiplier = (decimal.Decimal(highest_price) - decimal.Decimal(lowest_price))/decimal.Decimal(lowest_price)
    multiplier = round(multiplier, 2)
    percentage = round(multiplier * 100, 0)
    if div.empty:
        return multiplier,percentage
    payout,shares=dividend(ticker,start_date,end_date)
    payout_multiplier=round(payout/round(lowest_price,2),2)
    new_multiplier=round(multiplier+decimal.Decimal(payout_multiplier),2)
    reinvest_multiplier=round(decimal.Decimal(shares)*multiplier,2)
    return new_multiplier,reinvest_multiplier

def get_multiplier_percentage(ticker,lowest_price, highest_price):
    ticker_obj = yf.Ticker(ticker)
    div=ticker_obj.dividends
    start_date,end_date=get_first_trade_date_end_date(ticker)
    lowest_price=round(lowest_price,2)
    highest_price=round(highest_price,2)
    multiplier = (decimal.Decimal(highest_price) - decimal.Decimal(lowest_price))/decimal.Decimal(lowest_price)
    multiplier = round(multiplier, 2)
    percentage = round(multiplier * 100, 0)
    if div.empty:
        return multiplier,percentage
    payout,shares=dividend(ticker,start_date,end_date)
    payout_multiplier=round(payout/round(lowest_price,2),2)
    new_multiplier=round(multiplier+decimal.Decimal(payout_multiplier),2)
    reinvest_multiplier=round(decimal.Decimal(shares)*multiplier,2)
    return reinvest_multiplier,reinvest_multiplier*100

#Unincorporated feature, can multiply the multiplier by a specific amount      
def calculate_dollar_amount(multiplier):
    dollar = int(input("Input a dollar amount to calculate: $"))
    if dollar <= 0:
        print("No valid value input, heading to main menu...\n")
        return
    total = int(dollar * multiplier)
    print(f"${dollar:,.2f} would be equal to: ${total:,.2f} \n")

#Print statements to use
def print_statements(ticker,low_date,low_price,high_date,high_price):
    ticker_obj = yf.Ticker(ticker)
    div=ticker_obj.dividends
    info=ticker_obj.info
    currency = info['currency']
    name=info['longName']
    if div.empty:
        print(f"\n{ticker.upper()} has no dividend")
        print(f"\nThe Lowest price in this stock's history was: ${low_price:,.2f} {currency} on {low_date}")
        print(f"The Highest price in this stock's history was: ${high_price:,.2f} {currency} on {high_date}")
        if low_date <= high_date:
            multiplier,percentage = get_multiplier_percentage(ticker,low_price,high_price)
            print(f"You could have made: {multiplier:,.2f}x times your investment or a {percentage:,.2f}% increase in your capital with {name}\n")
            return 1
        else:
            percentage=neg_percentage(low_date,low_price,high_date,high_price)
            print(f"You would have lost {percentage:,.2f}% of your capital with {name} during this time period\n")
            return 0
    else:
        print(f"\n{ticker.upper()} has a dividend")
        print(f"\nThe Lowest price during the specified time period was: ${low_price:,.2f} {currency} on {low_date}")
        print(f"The Highest price during the specified time period was: ${high_price:,.2f} {currency} on {high_date}\n")
        if low_date <= high_date:
            new_multiplier,reinvest_multiplier = get_multiplier_percentage_both_divs(ticker,low_price,high_price)
            print(f"\nmultiplier w/ dividend payout: {new_multiplier:,.2f}x, percentage would be {new_multiplier*100:,.2f}%")
            print(f"multiplier w/ dividend reinvesting: {reinvest_multiplier:,.2f}x, percentage would be {reinvest_multiplier*100:,.2f}%\n")
            return 1
        else:
            percentage=neg_percentage(low_date,low_price,high_date,high_price)
            print(f"You would have lost {percentage:,.2f}% of your capital with {name} during this time period\n")
            return 0

#Check if a stock is at its lowest low
def underwater_check(uw1,uw2,ticker1,ticker2,percentage1,percentage2):
    if uw1 == 1 and uw2 == 1:
        if percentage1 > percentage2:
            print(f"{ticker1.upper()} had {percentage1-percentage2:,.2f}% better returns than {ticker2.upper()}\n")
        elif percentage2 > percentage1:
            print(f"{ticker2.upper()} had {percentage2-percentage1:,.2f}% better returns than {ticker1.upper()}\n")    
        else:
            print(f"{ticker1.upper()} had similar returns to {ticker2.upper()}: {percentage1}%")
    if uw2 == 1:
        percentage1=0
        if percentage2 > percentage1:
            print(f"{ticker2.upper()} had {percentage2-percentage1:,.2f}% better returns than {ticker1.upper()}\n")    
        else:
            print(f"{ticker1.upper()} had similar returns to {ticker2.upper()}: {percentage1}%")  
    if uw1 == 1:
        percentage2=0
        if percentage1 > percentage2:
            print(f"{ticker1.upper()} had {percentage1-percentage2:,.2f}% better returns than {ticker2.upper()}\n")
        else:
            print(f"{ticker1.upper()} had similar returns to {ticker2.upper()}: {percentage1}%")  
    if uw1 == 0 and uw2 == 0:
        print(f"Both {ticker1.upper()} and {ticker2.upper()} had horrible returns...\n") 

#Dividend
def dividend(ticker,start_date,end_date):
    ticker_obj = yf.Ticker(ticker)
    div = ticker_obj.dividends
    if not div.empty:
        payout=divvy_payout(div)
        reinvest_shares=divvy_reinvestment(ticker,start_date,end_date)
        return payout,reinvest_shares
    else:
        print("No dividend information is available\n")
        return

#Dividend Payout calculation
def divvy_payout(div):
    return sum(dividend_amount for dividend_date, dividend_amount in div.items())

#Dividend reinvestment calculation
def divvy_reinvestment(ticker,start_date,end_date):
    ticker_obj = yf.Ticker(ticker)
    hist_data = ticker_obj.history(start=start_date, end=end_date)
    data=get_ticker_data_no_progressbar(ticker)
    low_price,low_date=get_lowest_date_price(data,start_date,end_date)
    high_price,high_date=get_highest_date_price(data,start_date,end_date)
    # Calculate the number of shares with dividend reinvestment
    shares = 1  # Initial number of shares
    div = ticker_obj.dividends
    for dividend_date, dividend_amount in div.items():
        dividend_date = dividend_date.strftime('%Y-%m-%d')#Format it to allow for comparison operators
        if low_date <= dividend_date <= high_date:
        # Get the closing price on the dividend date
            close_price = hist_data.loc[dividend_date, "Close"]
        # Calculate the number of shares purchased with the dividend amount
            shares_purchased = dividend_amount / close_price
        # Update the total number of shares
            shares += shares_purchased
    return round(shares,2)

def neg_percentage(low_date,low_price,high_date,high_price):
    if low_date>high_date:
        return (low_price-high_price)/high_price*100
         
#Three main functions
#-----------------------

def SearchStock():
    while True:
        try:
            ticker = input("Enter Ticker Symbol or 'exit' to return to menu:")
            if ticker == "exit":
                return
            data = get_ticker_data(ticker)
            break
        except Exception:
            print(f"Error: Ticker symbol '{ticker}' not found in the yfinance library")
            print("Please only enter the Ticker symbol of the stock\n")
            continue
# create a Ticker object for the specified ticker symbol
    first_trade_date = data.index[1].date()
    current_date = datetime.date.today()
# create ticker object to access info elements(Currency,longName,Dividends,etc..)
    ticker_obj = yf.Ticker(ticker)
    info = ticker_obj.info
    name = info['longName']
# retrieve information about the stock, including the first trade date
    print(f"\nThe first tradeable date for {name} was {first_trade_date}")
# define the start and end dates for the historical data
    if start_date := input(f"Enter a start date (yyyy-mm-dd) since {first_trade_date} or press enter to use first trade date: "):
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
    else:
        start_date=first_trade_date
    if end_date := input(f"Enter an end date to calculate from (yyyy-mm-dd) or press enter to use yesterday's date {current_date- datetime.timedelta(days=1)}: "):
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
    else:
        end_date=current_date
# use the yfinance library to retrieve the historical data for the ticker
    lowest_price, low_date = get_lowest_date_price(data,start_date,end_date)
    highest_price,high_date = get_highest_date_price(data,start_date,end_date)
    print_statements(ticker,low_date,lowest_price,high_date,highest_price)
                
def CompareSP500():
# Get the tickers for the S&P 500 and create a dictionary with all S&P500 tickers and their data
    #table=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    #df = table[0]
    #sp500_tickers = df['Symbol'].tolist()
    sp500_tickers = ["MMM", "AOS", "ABT", "ABBV", "ACN", "ATVI", "ADM", "ADBE", "ADP", "AAP", "AES", "AFL", "A", "APD", "AKAM", "ALK", "ALB", "ARE", "ALGN", "ALLE", "LNT", "ALL", "GOOGL", "GOOG", "MO", "AMZN", "AMCR", "AMD", "AEE", "AAL", "AEP", "AXP", "AIG", "AMT", "AWK", "AMP", "ABC", "AME", "AMGN", "APH", "ADI", "ANSS", "AON", "APA", "AAPL", "AMAT", "APTV", "ACGL", "ANET", "AJG", "AIZ", "T", "ATO", "ADSK", "AZO", "AVB", "AVY", "AXON", "BKR", "BALL", "BAC", "BBWI", "BAX", "BDX", "WRB", "BRK-B", "BBY", "BIO", "TECH", "BIIB", "BLK", "BK", "BA", "BKNG", "BWA", "BXP", "BSX", "BMY", "AVGO", "BR", "BRO", "BF-B", "BG", "CHRW", "CDNS", "CZR", "CPT", "CPB", "COF", "CAH", "KMX", "CCL", "CARR", "CTLT", "CAT", "CBOE", "CBRE", "CDW", "CE", "CNC", "CNP", "CDAY", "CF", "CRL", "SCHW", "CHTR", "CVX", "CMG", "CB", "CHD", "CI", "CINF", "CTAS", "CSCO", "C", "CFG", "CLX", "CME", "CMS", "KO", "CTSH", "CL", "CMCSA", "CMA", "CAG", "COP", "ED", "STZ", "CEG", "COO", "CPRT", "GLW", "CTVA", "CSGP", "COST", "CTRA", "CCI", "CSX", "CMI", "CVS", "DHI", "DHR", "DRI", "DVA", "DE", "DAL", "XRAY", "DVN", "DXCM", "FANG", "DLR", "DFS", "DISH", "DIS", "DG", "DLTR", "D", "DPZ", "DOV", "DOW", "DTE", "DUK", "DD", "DXC", "EMN", "ETN", "EBAY", "ECL", "EIX", "EW", "EA", "ELV", "LLY", "EMR", "ENPH", "ETR", "EOG", "EPAM", "EQT", "EFX", "EQIX", "EQR", "ESS", "EL", "ETSY", "RE", "EVRG", "ES", "EXC", "EXPE", "EXPD", "EXR", "XOM", "FFIV", "FDS", "FICO", "FAST", "FRT", "FDX", "FITB", "FSLR", "FE", "FIS", "FISV", "FLT", "FMC", "F", "FTNT", "FTV", "FOXA", "FOX", "BEN", "FCX", "GRMN", "IT", "GEHC", "GEN", "GNRC", "GD", "GE", "GIS", "GM", "GPC", "GILD", "GL", "GPN", "GS", "HAL", "HIG", "HAS", "HCA", "PEAK", "HSIC", "HSY", "HES", "HPE", "HLT", "HOLX", "HD", "HON", "HRL", "HST", "HWM", "HPQ", "HUM", "HBAN", "HII", "IBM", "IEX", "IDXX", "ITW", "ILMN", "INCY", "IR", "PODD", "INTC", "ICE", "IFF", "IP", "IPG", "INTU", "ISRG", "IVZ", "INVH", "IQV", "IRM", "JBHT", "JKHY", "J", "JNJ", "JCI", "JPM", "JNPR", "K", "KDP", "KEY", "KEYS", "KMB", "KIM", "KMI", "KLAC", "KHC", "KR", "LHX", "LH", "LRCX", "LW", "LVS", "LDOS", "LEN", "LNC", "LIN", "LYV", "LKQ", "LMT", "L", "LOW", "LYB", "MTB", "MRO", "MPC", "MKTX", "MAR", "MMC", "MLM", "MAS", "MA", "MTCH", "MKC", "MCD", "MCK", "MDT", "MRK", "META", "MET", "MTD", "MGM", "MCHP", "MU", "MSFT", "MAA", "MRNA", "MHK", "MOH", "TAP", "MDLZ", "MPWR", "MNST", "MCO", "MS", "MOS", "MSI", "MSCI", "NDAQ", "NTAP", "NFLX", "NWL", "NEM", "NWSA", "NWS", "NEE", "NKE", "NI", "NDSN", "NSC", "NTRS", "NOC", "NCLH", "NRG", "NUE", "NVDA", "NVR", "NXPI", "ORLY", "OXY", "ODFL", "OMC", "ON", "OKE", "ORCL", "OGN", "OTIS", "PCAR", "PKG", "PARA", "PH", "PAYX", "PAYC", "PYPL", "PNR", "PEP", "PFE", "PCG", "PM", "PSX", "PNW", "PXD", "PNC", "POOL", "PPG", "PPL", "PFG", "PG", "PGR", "PLD", "PRU", "PEG", "PTC", "PSA", "PHM", "QRVO", "PWR", "QCOM", "DGX", "RL", "RJF", "RTX", "O", "REG", "REGN", "RF", "RSG", "RMD", "RVTY", "RHI", "ROK", "ROL", "ROP", "ROST", "RCL", "SPGI", "CRM", "SBAC", "SLB", "STX", "SEE", "SRE", "NOW", "SHW", "SPG", "SWKS", "SJM", "SNA", "SEDG", "SO", "LUV", "SWK", "SBUX", "STT", "STLD", "STE", "SYK", "SYF", "SNPS", "SYY", "TMUS", "TROW", "TTWO", "TPR", "TRGP", "TGT", "TEL", "TDY", "TFX", "TER", "TSLA", "TXN", "TXT", "TMO", "TJX", "TSCO", "TT", "TDG", "TRV", "TRMB", "TFC", "TYL", "TSN", "USB", "UDR", "ULTA", "UNP", "UAL", "UPS", "URI", "UNH", "UHS", "VLO", "VTR", "VRSN", "VRSK", "VZ", "VRTX", "VFC", "VTRS", "VICI", "V", "VMC", "WAB", "WBA", "WMT", "WBD", "WM", "WAT", "WEC", "WFC", "WELL", "WST", "WDC", "WRK", "WY", "WHR", "WMB", "WTW", "GWW", "WYNN", "XEL", "XYL", "YUM", "ZBRA", "ZBH", "ZION", "ZTS"]
    percentage_list=[]
    total_tickers = len(sp500_tickers)
    start_time=time.time()
    print("\nPlease wait, calculating historical data and dividend information for all S&P 500 stocks, this may take a while...\n ")
# Loop through all tickers in the S&P 500
    for i, ticker in enumerate(sp500_tickers):
        #ticker = ticker.replace('.','-')
        try:
            data=get_ticker_data_no_progressbar(ticker)
            lowest_price, low_date = get_lowest_date_price_entirety(data)
            highest_price,high_date = get_highest_date_price_entirety(data)
            #lowest_price=round(lowest_price,2)
            #print(lowest_price)
            if not lowest_price or not highest_price:
                raise ValueError(f"\nNo data found for {ticker} or symbol may be delisted")
            multiplier,percentage = get_multiplier_percentage(ticker,lowest_price,highest_price)
            if low_date >= high_date:
                multiplier=None
                percentage=neg_percentage(low_date,lowest_price,high_date,highest_price)
            percentage_list.append([ticker,multiplier,percentage,low_date,lowest_price,high_date,highest_price])
            progress = (i+1)/total_tickers*100
            elapsed_time = time.time() - start_time
            eta = (elapsed_time / progress) * (100 - progress)
            eta_str = time.strftime('%H:%M:%S', time.gmtime(eta))
            print(f"\rProgress: '${ticker}' {progress:.2f}% ETA: {eta_str} or press 'q' then 'enter' to return to menu: ", end='', flush=True)
            if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                line = input()
                if line.lower() == 'q':
                    print("\nReturning to main menu...\n")
                    return
        except Exception as e:
            print(f"\rError processing {ticker}: {str(e)}\n", end='', flush=False)
            continue
# Sort the percentage list by descending percentage, move it to a pd dataframe and then print result
    elapsed_time=time.time()-start_time
    elapsed_time = time.strftime('%H:%M:%S', time.gmtime(elapsed_time))
    print(f"Actual time: {elapsed_time}")
    df = pd.DataFrame(percentage_list, columns=['Ticker', 'Multiplier', 'Percentage','ATL Date','ATL Price','ATH Date','ATH Price'])
    df_sorted = df.sort_values('Percentage', ascending=False)
    df_sorted['Multiplier'] = df['Multiplier'].apply(lambda x: '{:,.2f}x'.format(x) if x is not None else 'N/A')
    df_sorted['Percentage'] = df['Percentage'].apply(lambda x: '{:,.0f}%'.format(x))
    df_sorted['ATL Price'] = df_sorted['ATL Price'].apply(lambda x: '${:,.2f}'.format(float(x)))
    df_sorted['ATH Price'] = df_sorted['ATH Price'].apply(lambda x: '${:,.2f}'.format(float(x)))
    df_sorted.index = df_sorted.index + 1
    df_sorted.columns = ['Ticker', 'Multiplier', 'Percentage','ATL Date','ATL Price','ATH Date','ATH Price']
    df_sorted = df_sorted.reset_index(drop=False)
    df_sorted['Ranks'] = df_sorted.index + 1
    df_sorted = df_sorted[['Ranks', 'Ticker', 'Multiplier', 'Percentage','ATL Date','ATL Price','ATH Date','ATH Price']]
    print("\n")
    print(df_sorted)
    print("\n")
    csv = input("Would you like to turn this into a .CSV file? (Y/N)")
    if csv.upper()=="Y":
        if name := input("Please input a name for your file, or press enter to use the default 'BestPerformers.csv': "):
            df_sorted.to_csv(f'{name}.csv', index=False)
        else:
            df_sorted.to_csv('BestPerformers.csv', index=False)
    print("\n")
    
def CompareStocks():
    while True:
        try:
            ticker1 = input("Enter first ticker symbol or 'exit' to return to menu:")
            if ticker1 == "exit":
                return
            data1 = get_ticker_data(ticker1)
            break
        except Exception:
            print(f"Error: Ticker symbol '{ticker1}' not found in the yfinance library")
            print("Please only enter the Ticker symbol of the stock\n")
            continue
    while True:
        try:
            ticker2 = input("Enter second ticker symbol or 'exit' to return to menu:")
            if ticker2 == "exit":
                return
            data2 = get_ticker_data(ticker2)
            break
        except Exception:
            print(f"Error: Ticker symbol '{ticker2}' not found in the yfinance library")
            print("Please only enter the Ticker symbol of the stock\n")
            continue
    first_trade_date1 = data1.index[1].date()
    first_trade_date2 = data2.index[1].date()
    ticker_obj1 = yf.Ticker(ticker1)
    ticker_obj2 = yf.Ticker(ticker2)
    info1 = ticker_obj1.info
    info2 = ticker_obj2.info
    name1 = info1['longName']
    name2 = info2['longName']
    print(f"\nThe first tradeable date for {name1} was {first_trade_date1}") 
    lowest_price1, low_date1 = get_lowest_date_price_entirety(data1)
    highest_price1,high_date1 = get_highest_date_price_entirety(data1) 
    lowest_price2, low_date2 = get_lowest_date_price_entirety(data2)
    highest_price2,high_date2 = get_highest_date_price_entirety(data2)
    uw1=print_statements(ticker1,low_date1,lowest_price1,high_date1,highest_price1)
    print(f"\nThe first tradeable date for {name2} was {first_trade_date2}") 
    uw2=print_statements(ticker2,low_date2,lowest_price2,high_date2,highest_price2)
    multiplier1,percentage1=get_multiplier_percentage(ticker1,lowest_price1,highest_price1)
    multiplier2,percentage2=get_multiplier_percentage(ticker2,lowest_price2,highest_price2)
    underwater_check(uw1,uw2,ticker1,ticker2,percentage1,percentage2)

#Developer Mode for testing
def devMode():
    ticker = "aapl"
    ticker_obj = yf.Ticker(ticker)
    info = ticker_obj.info
    info_keys = info.keys()
    #sector=info['sector']
    #print(sector)
   # industry=info['industry']
    #beta=info['beta']
    #print(f"industry: {industry}")
    #for key in info_keys:
        #print(f"-'{key}'")
    exit()


#Main Menu
while True:
    option = input(f"""\
Enter:
1 to search the performance of a stock,
2 to compare each stock in the S&P 500,
3 to compare the performance of two stocks,
or 'exit' to quit.
""")
    if option=='1':
        SearchStock()
    elif option=='2':
        CompareSP500()
    elif option=='3':
        CompareStocks()
    elif option=='4':
        devMode()
    elif option =="exit":
        exit()
    else:
        print("Try a valid option")

 
"""
#Small sample to remember code

ticker = input("Enter Ticker Symbol:")
ticker_obj = yf.Ticker(ticker)
info = ticker_obj.info
info_keys = info.keys()
print(info_keys)
#    info = ticker_obj.info
 #   name = info['longName']
 #   currency = info['currency']
#info_keys = info.keys()

"""
