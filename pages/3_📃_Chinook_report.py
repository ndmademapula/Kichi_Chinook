import streamlit as st
import pandas as pd
import plotly.express as px
from constant import *
# import warnings
# warnings.filterwarnings('ignore')

from ultils import *
import Query

# Initialize connection.
# Uses st.cache_resource to only run once.
st.set_page_config(layout="wide")
st.title("Chinook OLAP reports")

br_options = [
    'Track sales per day, month, quarter, year?',
    'Which album has the most listeners?',
    'Which customers regularly buy music?',
    'Which customer spends the most money for buying album?',
    'Which employee helps achieve invoices the most?',
    'Which employee has the highest sales revenue?',
    'Which music genre is purchased the most by year?',
    'How much gerne music in playlist?',
    'How long does it take for customers to return to buy track?',
    'How much genre in playlist?',
]
slt_br = st.selectbox('Business Requirements', options=br_options, index=None, placeholder="Select business requirment...")

if slt_br == br_options[0]:
    #! st.write('Track sales per day, month, quarter, year?')
    day, month, quarter, year = st.tabs(['Day','Month','Quarter','Year'])
    with day:
        merged_df = pd.merge(df_FactSales, df_DimDate, left_on='InvoiceDateID', right_on='DateID')
        query = Query.query_1_day
        req_1 = Query.req_1_day
        selected_year = st.multiselect(
        label='Select Year', 
        options=list(req_1['Year'].astype(int).value_counts().index.to_list()), 
        default=list(req_1['Year'].astype(int).value_counts().index.to_list())
        )
        if selected_year:
            for i in sorted(selected_year):
                test = create_barchart(req_1[req_1['Year']==i], x='FullDate', y='Total Sales', color='Total Sales'
                                    , title=f'Daily Total Sales in {i}')
                test.update_layout(bargap=0)
                st.plotly_chart(test, use_container_width=True)
            st.balloons()
        col1, col2 = st.columns(2)
        with col1:
            st.code(query, language='sql')
        with col2:   
            st.dataframe(req_1)

    with month:
        query = Query.query_1_month
        req_1 = Query.req_1_month
        fig_1 = create_barchart(req_1, x='MonthName', y='Total Sales', color='Year'
                                , title='Monthly Total Sales Over Years')
        fig_2 = create_linechart(req_1, x='MonthName', y='Total Sales', color='Year'
                                , title='Monthly Total Sales Over Years')
        st.plotly_chart(fig_1)  
        with st.expander('See explanation'):
            st.write('Ở đây sẽ viết giải thích, nhưng mà chưa viết ○( ＾皿＾)っ Hehehe…')
        st.plotly_chart(fig_2)
        with st.expander('See explanation'):
            st.write('Ở đây sẽ viết giải thích, nhưng mà chưa viết ○( ＾皿＾)っ Hehehe…')

        col1, col2 = st.columns(2)
        with col1:
            st.code(query, language='sql')
        with col2:   
            st.dataframe(req_1)
    with quarter:
        query = Query.query_1_quarter
        req_1 = Query.req_1_quarter
        fig_1 = create_barchart(req_1, x='Quarter', y='Total Sales', color='Year'
                                , title='Quarterly Total Sales Over Years')
        fig_2 = create_linechart(req_1, x='Quarter', y='Total Sales', color='Year'
                                , title='Quarterly Total Sales Over Years')
        st.plotly_chart(fig_1)
        with st.expander('See explanation'):
            st.write('Ở đây sẽ viết giải thích, nhưng mà chưa viết ○( ＾皿＾)っ Hehehe…')
        st.plotly_chart(fig_2)
        with st.expander('See explanation'):
            st.write('Ở đây sẽ viết giải thích, nhưng mà chưa viết ○( ＾皿＾)っ Hehehe…')
        col1, col2 = st.columns(2)
        with col1:
            st.code(query, language='sql')
        with col2:   
            st.dataframe(req_1)
    with year:
        query = Query.query_1_year
        req_1 = Query.req_1_year
        fig_1 = create_barchart(req_1, x='Year', y='Total Sales', color='Total Sales'
                                , title='Total Sales Over Years')
        st.plotly_chart(fig_1)
        with st.expander('See explanation'):
            st.write('Ở đây sẽ viết giải thích, nhưng mà chưa viết ○( ＾皿＾)っ Hehehe…')

        fig_2 = create_bubblechart(req_1,x='Year', y='Total Sales', size='Total Sales', title='Total Sales Over Years', hover_name='Year', color='Total Sales')
        st.plotly_chart(fig_2)
        with st.expander('See explanation'):
            st.write('Ở đây sẽ viết giải thích, nhưng mà chưa viết ○( ＾皿＾)っ Hehehe…')
 
        col1, col2 = st.columns(2)
        with col1:
            st.code(query, language='sql')
        with col2:   
            st.dataframe(req_1)

if slt_br == br_options[1]:
    #! st.write('Which album has the most listeners?')
    top_k = st.slider(':green_heart: Indicate the number of albums you wish to return', 
                      min_value=1, max_value=347, value=20)
    query = Query.query_2%top_k
    req_2 = Query.req_2.head(top_k)
    fig_1 = create_barchart(req_2,x='AlbumTitle', y='Views',title='Albums have the most listeners', color='Views')
    st.plotly_chart(fig_1, use_container_width=True)
    with st.expander('See explanation'):
            st.write('Ở đây sẽ viết giải thích, nhưng mà chưa viết ○( ＾皿＾)っ Hehehe…')

    query_plt = Query.query_2_1%top_k
    req_plt = Query.req_2_1.head(top_k)
    fig_2 = create_bubblechart(req_plt,x='Song Duration', y='Views', size='No of Track', title='Albums have the most listeners, its size by number of tracks in the album', color='Views',hover_name='AlbumTitle')
    fig_2.update_traces(mode='markers', marker=dict(sizemode='area', line_width=2))
    st.plotly_chart(fig_2, use_container_width=True)
    with st.expander('See explanation'):
            st.write('Ở đây sẽ viết giải thích, nhưng mà chưa viết ○( ＾皿＾)っ Hehehe…')
    col1, col2 = st.columns(2)
    with col1:
        st.code(query, language='sql')
    with col2:
        st.dataframe(req_2)

if slt_br == br_options[2]:
    st.warning('(ˉ▽￣～) This requirement solution is still in rechecking...')
    #! st.write('Which customers regularly buy music?')
    year, monthyear = st.tabs(['Year','Month by Year'])
    with year:
        top_k = st.slider(':eyes: Identify the number of customers who regularly buy music', 
                      min_value=1, max_value=59, value=5)
        query = Query.query_3_year%top_k
        req_3_year = Query.req_3_year.head(top_k)
        fig_1 = create_barchart(req_3_year, x='CustomerName', y='Year', title="Customers' regular purchasing frequency over the years", color='Year')
        fig_1.update_layout(
            yaxis_title='Number of Buying by Year'
        )
        st.plotly_chart(fig_1,use_container_width=True)
        with st.expander('See explanation'):
            st.write('Ở đây sẽ viết giải thích, nhưng mà chưa viết ○( ＾皿＾)っ Hehehe…')
        col1, col2 = st.columns(2)
        with col1:
            st.code(query, language='sql')
        with col2:
            st.dataframe(req_3_year)
    with monthyear:
        query = Query.query_3_monthyear
        req_3_monthyear = Query.req_3_monthyear

        fig_2 = create_barchart(req_3_monthyear, x='CustomerName', y='Month', title="Customers' regular purchasing frequency over the Month by year", color='Year')
        fig_2.update_layout(
            yaxis_title='Number of Buying by Month by Year'
        )
        st.plotly_chart(fig_2,use_container_width=True)
        with st.expander('See explanation'):
            st.write('Ở đây sẽ viết giải thích, nhưng mà chưa viết ○( ＾皿＾)っ Hehehe…')
        col1, col2 = st.columns(2)
        with col1:
            st.code(query, language='sql')
        with col2:
            st.dataframe(req_3_monthyear)
    
if slt_br == br_options[3]:
    # !st.write('Which customer spends the most money for buying album?')
    top_k = st.slider(':eyes: Identify the number of customers who spend the most money on purchasing albums', 
                      min_value=1, max_value=59, value=5)
    query = Query.query_4%top_k
    req_4 = Query.req_4.head(top_k)
    fig_1 = create_barchart(req_4,x='CustomerName', y='Total Sales', color='Total Sales', title='Top customers spend the most money')
    st.plotly_chart(fig_1, use_container_width=True)
    with st.expander('See explanation'):
        st.write('Ở đây sẽ viết giải thích, nhưng mà chưa viết ○( ＾皿＾)っ Hehehe…')

    fig_2 = create_bubblechart(req_4,x='Total No of invoices', y='Total Sales', size='Total Sales', title='Top customers spend the most money and total number of order', color='Total Sales', hover_name='CustomerName')
    fig_2.update_layout(xaxis = dict(autorange="reversed"))
    st.plotly_chart(fig_2, use_container_width=True)
    with st.expander('See explanation'):
        st.write('Ở đây sẽ viết giải thích, nhưng mà chưa viết ○( ＾皿＾)っ Hehehe…')

    col1, col2 = st.columns(2)
    with col1:
        st.code(query, language='sql')
    with col2:
        st.dataframe(req_4)

if slt_br == br_options[4]:
    # st.write('Which employee helps achieve invoices the most?')
    query = Query.query_5
    req_5 = Query.req_5
    fig_1 = create_piechart(req_5,names='EmployeeId', values='Total Invoices', color='EmployeeId', title="How many invoices each employees achieve",hover_name='EmployeeName')
    fig_1_1 = create_barchart(req_5,x='EmployeeName', y="Total Invoices", color='Total Invoices',title="How many invoices each employees achieve")
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_1,use_container_width=True)
    with col2:
        st.plotly_chart(fig_1_1, use_container_width=True)
    with st.expander('See explanation'):
        st.write('Ở đây sẽ viết giải thích, nhưng mà chưa viết ○( ＾皿＾)っ Hehehe…')
    col1, col2 = st.columns(2)
    with col1:
        st.code(query, language='sql')
    with col2:
        st.dataframe(req_5)

    query_time = Query.query_5_time
    req_5_time = Query.req_5_time
    query_year = Query.query_5_year
    req_5_year = Query.req_5_year
    selected_emp = st.multiselect(
        label='Select Employee', 
        options=list(req_5_time['EmployeeId'].astype(int).value_counts().index.to_list()), 
        default=list(req_5_time['EmployeeId'].astype(int).value_counts().index.to_list())
        )

    if selected_emp:
        fulldate, year = st.tabs(['Full Date', 'Year'])
        for i in sorted(selected_emp):
            i = int(i)
            with fulldate: 
                fig_2 = create_barchart(req_5_time[req_5_time["EmployeeId"]==i], x="FullDate", y="Total Invoices", title=f"How many invoices that Employee have ID = {i} achieve")
                st.plotly_chart(fig_2, use_container_width=True)               

            with year:
                fig_2 = create_barchart(req_5_year[req_5_year["EmployeeId"]==i], x="MonthOfYear", y="Total_Invoices", color='Year', title=f"How many invoices that Employee have ID = {i} achieve")
                st.plotly_chart(fig_2, use_container_width=True)
                col1, col2 = st.columns(2)
        with fulldate:
            col1, col2 = st.columns(2)
            with col1:
                st.code(query_time, language='sql')
            with col2:
                st.dataframe(req_5_time) 
        with year:
            col1, col2 = st.columns(2)
            with col1:
                st.code(query_year, language='sql')
            with col2:
                st.dataframe(req_5_year) 

if slt_br == br_options[5]:
    # st.write('Which employee has the highest sales revenue?')
    query = Query.query_6
    req_6 = Query.req_6
    fig_1 = create_piechart(req_6,names='EmployeeId', values='Total_Sales', color='EmployeeId', title="How many Sales revenue each employees achieve",hover_name='EmployeeName')
    fig_1_1 = create_barchart(req_6,x='EmployeeName', y="Total_Sales", color='Total_Sales',title="How many invoices each employees achieve")
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_1,use_container_width=True)
    with col2:
        st.plotly_chart(fig_1_1, use_container_width=True)
    with st.expander('See explanation'):
        st.write('Ở đây sẽ viết giải thích, nhưng mà chưa viết ○( ＾皿＾)っ Hehehe…')

    query_time = Query.query_6_time
    req_6_time = Query.req_6_time
    query_year = Query.query_6_year
    req_6_year = Query.req_6_year
    selected_emp = st.multiselect(
        label='Select Employee', 
        options=list(req_6_time['EmployeeId'].astype(int).value_counts().index.to_list()), 
        default=list(req_6_time['EmployeeId'].astype(int).value_counts().index.to_list())
        )

    if selected_emp:
        fulldate, year = st.tabs(['Full Date', 'Year'])
        for i in sorted(selected_emp):
            i = int(i)
            with fulldate: 
                fig_2 = create_barchart(req_6_time[req_6_time["EmployeeId"]==i], x="FullDate", y="Total_Sales", title=f"How many Sales revenue that Employee have ID = {i} achieve")
                st.plotly_chart(fig_2, use_container_width=True)                

            with year:
                fig_2 = create_barchart(req_6_year[req_6_year["EmployeeId"]==i], x="MonthOfYear", y="Total_Sales", color='Year', title=f"How many Sales revenue that Employee have ID = {i} achieve")
                st.plotly_chart(fig_2, use_container_width=True)
        with fulldate:
            col1, col2 = st.columns(2)
            with col1:
                st.code(query_time, language='sql')
            with col2:
                st.dataframe(req_6_time) 
        with year:
            col1, col2 = st.columns(2)
            with col1:
                st.code(query_year, language='sql')
            with col2:
                st.dataframe(req_6_year) 

if slt_br == br_options[6]:
    # st.write('Which music genre is purchased the most by year?')
    with st.expander('Number of Genre in store'):
        req = df_DimGenre
        st.dataframe(req)
    day, month, quarter, year = st.tabs(['Day','Month','Quarter','Year'])
    with day:
        query = Query.query_7_day
        req_7 = Query.req_7_day
        test = create_barchart(req_7, x='FullDate', y='GenreId', color='Total Sales'
                            , title=f'Total Sales of Genre')
        st.plotly_chart(test, use_container_width=True)
        col1, col2 = st.columns(2)
        with col1:
            st.code(query, language='sql')
        with col2:   
            st.dataframe(req_7)

    with month:
        st.write('もう諦めた。～(　TロT)σ')
    #     query = Query.query_1_month
    #     req_1 = run_query(query)
    #     fig_1 = create_barchart(req_1, x='MonthName', y='Total Sales', color='Year'
    #                             , title='Monthly Total Sales Over Years')
    #     fig_2 = create_linechart(req_1, x='MonthName', y='Total Sales', color='Year'
    #                             , title='Monthly Total Sales Over Years')
    #     st.plotly_chart(fig_1)  
    #     with st.expander('See explanation'):
    #         st.write('Ở đây sẽ viết giải thích, nhưng mà chưa viết ○( ＾皿＾)っ Hehehe…')
    #     st.plotly_chart(fig_2)
    #     with st.expander('See explanation'):
    #         st.write('Ở đây sẽ viết giải thích, nhưng mà chưa viết ○( ＾皿＾)っ Hehehe…')

    #     col1, col2 = st.columns(2)
    #     with col1:
    #         st.code(query, language='sql')
    #     with col2:   
    #         st.dataframe(req_1)
    with quarter:
        st.write('もう諦めた。～(　TロT)σ')
    #     query = Query.query_1_quarter
    #     req_1 = run_query(query)
    #     fig_1 = create_barchart(req_1, x='Quarter', y='Total Sales', color='Year'
    #                             , title='Quarterly Total Sales Over Years')
    #     req_1 = run_query(query)
    #     fig_2 = create_linechart(req_1, x='Quarter', y='Total Sales', color='Year'
    #                             , title='Quarterly Total Sales Over Years')
    #     st.plotly_chart(fig_1)
    #     with st.expander('See explanation'):
    #         st.write('Ở đây sẽ viết giải thích, nhưng mà chưa viết ○( ＾皿＾)っ Hehehe…')
    #     st.plotly_chart(fig_2)
    #     with st.expander('See explanation'):
    #         st.write('Ở đây sẽ viết giải thích, nhưng mà chưa viết ○( ＾皿＾)っ Hehehe…')
    #     col1, col2 = st.columns(2)
    #     with col1:
    #         st.code(query, language='sql')
    #     with col2:   
    #         st.dataframe(req_1)
    with year:
        st.write('もう諦めた。～(　TロT)σ')

    #     query = Query.query_1_year
    #     req_1 = run_query(query)
    #     fig_1 = create_barchart(req_1, x='Year', y='Total Sales', color='Total Sales'
    #                             , title='Total Sales Over Years')
    #     st.plotly_chart(fig_1)
    #     with st.expander('See explanation'):
    #         st.write('Ở đây sẽ viết giải thích, nhưng mà chưa viết ○( ＾皿＾)っ Hehehe…')

    #     fig_2 = create_bubblechart(req_1,x='Year', y='Total Sales', size='Total Sales', title='Total Sales Over Years', hover_name='Year', color='Total Sales')
    #     st.plotly_chart(fig_2)
    #     with st.expander('See explanation'):
    #         st.write('Ở đây sẽ viết giải thích, nhưng mà chưa viết ○( ＾皿＾)っ Hehehe…')
 
    #     col1, col2 = st.columns(2)
    #     with col1:
    #         st.code(query, language='sql')
    #     with col2:   
    #         st.dataframe(req_1)

if slt_br == br_options[7]:
    #? st.write('How much gerne music in playlist?')
    st.warning('இ௰இ This requirement is in the Waitlist...')

if slt_br == br_options[8]:
    st.warning('(ˉ▽￣～) This requirement solution is still in rechecking...')
    # ! st.write('How long does it take for customers to return to buy track?')
    top_k = st.slider(':heart: Indicate the number of customer you wish to return', 
                      min_value=1, max_value=59, value=10)
        
    query_last = Query.query_9_last%top_k
    query_avg = Query.query_9_avg%top_k

    req_9_last = Query.req_9_last.head(top_k)
    req_9_avg = Query.req_9_avg.head(top_k)

    # filter = st.checkbox('Do you want to sort data by number of days?')
    # if filter:
    #     order = st.radio(label='Choose filter order', options=["Descending","Ascending"],index=0, key='horizontal')
    #     query_last = query_last.replace('order by fs.CustomerId', "order by 'Average Days returned' desc")
    #     query_avg = query_avg + "order by NumberOfDaysReturned desc"
    #     if order == 'Descending':
    #         query_last = query_last.replace('desc', 'asc')
    #         query_avg = query_avg.replace('desc', 'asc')

    fig_1 = create_barchart(req_9_last,x='CustomerName', y='NumberOfDaysReturned',title='Customers Number of Returned Days since last order', color='NumberOfDaysReturned')
    st.plotly_chart(fig_1, use_container_width=True)
    with st.expander('See explanation'):
        st.write('Ở đây sẽ viết giải thích, nhưng mà chưa viết ○( ＾皿＾)っ Hehehe…')

    col1, col2 = st.columns(2)
    with col1:
        st.code(query_last, language='sql')
    with col2:
        st.dataframe(req_9_last)

    fig_2 = create_barchart(req_9_avg,x='CustomerName', y='Average Days returned',title='Customers Average Returned Days', color='Average Days returned')
    st.plotly_chart(fig_2, use_container_width=True)
    with st.expander('See explanation'):
        st.write('Ở đây sẽ viết giải thích, nhưng mà chưa viết ○( ＾皿＾)っ Hehehe…')

    col1, col2 = st.columns(2)
    with col1:
        st.code(query_avg, language='sql')
    with col2:
        st.dataframe(req_9_avg)

if slt_br == br_options[9]:
    #? st.write('How much genre in playlist?')
    st.warning('இ௰இ This requirement is in the Waitlist...')

if slt_br == None:
    st.warning("Select one",icon="👆")
    st.write("Ở đây sẽ giới thiệu về business requirements và kêu người ta chọn trong select box")