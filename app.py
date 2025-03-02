import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px

# ---------------------
# Cache the data load so it doesn't reload on every change
@st.cache_data
def load_data():
    # Replace with the raw URL to your CSV on GitHub
    url = "https://raw.githubusercontent.com/boonhowchew/malaysia-primary-care-research/main/REALQUAMI_Dataset_Merged.csv"
    df = pd.read_csv(url)
    # Ensure IDyear is numeric, drop missing years, and convert to int
    df = df.dropna(subset=['IDyear']).copy()
    df['IDyear'] = pd.to_numeric(df['IDyear'], errors='coerce').astype(int)
    return df

df = load_data()

# ---------------------
# Data Cleaning for CA Specialty
# ---------------------
df['Caspecialty'] = df['Caspecialty'].astype(str).str.strip()
df['Caspecialty'] = df['Caspecialty'].replace({
    'nan': 'Unknown', 'NaN': 'Unknown', '': 'Unknown', 'Not stated': 'Unknown'
})
df['Caspecialty'] = df['Caspecialty'].str.lower()
df['Caspecialty'] = df['Caspecialty'].replace({
    'family medicine': 'Family medicine',
    'eye': 'Eye',
    'unknown': 'Unknown'
})
# Compute category order (descending count) and move 'Unknown' to the end
counts = df['Caspecialty'].value_counts()
counts = counts[counts > 0]
cat_list = list(counts.index)
if 'Unknown' in cat_list:
    cat_list.remove('Unknown')
    cat_list.append('Unknown')

# ---------------------
# Data Cleaning for Journal Hierarchy (for Sunburst)
# ---------------------
hierarchy_cols = ['JournalLoc', 'JournalScop']
for col in hierarchy_cols:
    df[col] = df[col].fillna("Unknown")
    df[col] = df[col].replace(r'^\s*$', "Unknown", regex=True)
    df[col] = df[col].str.strip().str.title()

# Create shorter labels for display (adjust truncation length as needed)
df['JournalLoc_short'] = df['JournalLoc'].apply(lambda x: x if len(x) <= 15 else x[:10] + "...")
df['JournalScop_short'] = df['JournalScop'].apply(lambda x: x if len(x) <= 15 else x[:10] + "...")

# ---------------------
# 1. HISTOGRAM: Annual Publication Trend
# ---------------------
min_year = df['IDyear'].min()
max_year = df['IDyear'].max()

fig1, ax1 = plt.subplots(figsize=(6,4))
sns.histplot(
    data=df,
    x='IDyear',
    bins=range(min_year, max_year+1),
    kde=False,
    ax=ax1
)
ax1.set_title("Annual Publication Trend (Histogram)")
ax1.set_xlabel("Publication Year")
ax1.set_ylabel("Number of Publications")
plt.tight_layout()
st.pyplot(fig1)

# ---------------------
# 2. HORIZONTAL BAR CHART: CA Specialty
# ---------------------
fig2, ax2 = plt.subplots(figsize=(8,6))
sns.countplot(
    y='Caspecialty',
    data=df,
    order=cat_list,
    ax=ax2
)
for p in ax2.patches:
    width = p.get_width()
    if width > 0:
        ax2.annotate(
            f"{int(width)}",
            (width, p.get_y() + p.get_height()/2),
            ha='left', va='center'
        )
total_rows = len(df)
ax2.set_title(f"Histogram of CA Specialty [Total: {total_rows}]")
ax2.set_xlabel("Count of Studies")
ax2.set_ylabel("CA Specialty")
plt.tight_layout()
st.pyplot(fig2)

# ---------------------
# 3. LINE GRAPH: Total Counts by Publication Year
# ---------------------
df_line = df.groupby('IDyear')[['AuthorNum', 'InstitNum', 'AuthorOvNum', 'InstitOvNum']].sum().reset_index()

fig3, ax3 = plt.subplots(figsize=(8,5))
for col in ['AuthorNum', 'InstitNum', 'AuthorOvNum', 'InstitOvNum']:
    sns.lineplot(data=df_line, x='IDyear', y=col, marker='o', label=col, ax=ax3)
ax3.set_title("Total Counts of Authors, Institutions, Overseas Authors, and Overseas Institutions by Year")
ax3.set_xlabel("Publication Year")
ax3.set_ylabel("Total Count")
ax3.legend()
plt.tight_layout()
st.pyplot(fig3)

# ---------------------
# 4. SUNBURST CHART: Journal Locality and Scope
# ---------------------
fig4 = px.sunburst(
    df,
    path=['JournalLoc_short', 'JournalScop_short'],
    title="Multilayer Pie Chart: Journal Locality and Scope",
    custom_data=['JournalLoc', 'JournalScop']
)
fig4.update_traces(
    hovertemplate='<b>Journal Loc:</b> %{customdata[0]}<br><b>Journal Scope:</b> %{customdata[1]}<br>Count: %{value}<extra></extra>',
    textinfo="label+percent entry"
)
st.plotly_chart(fig4)

# ---------------------
# SAVE CHARTS & CLEANED DATASET TO THE SAME FOLDER
# ---------------------
folder_path = "/Users/mygoddess/Desktop/Research Integrity/REALQUAMI/Datasets/charts/malaysia-primary-care-research"

fig1.savefig(f"{folder_path}/Annual_Publication_Trend_Histogram.png", dpi=300, bbox_inches='tight')
fig2.savefig(f"{folder_path}/Caspecialty_Histogram.png", dpi=300, bbox_inches='tight')
fig3.savefig(f"{folder_path}/LineGraph_TotalCounts.png", dpi=300, bbox_inches='tight')
# For Plotly, if Kaleido is installed, you can save the sunburst chart as an image:
# fig4.write_image(f"{folder_path}/Journal_Sunburst.png", scale=2)

df.to_csv(f"{folder_path}/REALQUAMI_Dataset_Cleansed.csv", index=False)

# ---------------------
# DOWNLOAD BUTTONS
# ---------------------
st.markdown("## Download Files")
with open(f"{folder_path}/Annual_Publication_Trend_Histogram.png", "rb") as file_chart:
    st.download_button(
         label="Download Annual Publication Trend Histogram",
         data=file_chart,
         file_name="Annual_Publication_Trend_Histogram.png",
         mime="image/png"
    )

with open(f"{folder_path}/Caspecialty_Histogram.png", "rb") as file_chart:
    st.download_button(
         label="Download CA Specialty Histogram",
         data=file_chart,
         file_name="Caspecialty_Histogram.png",
         mime="image/png"
    )

with open(f"{folder_path}/LineGraph_TotalCounts.png", "rb") as file_chart:
    st.download_button(
         label="Download Line Graph Total Counts",
         data=file_chart,
         file_name="LineGraph_TotalCounts.png",
         mime="image/png"
    )

with open(f"{folder_path}/REALQUAMI_Dataset_Cleansed.csv", "rb") as file_csv:
    st.download_button(
         label="Download Cleaned Dataset CSV",
         data=file_csv,
         file_name="REALQUAMI_Dataset_Cleansed.csv",
         mime="text/csv"
    )
