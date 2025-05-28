# generate_report.py

import matplotlib.pyplot as plt
from fpdf import FPDF
import pandas as pd
import os

def create_visuals(df):
    plt.figure(figsize=(10, 6))

    # Convert 'created_at' to datetime
    df['Date'] = pd.to_datetime(df['created_at'])

    # Create 'Total' column from line_items if not present
    if 'Total' not in df.columns:
        df['Total'] = df['line_items'].apply(
            lambda items: sum(item['quantity'] * float(item['price']) for item in items)
        )

    # Group by date and sum sales
    daily_sales = df.groupby(df['Date'].dt.date)['Total'].sum()
    daily_sales.plot(kind='bar', color='skyblue')

    plt.title("Daily Sales")
    plt.ylabel("Total Amount")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("sales_chart.png")
    plt.close()

def generate_pdf(df, output_path="weekly_report.pdf"):
    create_visuals(df)

    pdf = FPDF()
    pdf.add_page()

    # Title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "Weekly Shopify Sales Report", ln=True, align='C')
    pdf.ln(10)

    # Create 'Total' column if needed again
    if 'Total' not in df.columns:
        df['Total'] = df['line_items'].apply(
            lambda items: sum(item['quantity'] * float(item['price']) for item in items)
        )

    # Summary stats
    total_revenue = df['Total'].sum()
    num_orders = len(df)
    avg_order = df['Total'].mean()

    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"Total Revenue: ${total_revenue:.2f}", ln=True)
    pdf.cell(200, 10, f"Number of Orders: {num_orders}", ln=True)
    pdf.cell(200, 10, f"Average Order Value: ${avg_order:.2f}", ln=True)
    pdf.ln(10)

    # Insert chart
    pdf.image("sales_chart.png", x=10, w=180)

    # Save and cleanup
    pdf.output(output_path)
    os.remove("sales_chart.png")
