import streamlit as st
import pandas as pd

introduction = r'''The data warehouse and integration project described herein revolves around harnessing the Chinook dataset to extract meaningful business insights and facilitate analytical reporting. At its core, the initiative involves integrating the diverse data from the Chinook dataset into a unified data warehouse. This integration process ensures that data is organized, cleaned, and optimized for analysis.

The project unfolds through several key phases:
- :red[Business Case Analysis]: The initial focus is on understanding the Digital Media Store, encompassing data modeling, schema design, and defining business requirements and goals. The identification of key performance indicators (KPIs) sets the strategic direction for subsequent analyses.

- :red[Data Warehouse Integration]: Practical implementation takes shape as the Chinook dataset is integrated into the data warehouse. This step lays the groundwork for comprehensive data analysis and reporting.

- :red[OLAP Cube Creation]: Multidimensional analysis is facilitated through the creation of Online Analytical Processing (OLAP) cubes.

- :red[Chinook Report]: The heart of the project lies in this section, where a detailed analysis of the Chinook dataset unfolds, including sales performance, customer insights, product analysis, employee performance, marketing strategies, and listening habits. Leveraging multiple technologies, including MDX queries, T-SQL queries, and Power BI, to conduct a comprehensive analysis of the integrated Chinook dataset.

- :red[Interactive Data App]: To enhance user accessibility and interaction, a user-friendly Interactive Data App is introduced. Utilizing the Streamlit framework, the app offers an intuitive and responsive environment, allowing users to navigate through various analyses and reports effortlessly.'''

appreciation = ''''''

def main():
    st.set_page_config(layout="wide")
    st.title("Chinook")
    st.subheader("Kichi's Data Warehouse and Intergration Final project")
    st.markdown(introduction)
    st.divider()
    st.markdown(appreciation)

if __name__ == "__main__":
    main()
