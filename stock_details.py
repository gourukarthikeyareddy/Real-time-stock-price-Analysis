import yfinance as yf
import csv
import boto3

# Top 50 company symbols
COMPANY_SYMBOLS = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "BRK-B", "META", "V", "UNH",
    "JNJ", "XOM", "JPM", "PG", "PYPL", "TSM", "NSRGY", "RHHBY", "CVX", "LLY",
    "WMT", "MA", "PFE", "KO", "PEP", "ABBV", "ADBE", "ORCL", "BAC", "CMCSA",
    "CSCO", "CRM", "INTC", "NFLX", "T", "VZ", "AVGO", "DIS", "TM", "MRK",
    "BMY", "HON", "ABT", "QCOM", "MDT", "LOW", "COST", "ACN", "IBM"
]

BUCKET_NAME = "daily-stock-data-bucket"  # Replace with your S3 bucket name

# Create boto3 session
session = boto3.Session(
    aws_access_key_id='*****************',  # Replace with your access key
    aws_secret_access_key='*************************',  # Replace with your secret key
    region_name='us-east-1'  # Replace with your region (e.g., 'us-east-1')
)
s3_client = session.client("s3")


def fetch_company_details(symbol):
    """
    Fetch company profile details from Yahoo Finance.
    """
    stock = yf.Ticker(symbol)
    info = stock.info
    return {
        "symbol": symbol,
        "company_name": info.get("longName"),
        "sector": info.get("sector"),
        "industry": info.get("industry"),
        "country": info.get("country"),
        "market_cap": info.get("marketCap"),
        "pe_ratio": info.get("trailingPE"),
        "exchange": info.get("exchange"),
    }


def save_to_csv(data, file_path):
    """
    Save data to a CSV file.
    """
    headers = [
        "symbol", "company_name", "sector", "industry", "country", 
        "market_cap", "pe_ratio", "exchange"
    ]
    try:
        with open(file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)
        print(f"Data saved to CSV file: {file_path}")
    except Exception as e:
        print(f"Error saving data to CSV: {e}")


def main():
    company_details = []
    for symbol in COMPANY_SYMBOLS:
        try:
            details = fetch_company_details(symbol)
            company_details.append(details)
            print(f"Fetched details for {symbol}")
        except Exception as e:
            print(f"Failed to fetch details for {symbol}: {e}")

    # Save the company details to a local CSV file
    csv_file_path = "company_details.csv"
    save_to_csv(company_details, csv_file_path)

    # Upload to S3
    s3_key = "stock_details/stock_details.csv"
    try:
        s3_client.upload_file(csv_file_path, BUCKET_NAME, s3_key)
        print(f"Uploaded {csv_file_path} to s3://{BUCKET_NAME}/{s3_key}")
    except Exception as e:
        print(f"Error uploading to S3: {e}")


if __name__ == "__main__":
    main()