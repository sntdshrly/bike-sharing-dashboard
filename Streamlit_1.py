# =============================================================================
# HOW TO INSTALL STREAMLIT
# >> pip install streamlit
# >> streamlit hello
#
# HOW TO RUN
# >> streamlit run "C:\Users\SHERLY SANTIADI\PycharmProjects\Streamlit 1\Streamlit_1.py"
# =============================================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def background():
    st.set_page_config(layout="wide", page_title="Bike Sharing Dashboard", page_icon=":bike:",
                       initial_sidebar_state="expanded")
    st.write(
        """
        # Bike Sharing Dashboard :sparkles:
        """
    )
    with st.sidebar:
        st.image("images/logo.png")
    return

def read_data(csv):
    df = pd.read_csv(csv)
    return df

def jumlah_order_harian(df):
    # Fungsi grouping
    daily_orders_df = df.groupby('dteday').agg({
        'cnt': 'sum'
    }).reset_index()
    daily_orders_df['dteday'] = pd.to_datetime(daily_orders_df['dteday'])

    # Visualisasi
    st.subheader('Jumlah Rental Harian')
    min_date = pd.to_datetime(df['dteday'].min())
    max_date = pd.to_datetime(df['dteday'].max())
    start_date, end_date = st.date_input(
        label='Date Range',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    filtered_df = df[
        (df['dteday'] >= start_date.strftime('%Y-%m-%d')) & (df['dteday'] <= end_date.strftime('%Y-%m-%d'))
        ]
    total_orders = filtered_df['cnt'].sum()
    st.metric('Total Orders', value=total_orders)
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.hist(daily_orders_df['cnt'], bins=10, color='#90CAF9')
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=15)
    st.pyplot(fig)
    return

def jumlah_order_holiday(df):
    # Fungsi grouping
    holiday_orders_df = df.groupby('holiday').agg({
        'cnt': 'sum'
    }).reset_index()
    holiday_orders_df['holiday'] = holiday_orders_df['holiday'].map({
        0: 'Holiday',
        1: 'Work day'
    })

    # Visualisasi
    st.subheader('Jumlah Rental Holiday vs. Workday')
    df['category'] = df['holiday'].apply(lambda x: 'Holiday' if x else 'Workday')
    fig, ax = plt.subplots(figsize=(16, 8))
    colors = {'Holiday': '#90CAF9', 'Workday': '#FFA726'}
    for category, color in colors.items():
        data = df[df['category'] == category]
        ax.scatter(data.index, data['cnt'], color=color, label=category, alpha=0.6)
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=15)
    ax.legend()
    st.pyplot(fig)
    return

def main():
    background()
    day_df = read_data('data/day.csv')
    jumlah_order_harian(day_df)
    jumlah_order_holiday(day_df)

if __name__ == '__main__':
    main()