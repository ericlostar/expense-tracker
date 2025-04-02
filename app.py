import streamlit as st
import pandas as pd
import datetime

categories = {
    'Medical': ['doctor', 'hospital', 'medicine', 'pharmacy'],
    'Education': ['school', 'tuition', 'bookstore', 'university'],
    'Business': ['office', 'stationery', 'client', 'business'],
    'Charity': ['donation', 'charity'],
    'Transportation': ['gas', 'uber', 'taxi', 'bus'],
    'Personal': ['restaurant', 'movie', 'shopping', 'amazon']
}

def categorize_expense(description):
    description = description.lower()
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in description:
                return category
    return 'Other'

if 'expenses' not in st.session_state:
    st.session_state.expenses = pd.DataFrame(columns=['Date', 'Merchant', 'Description', 'Amount', 'Category', 'Entered By'])

st.title("💰 Daily Expense Tracker")

with st.form("manual_entry"):
    st.header("Add Expense Manually")
    date = st.date_input("Date", datetime.date.today())
    merchant = st.text_input("Merchant")
    description = st.text_input("Description")
    amount = st.number_input("Amount", min_value=0.01, step=0.01)
    entered_by = st.text_input("Entered By")
    submitted = st.form_submit_button("Add Expense")
    
    if submitted:
        new_expense = {
            'Date': date, 
            'Merchant': merchant,
            'Description': description,
            'Amount': amount,
            'Category': categorize_expense(description),
            'Entered By': entered_by
        }
        st.session_state.expenses = pd.concat([st.session_state.expenses, pd.DataFrame([new_expense])], ignore_index=True)
        st.success("Expense added successfully!")

st.header("Bulk Import from CSV")
uploaded_file = st.file_uploader("Choose a CSV file", type='csv')

if uploaded_file is not None:
    imported_df = pd.read_csv(uploaded_file)
    imported_df['Category'] = imported_df['Description'].apply(categorize_expense)
    entered_by_bulk = st.text_input("Entered By (Bulk Import)", "Bulk User")
    imported_df['Entered By'] = entered_by_bulk
    
    if st.button("Import Expenses"):
        st.session_state.expenses = pd.concat([st.session_state.expenses, imported_df], ignore_index=True)
        st.success("CSV data imported successfully!")

st.header("Expenses")
st.dataframe(st.session_state.expenses)

def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

csv = convert_df(st.session_state.expenses)

st.download_button(
    label="Download Expenses as CSV",
    data=csv,
    file_name=f'expenses_{datetime.datetime.now().strftime('%Y%m%d')}.csv',
    mime='text/csv',
)

