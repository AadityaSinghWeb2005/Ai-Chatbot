
import streamlit as st
from openai import OpenAI

# Page configuration
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 My AI Chatbot")
st.caption("Powered by OpenRouter")

# API key input
with st.sidebar:
    st.header("Settings")

    api_key = st.text_input(
        "Enter your OpenRouter API Key",
        type="password",
        placeholder="sk-or-v1-..."
    )

    model = st.selectbox(
        "Choose AI Model",
        [
            "openai/gpt-4o-mini",
            "google/gemini-2.5-flash",
            "openrouter/free"
        ]
    )

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
prompt = st.chat_input("Ask me anything...")

if prompt:
    if not api_key:
        st.warning("Please enter your OpenRouter API key in Settings.")

    else:
        # Display and save user message
        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            # OpenRouter client
            client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=api_key
            )

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = client.chat.completions.create(
                        model=model,
                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "You are a helpful AI assistant. "
                                    "Answer clearly and explain concepts "
                                    "in simple language."
                                )
                            },
                            *st.session_state.messages
                        ]
                    )

                    answer = response.choices[0].message.content
                    answer = answer or "The model returned an empty response."
                    st.markdown(answer)

            # Save assistant response
            st.session_state.messages.append(
                {"role": "assistant", "content": answer}
            )

        except Exception as e:
            st.error(f"Something went wrong: {e}")
