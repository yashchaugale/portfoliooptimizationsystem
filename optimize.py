import streamlit as st
import pickle
import numpy as np
import pandas as pd

# Load the model data for portfolio optimization
@st.cache
def load_model():
    with open('savedsteps1.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

data = load_model()    
Maxreturnincl = data["MaxReturnShortincl"] 
MaxReturnNoShort = data["MaxReturnNoShort"]
MinVararray = data["MinVararray"]

# Define stocks for portfolio optimization globally
stocks = [
    "GOOGL", "RWE.DE", "O", "KO", "CRWD", "LIN", "CLH", "ENPH", 
    "PEP", "MSFT", "ASML.AS", "PRX.AS", "NPI.TO", "PG", "EL", 
    "VALE", "ALB", "MP", "BHP.AX"
]

def show_weights(weights, selected_stocks):
    stock_weights = {stock: weight for stock, weight in zip(stocks, weights)}
    for stock in selected_stocks:
        if stock in stock_weights:
            percentage = stock_weights[stock] * 100
            st.write(f"{stock}: {percentage:.2f}%")

def plot_comparison(custom_portfolio, max_return_short, max_return_no_short, min_var):
    portfolio_df = pd.DataFrame({
        'Custom Portfolio': custom_portfolio,
        'Max Return (Short)': max_return_short,
        'Max Return (No Short)': max_return_no_short,
        'Min Variance': min_var
    })
    st.line_chart(portfolio_df)

def portfolio_optimization():
    st.title("Portfolio Optimization")

    selected_stocks = st.multiselect("Choose your stocks:", stocks, key="stock_selector")

    if st.button("Maximum Return with Short"):
        if selected_stocks:
            st.subheader("Weights (Maximum Return with Shorting)")
            show_weights(Maxreturnincl, selected_stocks)
        else:
            st.warning("Please select at least one stock.")
    
    if st.button("Maximum Return without Short"):
        if selected_stocks:
            st.subheader("Weights (Maximum Return without Shorting)")
            show_weights(MaxReturnNoShort, selected_stocks)
        else:
            st.warning("Please select at least one stock.")
    
    if st.button("Minimum Variance"):
        if selected_stocks:
            st.subheader("Weights (Minimum Variance)")
            show_weights(MinVararray, selected_stocks)
        else:
            st.warning("Please select at least one stock.")

    custom_weights = []
    if selected_stocks:
        st.write("Enter the weightages for the selected stocks:")
        for stock in selected_stocks:
            weight = st.number_input(f"Weight for {stock} (%)", min_value=0.0, value=5.0, key=f"weight_input_{stock}")
            custom_weights.append(weight)

    if st.button("Compare Portfolios"):
        if selected_stocks and len(custom_weights) == len(selected_stocks):
            st.subheader("Portfolio Comparison")
            custom_weights = np.array(custom_weights) / 100  # Convert percentage to decimal
            cumulative_returns = np.random.normal(loc=1.02, scale=0.02, size=(len(stocks), 100))
            stock_indices = [stocks.index(stock) for stock in selected_stocks]
            selected_returns = cumulative_returns[stock_indices, :]
            custom_portfolio = np.dot(custom_weights, selected_returns)
            max_return_short_portfolio = np.dot(Maxreturnincl, cumulative_returns)
            max_return_no_short_portfolio = np.dot(MaxReturnNoShort, cumulative_returns)
            min_var_portfolio = np.dot(MinVararray, cumulative_returns)
            plot_comparison(custom_portfolio, max_return_short_portfolio, max_return_no_short_portfolio, min_var_portfolio)
        else:
            st.warning("Please select stocks and provide weightages for all selected stocks.")
