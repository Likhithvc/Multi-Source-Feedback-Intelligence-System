"""
Report service module.

Handles PDF report generation.
"""

import os
from datetime import datetime

import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


# Configuration
REPORT_DIR = "data"


def generate_pdf_report(df: pd.DataFrame, trends: dict):
    """Generate weekly PDF report."""
    if df.empty:
        return
    
    os.makedirs(REPORT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d")
    filepath = os.path.join(REPORT_DIR, f"weekly_report_{timestamp}.pdf")
    
    print(f"\nGenerating PDF report...")
    
    try:
        c = canvas.Canvas(filepath, pagesize=letter)
        width, height = letter
        
        # Title
        c.setFont("Helvetica-Bold", 20)
        c.drawString(50, height - 50, "Feedback Intelligence Report")
        
        # Date
        c.setFont("Helvetica", 12)
        c.drawString(50, height - 75, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        # Summary section
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, height - 110, "Summary")
        
        c.setFont("Helvetica", 11)
        y = height - 135
        c.drawString(50, y, f"Total Feedback Analyzed: {len(df)}")
        y -= 20
        c.drawString(50, y, f"Overall Sentiment Trend: {trends.get('overall_trend', 'N/A')}")
        y -= 20
        c.drawString(50, y, f"Average Sentiment Score: {trends.get('avg_sentiment', 'N/A')}")
        
        # Sentiment breakdown
        y -= 40
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, "Sentiment Breakdown")
        
        c.setFont("Helvetica", 11)
        y -= 25
        sentiment_counts = df['sentiment_label'].value_counts().to_dict()
        for label, count in sentiment_counts.items():
            pct = count / len(df) * 100
            c.drawString(50, y, f"{label.capitalize()}: {count} ({pct:.1f}%)")
            y -= 18
        
        # Category breakdown
        y -= 25
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, "Category Breakdown")
        
        c.setFont("Helvetica", 11)
        y -= 25
        category_counts = df['category'].value_counts().to_dict()
        for category, count in category_counts.items():
            pct = count / len(df) * 100
            c.drawString(50, y, f"{category}: {count} ({pct:.1f}%)")
            y -= 18
        
        # High priority issues
        y -= 25
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, "Top Priority Issues")
        
        c.setFont("Helvetica", 10)
        y -= 25
        high_priority = df.nlargest(5, 'priority_score')[['content', 'category', 'priority_score']]
        for _, row in high_priority.iterrows():
            content_preview = row['content'][:60] + "..." if len(row['content']) > 60 else row['content']
            c.drawString(50, y, f"[{row['category']}] Score: {row['priority_score']:.1f}")
            y -= 15
            c.drawString(60, y, content_preview)
            y -= 20
            if y < 100:
                break
        
        c.save()
        print(f"  Report saved to {filepath}")
    except Exception as e:
        print(f"  Error generating PDF report: {e}")
