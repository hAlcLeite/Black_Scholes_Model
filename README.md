# Black_Shcoles_Model
A sleek, finance-themed Streamlit app for visualizing and analyzing financial data, built with a custom dark blue/black theme.

Black-Scholes Option Pricing Calculation:

1. Calculate Call and Put Option Prices using the Black-Scholes model.
  You can input custom parameters such as spot price, strike price, time to maturity, volatility, and risk-free interest rate.
  Real-Time Stock Price Fetching:

2. Fetch the current stock price using a stock ticker symbol via the Yahoo Finance API (optional).
  Users can also manually input the current stock price if they choose.
  Profit and Loss (PnL) Calculation:

3. Calculate the Profit and Loss (PnL) for both Call and Put options based on a specified purchase price and current option prices.
  Interactive Heatmap of Call Option Prices:

4. Visualize the Call Option Prices as a heatmap based on a range of spot prices and volatility values.
  The heatmap dynamically updates based on the user-defined ranges for spot prices and volatilities.
  Customizable Input Parameters:

5. Users can customize a variety of parameters, including:
  Spot Price Range: Define the minimum and maximum spot prices to visualize option price behaviour.
  Volatility Range: Adjust the minimum and maximum volatility values for the heatmap.
  Strike Price, Time to Maturity, and Interest Rate: You can set your own values to compute the option prices.
  Financial-Themed User Interface:

6. A sleek, black/blue-themed dashboard with a professional financial design.
  Custom colour-coded metrics for PnL (green for profit, red for loss).
  Responsive Sidebar for Inputs:

7. ll input options are neatly organized in the sidebar for a clean, easy-to-navigate interface.
  Dynamic toggling between manual stock price input and fetching real-time data.
  Visualization Enhancements:

8. The heatmap colour scheme uses a red-green gradient to represent option prices visually, with adjustments to match the app's overall dark theme.
High-contrast text and annotations to fit the finance-themed dashboard.
