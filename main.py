import pandas as pd
import matplotlib.pyplot as plt 
#import plotly
import plotly.express as px


import streamlit as st

data = pd.read_csv("./input/data_2024.csv", encoding="shift-jis", header=2)
data = data.drop(data.index[0:2], axis=0)

cols = [c for c in data.columns if ".1" not in c and ".2" not in c and ".3" not in c]
data = data[cols]

data["月日"] = data["年月日"].apply(lambda x: x.replace("2024/", ""))

fig = px.line(data, x="月日", y=cols[1:], 
              title="2024年の東京の気象情報")

#st.line_chart(data, x="年月日", y=["平均気温(℃)","最高気温(℃)","最低気温(℃)","日照時間(時間)"])

st.plotly_chart(fig)