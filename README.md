# StocksFinder

This service aims to provide every user with the information they need to make better financial choices when it comes to investing in the stock market and cryptocurrency. 

We provide chart data, Financial News, Information Sheets, and resources to help investors at every level better their investment practices


## Use
Use the link https://stocksfinder.herokuapp.com/

1. On the homepage, price action of the major indeces, your personalized watchlist, and financial recent financial news
2. In the search tab you are able to input a stock you want to search, provide a time period and interval and an interactive chart of its price action will be provided, under that you will find the stocks infomation sheet which includes a vast array of information about the stock including sector, industry, etc.
3. The signup and login allow you to have your own personalized watchlist but this feature does not work on heroku (heroku issue with flask SQL Alchemy)

## Running on local enviorment

1. Setup a flask enviroment on your local machine, link to tutorial using VSCode: https://www.youtube.com/watch?v=GHvj1ivQ7ms

2. Make sure you pip/pip3 install yfinance, flask, flask wtf, newsdataapi, form ,flask_behind_proxy, email_validator, flask_login

3. Run app.py on your machine and go to the local url provided to you i.e http://127.0.0.1:5000

## Future Features

We plan on providing more features in the future, such as:

- More customization/features for each user like paper trading
- Find a work around to the heroku database with SQL Alchemy problem
