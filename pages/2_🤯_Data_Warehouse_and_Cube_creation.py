import streamlit as st
import pandas as pd
import pyodbc
from PIL import Image
from constant import *

img_cube = Image.open(r'Images/Cube.png')
st.image(img_cube, caption='Chinook Cube', output_format='PNG')
col1, col2, col3 = st.columns(3)

with col1: 
    img_cube = Image.open('Images/FactGenre_Cube.png')
    st.image(img_cube, caption='Fact Genre Cube', use_column_width='auto')
with col2: 
    img_cube = Image.open('Images/FactListen_Cube.png')
    st.image(img_cube, caption='Fact Listen Cube', use_column_width='auto')
with col3: 
    img_cube = Image.open('Images/FactSales_Cube.png')
    st.image(img_cube, caption='Fact Sales Cube', use_column_width='auto')

st.subheader('Fact Tables')

st.write("Fact Sales Table")
st.dataframe(df_FactSales)

st.write("Fact Listen Table")
st.dataframe(df_FactListen)

st.write("Fact Genre Table")
st.dataframe(df_DimGenre)

st.subheader('Dimensions Tables')

st.write("Customer Dimension Table")
st.dataframe(df_DimCustomer)

st.write("Employee Dimension Table")
st.dataframe(df_DimEmployee)

st.write("Track Dimension Table")
st.dataframe(df_DimTrack)

st.write("Date Dimension Table")
st.dataframe(df_DimDate)

st.write("Genre Dimension Table")
st.dataframe(df_DimGenre)

st.write("Album Dimension Table")
st.dataframe(df_DimAlbum)