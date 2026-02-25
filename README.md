<div align="center">

# 📊 Feedback Intelligence System

**Transform raw user feedback into actionable product insights**

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=flat&logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

</div>

---

A production-ready feedback intelligence pipeline that collects user reviews from multiple sources (Google Play Store and external CSV uploads), performs sentiment analysis using both rule-based and transformer models, categorizes feedback, calculates priority scores, and generates actionable insights through an interactive dashboard and PDF reports.

<br>

## 🚀 Overview

This system automates the process of collecting, analyzing, and visualizing user feedback at scale. It fetches reviews from Google Play Store and imports feedback from external CSV files, applies natural language processing techniques to understand sentiment and categorize issues, then prioritizes feedback based on negativity, frequency, and recency. The results are stored in a SQLite database, exported to CSV, and visualized through an interactive Streamlit dashboard.

**Use Cases:**
- Product managers tracking user sentiment trends
- Development teams prioritizing bug fixes based on user impact
- Customer success teams identifying recurring pain points
- Stakeholders reviewing weekly feedback summaries via PDF reports

<br>

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| **Google Play Store Integration** | Fetches up to 1000 reviews per run using the official scraper API |
| **CSV Upload Support** | Import feedback from external CSV files for batch processing |
| **Multi-Source Ingestion** | Combines data from all sources using pandas.concat() with proper source tracking |
| **Dual Sentiment Analysis** | Combines NLTK VADER (fast, rule-based) with HuggingFace DistilBERT (accurate, transformer-based) |
| **Keyword-Based Categorization** | Classifies feedback into Bug, Feature Request, Performance, UI/UX, or Other |
| **Priority Scoring Algorithm** | Multiplicative decay formula prioritizing recent, negative, frequent issues |
| **Trend Detection** | Identifies improving, declining, or stable sentiment patterns over time |
| **SQLite Persistence** | Stores all processed feedback with full schema |
| **CSV Export** | Timestamped exports for external analysis |
| **PDF Reports** | Auto-generated weekly summaries with sentiment breakdown and top issues |
| **Interactive Dashboard** | Streamlit-based UI with filters, charts, and data tables |

<br>

---

## 🧠 System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        FEEDBACK INTELLIGENCE SYSTEM                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   ┌──────────────┐    ┌──────────────┐                               │
│   │ Google Play  │    │  CSV Upload  │                               │
│   │  (Live API)  │    │   (Batch)    │                               │
│   └──────┬───────┘    └──────┬───────┘                               │
│          │                   │                                       │
│          └─────────┬─────────┘                                       │
│                    ▼                                                 │
│          ┌──────────────────┐                                        │
│          │  pandas.concat() │                                        │
│          │  (Merge Sources) │                                        │
│          └────────┬─────────┘                                        │
│                   ▼                                                  │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐          │
│   │   Cleaner    │───▶│  Sentiment   │───▶│  Categorizer │          │
│   │  (text prep) │    │  (VADER +    │    │  (keywords)  │          │
│   └──────────────┘    │  Transformer)│    └──────┬───────┘          │
│                       └──────────────┘           │                   │
│                                                  │                   │
│          ┌───────────────────────────────────────┘                   │
│          ▼                                                           │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐          │
│   │   Priority   │───▶│    Trend     │───▶│   Storage    │          │
│   │   Scoring    │    │   Analysis   │    │  (DB + CSV)  │          │
│   └──────────────┘    └──────────────┘    └──────┬───────┘          │
│                                                  │                   │
│          ┌───────────────────────────────────────┘                   │
│          ▼                                                           │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐          │
│   │   SQLite     │    │     CSV      │    │     PDF      │          │
│   │   Database   │    │    Export    │    │    Report    │          │
│   └──────────────┘    └──────────────┘    └──────────────┘          │
│                                                                      │
│   ┌─────────────────────────────────────────────────────────────┐   │
│   │                  STREAMLIT DASHBOARD                         │   │
│   │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────────────┐ │   │
│   │  │ Filters │  │ Metrics │  │ Charts  │  │ Priority Table  │ │   │
│   │  └─────────┘  └─────────┘  └─────────┘  └─────────────────┘ │   │
│   └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

<br>

---

## 🛠 Tech Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.10+ |
| Data Processing | Pandas |
| Sentiment (Rule-based) | NLTK VADER |
| Sentiment (ML) | HuggingFace Transformers (DistilBERT) |
| Data Fetching | google-play-scraper |
| Database | SQLite + SQLAlchemy ORM |
| Dashboard | Streamlit |
| Visualization | Matplotlib |
| PDF Generation | ReportLab |

<br>

---

## � Multi-Source Integration

The system supports multiple feedback sources that are combined into a unified processing pipeline:

| Source | Type | Description |
|--------|------|-------------|
| **Google Play Store** | Live API | Fetches up to 1000 reviews in real-time using `google-play-scraper` |
| **CSV Upload** | Batch File | Imports feedback from `data/external_feedback.csv` (optional) |

### How Sources Are Merged

1. **Fetch Phase**: Each source is fetched independently
   - Google Play: Live API call via `src/fetchers/google_play.py`
   - CSV: File load via `src/fetchers/csv_loader.py`

2. **Combine Phase**: DataFrames are merged using `pandas.concat()`
   - `ignore_index=True` ensures clean row indices
   - `source` column preserved (`google_play` or `CSV Upload`)

3. **Graceful Handling**:
   - If CSV file doesn't exist, pipeline continues with Google Play data only
   - If Google Play fails, pipeline continues with CSV data only
   - Record counts are printed per source for transparency

### CSV File Format

External CSV files must have these columns:
```
content,rating,date
"Great app!",5,2026-02-20
"Crashes often",1,2026-02-19
```

<br>

---

## 📁 Folder Structure

```
feedback-intelligence-system/
│
├── app.py                       # Main entry point
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── .gitignore                   # Git ignore rules
│
├── src/
│   ├── fetchers/
│   │   ├── google_play.py       # Google Play Store scraper
│   │   └── csv_loader.py        # CSV file loader
│   │
│   ├── processing/
│   │   ├── cleaner.py           # Text preprocessing
│   │   ├── sentiment.py         # VADER + Transformer sentiment
│   │   └── categorizer.py       # Keyword-based categorization
│   │
│   ├── intelligence/
│   │   ├── trend.py             # Sentiment trend analysis
│   │   └── priority.py          # Priority scoring algorithm
│   │
│   ├── database/
│   │   ├── db.py                # SQLAlchemy engine & session
│   │   └── models.py            # Feedback ORM model
│   │
│   ├── reports/
│   │   └── pdf_report.py        # PDF report generator (unused)
│   │
│   └── services/
│       ├── pipeline.py          # Main orchestration logic
│       ├── storage_service.py   # Database & CSV storage
│       ├── trend_service.py     # Trend analysis wrapper
│       └── report_service.py    # PDF report generation
│
├── dashboard/
│   └── app.py                   # Streamlit dashboard
│
└── data/
    ├── external_feedback.csv    # External CSV input (optional)
    ├── feedback.db              # SQLite database (generated)
    ├── processed_feedback_*.csv # Exported CSV files (generated)
    └── weekly_report_*.pdf      # PDF reports (generated)
```

<br>

---

## ⚙️ Installation

### Prerequisites

- Python **3.10** or higher
- pip package manager

### Steps

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/feedback-intelligence-system.git
   cd feedback-intelligence-system
   ```

2. **Create virtual environment**

   ```bash
   python -m venv myenv
   ```
   
   ```bash
   # Windows
   myenv\Scripts\activate
   
   # macOS/Linux
   source myenv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Download NLTK data** *(happens automatically on first run)*

   ```bash
   python -c "import nltk; nltk.download('vader_lexicon')"
   ```

<br>

---

## ▶️ How to Run

### Run the Pipeline

Fetches reviews, processes them, stores to database, exports CSV, and generates PDF report.

```bash
python app.py
```

<details>
<summary><b>View expected output</b></summary>

```
==================================================
Feedback Intelligence System
==================================================
Fetching Google Play reviews...
  Fetched 1000 Google Play reviews
Fetching CSV feedback...
  Fetched 150 CSV records

Records fetched per source:
  - Google Play: 1000
  - CSV: 150
Total feedback collected: 1150

Processing feedback...
  Initializing sentiment analyzer...
  Cleaning text...
  Running VADER sentiment analysis...
  Running Transformer sentiment analysis...
  Categorizing feedback...
  Calculating priority scores...
Processing complete. 1150 records processed.

Storing to database...
  Stored 1150 records to database

Saved processed data to data/processed_feedback_20260224_143052.csv

Running trend analysis...
  Overall trend: stable
  Average sentiment: 0.127

Generating PDF report...
  Report saved to data/weekly_report_20260224.pdf

==================================================
Pipeline complete!
==================================================
```

</details>

### Run the Dashboard

Interactive web interface for exploring feedback data.

```bash
streamlit run dashboard/app.py
```

> Opens at `http://localhost:8501`

<br>

---

## 📦 Output Artifacts

| Artifact | Location | Description |
|----------|----------|-------------|
| **SQLite Database** | `data/feedback.db` | Persistent storage of all processed feedback |
| **CSV Export** | `data/processed_feedback_YYYYMMDD_HHMMSS.csv` | Timestamped export for analysis |
| **PDF Report** | `data/weekly_report_YYYYMMDD.pdf` | Summary report with charts |

### Database Schema

```sql
CREATE TABLE feedback (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    content         TEXT NOT NULL,
    source          VARCHAR(50) NOT NULL,
    rating          FLOAT,
    sentiment_label VARCHAR(20),
    sentiment_score FLOAT,
    category        VARCHAR(50),
    priority_score  FLOAT,
    date            DATETIME
);
```

<br>

---

## 📊 Dashboard Capabilities

| Feature | Description |
|---------|-------------|
| **Date Range Filter** | Filter feedback by date period |
| **Source Filter** | Filter by data source (google_play, CSV Upload) |
| **Sentiment Filter** | Filter by positive/negative/neutral |
| **Metrics Cards** | Total count, avg sentiment, positive %, negative % |
| **Sentiment Pie Chart** | Visual distribution of sentiment labels |
| **Trend Line Chart** | Daily sentiment score over time |
| **Category Bar Chart** | Feedback count by category |
| **Top Issues Table** | Categories ranked by frequency with avg scores |
| **High Priority Table** | Top 10 urgent feedback items |

<br>

---

## 💡 Design Decisions

### Why VADER + Transformer?

- **VADER** is fast, requires no GPU, and performs well on social media text with emojis and slang. It's used as the primary sentiment source.
- **DistilBERT Transformer** provides higher accuracy for nuanced text. Both are computed and stored, allowing future analysis to compare or ensemble results.

### Why Multiplicative Priority Decay?

The priority formula `(negativity × recency_weight × 80) + (frequency × 3)` uses multiplication rather than addition because:

- A very negative review from 30+ days ago should **NOT** remain high priority
- Recency acts as a decay factor: even strong negativity fades over time
- This prevents stale issues from dominating the priority list

### Why Simulated Dates?

Reviews are distributed across the last 7 days using `df.index % 7` to demonstrate the trend analysis feature. In production, actual review timestamps would be preserved.

<br>

---

## ⚠️ Limitations

| Limitation | Details |
|------------|---------|
| **Single Data Source** | Currently only fetches from Google Play Store |
| **English Only** | Sentiment models trained on English text |
| **Keyword Categorization** | Simple keyword matching; no ML-based classification |
| **No Real-time Updates** | Batch processing only; no streaming |
| **Local Storage** | SQLite not suitable for distributed deployments |
| **No Authentication** | Dashboard has no access control |

<br>

---

## 🔮 Future Improvements

- [ ] Implement Reddit/Twitter social media fetchers
- [ ] Add ML-based topic modeling (LDA, BERTopic)
- [ ] Implement real-time streaming pipeline
- [ ] Add user authentication to dashboard
- [ ] Migrate to PostgreSQL for production
- [ ] Add email alerts for negative sentiment spikes
- [ ] Implement A/B comparison between app versions
- [ ] Add export to Google Sheets / Notion

<br>

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

<br>

---

## 👤 Author

**Likhith V C**

- 📧 Email: likhithvc21@gmail.com
- 🐙 GitHub: [@likhithvc](https://github.com/likhithvc)
- 💼 LinkedIn: [Likhith V C](https://linkedin.com/in/likhithvc)

<br>

---

<div align="center">

*Last updated: February 2026*

</div>
