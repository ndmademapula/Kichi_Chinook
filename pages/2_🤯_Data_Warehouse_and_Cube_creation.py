import streamlit as st
from PIL import Image
from constant import *

st.subheader(':sparkles: Project workflow')
workflow = '''
### The implementation of this project is structred from 4 stages: 

**:red[(1) ETL process]**: the process which extract, loading and transformation data from multiple sources (CSV, XLX and OLE DB files).

**:red[(2) OLAP cube creation]**: which is the Middle Tier of the architecture, takes center stage in the subsequent phase as SQL Server Analysis Services (SSAS) is employed to craft Online Analytical Processing (OLAP) cubes. 

**:red[(3) OLAP reports]**: Introduces the field of OLAP reporting in The Top Tier of the architecture. In order to obtain valuable insights from the OLAP cubes.

**:red[(4) Data interactive Web app]**: This web app is our demostration of this stage.
'''
col0, col1, col2 = st.columns([1,2,3])
with col0:
    st.write('')
with col1:
    img_wf = Image.open(r'Images/1.png')
    st.image(img_wf, caption='Chinook Cube', output_format='PNG', width=250)
with col2:
    st.markdown(workflow)

st.divider()
st.subheader(':tada: Cube structure')
st.markdown('''This Data Source View shows show the relationship between dimension and fact tables. ''')
img_cube = Image.open(r'Images/Cube.png')
st.image(img_cube, caption='Chinook Cube', output_format='PNG')

st.subheader(':dizzy: About Chinook Cube')

col1,col2 = st.columns(2)
with col1:
    img_cube = Image.open('Images/FactSales_Cube.png')
    st.image(img_cube, caption='Fact Sales Cube', use_column_width='auto')
with col2:
    fact, dim1, dim2, dim3, dim4= st.tabs(["Fact Sales",'Dim Employee','Dim Track', 'Dim Customer', 'Dim Date'])
    with fact:
        st.dataframe(df_FactSales)
    with dim1:
        st.dataframe(df_DimEmployee)
    with dim2:
        st.dataframe(df_DimTrack)
    with dim3:
        st.dataframe(df_DimCustomer)
    with dim4:
        st.dataframe(df_DimDate)

col1, col2 = st.columns(2)
with col1: 
    img_cube = Image.open('Images/FactGenre_Cube.png')
    st.image(img_cube, caption='Fact Genre Cube', use_column_width='auto')
with col2:
    fact, dim1, dim2, dim3 = st.tabs(["Fact Genre",'Dim Date','Dim Customer', 'Dim Genre'])
    with fact:
        st.dataframe(df_DimGenre)
    with dim1:
        st.dataframe(df_DimDate)
    with dim2:
        st.dataframe(df_DimCustomer)
    with dim3:
        st.dataframe(df_DimGenre)
col1,col2 = st.columns(2)
with col1: 
    img_cube = Image.open('Images/FactListen_Cube.png')
    st.image(img_cube, caption='Fact Listen Cube', use_column_width='auto')
with col2:
    fact, dim1, dim2, dim3 = st.tabs(["Fact Listen",'Dim Album','Dim Track', 'Dim Genre'])
    with fact:
        st.write("Fact Listen Table")
        st.dataframe(df_FactListen)
    with dim1:
        st.dataframe(df_DimAlbum)
    with dim2:
        st.dataframe(df_DimTrack)
    with dim3:
        st.dataframe(df_DimGenre)
