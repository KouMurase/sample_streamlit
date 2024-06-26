import plotly
import datetime as dt
import plotly.express as px
import pandas as pd
import streamlit as st
from datetime import datetime#, timedelta
from PIL import Image
import os
from pathlib import Path
import base64

#import streamlit_authenticator as sa
#import hmac


def main():

    #img = Image.open("./app/static/impala.png")

    #st.image(img, caption='icon', use_column_width=False, width=150)

    image_bytes = Path("./input/impala.png").read_bytes()
    image_encoded = base64.b64encode(image_bytes).decode()

    # HTML埋め込み
    st.markdown("""
        <style>
        .my-text {
            color: white;
            font-size: 24px;
            background-color: #000080;
            padding: 10px;
            border-radius: 10px;
        }
        </style>
        """
        +f"""
        <p class='my-text'>Hello World! <br>
        <img src="data:image/png;base64,{image_encoded}" height="150" width="150" style="vertical-align:middle;"></p>
        </p>
        """, unsafe_allow_html=True)


    data = pd.read_csv("./input/data_20240329.csv", encoding="shift-jis", header=2)
    data = data.drop(data.index[0:2], axis=0)

    cols = [c for c in data.columns if ".1" not in c and ".2" not in c and ".3" not in c]
    data = data[cols]

    data["月日"] = data["年月日"].apply(lambda x: x.replace("2024/", ""))

    fig = px.line(data, x="月日", y=["平均気温(℃)","最高気温(℃)","最低気温(℃)"],
                color_discrete_map={
                    "平均気温(℃)": "#ffa500",
                    "最高気温(℃)": "#ff6347",
                    "最低気温(℃)": "#4169e1",
                },
                title="2024年の東京の気象情報")

    #st.line_chart(data, x="年月日", y=["平均気温(℃)","最高気温(℃)","最低気温(℃)","日照時間(時間)"])
    st.plotly_chart(fig)


    #######################
    # 積算気温
    #######################

    data["年月日"] = pd.to_datetime(data["年月日"])
    data["積算気温"] = data[data["年月日"]>=dt.datetime(2024,2,1)]["平均気温(℃)"].cumsum()

    # 開始日と終了日を定義
    start_date = datetime(2024, 2, 1)
    end_date = datetime(2024, 4, 30)
    # 日付の範囲を生成
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    # データフレームを作成
    df = pd.DataFrame(date_range, columns=['年月日'])
    df = df.merge(data[["年月日", "積算気温"]], on="年月日", how="left")

    fig2 = px.line(df, x="年月日", y="積算気温", 
                title="2024年の東京の積算気温(2/1から)")
    fig2.update_layout(yaxis=dict(range=[0, 600]))
    # ピンク色の一線を追加
    fig2.add_shape(type='line',
                x0= datetime(2024, 2, 1), y0=600,  # 線の始点
                x1=datetime(2024, 4, 30), y1=600,  # 線の終点
                line=dict(color='pink', width=20))  # 線の色と太さ

    st.plotly_chart(fig2)

if __name__=="__main__":
    print(os.getcwd())
    main()