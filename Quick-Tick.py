import sys
import matplotlib.pyplot as plt
import numpy as np
import yfinance as yf
from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import QThread, pyqtSignal

class StockAnalyzer(QWidget):
    def __init__(self):
        super().__init__()

        # create the GUI widgets
        self.ticker_label = QLabel("Enter a Ticker Symbol:")
        self.ticker_edit = QLineEdit()
        self.basic_info_button = QPushButton("Basic Info")
        self.historical_data_button = QPushButton("Historical Data")
        self.risk_return_button = QPushButton("Risk and Return")
        self.dividend_yield_button = QPushButton("Dividend Yield")
        self.technical_indicators_button = QPushButton("Technical Indicators")
        self.result_label = QLabel()

        # connect the buttons to their respective functions
        self.basic_info_button.clicked.connect(self.get_basic_info)
        self.historical_data_button.clicked.connect(self.get_historical_data)
        self.risk_return_button.clicked.connect(self.get_risk_return)
        self.dividend_yield_button.clicked.connect(self.get_dividend_yield)
        self.technical_indicators_button.clicked.connect(self.get_technical_indicators)

        # create the layout and add the widgets
        layout = QVBoxLayout()
        layout.addWidget(self.ticker_label)
        layout.addWidget(self.ticker_edit)
        layout.addWidget(self.basic_info_button)
        layout.addWidget(self.historical_data_button)
        layout.addWidget(self.risk_return_button)
        layout.addWidget(self.dividend_yield_button)
        layout.addWidget(self.technical_indicators_button)
        layout.addWidget(self.result_label)

        # set the layout for the widget
        self.setLayout(layout)

    def validate_ticker(self, ticker):
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            return True
        except:
            return False

    def get_basic_info(self):
        ticker = self.ticker_edit.text()
        if not self.validate_ticker(ticker):
            self.result_label.setText("Invalid ticker symbol. Please enter a valid ticker symbol.")
            return
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            basic_info_str = f"Name: {info['longName']}\n" \
                             f"Industry: {info['industry']}\n" \
                             f"Market Cap: {info['marketCap']}\n" \
                             f"Country: {info['country']}\n" \
                             f"Sector: {info['sector']}\n" \
                             f"PE Ratio: {info['trailingPE']:.2f}\n" \
                             f"Forward PE Ratio: {info['forwardPE']:.2f}\n" \
                             f"PEG Ratio: {info['pegRatio']:.2f}\n" \
                             f"Price-to-Sales Ratio: {info['priceToSalesTrailing12Months']:.2f}\n" \
                             f"Price-to-Book Ratio: {info['priceToBook']:.2f}\n" \
                             f"52-Week High: {info['fiftyTwoWeekHigh']:.2f}\n" \
                             f"52-Week Low: {info['fiftyTwoWeekLow']:.2f}"
            self.result_label.setText(basic_info_str)
        except:
            self.result_label.setText("Data not available for this stock.")

    def get_historical_data(self):
        ticker = self.ticker_edit.text()
        if not self.validate_ticker(ticker):
            self.result_label.setText("Invalid ticker symbol. Please enter a valid ticker symbol.")
            return
        try:
            stock = yf.Ticker(ticker)
            hist_data = stock.history(period='max')
            fig, ax = plt.subplots()
            ax.plot(hist_data.index, hist_data['Close'], label='Close')
            ax.plot(hist_data.index, hist_data['Open'], label='Open')
            ax.legend()
            ax.set_xlabel('Date')
            ax.set_ylabel('Price')
            ax.set_title(f'{ticker} Historical Data')
            plt.show()
        except:
            self.result_label.setText("Data not available for this stock.")

    def get_risk_return(self):
        ticker = self.ticker_edit.text()
        if not self.validate_ticker(ticker):
            self.result_label.setText("Invalid ticker symbol. Please enter a valid ticker symbol.")
            return
        try:
            stock = yf.Ticker(ticker)
            hist_data = stock.history(period='max')
            returns = hist_data['Close'].pct_change()
            volatility = returns.std()
            annualized_return = ((1 + returns.mean()) ** 252) - 1
            fig, ax = plt.subplots()
            ax.hist(returns, bins=50, alpha=0.5)
            ax.axvline(x=volatility, color='red', linestyle='--', label='Volatility')
            ax.legend()
            ax.set_xlabel('Returns')
            ax.set_ylabel('Frequency')
            ax.set_title(f'{ticker} Risk and Return')
            plt.show()
        except:
            self.result_label.setText("Data not available for this stock.")

    def get_dividend_yield(self):
        ticker = self.ticker_edit.text()
        if not self.validate_ticker(ticker):
            self.result_label.setText("Invalid ticker symbol. Please enter a valid ticker symbol.")
            return
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            dividend_yield = info['dividendYield']
            self.result_label.setText(f"Dividend Yield: {dividend_yield:.4f}")
        except:
            self.result_label.setText("Data not available for this stock.")

    def get_technical_indicators(self):
        ticker = self.ticker_edit.text()
        if not self.validate_ticker(ticker):
            self.result_label.setText("Invalid ticker symbol. Please enter a valid ticker symbol.")
            return
        try:
            stock = yf.Ticker(ticker)
            hist_data = stock.history(period='max')
            sma_50 = hist_data['Close'].rolling(window=50).mean()
            sma_200 = hist_data['Close'].rolling(window=200).mean()
            fig, ax = plt.subplots()
            ax.plot(hist_data.index, hist_data['Close'], label='Close')
            ax.plot(hist_data.index, sma_50, label='SMA 50')
            ax.plot(hist_data.index, sma_200, label='SMA 200')
            ax.legend()
            ax.set_xlabel('Date')
            ax.set_ylabel('Price')
            ax.set_title(f'{ticker} Technical Indicators')
            plt.show()
        except:
            self.result_label.setText("Data not available for this stock.")

class AnalysisThread(QThread):
    analysis_complete = pyqtSignal(str)

    def __init__(self, func):
        super().__init__()
        self.func = func

    def run(self):
        self.func()
        self.analysis_complete.emit("Analysis complete.")

if __name__ == '__main__':
    # create the QApplication
    app = QApplication(sys.argv)

    # create the widget
    analyzer = StockAnalyzer()

    # show the widget
    analyzer.show()

    # run the event loop
    sys.exit(app.exec_())
