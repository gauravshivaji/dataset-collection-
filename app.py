import streamlit as st
import yfinance as yf
import pandas as pd

st.title("NIFTY 500 Closing Price Downloader")

st.write("Download closing price dataset for all Nifty 500 stocks")

# Select date range
start_date = st.date_input("Start Date")
end_date = st.date_input("End Date")

# Load ticker list
symbols = pd.read_csv("nifty500_symbols.csv")
tickers = symbols["Symbol"].tolist()

if st.button("Download Closing Prices"):

    st.write("Fetching data... please wait")

    ticker_string = " ".join(tickers)

    # Download data from Yahoo Finance
    data = yf.download(
        ticker_string,
        start=start_date,
        end=end_date,
        group_by="ticker",
        threads=True,
        progress=False
    )

    final_data = []

    for ticker in tickers:

        try:
            close_prices = data[ticker]["Close"]

            df = close_prices.reset_index()

            df["Ticker"] = ticker

            final_data.append(df)

        except:
            pass

    result = pd.concat(final_data)

    result = result[["Date", "Ticker", "Close"]]

    st.success("Data Downloaded Successfully")

    st.dataframe(result)

    # CSV Download
    csv = result.to_csv(index=False)

    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="nifty500_closing_prices.csv",
        mime="text/csv"
    )

    # Excel Download
    excel_file = "nifty500_closing_prices.xlsx"
    result.to_excel(excel_file, index=False)

    with open(excel_file, "rb") as f:
        st.download_button(
            label="Download Excel",
            data=f,
            file_name=excel_file
        )
