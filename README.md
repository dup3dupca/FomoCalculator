# FomoCalculator
Welcome to the FOMO calculator, this program allows you to calculate the All-Time Low and the All-Time High of a stock or index in order to find out how much you could have made if you bought at the bottom and sold at the top.

KeyWords: 
-ATL: All-Time Low
-ATH: All-Time High

-Multiplier: This is a way for users to calculate returns, instead of using percentage values, a multiplier is divided by 100 in order for the user to see how much they could have made, for example 100% is equal to 1x, a 1x can be seen as the multiplier amount for any amount of money you wish to calculate. If a user had bought $1000 of a stock at its ATL and sold at its ATH, you can use the multiplier value to calculate the return you would have had i.e $1000 on a 2x multiplier is $2000

This program uses the yfinance library in order to retrieve historical data from yahoo finance, using this data we calculate the lowest low of a stock's price and its highest high. By doing this we calculate the percentage by using the formula- (highest_price-lowest_price / lowest_price), this formula should calculate the percentage return and the multiplier amount resulted if you bought the stock at its lowest price and sold it at its highest price.

If a stock is currently at its lowest levels or near its All-Time Low, then the stock is considered "Underwater" as its All-Time High is calculated before the All-Time Low which means that the stock has fell. We may incorporate a negative percentage calculation for these occasions but we have no intention to do so as of right now, so if the key-word "Underwater" appears, just note that the ATH has occurred before the ATL, so you would have potentially lost money. (UPDATED: code will return a negative percentage if start date is later than the end date)

The program also allows for user-input start dates and end dates, the start date is the period from where the historical data will start being calculated and the end date is the period where the historical data will stop being calculated. By default, the value for the start date is the first trade date of the company or the IPO and the default value for the end date is todays date. This does not mean that you can see today's historical data as yahoo finance adds the previous day to the historical data and not todays data. (Historical data lags behind by one day)

Some companies do not have historical data available since inception, i.e $KO, $XOM, $MO,etc... , This may be due to the historical data not being digitized from before 1960, which is why for certain companies the first trade date will be starting from 1960 instead of its actual inception date. For stocks that have IPO'd from 1970 forward, most historical data is made available.


This program calculates dividend values in two ways, the first is the dividend payout, in order to calculate this we first find the start date and end date input to the stock, if the stock has a dividend from this period we calculate the sum of each of the dividend payments and then divide it by the lowest price and add it to the percentage and multiplier variables. The other way is dividend reinvesting, in order to calculate this we find the start date and end date, afterward be begin by finding the corresponding day that the stock had a dividend on, we then calculate how many shares would have been bought using the dividend amount paid and the stock's closing price on that day. We then iterate through this for each of the dividend periods and return a total that is equal to the number of shares you would have due to the reinvesting period. We then multiply this amount by the multiplier  in order to calculate the multiplier and percentage returns for dividend reinvestment. We are not completely sure if this is how it should be calculated, but are open to suggestions.

The program has three functions: 

   1. The first is to view a stocks performance. In this function, we allow the user to input a stock name if it is valid, then select the start date and end date to calculate from, pressing "enter" will use the default values, the format must be in (YYYY-MM-DD) in order to register. The program then prints the stocks lowest price and its date and the highest price and its date. It then calculates the percentage and multiplier returns by using the formula: (highest_price-lowest_price)/lowest_price. The result is the multiplier value and when it is multiplied by 100, it becomes the percentage value.

   2. The second is to calculate each individual stock in the S&P500 and calculate its multiplier and percentage returns. In the code, we have two options on where to obtain our data from, one is from a Wikipedia page that includes the ticker symbols of all 500 stocks in the S&P500, this method is useful because it is flexible over time as stocks are added and removed from the index. The second method is simply a list which includes all 500 of the stocks currently included, this method is faster, but is static so over time the stocks in the list will need to be manually changed to the new stocks. We set the start dates and end dates to the inception period and todays date in order to calculate the results. We then iterate through each and every stock in the list and calculate the multiplier, percentage, lowest date, lowest price, highest date and highest price. We include all of these in the final list and index it in order for the user to see which stocks have performed better than the other in this list, any stocks that are underwater are not included into this list.We then allow the option for the user to turn this data into a .CSV file in order to save time rather than performing this all over again. There are errors that occur during this process which might leave certain stocks not calculated, so if you remember the names you can go back and calculate them individually using the first function

   3. The third is a function to compare two individual stocks, by default the start date and end date will be set to the inception and todays date. We then provide the user with the information of the stocks ATL and its date and the ATH and its date. We then calculate the stocks performance with multiplier and percentage variables and compare the percentage value between the two stocks. If one stock performs better than the other, then that stocks percentage will be deducted by the value of the other stocks percentage. This number is then printed to show the difference of performance between the two stocks. If a stock the user entered is underwater, then the default value of the stock will become 0. 

   4. The hidden function is a DEVMODE feature which allows developers to practice using the functions from the yfinance library



Overall, that is the basis of my program, thank you for using it and be sure to include any bugs, missing features or ideas that you would like to see implemented at a future date. 

Thank you very much,
                    Dup3dupca
