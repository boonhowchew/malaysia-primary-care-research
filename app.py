import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px
import base64
import os

# Must be the first Streamlit command:
st.set_page_config(layout="wide")

# -----------------------------------------------------------------------------
# Helper Function: Store Visitor Registration Data
# -----------------------------------------------------------------------------
def store_visitor_data(data):
    """
    Append visitor data (dictionary) to a CSV file stored in the repository folder.
    """
    csv_file = "visitor_data.csv"  # This file is saved in the same folder as app.py
    if os.path.exists(csv_file):
        df_existing = pd.read_csv(csv_file)
        df_existing = df_existing.append(data, ignore_index=True)
        df_existing.to_csv(csv_file, index=False)
    else:
        df_new = pd.DataFrame([data])
        df_new.to_csv(csv_file, index=False)

# -----------------------------------------------------------------------------
# Load Data (cached)
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    # Use the raw URL to your CSV on GitHub.
    url = "https://raw.githubusercontent.com/boonhowchew/malaysia-primary-care-research/main/REALQUAMI_Dataset_Merged.csv"
    # Using on_bad_lines='skip' and the Python engine for more robust parsing.
    df = pd.read_csv(url, on_bad_lines='skip', engine='python', encoding='utf-8')
    # Ensure IDyear is numeric, drop rows with missing IDyear, and convert to int.
    df = df.dropna(subset=['IDyear']).copy()
    df['IDyear'] = pd.to_numeric(df['IDyear'], errors='coerce').astype(int)
    return df

df = load_data()

# -----------------------------------------------------------------------------
# Visitor Analytics: Update and Display Counts
# -----------------------------------------------------------------------------
counter_file = "visitor_count.txt"
try:
    with open(counter_file, "r") as f:
        total_visitors = int(f.read().strip())
except:
    total_visitors = 0
total_visitors += 1
with open(counter_file, "w") as f:
    f.write(str(total_visitors))

if os.path.exists("visitor_data.csv"):
    registered_visitors = pd.read_csv("visitor_data.csv").shape[0]
else:
    registered_visitors = 0

# -----------------------------------------------------------------------------
# Sidebar: Registration Form & Analytics
# -----------------------------------------------------------------------------
if "registered" not in st.session_state:
    st.session_state["registered"] = False

st.sidebar.header("Visitor Registration")

if not st.session_state["registered"]:
    with st.sidebar.form("registration_form"):
        first_name = st.text_input("First Name *")
        last_name = st.text_input("Last Name *")
        email = st.text_input("Email Address *")
        affiliation = st.text_input("Affiliation / Organization")
        purpose = st.selectbox(
            "Purpose of Downloading the Dataset",
            ["Contributing to the dataset", "Research", "Academic Coursework", "Personal Interest", "Other"]
        )
        consent = st.checkbox("I agree to the terms of use and consent to provide my personal data.")
        submitted = st.form_submit_button("Submit Registration")
    if submitted:
        if not (first_name and last_name and email and consent):
            st.sidebar.error("Please fill in first name, last name, email and agree to the terms.")
        else:
            new_row = {
                "First Name": first_name,
                "Last Name": last_name,
                "Email": email,
                "Affiliation": affiliation,
                "Purpose": purpose
            }
            store_visitor_data(new_row)
            st.session_state["registered"] = True
            st.sidebar.success("Registration successful! Reloading page...")
            st.experimental_rerun()
else:
    st.sidebar.subheader("Visitor Analytics")
    st.sidebar.write("Total Visitors: ", total_visitors)
    st.sidebar.write("Registered Visitors: ", registered_visitors)

# -----------------------------------------------------------------------------
# Main Page Content
# -----------------------------------------------------------------------------
st.title("Malaysian Primary Care Research Dashboard, 1962 to 2019")
st.write("This dashboard updates automatically whenever the dataset on GitHub is updated.")

with st.expander("Project Synopsis"):
    st.markdown("""
        **Background**  
        The research landscape that encompasses study designs, execution processes, and resulting outputs can evolve 
        in numerous ways, reflecting shifts in priorities, innovations, and the impact of external influences on its enterprises.  
        Much research waste has been increasingly reported. Poorly conducted clinical and biomedical research is detrimental to health  
        outcomes due to misleading evidence. This systematic review aims to describe the characteristics and examine the quality of  
        clinical and biomedical research in Malaysia and Indonesia.
        
        **Methods**  
        A search was conducted in PubMed, Cochrane Library, CINAHL, and PsycINFO to identify published clinical and biomedical research  
        from 1962 to 2019 from Malaysia. An additional search is conducted in MyMedR. Identified studies are screened by a team of reviewers,  
        relevant data extracted, and quality assessed. Phase 1 reports descriptive characteristics; Phase 2 validates a research quality tool.
        
        **Results**  
        Of 4513 articles, 1078 were included in this qualitative synthesis (see flow diagram). The dataset reflects research from the  
        Malaysian primary care setting; the search strategy is available [here](https://rb.gy/jd91ey). Researchers are invited to review  
        and refine the dataset.
        
        **Discussion**  
        The results serve as baseline data for future evaluations and comparisons. They provide insights for stakeholders, helping to  
        prioritize future research initiatives.
        
        **Registration**  
        PROSPERO 2020, CRD42020152907, available from:  
        [https://www.crd.york.ac.uk/prospero/display_record.php?ID=CRD42020152907](https://www.crd.york.ac.uk/prospero/display_record.php?ID=CRD42020152907)  
        and Open Science Framework: [https://osf.io/w85ce](https://osf.io/w85ce)
        
        **Keywords**: Systematic Review; Clinical Research; Biomedical Research; Research Characteristics; Research Quality; Malaysia; Indonesia
        """)

with st.expander("Project Team Members"):
    st.markdown("""
        **Project Lead**  
        Boon-How Chew, Department of Family Medicine, Faculty of Medicine & Health Sciences, Universiti Putra Malaysia,  
        43400 Serdang, Selangor, Malaysia.  
        Tel: +603-89472520, Fax: +603-89472328, email: [chewboonhow@upm.edu.my](mailto:chewboonhow@upm.edu.my)
        
        **Team Members**  
        - Shaun Wen Huey Lee; [shaun.lee@monash.edu](mailto:shaun.lee@monash.edu) – School of Pharmacy, Monash University Malaysia  
        - Lim Poh Ying; [pohying_my@upm.edu.my](mailto:pohying_my@upm.edu.my) – Department of Community Health, Universiti Putra Malaysia  
        - Soo Huat Teoh; [soohuat@usm.my](mailto:soohuat@usm.my) – Advanced Medical and Dental Institute, Universiti Sains Malaysia  
        - Aneesa Abdul Rashid; [aneesa@upm.edu.my](mailto:aneesa@upm.edu.my) – Department of Family Medicine, Universiti Putra Malaysia  
        - Navin Kumar Devaraj; [knavin@upm.edu.my](mailto:knavin@upm.edu.my) – Department of Family Medicine, Universiti Putra Malaysia  
        - Adibah Hanim Ismail @ Daud; [adibahanim@upm.edu.my](mailto:adibahanim@upm.edu.my) – Department of Family Medicine, Universiti Putra Malaysia  
        - Abdul Hadi Abdul Manap; [abhadi@upm.edu.my](mailto:abhadi@upm.edu.my) – Department of Family Medicine, Universiti Putra Malaysia  
        - Fadzilah Mohamad; [ilafadzilah@upm.edu.my](mailto:ilafadzilah@upm.edu.my) – Department of Family Medicine, Universiti Putra Malaysia  
        - Aaron Fernandez; [aaron@upm.edu.my](mailto:aaron@upm.edu.my) – Department of Psychiatry, Universiti Putra Malaysia  
        - Hanifatiyah Ali; [fatiyah@upm.edu.my](mailto:fatiyah@upm.edu.my) – Department of Family Medicine, Universiti Putra Malaysia  
        - Puteri Shanaz Jahn Kassim; [shanaz@upm.edu.my](mailto:shanaz@upm.edu.my) – Department of Family Medicine, Universiti Putra Malaysia  
        - Nurainul Hana Shamsuddin; [nurainul@upm.edu.my](mailto:nurainul@upm.edu.my) – Department of Family Medicine, Universiti Putra Malaysia  
        - Noraina Muhamad Zakuan; [noraina@upm.edu.my](mailto:noraina@upm.edu.my) – Department of Biomedical Sciences, Universiti Putra Malaysia  
        - Akiza Roswati Abdullah; [akiza@upm.edu.my](mailto:akiza@upm.edu.my) – Medical and Health Sciences Library, Universiti Putra Malaysia  
        - Indah S. Widyahening; [indah_widyahening@ui.ac.id](mailto:indah_widyahening@ui.ac.id) – Department of Community Medicine, Universitas Indonesia
        """)

st.markdown("### Flow Chart")
st.image("Flow.png", caption="PRISMA Flow Chart", use_container_width=True)

st.subheader("Dataset Overview")
st.write(f"Total Publications: {len(df)}")
st.dataframe(df.head(10))

if st.session_state["registered"]:
    invitation_markdown = """
    **Invitation to Contribute**  
    We invite you to explore and refine the dataset for improved accuracy and completeness.
    
    - **CSV Dataset (view-only)**: [Link Here](https://drive.google.com/file/d/1LS__cmX58gZnZ4uiaYZ4nIslN6HhthuM/view?usp=share_link)
    - **Excel Google Sheet Dataset (editable)**: [Link Here](https://docs.google.com/spreadsheets/d/1XMSbSG-GEi67Pt6HMaDLUE_LjYNvfuoXxIPW_HjZPrc/edit?usp=share_link)
    - **Metadata Explanation**: [Link Here](https://drive.google.com/file/d/1aPG4fBL0T0YdNIxMUpKhpB7J2rbK81d0/view?usp=share_link)
    """
else:
    invitation_markdown = """
    **Invitation to Contribute**  
    We invite you to explore and refine the dataset for improved accuracy and completeness.  
    <span title="Please register to enable dataset download and access to external datasets." style="color:gray;cursor:not-allowed;">
    - **CSV Dataset (view-only)**: Link Here  
    - **Excel Google Sheet Dataset (editable)**: Link Here  
    - **Metadata Explanation**: Link Here  
    </span>
    """
st.markdown(invitation_markdown, unsafe_allow_html=True)

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
counts = df['Caspecialty'].value_counts()
counts = counts[counts > 0]
cat_list = list(counts.index)
if 'Unknown' in cat_list:
    cat_list.remove('Unknown')
    cat_list.append('Unknown')

hierarchy_cols = ['JournalLoc', 'JournalScop']
for col in hierarchy_cols:
    df[col] = df[col].fillna("Unknown")
    df[col] = df[col].replace(r'^\s*$', "Unknown", regex=True)
    df[col] = df[col].str.strip().str.title()

df['JournalLoc_short'] = df['JournalLoc'].apply(lambda x: x if len(x) <= 15 else x[:10] + "...")
df['JournalScop_short'] = df['JournalScop'].apply(lambda x: x if len(x) <= 15 else x[:10] + "...")

min_year = df['IDyear'].min()
max_year = df['IDyear'].max()
fig1, ax1 = plt.subplots(figsize=(6,4))
sns.histplot(data=df, x='IDyear', bins=range(min_year, max_year+1), kde=False, ax=ax1)
ax1.set_title("Annual Publication Trend (Histogram)")
ax1.set_xlabel("Publication Year")
ax1.set_ylabel("Number of Publications")
plt.tight_layout()
st.pyplot(fig1)

fig2, ax2 = plt.subplots(figsize=(8,6))
sns.countplot(y='Caspecialty', data=df, order=cat_list, ax=ax2)
for p in ax2.patches:
    width = p.get_width()
    if width > 0:
        ax2.annotate(f"{int(width)}", (width, p.get_y() + p.get_height()/2), ha='left', va='center')
total_rows = len(df)
ax2.set_title(f"Histogram of CA Specialty [Total: {total_rows}]")
ax2.set_xlabel("Count of Studies")
ax2.set_ylabel("CA Specialty")
plt.tight_layout()
st.pyplot(fig2)

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

st.markdown("### Additional Overview of Research Characteristics")
st.image(
    "Six_Histograms_Combined.png",
    caption="Six Histograms of Article Type, Field of Study, Study Design, Level of Study, Quant Study Type, and Data Collection Methods",
    use_container_width=True
)

folder_path = "charts"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

fig1.savefig(f"{folder_path}/Annual_Publication_Trend_Histogram.png", dpi=300, bbox_inches='tight')
fig2.savefig(f"{folder_path}/Caspecialty_Histogram.png", dpi=300, bbox_inches='tight')
fig3.savefig(f"{folder_path}/LineGraph_TotalCounts.png", dpi=300, bbox_inches='tight')
# If Kaleido is installed, you can also save the Plotly chart:
# fig4.write_image(f"{folder_path}/Journal_Locality_and_Scope_SunburstChart.png", scale=2)

df.to_csv(f"{folder_path}/REALQUAMI_Dataset_Cleansed.csv", index=False)

if st.session_state["registered"]:
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
