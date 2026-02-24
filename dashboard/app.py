"""
Streamlit dashboard application.

Interactive dashboard for visualizing feedback insights and analytics.
"""

import os
import glob
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# Page configuration
st.set_page_config(
    page_title="Feedback Intelligence Dashboard",
    page_icon="📊",
    layout="wide"
)


def load_latest_csv():
    """Load the most recent processed CSV file from data/ folder."""
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    csv_files = glob.glob(os.path.join(data_dir, "processed_feedback_*.csv"))
    
    if not csv_files:
        return None
    
    # Get most recent file
    latest_file = max(csv_files, key=os.path.getctime)
    df = pd.read_csv(latest_file)
    df['date'] = pd.to_datetime(df['date'])
    return df


def apply_filters(df, date_range, sources, sentiments):
    """Apply sidebar filters to dataframe."""
    filtered = df.copy()
    
    # Date filter
    filtered = filtered[
        (filtered['date'].dt.date >= date_range[0]) &
        (filtered['date'].dt.date <= date_range[1])
    ]
    
    # Source filter
    if sources:
        filtered = filtered[filtered['source'].isin(sources)]
    
    # Sentiment filter
    if sentiments:
        filtered = filtered[filtered['sentiment_label'].isin(sentiments)]
    
    return filtered


def main():
    """Main dashboard application."""
    st.title("📊 Feedback Intelligence Dashboard")
    
    # Load data
    df = load_latest_csv()
    
    if df is None or df.empty:
        st.warning("No processed feedback data found. Run app.py first to generate data.")
        return
    
    # Sidebar filters
    st.sidebar.header("Filters")
    
    # Date range filter
    min_date = df['date'].min().date()
    max_date = df['date'].max().date()
    date_range = st.sidebar.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Ensure date_range is a tuple of two dates
    if len(date_range) != 2:
        date_range = (min_date, max_date)
    
    # Source filter
    all_sources = df['source'].unique().tolist()
    sources = st.sidebar.multiselect("Source", all_sources, default=all_sources)
    
    # Sentiment filter
    all_sentiments = df['sentiment_label'].unique().tolist()
    sentiments = st.sidebar.multiselect("Sentiment", all_sentiments, default=all_sentiments)
    
    # Apply filters
    filtered_df = apply_filters(df, date_range, sources, sentiments)
    
    if filtered_df.empty:
        st.warning("No data matches the selected filters.")
        return
    
    # Metrics row
    st.header("Overview")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Feedback", len(filtered_df))
    
    with col2:
        avg_sentiment = filtered_df['sentiment_score'].mean()
        st.metric("Avg Sentiment", f"{avg_sentiment:.3f}")
    
    with col3:
        positive_pct = (filtered_df['sentiment_label'] == 'positive').mean() * 100
        st.metric("Positive %", f"{positive_pct:.1f}%")
    
    with col4:
        negative_pct = (filtered_df['sentiment_label'] == 'negative').mean() * 100
        st.metric("Negative %", f"{negative_pct:.1f}%")
    
    st.divider()
    
    # Charts row
    chart_col1, chart_col2 = st.columns(2)
    
    # Sentiment distribution pie chart
    with chart_col1:
        st.subheader("Sentiment Distribution")
        sentiment_counts = filtered_df['sentiment_label'].value_counts()
        
        fig1, ax1 = plt.subplots(figsize=(6, 4))
        colors = {'positive': '#2ecc71', 'negative': '#e74c3c', 'neutral': '#95a5a6'}
        pie_colors = [colors.get(label, '#3498db') for label in sentiment_counts.index]
        ax1.pie(
            sentiment_counts.values,
            labels=sentiment_counts.index,
            autopct='%1.1f%%',
            colors=pie_colors,
            startangle=90
        )
        ax1.axis('equal')
        st.pyplot(fig1)
        plt.close(fig1)
    
    # Trend line chart
    with chart_col2:
        st.subheader("Sentiment Trend Over Time")
        daily_sentiment = filtered_df.groupby(filtered_df['date'].dt.date)['sentiment_score'].mean()
        
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        ax2.plot(daily_sentiment.index, daily_sentiment.values, marker='o', linewidth=2, color='#3498db')
        ax2.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
        ax2.set_xlabel("Date")
        ax2.set_ylabel("Avg Sentiment Score")
        ax2.tick_params(axis='x', rotation=45)
        fig2.tight_layout()
        st.pyplot(fig2)
        plt.close(fig2)
    
    st.divider()
    
    # Category breakdown
    st.header("Category Analysis")
    cat_col1, cat_col2 = st.columns(2)
    
    with cat_col1:
        st.subheader("Feedback by Category")
        category_counts = filtered_df['category'].value_counts()
        
        fig3, ax3 = plt.subplots(figsize=(6, 4))
        bars = ax3.barh(category_counts.index, category_counts.values, color='#3498db')
        ax3.set_xlabel("Count")
        ax3.invert_yaxis()
        fig3.tight_layout()
        st.pyplot(fig3)
        plt.close(fig3)
    
    with cat_col2:
        st.subheader("Top 5 Issues by Frequency")
        top_issues = filtered_df.groupby('category').agg({
            'content': 'count',
            'sentiment_score': 'mean',
            'priority_score': 'mean'
        }).rename(columns={'content': 'count'})
        top_issues = top_issues.sort_values('count', ascending=False).head(5)
        top_issues['sentiment_score'] = top_issues['sentiment_score'].round(3)
        top_issues['priority_score'] = top_issues['priority_score'].round(2)
        st.dataframe(top_issues, use_container_width=True)
    
    st.divider()
    
    # Recent high priority feedback
    st.header("High Priority Feedback")
    high_priority = filtered_df.nlargest(10, 'priority_score')[
        ['date', 'source', 'category', 'sentiment_label', 'priority_score', 'content']
    ].copy()
    high_priority['date'] = high_priority['date'].dt.strftime('%Y-%m-%d')
    high_priority['content'] = high_priority['content'].str[:100] + '...'
    st.dataframe(high_priority, use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()