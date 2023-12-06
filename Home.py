import streamlit as st
import pandas as pd

introduction = r'''The data warehouse and integration project described herein revolves around harnessing the Chinook dataset to extract meaningful business insights and facilitate analytical reporting. At its core, the initiative involves integrating the diverse data from the Chinook dataset into a unified data warehouse. This integration process ensures that data is organized, cleaned, and optimized for analysis.

The project unfolds through several key phases:
- :red[Business Case Analysis]: The initial focus is on understanding the Digital Media Store, encompassing data modeling, schema design, and defining business requirements and goals. The identification of key performance indicators (KPIs) sets the strategic direction for subsequent analyses.

- :red[Data Warehouse Integration]: Practical implementation takes shape as the Chinook dataset is integrated into the data warehouse. This step lays the groundwork for comprehensive data analysis and reporting.

- :red[OLAP Cube Creation]: Multidimensional analysis is facilitated through the creation of Online Analytical Processing (OLAP) cubes.

- :red[Chinook Report]: The heart of the project lies in this section, where a detailed analysis of the Chinook dataset unfolds, including sales performance, customer insights, product analysis, employee performance, marketing strategies, and listening habits. Leveraging multiple technologies, including MDX queries, T-SQL queries, and Power BI, to conduct a comprehensive analysis of the integrated Chinook dataset.

- :red[Interactive Data App]: To enhance user accessibility and interaction, a user-friendly Interactive Data App is introduced. Utilizing the Streamlit framework, the app offers an intuitive and responsive environment, allowing users to navigate through various analyses and reports effortlessly.'''

appreciation = r'''
We would like to express our sincere gratitude and appreciation to all those who have contributed to the completion of this Data warehouse and Integration subject. Your support, guidance, and assistance have been invaluable throughout this journey.

First and foremost, we would like to thank our supervisor, MSc. Lê Bá Thiền, for your unwavering support and invaluable guidance. Your expertise and insights have been instrumental in shaping the direction of this project and ensuring its success.

We are also deeply thankful to my colleagues and peers who provided valuable feedback, engaged in meaningful discussions, and offered their expertise whenever I needed it. Your input has enriched the quality of this work.

Last but not least, we want to express my heartfelt thanks to my family and friends for their continuous encouragement and understanding during this endeavour. Your unwavering support kept me motivated and determined to see this project through.

To everyone mentioned above and to anyone else who played a role, no matter how big or small, in the completion of this project, please accept my sincerest thanks.

Love,

:red[Group Gogi]
'''
mem_info = f'''

| No. | Full name             | Student ID   |
|----:|-----------------------|--------------|
| 1   | Nguyễn Đinh Minh Anh  | K214162141   |
| 2   | Phan Cao Bảo Trâm     | K214160996   |
| 3   | Huỳnh Thị Kim Ngân    | K214160992   |
| 4   | Lê Thị Bích Vân       | K214162159   |

'''
def main():
    st.set_page_config(layout="wide")
    st.title("Chinook")
    st.subheader("Gogi's Data Warehouse and Intergration Final project")
    st.caption('This Web App is a Demo of Gogi group for Data Warehouse and Integration Course. By using Streamlit framework and connect to database in our local server and deploy it to Streamlit Cloud for global use, an interactive data web app for Chinook Digital Media Store have been created.')
    intro, mem, appre = st.tabs(['About', 'Members', 'Appreciation'])
    with intro:
        st.markdown(introduction)
    with mem:
        st.markdown(mem_info)
    with appre:
        st.markdown(appreciation)
    st.divider()

if __name__ == "__main__":
    main()
