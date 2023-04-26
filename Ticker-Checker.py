import yfinance as yf
import matplotlib.pyplot as plt

def get_ticker_info(ticker):
    # Get data for the specified ticker
    data = yf.Ticker(ticker)
    # Return the data
    return data

def show_basic_info(data):
    # Display basic info about the stock
    info = data.info
    print(f"Name: {info['longName']}")
    print(f"Industry: {info['industry']}")
    print(f"Sector: {info['sector']}")
    print(f"Country: {info['country']}")
    print(f"Market Cap: {info['marketCap']}")
    print(f"PE Ratio: {info['trailingPE']}")
    print(f"Forward PE Ratio: {info['forwardPE']}")
    print(f"PEG Ratio: {info['pegRatio']}")

def show_historical_data(data):
    # Get historical data for the stock
    history = data.history(period="max")

    # Display the historical data
    fig, ax = plt.subplots()
    ax.plot(history.index, history["Close"])
    ax.set(xlabel='Date', ylabel='Price', title='Historical Stock Prices')
    plt.show()

def calculate_risk_return(data):
    # Get historical data for the stock
    history = data.history(period="max")

    # Calculate the daily returns
    history["daily_return"] = history["Close"].pct_change()

    # Calculate the mean daily return and daily volatility
    mean_daily_return = history["daily_return"].mean()
    daily_volatility = history["daily_return"].std()

    # Calculate the annualized values
    annualized_return = (1 + mean_daily_return) ** 252 - 1
    annualized_volatility = daily_volatility * 252 ** 0.5

    # Display the results
    print(f"Annualized Return: {annualized_return:.4%}")
    print(f"Annualized Volatility: {annualized_volatility:.4%}")

    # Plot the daily returns
    fig, ax = plt.subplots()
    ax.plot(history.index, history["daily_return"])
    ax.set(xlabel='Date', ylabel='Daily Return', title='Daily Returns')
    plt.show()

def calculate_dividend_yield(data):
    # Get the latest dividend yield for the stock
    div_yield = data.info["dividendYield"]

    # Display the dividend yield
    print(f"Dividend Yield: {div_yield:.4%}")

def main():
    # Get input from the user
    while True:
        ticker = input("Enter a ticker symbol (or QUIT to exit): ").upper()
        if ticker == "QUIT":
            break

        # Get the data for the specified ticker
        data = get_ticker_info(ticker)

        # Get the user's choice and perform the corresponding action
        while True:
            choice = input("What would you like to do?\n1. Show basic info\n2. Show historical data\n3. Calculate risk and return\n4. Calculate dividend yield\n5. Exit\nEnter a number: ")
            if choice == "1":
                show_basic_info(data)
            elif choice == "2":
                show_historical_data(data)
            elif choice == "3":
                calculate_risk_return(data)
            elif choice == "4":
                calculate_dividend_yield(data)
            elif choice == "5":
                break

if __name__ == "__main__":
    main()
3