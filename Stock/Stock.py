import yfinance as yf
import pandas as pd
import streamlit as st
import pandas_ta as ta  # we can also use ta-lib but was failing to install tab-lib so i used pandas_ta
from datetime import datetime, timedelta


def get_stock_data(stock_name):
    try:
        # Add .NS for NSE stocks (e.g., TCS.NS)
        stock = yf.Ticker(f"{stock_name}.NS")
        end_date = datetime.today()
        start_date = end_date - timedelta(days=365) 
        data = stock.history(start=start_date, end=end_date)
        return data
    except Exception as e:
        st.error(f"Error fetching data for {stock_name}: {e}")
        return None


def calculate_indicators(data):
    if data is not None and not data.empty:
   
        data['RSI'] = ta.rsi(data['Close'], length=14)  
       
        data['SMA_50'] = ta.sma(data['Close'], length=50)  
        return data
    return None

def generate_recommendation(data):
    if data is not None and not data.empty:
        latest_close = data['Close'].iloc[-1]
        latest_rsi = data['RSI'].iloc[-1]
        sma_50 = data['SMA_50'].iloc[-1]

     
        if latest_close > sma_50 and latest_rsi < 30:
            return "Buy (Oversold & Price > SMA-50)"
        elif latest_close < sma_50 and latest_rsi > 70:
            return "Sell (Overbought & Price < SMA-50)"
        else:
            return "Hold (Neutral)"
    return "No recommendation (Insufficient data)"


def main():
    st.title("📈 Indian Stock Recommendation System")
    st.write("Enter a stock symbol (e.g., Tcs, Infy, Relience):")

 
    stock_name = st.text_input("Stock Symbol:", "").strip().upper()
    if not stock_name:
        st.warning("Please enter a stock symbol.")
        return

 
    data = get_stock_data(stock_name)
    if data is None or data.empty:
        st.error("Invalid stock symbol or no data available.")
        return

   
    data = calculate_indicators(data)
    if data is None:
        st.error("Failed to calculate indicators.")
        return

  
    latest_close = data['Close'].iloc[-1]
    st.subheader(f"Latest Closing Price for {stock_name}: ₹{latest_close:.2f}")

    # Generate and display recommendation
    recommendation = generate_recommendation(data)
    st.subheader("Recommendation:")
    if "Buy" in recommendation:
        st.success(recommendation)
    elif "Sell" in recommendation:
        st.error(recommendation)
    else:
        st.warning(recommendation)

    
    st.subheader("Price Trend (1 Year)")
    st.line_chart(data[['Close', 'SMA_50']])
# for RSI
    st.subheader("RSI (14-day)")
    st.line_chart(data['RSI'])
    st.write("RSI > 70 = Overbought, RSI < 30 = Oversold")

if __name__ == "__main__":
    main()