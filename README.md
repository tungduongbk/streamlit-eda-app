# streamlit-eda-app

Sample API using FastAPI and Streamlit to show data on app with async http.
This API works with stock data that queries from [Yahoo Finance](https://pypi.org/project/yahoo-finance/)
and some data analytics for Convenience store brands.


## Endpoints
GET /docs - OpenAPI documentation (generated by FastAPI)
GET /stocks/history - get timeseries stock data given ticker symbol
GET /stocks/search - search any company by name, ticker and return timeseries stock.

## Requirements
Python >= 3.7
Requirements listed on requirements.txt
Streamlit installed


## Quickstart
- Clone this repo
- Start with docker-compose:
```docker-compose up -d --build```

Enter [http://localhost:8561](http://localhost:8561) to interact with app
You can go to [http://localhost:8083/docs](http://localhost:8083/docs) to see API documentation

## Demo
