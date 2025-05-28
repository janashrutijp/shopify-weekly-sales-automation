# main.py

from email_report import send_email_with_pdf
from fetch_shopify_data import fetch_orders
from generate_report import generate_pdf

if __name__ == "__main__":
    print("📥 Fetching data...")

    # Use certifi for SSL verification inside fetch_orders or here if needed
    df = fetch_orders()
    print(f"✅ {len(df)} orders fetched.")
    print("Columns:", list(df.columns))
    print(df.head())  # Shows the first few rows of data
    if df.empty:
        print("No orders this week.")
    else:
        print("✅ Orders fetched:", len(df))
        print("Generating PDF report...")
        generate_pdf(df)

        print("Sending report...")
        send_email_with_pdf(
            subject="Weekly Shopify Sales Report",
            body="Hi,\n\nPlease find attached the latest weekly sales report.\n\nBest,\nYour Intern.",
            attachment_path="weekly_report.pdf"
        )
