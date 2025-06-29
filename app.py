
import streamlit as st
import pandas as pd
from docx import Document

# ======== LOADING DATA ========
@st.cache_data
def load_data():
    df = pd.read_excel("dataset/Chatbot Questions & Answers (1).xlsx")
    return df

@st.cache_data
def load_handbook_text():
    doc = Document("dataset/Kepler College_Student Handbook.docx")
    return "\n".join([p.text for p in doc.paragraphs if p.text.strip() != ""])

df = load_data()
handbook_text = load_handbook_text()

# ======== STYLING ========
st.set_page_config(page_title="Kepler Chatbot", page_icon="🎓", layout="wide")
st.markdown("""
<style>
.stApp {
    background-color: #f5f7fa;
    color: #0C2340;
}
.question-box {
    background-color: #0C2340;
    color: white;
    padding: 1rem;
    border-radius: 10px;
    margin-bottom: 10px;
}
.answer-box {
    background-color: #2ECC71;
    color: white;
    padding: 1rem;
    border-radius: 10px;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# ======== MAIN INTERFACE ========
st.title("🎓 Kepler Chatbot Assistant")
st.markdown("Ask anything related to Kepler from Q&A or Student Handbook.")

chat_history = st.session_state.get("chat_history", [])
query = st.text_input("Type your question here:")

# ======== SEARCH ENGINE ========
if query:
    chat_history.append(("You", query))
    match = df[df['Questions'].str.lower().str.contains(query.lower())]

    if not match.empty:
        for _, row in match.iterrows():
            q = row['Questions']
            a = row['Answers']
            st.markdown(f"<div class='question-box'>{q}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='answer-box'>{a}</div>", unsafe_allow_html=True)
            chat_history.append(("Bot", a))
    else:
        matches = [line for line in handbook_text.split("\n") if query.lower() in line.lower()]
        if matches:
            st.success("Found matches in Handbook:")
            for line in matches:
                st.markdown(f"<div class='answer-box'>{line}</div>", unsafe_allow_html=True)
                chat_history.append(("Bot", line))
        else:
            msg = "Sorry, no answer found in Q&A or Handbook."
            st.warning(msg)
            chat_history.append(("Bot", msg))

# Show chat history
if chat_history:
    st.divider()
    st.markdown("### 🧠 Chat History")
    for sender, message in chat_history[-10:]:
        role = "🧑" if sender == "You" else "🤖"
        st.markdown(f"**{role} {sender}:** {message}")

st.session_state.chat_history = chat_history
