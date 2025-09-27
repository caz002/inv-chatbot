import streamlit as st
import yfinance as yf
import altair as alt
import plotly.graph_objects as go

@st.cache_data
def fetch_stock_info(symbol):
    stock = yf.Ticker(symbol)
    return stock.info
@st.cache_data
def fetch_quarterly_financials(symbol):
    stock = yf.Ticker(symbol)
    return stock.quarterly_financials.T

@st.cache_data
def fetch_annual_financials(symbol):
    stock = yf.Ticker(symbol)
    return stock.financials.T

@st.cache_data
def fetch_weekly_price_history(symbol):
    stock = yf.Ticker(symbol)
    return stock.history(period='1y', interval='1wk')

st.title('Stock Dashboard')
symbol = st.text_input('Enter a stock symbol', 'AAPL')

information = fetch_stock_info(symbol)

st.header('Company Information')

st.subheader(f'Name: {information["longName"]}')
st.subheader(f'Market Cap: ${information["marketCap"]:,}')
st.subheader(f'Sector: {information["sector"]}')

price_history = fetch_weekly_price_history(symbol)

st.header('Chart')

price_history = price_history.rename_axis('Date').reset_index()
candle_stick_chart = go.Figure(data=[go.Candlestick(
    x=price_history['Date'],
    open=price_history['Open'],
    low=price_history['Low'],
    high=price_history['High'],
    close=price_history['Close']
)])
candle_stick_chart.update_layout(xaxis_rangeslider_visible=False)
st.plotly_chart(candle_stick_chart, use_container_width=True)

quarterly_financials = fetch_quarterly_financials(symbol)
annual_financials = fetch_annual_financials(symbol)

st.header('Financials')
selection = st.segmented_control(label='Period', options=['Quarterly', 'Annual'], default='Quarterly')