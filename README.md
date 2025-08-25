# Pharmacy KPI Dashboard & API

![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square)
![FastAPI Version](https://img.shields.io/badge/FastAPI-0.116.1-009688?style=flat-square)
![MongoDB](https://img.shields.io/badge/Database-MongoDB-4EA94B?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

A comprehensive system designed to track, analyze, and visualize key performance indicators (KPIs) for pharmacies. This project features a robust FastAPI-based API for data access and a user-friendly web dashboard for insightful visualizations.

## ✨ Features

* **API Endpoints:** Provides a rich set of API endpoints to access calculated KPIs, including sales value, prescription volume, inventory levels, stock-outs, near expiries, cash reconciliation, and top sellers.
* **Efficient Data Processing:** Leverages Pandas and NumPy for high-performance data loading and preprocessing from CSV files into a MongoDB database.
* **Interactive Web Dashboard:** A simple yet effective web interface (built with Flask and Jinja2) to present key pharmacy metrics in an easily digestible format.
* **Modular Architecture:** Organized into distinct modules for API routers, data processing services, and a dedicated script for seamless data ingestion, promoting maintainability and scalability.

## 🚀 Technologies Used

* **Backend:** Python, FastAPI, Uvicorn, Motor (async MongoDB driver)
* **Data Processing:** Pandas, NumPy
* **Database:** MongoDB
* **Web Dashboard:** Flask, Jinja2
* **Dependency Management:** `pip`

## 🛠️ Installation

### Prerequisites

Before you begin, ensure you have the following installed:

* **Python 3.8+**
* **MongoDB:** Install MongoDB and ensure it's running, or have access to a MongoDB Atlas cluster.

### Setup Steps

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/pharmacy-kpi.git
    cd pharmacy-kpi
    ```

2. **Create a virtual environment:**

    ```bash
    python -m venv .venv
    ```

3. **Activate the virtual environment:**

    * **Windows:**

        ```bash
        .venv\Scripts\activate
        ```

    * **macOS/Linux:**

        ```bash
        source .venv/bin/activate
        ```

4. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

5. **Configure Environment Variables:**
    Create a `.env` file in the root directory of the project (`c:\Users\Ahmed\DEV PROJECTS\pharmacy-kpi\.env`) and add your MongoDB connection string and database name:

    ```env
    MONGO_URI="mongodb://localhost:27017/" # Or your MongoDB Atlas connection string
    DB_NAME="pharmacy_kpi_db"
    ```

## 💡 Usage

### 1. Loading Data

The project includes a convenient script to load your initial CSV data into MongoDB. Ensure your primary dataset (`all_in_one_kpi_dataset.csv`) is placed within the `data/` directory.

```bash
python scripts/load_csv_to_db.py
```

*Note: If your CSV file has a different name or structure, you may need to modify `scripts/load_csv_to_db.py` accordingly.*

### 2. Running the FastAPI Application

Start the API server using Uvicorn. This will make the KPI data accessible via RESTful endpoints.

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be accessible at `http://localhost:8000`. You can explore the interactive API documentation (Swagger UI) at `http://localhost:8000/docs`.

### 3. Accessing the Dashboard

The dashboard is a separate Flask application that provides a visual overview of the KPIs. While the FastAPI application is running, open a **new terminal**, activate your virtual environment, and run the dashboard app:

```bash
cd reporting
python app.py
```

The dashboard will typically be accessible in your web browser at `http://127.0.0.1:5000/`.

### API Endpoints Overview

The API is structured with various endpoints, each dedicated to a specific category of pharmacy KPIs:

* `/sales`: Sales value and revenue-related KPIs.
* `/rx_volume`: Prescription volume and related metrics.
* `/inventory`: Current inventory levels and stock status.
* `/stock_outs`: Analysis of out-of-stock incidents.
* `/near_expiries`: Products nearing their expiry dates.
* `/cash_reconciliation`: Insights into cash flow and reconciliation.
* `/top_sellers`: Identification of best-selling products.

For detailed information on each endpoint, including request/response schemas, please refer to the interactive API documentation at `http://localhost:8000/docs`.

## 📂 Project Structure

```directory
.
├── .env                      # Environment variables for database connection
├── api_descriptions.json     # (Optional) API endpoint descriptions
├── config.py                 # Application-wide configuration settings
├── database.py               # MongoDB connection and setup
├── dependencies.py           # FastAPI dependency injection utilities
├── main.py                   # Main FastAPI application entry point
├── models.py                 # Pydantic models for data validation and serialization
├── README.md                 # Project README file
├── requirements.txt          # Python package dependencies
├── test_endpoints.py         # Unit and integration tests for API endpoints
├── .venv/                    # Python virtual environment
├── data/
│   └── all_in_one_kpi_dataset.csv # Sample dataset for loading
├── notebooks/                # Jupyter notebooks for data exploration and analysis
├── reporting/
│   ├── app.py                # Flask application for the web dashboard
│   └── templates/
│       └── dashboard.html    # HTML template for the dashboard UI
├── routers/                  # FastAPI routers, each handling specific KPI categories
│   ├── cash_reconciliation.py
│   ├── inventory_levels.py
│   ├── near_expiries.py
│   ├── rx_volume.py
│   ├── sales_value.py
│   ├── stock_outs.py
│   └── top_sellers.py
└── services/                 # Business logic, data processing, and calculation functions
    ├── calculations.py
    └── data_preprocessing.py
```

## 🤝 Contributing

Contributions are highly welcome! If you'd like to contribute, please fork the repository, create a new branch for your features or bug fixes, and submit a pull request.

## 📄 License

This project is licensed under the MIT License. A `LICENSE` file should be created in the root directory of the project for full details.

## 📧 Contact

For any questions, feedback, or issues, please open an issue on the GitHub repository.
