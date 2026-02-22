# Feedback Intelligence System

A multi-source feedback intelligence system that collects, analyzes, and visualizes user feedback.

## Project Structure

```
├── src/
│   ├── fetchers/         # Data collection modules
│   ├── processing/       # Text processing & analysis
│   ├── intelligence/     # Trend & priority analysis
│   ├── reports/          # Report generation
│   └── database/         # Database models & connections
├── dashboard/            # Streamlit dashboard
├── data/                 # Data storage
├── app.py                # Main entry point
├── requirements.txt      # Dependencies
└── .env.example          # Environment variables template
```

## Setup

1. Create a virtual environment
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and configure your API keys
4. Run the application: `python app.py`
