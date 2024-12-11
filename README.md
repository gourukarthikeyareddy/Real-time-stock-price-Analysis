# Real-time-stock-price-Analysis

**1. Project Overview:**

This project aimed to build an automated, scalable, and reliable data pipeline to fetch stock market data from the Finnhub API, and Yahoo Finance and store it in AWS Redshift for further analysis and reporting. The system ensures that stock data is updated daily on weekdays, leveraging AWS services such as IAM, Redshift, Lambda, S3, Secret Manager, and Event Bridge.

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

Sample Data:

{

        "symbol": "AAPL",
        
        "date": "2024-11-28",
        
        "open_price": 234.465,
        
        "close_price": 234.93,
        
        "high_price": 235.69,
        
        "low_price": 233.8101,
        
        "previous_close_price": 235.06,
        
        "timestamp": 1732741200
        
    }

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


Sample Data:

{

        "symbol": "AAPL",
        
        "company_name": "Apple Inc.",
        
        "sector": "Technology",
        
        "industry": "Consumer Electronics",
        
        "country": "United States",
        
        "market_cap": 3550927912960,
        
        "pe_ratio": 38.57389,
        
        "exchange": "NMS"
        
    }

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

      CRON Expression : cron(0 17 ? * MON-FRI *)

**2. Storing Data in S3**

  •	Storage Structure:
    
    Data for each day was stored in a dedicated folder within an S3 bucket (e.g., s3://daily-stock-data-bucket/YYYY-MM-DD/).
    Multiple JSON files were created for individual stock symbols.

**3. Merging and Loading Data**

  • Lambda Function:
    
    A second Lambda function was designed to trigger at 5:15 PM (EST) after the stock data for the day was saved to S3.
    Merged all JSON files for the day into a single consolidated JSON file.

    CRON Expression : cron(15 17 ? * MON-FRI *)
 
  • Event Trigger:
    
    AWS EventBridge was configured to trigger the Lambda function at 5:15 PM (EST) on weekdays.

  •	Data Insertion into Redshift:
    
    The merged JSON file data will be stored in the Redshift database.

#  

**5. Tableau Dashboard**

![image](https://github.com/user-attachments/assets/5b104dc1-1b2f-476a-9367-c1e34f9d2b04)
