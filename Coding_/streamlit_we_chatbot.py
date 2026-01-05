import streamlit as st
from PIL import Image
import os
from rag_pipeline import ask_we_bot, add_user_documents
st.set_page_config(
    page_title="WE Chatbot",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="collapsed"
)
# Custom CSS for full screen, buttons, chat bubbles
st.markdown("""
<style>
body, .block-container {
    background-color: #f2f2f2;
    padding: 0;
    margin: 0;
}

/* Title font bold and darker */
h1, h2, h3, h4, h5, h6 {
    font-weight: 700;
    color: #1a1a1a;  
}

/* Landing Page welcome text */
.landing-text {
    color: #1a1a1a;       
    font-size: 28px;     
    font-weight: bold;
    text-align: center;
    margin-top: 20px;
}

/* START button */
.stButton>button {
    background-color: #e60000;
    color: white;
    height: 3em;
    width: 200px;
    border-radius: 20px;
    font-size: 22px;
    font-weight: bold;
    margin: 10px auto;
    display: block;
    cursor: pointer;
}

/* Quick question bubbles */
.quick-btn {
    background-color: #ffcccc;
    color: #000000;
    font-size: 18px;
    font-weight: bold;
    padding: 12px 20px;
    border-radius: 20px;
    margin: 5px 5px 5px 0;
    cursor: pointer;
    display:inline-block;
}

/* Chat bubbles */
.user-msg {
    text-align:right;
    background-color:#ffe6e6;
    color: #1a1a1a;      
    padding:16px;
    border-radius:20px 20px 0 20px;
    margin:5px 0;
    font-weight:bold;
    font-size:18px;
    max-width:90%;
    clear:both;
    overflow-wrap: break-word;
}
.bot-msg {
    text-align:left;
    background-color:#fff2e6;
    color: #1a1a1a;      
    padding:16px;
    border-radius:20px 20px 20px 0;
    margin:5px 0;
    font-weight:bold;
    font-size:18px;
    max-width:90%;
    clear:both;
    overflow-wrap: break-word;
}

/* Full screen for landing page */
.full-screen {
    height: 100vh;
    display:flex;
    flex-direction:column;
    justify-content:center;
    align-items:center;
}

/* Image full width */
.landing-img {
    width: 80%;
    max-width:600px;
    margin-bottom:20px;
}
</style>
""", unsafe_allow_html=True)
if 'chat_started' not in st.session_state:
    st.session_state.chat_started = False
if 'history' not in st.session_state:
    st.session_state.history = []

if not st.session_state.chat_started:
    st.markdown('<div class="full-screen">', unsafe_allow_html=True)
    img_path = "IMG-20230110-WA0017.jpg"
    if os.path.exists(img_path):
        st.image(img_path, use_column_width=True, caption=None)    
    st.markdown('<div class="landing-text">Welcome to WE Chatbot<br>Your intelligent assistant for all Telecom Egypt (WE) services.</div>', unsafe_allow_html=True)
    
    # START button at bottom
    st.markdown("<div style='position:fixed; bottom:50px; width:100%; text-align:center'>", unsafe_allow_html=True)
    if st.button("START"):
        st.session_state.chat_started = True
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
# Chat Page
else:
    st.subheader("WE Chat Support")
    uploaded_files = st.file_uploader(
        "Upload Documents (PDF, DOCX, TXT, HTML, Images)",
        type=["pdf","docx","txt","html","jpg","jpeg","png"], 
        accept_multiple_files=True
    )
    if uploaded_files:
        file_paths = []
        for file in uploaded_files:
            os.makedirs("temp_uploads", exist_ok=True)
            save_path = os.path.join("temp_uploads", file.name)
            with open(save_path, "wb") as f:
                f.write(file.getbuffer())
            file_paths.append(save_path)
        add_user_documents(file_paths)
        st.success(f"Added {len(file_paths)} document(s) successfully!")
    st.markdown("**Quick Questions:**")
    quick_buttons = [
        "How to activate WE Pay?", "How to subscribe to a plan?",
        "Check my balance", "فاتورة الانترنت", "تفعيل باقة جديدة"
    ]
    for btn in quick_buttons:
        if st.button(btn, key=btn):
            st.session_state.history.append(("user", btn))
            answer, sources = ask_we_bot(btn)
            st.session_state.history.append(("bot", answer, sources))
    user_input = st.text_input("Type your question here (English / Arabic):", key="user_input")
    if st.button("Send", key="send") and user_input.strip() != "":
        st.session_state.history.append(("user", user_input))
        answer, sources = ask_we_bot(user_input)
        st.session_state.history.append(("bot", answer, sources))
        st.session_state.user_input = ""  

    for entry in st.session_state.history:
        if entry[0] == "user":
            st.markdown(f"<div class='user-msg'>{entry[1]}</div>", unsafe_allow_html=True)
        else:
            bot_msg = entry[1]
            source_text = "<br>".join([f"[SOURCE]: {s['source']} | [PAGE]: {s['page']}" for s in entry[2]])
            st.markdown(f"<div class='bot-msg'>{bot_msg}<br>{source_text}</div>", unsafe_allow_html=True)
