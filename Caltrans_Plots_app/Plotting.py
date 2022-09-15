# imports
import streamlit as st
import pandas as pd
import plotly.express as px
import csv
from Caltrans_module import *
from Caltrans_module import title_info, page_info_dict, heading_list, newparatext, support_links_dict, copyright_statement

# Streamlit and pandas to write display various headers and information texts
st.set_page_config(page_title="Caltrans-Plots")
st.title("Caltrans-Plots 📈")

container = st.container()
container.write(title_info)
container.write("Page information:")
df1 = pd.DataFrame(data=page_info_dict, index=[1])
container.write(df1)
container.write("2 Charts for:")
container.write(heading_list)
st.write(newparatext)

# dropdown menu to browse and upload csv files using streamlit
st.subheader("Choose one csv file to upload")

uploaded_file = st.file_uploader('Choose a CSV file', type=['csv'])

if uploaded_file:
    st.markdown("----")
    df2 = pd.read_csv(uploaded_file)
    st.dataframe(df2)

# copyright information and social media links as footer display using streamlit and pandas
st.write("Social Media & Support Links, California Government:")
df2 = pd.DataFrame(data=support_links_dict )
st.write(df2)
st.write(copyright_statement)

#----End of Plotting.py file----------------------------------------------------------------
# Coder: Swati Mishra
