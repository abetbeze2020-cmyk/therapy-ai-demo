# app_public.py
import streamlit as st
import datetime as dt
from openai import OpenAI

# --- Streamlit Cloud secrets ---
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --- App title ---
st.set_page_config(page_title="Therapy Continuity Demo", page_icon="🧠", layout="centered")
st.title("🧠 Therapy Continuity (Demo)")

st.markdown("---")
st.header("💬 Chat")

# Keep chat in memory only (not saved to disk)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Show chat messages
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(f"""
            <div style='text-align:right;
                        background-color:#000000;
                        color:#FFFFFF;
                        border-radius:12px;
                        padding:10px;
                        margin:6px 0;
                        display:inline-block;
                        max-width:80%;'>
                {msg['content']}
            </div>
        """, unsafe_allow_html=True)

    elif msg["role"] == "assistant":
        st.markdown(f"""
            <div style='text-align:left;
                        background-color:#1C1C1C;
                        color:#FFFFFF;
                        border-radius:12px;
                        padding:10px;
                        margin:6px 0;
                        display:inline-block;
                        max-width:80%;'>
                {msg['content']}
            </div>
        """, unsafe_allow_html=True)

# --- User input ---
user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_input,
        "timestamp": dt.datetime.now().isoformat()
    })

    # "AI is typing..." placeholder
    typing_placeholder = st.empty()
    typing_placeholder.markdown(f"""
        <div style='text-align:left;
                    background-color:#333333;
                    color:#CCCCCC;
                    border-radius:12px;
                    padding:10px;
                    margin:6px 0;
                    display:inline-block;
                    font-style:italic;
                    max-width:80%;'>
            AI is typing...
        </div>
    """, unsafe_allow_html=True)

    # --- System prompt ---
    messages = [{"role": m["role"], "content": m["content"]}
                for m in st.session_state.chat_history if m["role"] in ["user", "assistant"]]

    messages.insert(0, {
        "role": "system",
        "content": (
            "You are a gentle, reflective AI that helps someone continue their therapy work between sessions. "
            "You use calm, compassionate language, reflect feelings, and ask open-ended questions. "
            "Avoid giving directives or clinical labels; focus on empathy, understanding, and subtle reframing. "
            "If the user gives a number 0–10 at the start of a day, softly follow up by asking what makes it that number today. "
            "Avoid repeating the same question or reflection; instead, build naturally from what the user just said. "
            "When the user expresses anxiety, distress, or overwhelm, slow down and respond in short, calm sentences "
            "that focus on grounding, reassurance, and being present."
        )
    })

    # --- Generate AI reply ---
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        reply = response.choices[0].message.content.strip()
    except Exception as e:
        reply = f"⚠️ Error: {e}"

    typing_placeholder.empty()

    st.session_state.chat_history.append({
        "role": "assistant",
        "content": reply,
        "timestamp": dt.datetime.now().isoformat()
    })

    st.rerun()

st.markdown("---")
st.caption("Demo version — messages are not stored. Powered by OpenAI API.")
