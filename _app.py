import streamlit as st
import streamlit_authenticator as stauth

import yaml
from yaml.loader import SafeLoader

def run():
    st.title("Basic Authentication")

    # ユーザーの資格情報取得
    config = []
    with open('src/config.yml') as file:
        config = yaml.load(file, Loader = SafeLoader)

    # 認証
    authenticator = stauth.Authenticate(
        config['credentials'],
        cookie_name="some_cookie_name",
        key="some_key",
        cookie_expiry_days="1"
    )
    name, authentication_status, user_name = authenticator.login("Login", "main")
    

    # 判定
    if authentication_status:
        """
        認証成功時の処理
        """
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
        <p class='my-text'>Hello World! <br>
        <img src=".app/static/impala.png" height="150" width="150" style="vertical-align:middle;">
        </p>
        """, unsafe_allow_html=True)
        from app import main
        main()
        
    elif authentication_status is False:
        st.error("Username/password is incorrect")
    elif authentication_status is None:
        st.warning("Please enter your username and password")

if __name__ == "__main__":
    run()