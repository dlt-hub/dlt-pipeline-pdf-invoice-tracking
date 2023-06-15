import streamlit as st
import pandas as pd
import duckdb

conn = duckdb.connect('invoice_tracking.duckdb')

def load_data():
    query = 'SELECT * FROM invoice_tracking_data.invoice_tracking_resources'
    df = conn.execute(query).fetch_df()
    df = df.drop_duplicates(subset='invoice_number')
    df['invoice_amount'] = df['invoice_amount'].str.replace(',', '').astype(float)
    df['invoice_date'] = pd.to_datetime(df['invoice_date'])
    return df

@st.cache_data
def process_data(df):
    df['invoice_date'] = pd.to_datetime(df['invoice_date']).dt.strftime('%Y-%m')
    df_monthly = df.groupby(df.invoice_date).invoice_amount.sum().reset_index()
    df_monthly.columns = ['Month', 'Total Invoice Amount']
    df_customer = df.groupby('recipient_company_name').invoice_amount.sum().reset_index()
    df_customer.columns = ['Customer', 'Total Invoice Amount']

    return df, df_monthly, df_customer

def main():
    st.title("Invoice Tracking")

    df = load_data()
    df, df_monthly, df_customer = process_data(df)

    st.header("Total Invoice Amount Per Month")
    st.write(df_monthly)

    st.header("Total Invoice Amount Per Customer")
    st.write(df_customer)

    st.header("All Invoices")
    st.write(df)

if __name__ == '__main__':
    main()
