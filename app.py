import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from src.black_scholes import BlackScholes
from src.yahoo_api import get_stock_price
from src.pnl_calculator import calculate_pnl

# Page configuration
st.set_page_config(
    page_title="Black-Scholes Option Pricing Model",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Function to create heatmap data
def generate_heatmap_data(bs_model, spot_range, vol_range):
    call_prices = np.zeros((len(vol_range), len(spot_range)))
    put_prices = np.zeros((len(vol_range), len(spot_range)))

    # Generate the call and put prices for each combination of spot price and volatility
    for i, vol in enumerate(vol_range):
        for j, spot in enumerate(spot_range):
            bs_temp = BlackScholes(spot, bs_model.strike, bs_model.time_to_maturity, vol, bs_model.interest_rate)
            call_price, put_price = bs_temp.calculate_option_prices()
            call_prices[i, j] = call_price
            put_prices[i, j] = put_price

    return call_prices, put_prices

# Sidebar for User Inputs
with st.sidebar:
    st.title("📊 Black-Scholes Model Dashboard")
    st.write("`Created by Henrique Leite")

    # Option to choose between using a stock ticker or inputting the current price manually
    price_input_method = st.radio("Choose how to input the current price:", 
                                  ("Input Manually", "Fetch via Stock Ticker"))

    if price_input_method == "Fetch via Stock Ticker":
        # Input for Stock Ticker
        ticker = st.text_input("Enter Stock Ticker Symbol", value="AAPL")
        fetch_price_btn = st.button('Fetch Price')

        # Fetch stock price from Yahoo Finance API
        if fetch_price_btn:
            current_price = get_stock_price(ticker)
            if current_price:
                st.success(f"The current price of {ticker} is ${current_price:.2f}")
            else:
                st.error("Invalid ticker symbol or unable to fetch data.")
        else:
            current_price = 100.0  # Default value when no price is fetched

    else:
        # Input the current price manually
        current_price = st.number_input("Enter Current Price", value=100.0, min_value=0.0)

    # Other option parameters
    strike = st.number_input("Strike Price", value=100.0)
    time_to_maturity = st.number_input("Time to Maturity (Years)", value=1.0)
    volatility = st.number_input("Volatility (σ)", value=0.2)
    interest_rate = st.number_input("Risk-Free Interest Rate", value=0.05)

    # Heatmap range inputs
    spot_min = st.number_input('Min Spot Price', min_value=0.01, value=current_price * 0.8, step=0.01)
    spot_max = st.number_input('Max Spot Price', min_value=0.01, value=current_price * 1.2, step=0.01)
    vol_min = st.slider('Min Volatility for Heatmap', min_value=0.01, max_value=1.0, value=volatility * 0.5, step=0.01)
    vol_max = st.slider('Max Volatility for Heatmap', min_value=0.01, max_value=1.0, value=volatility * 1.5, step=0.01)
    
    spot_range = np.linspace(spot_min, spot_max, 10)
    vol_range = np.linspace(vol_min, vol_max, 10)

    # PnL inputs
    purchase_price_call = st.number_input("Purchase Price for Call Option", value=0.0)
    purchase_price_put = st.number_input("Purchase Price for Put Option", value=0.0)

# Main Page for Output Display
st.title("Black-Scholes Pricing Model Dashboard")

# Calculate Call and Put prices using Black-Scholes model
bs_model = BlackScholes(current_price, strike, time_to_maturity, volatility, interest_rate)
call_price, put_price = bs_model.calculate_option_prices()

# Calculate PnL for Call and Put options
pnl_call = calculate_pnl('call', purchase_price_call, call_price)
pnl_put = calculate_pnl('put', purchase_price_put, put_price)

# Display calculated option prices and PnL
st.subheader("Calculated Option Prices and PnL")

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.markdown(f"""
        <div class="metric-container metric-call">
            <div>
                <div class="metric-label">CALL Value</div>
                <div class="metric-value">${call_price:.2f}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="metric-container metric-put">
            <div>
                <div class="metric-label">PUT Value</div>
                <div class="metric-value">${put_price:.2f}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="metric-container metric-pnl">
            <div>
                <div class="metric-label">PnL (Call)</div>
                <div class="metric-value" style="color: {'green' if pnl_call >= 0 else 'red'}">${pnl_call:.2f}</div>
            </div>
            <div>
                <div class="metric-label">PnL (Put)</div>
                <div class="metric-value" style="color: {'green' if pnl_put >= 0 else 'red'}">${pnl_put:.2f}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# Heatmap for Call Prices
st.subheader("Heatmap of Call Option Prices")
call_prices, put_prices = generate_heatmap_data(bs_model, spot_range, vol_range)

# Create the heatmap figure with a dark background and white text
fig, ax = plt.subplots(figsize=(10, 8))

# Set the figure background color (outer area)
fig.patch.set_facecolor('#0E1117')  # Matching the Streamlit background

# Set the axis background color (plot area)
ax.set_facecolor('#0E1117')  # Matching the Streamlit background

# Create heatmap with red-yellow-green color scheme
sns.heatmap(call_prices, 
            xticklabels=np.round(spot_range, 2), 
            yticklabels=np.round(vol_range, 2), 
            annot=True, fmt=".2f", cmap="RdYlGn", 
            ax=ax, 
            cbar_kws={'ticks': [0, 5, 10, 15, 20, 25, 30]})  # Customizing the color bar ticks

# Set axis label and title colors to match the dark theme
ax.set_title('CALL Price Heatmap', color='#FAFAFA', fontsize=16)
ax.set_xlabel('Spot Price', color='#FAFAFA')
ax.set_ylabel('Volatility', color='#FAFAFA')

# Customize tick labels' colors to white for contrast
ax.tick_params(axis='x', colors='#FAFAFA')
ax.tick_params(axis='y', colors='#FAFAFA')

# Update the color bar label and ticks to fit the theme
cbar = ax.collections[0].colorbar
cbar.ax.yaxis.set_tick_params(color='#FAFAFA')  # Color of the tick marks
plt.setp(cbar.ax.yaxis.get_ticklabels(), color='#FAFAFA')  # Color of the tick labels

# Render the heatmap in the Streamlit app
st.pyplot(fig)

