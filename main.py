import streamlit as st
from optimize import portfolio_optimization
from predict import stock_prediction

def main():
    st.sidebar.title("Navigation")
    options = st.sidebar.radio("Select an option:", ("Portfolio Optimization", "Stock Prediction"))

    if options == "Portfolio Optimization":
        portfolio_optimization()
    elif options == "Stock Prediction":
        stock_prediction()

# Run the app
if __name__ == "__main__":
    main()
