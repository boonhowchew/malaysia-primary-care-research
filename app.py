import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

@st.cache_data
def load_data():
    # Replace the URL below with the raw URL of your CSV file on GitHub
    url = "https://raw.githubusercontent.com/boonhowchew/malaysia-primary-care-research/main/REALQUAMI_Dataset_Merged.csv"
    df = pd.read_csv(url)
    # Ensure IDyear is numeric and create a Period column
    df['IDyear'] = pd.to_numeric(df['IDyear'], errors='coerce')
    df['Period'] = df['IDyear'].apply(lambda x: 'Early (1962-1999)' if x < 2000 else 'Recent (2000-2019)')
    return df

df = load_data()

st.title("Malaysian Primary Care Research Dashboard")
st.write("This dashboard updates automatically whenever the dataset on GitHub is updated.")

st.subheader("Dataset Overview")
st.write(f"Total Publications: {len(df)}")
st.dataframe(df.head(10))

# Example Chart: Annual Publication Trend
pub_trend = df.groupby('IDyear').size().reset_index(name='Count')
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=pub_trend, x='IDyear', y='Count', marker='o', ax=ax)
ax.set_title("Annual Publication Trend")
ax.set_xlabel("Publication Year")
ax.set_ylabel("Number of Studies")
st.pyplot(fig)

st.write("More interactive charts and summaries can be added here...")