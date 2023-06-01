# FOMO Calculator

Welcome to the FOMO calculator! This program allows you to calculate the All-Time Low and the All-Time High of a stock or index, helping you determine potential gains if you bought at the bottom and sold at the top.

## Stock Analysis Tool

The Stock Analysis Tool is a Python script that analyzes historical stock data. It utilizes the Yahoo Finance API to retrieve stock data, performs calculations to determine the lowest and highest prices within a specified date range, checks for dividend payments, and calculates potential investment returns.

### Prerequisites

- Python 3.6 or higher
- requests library
- pandas library
- numpy library
- yfinance library
- datetime module
- decimal module
- time module
- sys module
- select module
- pytz library
- matplotlib library

### Getting Started

1. Clone the repository:

   $ git clone https://github.com/your-username/FomoCalculator.git

2. Install the required dependencies:

   $ pip install -m <requirements>

3. Run the script:

   $ python3 FomoCalculator.py

### Usage

1. Enter the ticker symbol of the stock you want to analyze or type 'exit' to return to the main menu.

2. Specify the date range for analysis. You can choose a start date or use the first trade date of the stock. You can also specify an end date or use yesterday's date as the default.

3. The script will retrieve the stock data and calculate the lowest and highest prices within the specified date range.

4. It will check if the stock paid dividends during that period and calculate potential investment returns.

5. The results will be displayed, including the lowest and highest prices, dividend information (if applicable), and potential investment returns.

### Compare S&P 500 Stocks

This script also provides a feature to compare historical data and dividend information for all stocks in the S&P 500 index.

1. Run the script and choose the option to compare S&P 500 stocks.

2. The script will retrieve the tickers of the S&P 500 stocks either from a web source or from one of the .csv files in the CSVDataFiles.zip folder. By default, the SP500.csv file is included but you can change it to the Russell2000,3000 or Wilshire5000 indexes by modifying the code with the .csv file you wish to use.

3. It will calculate the historical data and dividend information for each stock.

4. The results will be displayed, showing the stocks ranked by potential investment returns.

5. You can choose to export the results to a CSV file.

### Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please create an issue or submit a pull request.

### License

This project is licensed under the MIT License. See the LICENSE file for more details.

### Acknowledgments

- This project uses the Yahoo Finance API to retrieve stock data.
- The list of S&P 500 stocks is obtained from Wikipedia.

---

Thank you for using the FOMO Calculator! If you encounter any bugs, missing features, or have ideas for future enhancements, please don't hesitate to include them.

Thank you very much,
Dup3dupca