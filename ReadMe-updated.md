Welcome to the FOMO calculator, this program allows you to calculate the All-Time Low and the All-Time High of a stock or index in order to find out how much you could have made if you bought at the bottom and sold at the top.

Stock Analysis Tool
This is a Python script that allows you to analyze the historical data of stocks. It uses the Yahoo Finance API to retrieve stock data and performs calculations to determine the lowest and highest prices of a stock within a specified date range. It also checks if the stock has paid dividends during the specified period and calculates potential investment returns.

Prerequisites:
Python 3.6 or higher
requests library
pandas library
numpy library
yfinance library
datetime module
decimal module
time module
sys module
select module
pytz library
matplotlib library

Getting Started
Clone the repository:
 $ git clone https://github.com/your-username/stock-analysis-tool.git
Install the required dependencies:
 $ pip install -m <prerequisite>
Run the script:
 $ python3 FomoCalculator.py
Usage
Enter the ticker symbol of the stock you want to analyze or type 'exit' to return to the main menu.

Specify the date range for analysis. You can choose a start date or use the first trade date of the stock. You can also specify an end date or use yesterday's date as the default.

The script will retrieve the stock data and calculate the lowest and highest prices within the specified date range.

It will check if the stock paid dividends during that period and calculate potential investment returns.

The results will be displayed, including the lowest and highest prices, dividend information (if applicable), and potential investment returns.

Compare S&P 500 Stocks
This script also provides a feature to compare historical data and dividend information for all stocks in the S&P 500 index.

Run the script and choose the option to compare S&P 500 stocks.

The script will retrieve the tickers of the S&P 500 stocks either from a web source or a local database.

It will calculate the historical data and dividend information for each stock.

The results will be displayed, showing the stocks ranked by potential investment returns.

You can choose to export the results to a CSV file.

Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please create an issue or submit a pull request.

License
This project is licensed under the MIT License. See the LICENSE file for more details.

Acknowledgments
This project uses the Yahoo Finance API to retrieve stock data.
The list of S&P 500 stocks is obtained from Wikipedia.
Please make sure to update the necessary details and instructions according to your project's specific requirements.



Overall, that is the basis of my program, thank you for using it and be sure to include any bugs, missing features or ideas that you would like to see implemented at a future date. 

Thank you very much,
                    Dup3dupca