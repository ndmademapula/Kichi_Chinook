import streamlit as st
import plotly.express as px

def create_linechart(data, x, y, title, color=None, markers=True, **kwargs):
    fig = px.line(data, x=x, y=y, color=color, markers=markers, title=title)
    return fig

def create_barchart(data, x, y, title, color=None, **kwargs):
    fig = px.bar(data, x=x, y=y, color=color, title=title)
    return fig
def create_bubblechart(data, x, y, size, title, hover_name=None, color=None, **kwargs):
    fig = px.scatter(data, x=x, y=y, size=size, title=title, color=color, hover_name=hover_name, size_max=50)
    return fig
def create_piechart(data, names, values, title, color=None, hover_name=None):
    fig = px.pie(data,names=names, values=values,color=color, hover_name=hover_name, title=title)
    return fig