"""
Lab 2 — Data Pipeline: Retail Sales Analysis
Module 2 — Programming for AI & Data Science

Complete each function below. Remove the TODO: comments and pass statements
as you implement each function. Do not change the function signatures.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# ─── Configuration ────────────────────────────────────────────────────────────

DATA_PATH = 'data/sales_records.csv'
OUTPUT_DIR = 'output'


# ─── Pipeline Functions ───────────────────────────────────────────────────────

def load_data(filepath):
    """Load sales records from a CSV file.

    Args:
        filepath (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Raw sales records DataFrame.
    """
    df = pd.read_csv(filepath)
    print(f"Loaded {len(df)} records from {filepath}")
    return df


def clean_data(df):
    """Handle missing values and fix data types.

    - Fill missing 'quantity' values with the column median.
    - Fill missing 'unit_price' values with the column median.
    - Parse the 'date' column to datetime (use errors='coerce' to handle malformatted dates).
    - Print a progress message showing the record count after cleaning.

    Args:
        df (pd.DataFrame): Raw DataFrame from load_data().

    Returns:
        pd.DataFrame: Cleaned DataFrame (do not modify the input in place).
    """
    df = df.copy()
    df['quantity'] = df['quantity'].fillna(df['quantity'].median())
    df['unit_price'] = df['unit_price'].fillna(df['unit_price'].median())
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(subset=['quantity', 'unit_price'])
    print(f"Cleaned data: {len(df)} records")
    return df


def add_features(df):
    """Compute derived columns.

    - Add 'revenue' column: quantity * unit_price.
    - Add 'day_of_week' column: day name from the date column.

    Args:
        df (pd.DataFrame): Cleaned DataFrame from clean_data().

    Returns:
        pd.DataFrame: DataFrame with new columns added.
    """
    df['revenue'] = df['quantity'] * df['unit_price']
    df['day_of_week'] = df['date'].dt.day_name()
    return df


def generate_summary(df):
    """Compute summary statistics.

    Args:
        df (pd.DataFrame): Enriched DataFrame from add_features().

    Returns:
        dict: Summary with keys:
            - 'total_revenue': total revenue (sum)
            - 'avg_order_value': average order value (mean)
            - 'top_category': product category with highest total revenue
            - 'record_count': number of records in df
    """
    def generate_summary(df):
     """Compute summary statistics. Returns a dict."""
    summary = {
        'total_revenue': df['revenue'].sum(),
        'avg_order_value': df['revenue'].mean(),
        'top_category': df.groupby('product_category')['revenue'].sum().idxmax(),
        'record_count': len(df)
    }
    return summary


def create_visualizations(df, output_dir=OUTPUT_DIR):
    """Create and save 3 charts as PNG files.

    Charts to create:
    1. Bar chart: total revenue by product category
    2. Line chart: daily revenue trend (aggregate revenue by date)
    3. Horizontal bar chart: average order value by payment method

    Save each chart as a PNG using fig.savefig().
    Do NOT use plt.show() — it blocks execution in pipeline scripts.
    Close each figure with plt.close(fig) after saving.

    Args:
        df (pd.DataFrame): Enriched DataFrame from add_features().
        output_dir (str): Directory to save PNG files (create if needed).
    """
    import matplotlib.pyplot as plt
import os

def create_visualizations(df, output_dir='output'):
    """Create and save 3 charts to output_dir."""
    os.makedirs(output_dir, exist_ok=True)
    
    # الرسمة 1: إجمالي الإيرادات لكل فئة منتج
    fig, ax = plt.subplots()
    df.groupby('product_category')['revenue'].sum().plot(kind='bar', ax=ax)
    ax.set_title('Total Revenue by Category')
    fig.savefig(f'{output_dir}/revenue_by_category.png', dpi=150, bbox_inches='tight')
    plt.close(fig)

    # الرسمة 2: اتجاه الإيرادات اليومي
    fig, ax = plt.subplots()
    df.groupby('date')['revenue'].sum().plot(kind='line', ax=ax)
    ax.set_title('Daily Revenue Trend')
    fig.savefig(f'{output_dir}/daily_revenue_trend.png', dpi=150, bbox_inches='tight')
    plt.close(fig)

    # الرسمة 3: متوسط قيمة الطلب حسب طريقة الدفع
    fig, ax = plt.subplots()
    df.groupby('payment_method')['revenue'].mean().plot(kind='barh', ax=ax)
    ax.set_title('Avg Order Value by Payment Method')
    fig.savefig(f'{output_dir}/avg_order_by_payment.png', dpi=150, bbox_inches='tight')
    plt.close(fig)


def main():
    """Run the full data pipeline end-to-end."""
    def main():
     """Run the full pipeline end-to-end."""
    # 1. تحميل
    df = load_data('data/sales_records.csv')
    # 2. تنظيف
    df = clean_data(df)
    # 3. إضافة ميزات
    df = add_features(df)
    # 4. ملخص الإحصائيات
    summary = generate_summary(df)
    print("\n=== Summary Statistics ===")
    for key, value in summary.items():
        print(f"{key}: {value}")
    
    # 5. الرسومات البيانية
    create_visualizations(df)
    print("\nPipeline complete. Charts saved in 'output/' directory.")

if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()
