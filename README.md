# Get-Some-Stocks
Website aplication reviewing stocks. Allows to set up wallet, and track stock prices.

Visit website:

http://dawidlycz.pythonanywhere.com/

## About the App
Get-Some-Stocks is a web application built on the Django framework, allowing users to browse various stock markets around the world and analyze stock prices. Additionally, the application is equipped with built-in algorithms that, based on the chosen strategy, assess whether it is currently a good time to buy, sell, or wait.

### Key Features:
* Market Exploration: Get-Some-Stocks enables users to easily explore different stock exchanges worldwide. Whether you're interested in events on the bustling Wall Street in New York or dynamic markets in Asia, the application provides real-time data to keep you informed.

* Price Inspection: Dive into the details with the intuitive price inspection feature. Users can delve into detailed stock prices, historical data, and interactive charts to gain a deeper understanding of market movements.

* Price Tracking: Users have the ability to create their own wallets and add stocks to them. This feature enables them to track stock prices and monitor their growth within their chosen portfolios.

* Built-in Algorithms: The application comes with advanced algorithms tailored to various investment strategies. Based on your chosen approach, whether it's short-term trading, long-term strategies, or something in between, the algorithms provide valuable insights into the current market conditions.

* Decision Support: Get-Some-Stocks goes beyond merely displaying information by offering decision support. Depending on your chosen strategy, the app provides recommendations on whether it's a favorable time to buy, sell, or adopt a wait-and-see approach. These insights result from a thorough analysis of market trends and the powerful algorithms of the application.

* User-Friendly Interface: The app features a user-friendly interface, making it accessible to both novice and experienced investors. The intuitive design ensures seamless navigation through the wealth of available information.

* In a world where the financial market is constantly evolving, Get-Some-Stocks aims to be your reliable companion, assisting you in making informed decisions and optimizing your investment portfolio. Download the app now and embark on a journey of financial exploration and empowerment.

* API Integration: The application is integrated with Django Rest Framework, providing an API for additional functionality and seamless integration with other applications. This enables developers to extend the capabilities of Get-Some-Stocks and integrate it with external systems or services.

## Dependencies

The project relies on the following Python libraries and packages:

- [Alpha Vantage](https://www.alphavantage.co/): A powerful API for financial market data.
- [Matplotlib](https://matplotlib.org/): A comprehensive library for creating static, animated, and interactive visualizations.
- [yfinance](https://pypi.org/project/yfinance/): A library for fetching financial data from Yahoo Finance.
- [Pandas](https://pandas.pydata.org/): A versatile data manipulation and analysis library.
- [mysqlclient](https://pypi.org/project/mysqlclient/): A MySQL database connector for Django.
- [Django Rest Framework](https://www.django-rest-framework.org): A tool to create and use API.
Make sure to install these dependencies by running the following command:

```bash
pip install -r requirements.txt
