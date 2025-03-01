import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

@st.cache_data
def load_data():
    # Replace this with your raw CSV URL
    url = "https://raw.githubusercontent.com/your_username/malaysia-primary-care-research/main/REALQUAMI_Dataset_Merged.csv"
    df = pd.read_csv(url)
    df['IDyear'] = pd.to_numeric(df['IDyear'], errors='coerce')
    df['Period'] = df['IDyear'].apply(lambda x: 'Early (1962-1999)' if x < 2000 else 'Recent (2000-2019)')
    return df

def main():
    st.title("Malaysian Primary Care Research Dashboard")
    st.write("This dashboard updates automatically whenever the dataset on GitHub is updated.")

    # Load the data
    df = load_data()

    # 1. Synopsis (Background, Methods, Discussion, etc.)
    with st.expander("Project Synopsis"):
        st.markdown("""
        **Background**  
        The research landscape that encompass study designs, execution processes, and resulting outputs 
        can evolve in numerous ways, reflecting shifts in priorities, innovations, and the impact of external 
        influences on its enterprises. Much research waste has been increasingly reported...

        **Methods**  
        A search will be conducted in PubMed, Cochrane Library, CINAHL and PsycINFO to identify for published 
        clinical and biomedical research from 1962 to 2019 from Malaysia and/or Indonesia. Additional search 
        will also be conducted in MyMedR (Malaysian only)...

        **Discussion**  
        Results of this study will serve as the 'baseline' data for future evaluation and within the country 
        and between countries comparison...

        **Registration**  
        PROSPERO 2020, CRD42020152907: 
        [https://www.crd.york.ac.uk/prospero/display_record.php?ID=CRD42020152907](https://www.crd.york.ac.uk/prospero/display_record.php?ID=CRD42020152907)  
        Open Science Framework’s registry: [https://osf.io/w85ce](https://osf.io/w85ce)

        **Keywords**: Systematic Review; Clinical Research; Biomedical Research; Research Characteristics; 
        Research Quality; Malaysia; Indonesia
        """)

    # 2. Team Members and Contact Info
    with st.expander("Project Team Members"):
        st.markdown("""
        **Project Lead**  
        - Boon-How Chew, Department of Family Medicine, Faculty of Medicine & Health Sciences, UPM  
          Tel: +603-89472520, email: [chewboonhow@upm.edu.my](mailto:chewboonhow@upm.edu.my)

        **Team Members**  
        - Shaun Wen Huey Lee; [shaun.lee@monash.edu](mailto:shaun.lee@monash.edu)  
          School of Pharmacy, Monash University Malaysia, Selangor, Malaysia

        - Lim Poh Ying; [pohying_my@upm.edu.my](mailto:pohying_my@upm.edu.my)  
          Department of Community Health, UPM

        - Soo Huat Teoh; [soohuat@usm.my](mailto:soohuat@usm.my)  
          Advanced Medical and Dental Institute, USM

        - (continue listing the rest as needed)
        """)

    st.subheader("Dataset Overview")
    st.write(f"Total Publications: {len(df)}")
    st.dataframe(df.head(10))

    # Example chart or other existing code can remain here...
    st.markdown("### Annual Publication Trend")
    pub_trend = df.groupby('IDyear').size().reset_index(name='Count')
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=pub_trend, x='IDyear', y='Count', marker='o', ax=ax)
    ax.set_title("Annual Publication Trend")
    ax.set_xlabel("Publication Year")
    ax.set_ylabel("Number of Studies")
    st.pyplot(fig)

if __name__ == "__main__":
    main()