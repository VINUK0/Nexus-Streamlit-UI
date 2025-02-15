import streamlit as st
import sqlite3
import uuid

st.set_page_config(page_title="Nexus UI Login", layout="wide")

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


def authenticate_user(username: str, password: str) -> bool:
    
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
            
            st.markdown(body="""<style>.stAppViewContainer {
                    background-image: url('https://images8.alphacoders.com/134/thumb-1920-1344517.png');
                    background-size: cover;
                    background-position: center;
                    background-repeat: no-repeat;
                    }<style/>""", unsafe_allow_html=True)
            
            st.write("<p style='text-align: center; color: red; font-size: 2.0vw;'><strong>[Authorized Personnel Only]</strong></p>", unsafe_allow_html=True)
            
            st.text_input(label="Username", key="auth_username", placeholder="Your Name Here")
            st.text_input(label="Password", key="auth_password", placeholder="Your Password Here", type="password")
            
            submit_button = st.form_submit_button(label="Authorize", icon=":material/login:")
            
            st.markdown(body="""<style>
                    .st-key-login-container {
                        background: #00001a !important;
                        width: 50vw !important;
                        opacity: 0.93;
                        height: 48vh !important;
                        margin-top: 10vh;
                        margin-left: 25%;
                        border-radius: 25px;
                        border: none !important;
                        position: absolute;
                        }
                    .stForm {
                        border: none !important;
                    }
                        <style/>
                        """, unsafe_allow_html=True)
            
            
            
            if submit_button:
                auth : bool = authenticate_user(username=st.session_state.auth_username, password=st.session_state.auth_password)
                
                if auth:
                    st.session_state.active_login = True
                    st.rerun()
                else:
                    st.session_state.login_attemps += 1
            

@st.dialog(title="Authorization Successful")
def show_admin_msg() -> None:
    st.write(f":green[*Welcome*] :red[*Administrator | {st.session_state.username}*] :green[*, hope you have a wonderful time.*]")
    col1, col2, col3 = st.columns(spec=[0.4, 0.2, 0.4])
    col2.image(image="https://cdn-icons-png.flaticon.com/512/13906/13906210.png", width=64)

@st.dialog(title="Authorization Successful")
def show_user_msg() -> None:
    st.write(f":green[*Welcome {st.session_state.username}, hope you have a wonderful time.]*")
    
@st.dialog(title="Authorization Failed")
def show_failed_auth_msg() -> None:
    st.write(f":red[*If you forgot the password...there is currently no way to reset it, except contacting the server administrator.*]")

if st.session_state.active_login and st.session_state.auth_level == 1 and st.session_state.show_greet_popup == 0:
    show_admin_msg()
    st.session_state.show_greet_popup += 1
    
if st.session_state.active_login and st.session_state.auth_level == 0 and st.session_state.show_greet_popup == 0:
    show_user_msg()
    st.session_state.show_greet_popup += 1
    
if not st.session_state.active_login and st.session_state.login_attemps > 0:
    show_failed_auth_msg()
    st.session_state.Show_greet_popup += 1