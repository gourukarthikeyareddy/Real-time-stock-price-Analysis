# Real-time-stock-price-Analysis

**1. Project Overview:**

The goal of this project was to build an automated, scalable, and reliable data pipeline to fetch stock market data from the Finnhub API, and Yahoo Finance and store it in an Amazon RDS database for further analysis and reporting. The system ensures that stock data is updated daily on weekdays, leveraging AWS services such as IAM, Redshift, Lambda, S3, Secret Manager, and Event Bridge.

#  

**2. Data Sources:**

[Finnhub](https://finnhub.io/)

[Yahoo Finance](https://finance.yahoo.com/)

#  

**3. Table Design:**

**Stock_data table:**  This table stores the data of company stock price extracted from Finnhub API.

CREATE TABLE stock_data (
    symbol VARCHAR(10),
    date DATE,
    open_price FLOAT,
    close_price FLOAT,
    high_price FLOAT,
    low_price FLOAT,
    previous_close_price FLOAT,
    timestamp BIGINT
);

**Stock_details table:** This table contains the company details for the companies we are extracting from the Finnhub API. These company details are extracted from Yahoo Finance API.

CREATE TABLE stock_details (
    symbol VARCHAR(10) PRIMARY KEY,
    company_name VARCHAR(255),
    sector VARCHAR(100),
    industry VARCHAR(100),
    country VARCHAR(100),
    market_cap BIGINT,
    pe_ratio FLOAT,
    exchange VARCHAR(10)
);

#  

**4. AWS Architecture Diagram:**

![image](https://github.com/user-attachments/assets/1e3909c2-1a6f-408a-abee-c219610fe708)

#  

**5. WorkFlow:**

**1. Data Fetching and Storage**

   •	API Integration:
   
      Used Python and the requests library to interact with the Finnhub API.
      Retrieved stock data, including fields like symbol, date, open price, close price, high price, low price, and timestamps.

   •	First Lambda Function:
   
      A Lambda function was created to execute the API request and fetch stock data for the specified companies.
      The function transformed the API response into JSON and saved it to Amazon S3, organized into folders named by the current date.

   •	Event Trigger:
   
      AWS EventBridge was configured to trigger the Lambda function at 5:10 PM (EST) on weekdays.

**2. Storing Data in S3**

  •	Storage Structure:
    
    Data for each day was stored in a dedicated folder within an S3 bucket (e.g., s3://daily-stock-data-bucket/YYYY-MM-DD/).
    Multiple JSON files were created for individual stock symbols.

**3. Merging and Loading Data**

  • Lambda Function:
    
    A second Lambda function was designed to trigger at 5:15 PM (EST) after the stock data for the day was saved to S3.
    Merged all JSON files for the day into a single consolidated JSON file.
 
  • Event Trigger:
    
    AWS EventBridge was configured to trigger the Lambda function at 5:15 PM (EST) on weekdays.

  •	Data Insertion into Redshift:
    
    The merged JSON file data will be stored in the Redshift database.

