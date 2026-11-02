import streamlit as st
def footer_home():

    logo_url = "https://i.ibb.co/4r5X1FY/apnacollege.png"
    st.markdown(f"""
        <div style="display: flex; align-items: center; justify-content: center; margin-top: 2rem; gap: 6px;">
            <p style="color: white; font-weight: bold;"> Created with ❤️ by </p>
            <img src='{logo_url}' style="max-height:25px;"/>
        
        </div>

                
                """,unsafe_allow_html=True)

def footer_dashboard():

    logo_url = "https://i.ibb.co/4r5X1FY/apnacollege.png"
    st.markdown(f"""
        <div style="display: flex; align-items: center; justify-content: center; margin-top: 2rem; gap: 6px;">
            <p style="color: black; font-weight: bold;"> Created with ❤️ by <b>Sagar Panwar</b></p>
        
        </div>

                
                """,unsafe_allow_html=True)