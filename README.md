# ECB FX REST API
A simple REST API that provides historical foreign exchange (FX) rates published by the European Central Bank (ECB).

# Application flow
ECB Historical Data -->Data Updater -->ecb_rates.csv -->data_loader.py-->main.py -->FastAPI -->Swagger/Postman
# Overview
The ECB FX REST API allows users to retrieve exchange rates for a specific date and currency pair.
The API uses ECB historical exchange-rate data stored in a CSV file and provides the data through REST endpoints.

# Features
- Retrieve exchange rate for a specific date and currency pair
- Retrieve exchange rates for a date range
- Supports different currencies available in the ECB dataset
- Handles invalid dates and currencies
- Automatic data loading using Pandas
- Swagger/OpenAPI documentation
- Unit tests using Pytest
- Separate data updater component for refreshing ECB data

# Technology Stack
- Python
- FastAPI
- Pandas
- Uvicorn
- Pytest
- REST API
- Swagger / OpenAPI

# Project Structure
ecb_fx_api/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── data_loader.py
│   └── updater.py
│
├── data/
│   └── ecb_rates.csv
│
├── tests/
│   └── test_api.py
│
├── ecb_updater.py
├── requirements.txt
├── .gitignore
└── README.md
