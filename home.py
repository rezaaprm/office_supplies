# library dashboard
import streamlit as st
import streamlit_extras.add_vertical_space as avs

# lib manipulation data
import numpy as np
import pandas as pd

# library visualization
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
# ----------------------------------------------------------------------------------------------

# load-dataset with parse date
dataset = pd.read_csv("dataset/dataset-supply.csv", parse_dates=["Ship Date"])

# convert month to object
dataset['Month'] = dataset['Ship Date'].dt.month
# ----------------------------------------------------------------------------------------------

def unpivot_table(df, index, columns):

    # grouping by columns
    df = dataset.query("Category == @index").groupby(by=columns)["Sold"].aggregate("sum").reset_index()
    
    # change columns name
    df.columns = ["Category", "Labels", "Values"]

    # calculate percentage sold
    df["Percent"] = np.round(df["Values"] / df["Values"].sum()*100)

    # return values
    return df
# ----------------------------------------------------------------------------------------------

def lineplot(data):

    # create figure
    fig, ax = plt.subplots(figsize=(20,5))
    sns.lineplot(data=data, x="Labels", y="Percent", color="#006A4E", lw=2.5)

    # set labels
    ax.set_title("", fontsize=14)
    ax.set_xlabel("", fontsize=12)
    ax.set_ylabel("", fontsize=12)
    ax.grid(True)

    # custom labes
    ax.set_xticks(np.arange(1,13,1))
    ax.set_yticks(np.arange(0, 26, 5))
    return fig
# ----------------------------------------------------------------------------------------------

def barplot(data):

    # create figure
    fig, ax = plt.subplots(figsize=(10,5))
    sns.barplot(data=data, x="Labels", y="Percent", hue="Labels", palette="Greens", legend=False)

    # set labels
    ax.set_title("", fontsize=14)
    ax.set_xlabel("", fontsize=12)
    ax.set_ylabel("", fontsize=12)
    ax.grid(True)

    return fig
# ----------------------------------------------------------------------------------------------

# config web streamlit
st.set_page_config(page_title="My Dasboard",layout="wide")

# container-header
with st.container():
    
    # header-dashboard
    st.markdown("## Data Visualization for Sales of Office Products")
    avs.add_vertical_space(2)

    # choose category product
    index = st.selectbox(label="Choose a category products", options=("Furniture","Office Supplies","Technology"))
# ----------------------------------------------------------------------------------------------

# container-time-series
with st.container():
    fig = lineplot(unpivot_table(df=dataset, index=index, columns=["Category", "Month"]))
    st.pyplot(fig, use_container_width=True)

# split two-columns
col1, col2 = st.columns([0.5,0.5], gap="small")

# ...
with col1:
    # convert to unpivot
    st.success("Sales "+str(index)+" On Every Year")
    df = unpivot_table(df=dataset, index=index, columns=["Category", "Year"])
    df = df.sort_values(by="Values", ascending=True).tail(4)
    st.pyplot(barplot(df), use_container_width=True)

# ...
with col2:
    # convert to unpivot
    st.success("Sales "+str(index)+" By Ship Mode")
    df = unpivot_table(df=dataset, index=index, columns=["Category", "Ship Mode"])
    df = df.sort_values(by="Values", ascending=True).tail(4)
    st.pyplot(barplot(df), use_container_width=True)

# ...
with col1:
    # convert to unpivot
    st.success("Sales "+str(index)+" On Every Area")
    df = unpivot_table(df=dataset, index=index, columns=["Category", "Area"])
    df = df.sort_values(by="Values", ascending=True).tail(4)
    st.pyplot(barplot(df), use_container_width=True)

with col2:
    # convert to unpivot
    st.success("Sales "+str(index)+" On Every Region")
    df = unpivot_table(df=dataset, index=index, columns=["Category", "Region"])
    df = df.sort_values(by="Values", ascending=True).tail(4)
    st.pyplot(barplot(df), use_container_width=True)
