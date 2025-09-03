import os
import streamlit as st
from dotenv import load_dotenv
import time
from huggingface_hub import InferenceClient

if 'HF_TOKEN' in st.secrets:
    HF_TOKEN = st.secrets['HF_TOKEN']
    st.sidebar.success("API Key loaded from Streamlit Secrets.")


else:
    load_dotenv()
    HF_TOKEN = os.environ.get("HF_TOKEN")
    if HF_TOKEN:
        st.sidebar.info("API Key loaded from local environment.")
    else:
        st.sidebar.warning("API Key not found. Please set it in the sidebar.")
        HF_TOKEN = None


if HF_TOKEN:
    try:
        client = InferenceClient(
            provider="hf-inference",
            api_key=HF_TOKEN,
        )
        
        
        test_response = client.question_answering(
            question="What is the purpose?",
            context="This is a test of the API connection.",
            model="deepset/roberta-base-squad2",
        )
        API_CONNECTED = True
        st.sidebar.success("✅ API Connected Successfully!")
    except Exception as e:
        API_CONNECTED = False
        st.sidebar.error(f"❌ API Connection Failed: {str(e)}")
else:
    API_CONNECTED = False
    client = None


utar_context = """
Universiti Tunku Abdul Rahman (UTAR) is a private university in Malaysia with campuses in Kampar and Sungai Long. 
Established in 2002, UTAR has grown to become one of Malaysia's premier private universities.

Kampar Campus:
- Located in Kampar, Perak
- Spans over 1,300 acres with a beautiful lake
- Modern facilities and infrastructure
- Offers foundation, undergraduate, and postgraduate studies

Library:
- Located in Block H
- Open from 8am to 11pm
- Students can borrow books using student ID
- Study rooms can be booked online or at counter
- Undergraduates: 10 books for 2 weeks
- Postgraduates: 20 books for 30 days
- Red Spot books: special limits (1 book for 2 hours or overnight)

Cafeteria:
- Two main cafeterias: Block C and Block K
- Operating hours: 9am to 3pm
- Food options: Western, Malay, Chinese, Vegetarian, Arabic
- Various food stalls and push cart vendors

Scholarships:
- Automatic scholarships for SPM high achievers (5A's and above)
- Application-based scholarships: Lim Goh Tong, Hartalega, JYY-Group
- Study grants for siblings of UTAR students
- Zero-interest student loans available
- Apply through DEAS website

Sports Facilities:
- Gymnasium, swimming pool, basketball courts, badminton courts
- Sports clubs and activities
- Sports carnivals and inter-faculty games
- Community sports projects

Clubs and Societies:
- Over 60 clubs and societies
- Categories: course-based, cultural, sports, performing arts, voluntary
- Popular clubs: Photography Society, Dance Club, AI Club
- Regulation XIV governs all student societies

Accommodation:
- On-campus hostels: West Lake, East Lake, South Lake
- Room types: single, twin-sharing, triple-sharing
- Prices: RM300 to RM800 per month
- Facilities: WiFi, study areas, laundry, security
- First-year students guaranteed accommodation

Student Services:
- ID card replacement after tuition payment
- Vehicle stickers through DSA (not transferable)
- Lost items reported to DSS
- Insurance: local students (24/7 worldwide), international students (within Malaysia only)

Counseling Services:
- Free counseling for all students
- Appointments: phone (ext: 823/824), email, or visit DSA
- Confidential sessions
- Help with stress, relationships, mental health, academic pressure
- Staff counseling available through HR referral
"""


# Streamlit UI

st.set_page_config(
    page_title="University Life Chatbot",
    layout="centered",
    initial_sidebar_state="expanded"
)

# CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #2E5AAC;
        text-align: center;
    }
    .chat-container {
        background-color: #F0F2F6;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        max-height: 400px;
        overflow-y: auto;
    }
    .user-message {
        background-color: #2E5AAC;
        color: white;
        border-radius: 10px 10px 0 10px;
        padding: 10px;
        margin: 5px 0;
        text-align: right;
        max-width: 80%;
        margin-left: auto;
    }
    .bot-message {
        background-color: #E5E7EB;
        color: #1F2937;
        border-radius: 10px 10px 10px 0;
        padding: 10px;
        margin: 5px 0;
        text-align: left;
        max-width: 80%;
    }
    .stButton button {
        background-color: #2E5AAC;
        color: white;
        width: 100%;
    }
    .suggested-question {
        background-color: #E0E7FF;
        border: 1px solid #2E5AAC;
        border-radius: 15px;
        padding: 8px 15px;
        margin: 5px;
        display: inline-block;
        cursor: pointer;
    }
    .suggested-question:hover {
        background-color: #C7D2FE;
    }
    .api-status {
        padding: 8px;
        border-radius: 5px;
        margin-bottom: 15px;
        text-align: center;
    }
    .api-connected {
        background-color: #D1FAE5;
        color: #065F46;
    }
    .api-disconnected {
        background-color: #FEE2E2;
        color: #B91C1C;
    }
    .utar-blue {
        color: #2E5AAC;
    }
    </style>
""", unsafe_allow_html=True)


if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add welcome message
    st.session_state.messages.append({
        "role": "assistant", 
        "content": "Hello! I'm your UniLife AI assistant. Ask me anything about campus facilities, services, or student life!"
    })

if "user_input" not in st.session_state:
    st.session_state.user_input = ""


st.markdown('<h1 class="main-header">UniLife AI Assistant</h1>', unsafe_allow_html=True)


if API_CONNECTED:
    st.markdown('<div class="api-status api-connected">✅ Connected to Hugging Face QA API</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="api-status api-disconnected">❌ API Not Connected</div>', unsafe_allow_html=True)
    st.error("Please check your Hugging Face token and internet connection.")

st.markdown('<p class="utar-blue">Ask me anything about University Life - I can answer questions about facilities, services, and campus life!</p>', unsafe_allow_html=True)


st.subheader("Try These Questions")
suggested_questions = [
    "What are the library opening hours?",
    "What types of food are available?",
    "How can I apply  scholarships?",
    "What sports facilities are available?",
    "What types of clubs are available?"

]

cols = st.columns(len(suggested_questions))
for i, question in enumerate(suggested_questions):
    with cols[i]:
        if st.button(question, key=f"suggested_{i}"):
            st.session_state.user_input = question
            st.rerun()


st.markdown("### Conversation")
chat_container = st.container()

with chat_container:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f'<div class="user-message">{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-message">{msg["content"]}</div>', unsafe_allow_html=True)


user_input = st.text_input("Type your question here...", value=st.session_state.user_input, key="user_input_widget", label_visibility="collapsed")

col1, col2 = st.columns([5, 1])
with col1:
    ask_button = st.button("Ask", use_container_width=True)
with col2:
    clear_button = st.button("Clear", use_container_width=True)

if clear_button:
    st.session_state.messages = []
    st.session_state.user_input = ""
    st.session_state.messages.append({
        "role": "assistant", 
        "content": "Hello! I'm your UniLife AI assistant. Ask me anything about campus facilities, services, or student life!"
    })
    st.rerun()

if ask_button and user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    
    with st.spinner("Thinking..."):
        if API_CONNECTED:
            try:
                
                answer = client.question_answering(
                    question=user_input,
                    context=utar_context,
                    model="deepset/roberta-base-squad2",
                )
                response = answer.answer if answer.answer else "I couldn't find specific information about that in my knowledge base. Could you try asking about university facilities, services, or campus life?"
            except Exception as e:
                response = f"I encountered an error: {str(e)}. Please try again later."
        else:
            response = "API connection is not available. Please check your Hugging Face token and internet connection."
        
        
        message_placeholder = st.empty()
        full_response = ""
        for chunk in response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            message_placeholder.markdown(f'<div class="bot-message">{full_response}...</div>', unsafe_allow_html=True)
        
        message_placeholder.markdown(f'<div class="bot-message">{response}</div>', unsafe_allow_html=True)
        
      
        st.session_state.messages.append({"role": "assistant", "content": response})
        
    
    st.session_state.user_input = ""
    st.rerun()


st.markdown("---")
if API_CONNECTED:
    st.markdown(
        "<div style='text-align: center; color: gray;'>  Powered by Hugging Face AI</div>", 
        unsafe_allow_html=True
    )
else:
    st.markdown(
        "<div style='text-align: center; color: gray;'> API Not Connected</div>", 
        unsafe_allow_html=True
    )



with st.expander("About This AI Assistant"):
    st.markdown("""
    *UniLife AI Assistant**
    
    This assistant uses Hugging Face's Question Answering API to answer questions about:
    - Library services and hours
    - Cafeteria locations and food options
    - Scholarship opportunities
    - Sports facilities and activities
    - Student clubs and societies
    - Accommodation options
    - Student services
    - Counseling services
    
    The AI extracts answers from the provided context about University life.
    """)


