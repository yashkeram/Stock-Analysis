from src.data_loader import fetch_price_data, fetch_fundamentals

df = fetch_price_data("AAPL")
print(df.head())

fund = fetch_fundamentals("AAPL")
print(fund)
