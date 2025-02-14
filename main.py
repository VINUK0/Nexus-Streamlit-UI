import streamlit as st
import sqlite3
import uuid

if not "active_login" in st.session_state:
    st.session_state.active_login = False

if not "login_attemps" in st.session_state:
    st.session_state.login_attemps = 0
    
if not "show_greet_popup" in st.session_state:
    st.session_state.show_greet_popup = 0
    
if "history_id" not in st.session_state:
    st.session_state.history_id = uuid.uuid1()
    
if "display_name" not in st.session_state:
    st.session_state.display_name = ""


def authenticate_user(username: str, password: str):
    
    conn = sqlite3.connect(database='userauths.db')
    cursor = conn.cursor()

    # SQL command to retrieve user information based on username and password
    query = '''
    SELECT auth_level, private_google_api, private_anthropic_api, private_together_api, private_xai_api, private_openrouter_api, private_openai_api, private_glhf_api
    FROM user_auths
    WHERE username = ? AND password = ?;
    '''
    
    cursor.execute(query, (username, password))
    result = cursor.fetchone()

    conn.close()
    
    if result:
        auth_level, private_google_api, private_anthropic_api, private_together_api, private_xai_api, private_openrouter_api, private_openai_api, private_glhf_api= result
        st.session_state.private_google_api = private_google_api
        st.session_state.private_anthropic_api = private_anthropic_api
        st.session_state.private_together_api = private_together_api
        st.session_state.private_xai_api = private_xai_api
        st.session_state.private_openrouter_api = private_openrouter_api
        st.session_state.private_openai_api = private_openai_api
        st.session_state.private_glhf_api = private_glhf_api
        st.session_state.auth_level = auth_level
        st.session_state.username = username
        st.session_state.password = password
        
        
        return True
    else:
        
        return False





if not st.session_state.active_login:
    
    if "messages" in st.session_state:
        del st.session_state.messages
        
        
    
    with st.container(key="login-container"):
        with st.form(key="login_contro"):
            st.write("<h3 style='text-align: center; color: red;'>[Authorized Personnel Only]</h3>", unsafe_allow_html=True)
            
            st.text_input(label="Username", key="auth_username", placeholder="Your Name Here")
            st.text_input(label="Password", key="auth_password", placeholder="Your Password Here", type="password")
            
            submit_button = st.form_submit_button(label="Authorize", icon=":material/login:")
            
            st.markdown(body="""<style>
                .stAppViewContainer {
                    background-image: url('https://images8.alphacoders.com/134/thumb-1920-1344517.png');
                    background-size: cover;
                    background-position: center;
                    background-repeat: no-repeat;
                    }
                    .st-key-login-container {
                        background: #00001a !important;
                        width: 50vw !important;
                        height: 80vh !important;
                        margin-top: 10%;
                        margin-left: 25%;
                        }
                        <style/>
                        """, unsafe_allow_html=True)
            
            
            
            if submit_button:
                auth : bool = authenticate_user(username=st.session_state.auth_username, password=st.session_state.auth_password)
                
                if auth:
                    st.session_state.active_login = True
                    st.rerun()
                else:
                    st.session_state.auth_attemps += 1
            
