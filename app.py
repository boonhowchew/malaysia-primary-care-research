import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

@st.cache_data
def load_data():
    # Replace with your actual raw CSV URL
    url = "https://raw.githubusercontent.com/boonhowchew/malaysia-primary-care-research/main/REALQUAMI_Dataset_Merged.csv"
    df = pd.read_csv(url)
    df['IDyear'] = pd.to_numeric(df['IDyear'], errors='coerce')
    df['Period'] = df['IDyear'].apply(lambda x: 'Early (1962-1999)' if x < 2000 else 'Recent (2000-2019)')
    return df

def main():
    st.title("Malaysian Primary Care Research Dashboard")
    st.write("This dashboard updates automatically whenever the dataset on GitHub is updated.")

    # Load your dataset
    df = load_data()

    # ---------------------
    # 1. Project Synopsis (Background, Methods, Discussion, Registration)
    # ---------------------
    with st.expander("Project Synopsis"):
        st.markdown("""
        **Background**  
        The research landscape that encompass study designs, execution processes, and resulting outputs can evolve 
        in numerous ways, reflecting shifts in priorities, innovations, and the impact of external influences on its 
        enterprises. Much research waste has been increasingly reported. Poorly conducted clinical and biomedical 
        researches are detrimental to the health of the people and healthcare performance with misleading clinical 
        evidence. Efforts to improve research performance will need good data on the profiles and performance of past 
        research. This systematic review aims to describe the characteristics and examine the quality of 
        clinical and biomedical research in Malaysia and Indonesia (other country could participate in the same manner).

        **Methods**  
        A search will be conducted in PubMed, Cochrane Library, CINAHL and PsycINFO to identify for published clinical 
        and biomedical research from 1962 to 2019 from Malaysia and/or Indonesia. Additional search will also be 
        conducted in MyMedR (Malaysian only). Studies that were identified from the databases will be independently 
        screened by a team of reviewers, relevant information will be extracted and the quality of articles will be 
        assessed. In Phase 1, the characteristics of the research including the profiles of the researchers and the 
        journals in which they are published will be reported descriptively. In Phase 2, a research quality screening 
        tool will be validated to assess the research quality based on three domains of relevance, the credibility of 
        the methods and usefulness of the results. Associations between the research characteristics and quality will 
        be analysed. The independent effect of each of the determinant will be quantified in multivariable regression 
        analysis. Longitudinal trends of the research characteristics, health conditions studied and settings, among 
        others will be explored.

        **Results**
        Of 4513 articles, 1078 were included in this qualitative synthesis (https://rb.gy/zjwr8d). Dataset that is made
        available here was the results from the Malaysian primary care setting, the search strategy is available here (https://rb.gy/jd91ey).
        Malaysian colleagues and those whose studies and papers have been included or not included in the dataset are welcomed to check out
        the dataset, to clean the entries and to add to it if the papers are deem eligible based on criteria and search strategy.
        Other research-related outputs at primary care setting will be added in near future once this plarform works well.

        **Discussion**  
        Results of this study will serve as the 'baseline' data for future evaluation and within the country and between 
        countries comparison. This review may also provide informative results to a diverse range of stakeholders 
        including researchers, academics, funding agencies, academic institutions, policymakers, industry partners, 
        the public, publishers, research administrators, educators, students, and technology developers by offering 
        insights into the evolution of research conduct and performance from the past to the present. The longitudinal 
        and prospective trends of the research characteristics and quality could provide suggestions on improvement 
        initiatives. Additionally, information on health conditions, research settings, and whether they are over- or 
        under-studied may help future prioritization of research initiatives and resources.

        **Registration**  
        PROSPERO 2020, CRD42020152907, available from: 
        [https://www.crd.york.ac.uk/prospero/display_record.php?ID=CRD42020152907](https://www.crd.york.ac.uk/prospero/display_record.php?ID=CRD42020152907),  
        and Open Science Framework’s registry for Research on the Responsible Conduct of Research, 
        available from: [https://osf.io/w85ce](https://osf.io/w85ce).

        **Keywords**: Systematic Review; Clinical Research; Biomedical Research; Research Characteristics; 
        Research Quality; Malaysia; Indonesia
        """)

    # ---------------------
    # 2. Project Team Members
    # ---------------------
    with st.expander("Project Team Members"):
        st.markdown("""
        **Project Lead**  
        Boon-How Chew, Department of Family Medicine, Faculty of Medicine & Health Sciences, Universiti Putra Malaysia, 
        43400 Serdang, Selangor, Malaysia.  
        Tel: +603-89472520, Fax: +603-89472328, email: [chewboonhow@upm.edu.my](mailto:chewboonhow@upm.edu.my)

        **Team Members**  
        - Shaun Wen Huey Lee; [shaun.lee@monash.edu](mailto:shaun.lee@monash.edu)  
          School of Pharmacy, Monash University Malaysia, Jalan Lagoon Selatan, 47500 Bandar Sunway, Selangor, Malaysia

        - Lim Poh Ying; [pohying_my@upm.edu.my](mailto:pohying_my@upm.edu.my)  
          Department of Community Health, Faculty of Medicine and Health Science, Universiti Putra Malaysia, Malaysia

        - Soo Huat Teoh; [soohuat@usm.my](mailto:soohuat@usm.my)  
          Advanced Medical and Dental Institute (AMDI), Universiti Sains Malaysia, Bertam, Kepala Batas, Penang, Malaysia

        - Aneesa Abdul Rashid; [aneesa@upm.edu.my](mailto:aneesa@upm.edu.my)  
          Department of Family Medicine, Faculty of Medicine and Health Science, Universiti Putra Malaysia, Malaysia

        - Navin Kumar Devaraj; [knavin@upm.edu.my](mailto:knavin@upm.edu.my)  
          Department of Family Medicine, Faculty of Medicine and Health Science, Universiti Putra Malaysia, Malaysia

        - Adibah Hanim Ismail @ Daud; [adibahanim@upm.edu.my](mailto:adibahanim@upm.edu.my)  
          Department of Family Medicine, Faculty of Medicine and Health Science, Universiti Putra Malaysia, Malaysia

        - Abdul Hadi Abdul Manap; [abhadi@upm.edu.my](mailto:abhadi@upm.edu.my)  
          Department of Family Medicine, Faculty of Medicine and Health Science, Universiti Putra Malaysia, Malaysia

        - Fadzilah Mohamad; [ilafadzilah@upm.edu.my](mailto:ilafadzilah@upm.edu.my)  
          Department of Family Medicine, Faculty of Medicine and Health Science, Universiti Putra Malaysia, Malaysia

        - Aaron Fernandez; [aaron@upm.edu.my](mailto:aaron@upm.edu.my)  
          Department of Psychiatry, Faculty of Medicine and Health Science, Universiti Putra Malaysia, Malaysia

        - Hanifatiyah Ali; [fatiyah@upm.edu.my](mailto:fatiyah@upm.edu.my)  
          Department of Family Medicine, Faculty of Medicine and Health Science, Universiti Putra Malaysia, Malaysia

        - Puteri Shanaz Jahn Kassim; [shanaz@upm.edu.my](mailto:shanaz@upm.edu.my)  
          Department of Family Medicine, Faculty of Medicine and Health Science, Universiti Putra Malaysia, Malaysia

        - Nurainul Hana Shamsuddin; [nurainul@upm.edu.my](mailto:nurainul@upm.edu.my)  
          Department of Family Medicine, Faculty of Medicine and Health Science, Universiti Putra Malaysia, Malaysia

        - Noraina Muhamad Zakuan; [noraina@upm.edu.my](mailto:noraina@upm.edu.my)  
          Department of Biomedical Sciences, Faculty of Medicine and Health Science, Universiti Putra Malaysia, Malaysia

        - Akiza Roswati Abdullah; [akiza@upm.edu.my](mailto:akiza@upm.edu.my)  
          Medical and Health Sciences Library, Faculty of Medicine and Health Science, Universiti Putra Malaysia, Malaysia

        - Indah S. Widyahening; [indah_widyahening@ui.ac.id](mailto:indah_widyahening@ui.ac.id)  
          Department of Community Medicine, Faculty of Medicine, Universitas Indonesia, Jakarta, Indonesia
        """)

    # ---------------------
    # Example: Simple Dataset Overview
    # ---------------------
    st.subheader("Dataset Overview")
    st.write(f"Total Publications: {len(df)}")
    st.dataframe(df.head(10))

    # (Optional) Example Chart
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
