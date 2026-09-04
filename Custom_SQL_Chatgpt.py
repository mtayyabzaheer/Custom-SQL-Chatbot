
from sqlalchemy import label
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
import streamlit as st

# -----------------------------
# Streamlit Page Configuration
# -----------------------------
st.set_page_config(
    page_title="SQL Assistant",
    page_icon="🗄️"
)

st.header("SQL Assistant 🗄️")

# -----------------------------
# Get API Key from User
# -----------------------------
api_key = st.text_input(
    "Enter your OpenAI API Key",
    type="password",
    placeholder="sk-..."
)

# -----------------------------
# SQL Assistant System Prompt
# -----------------------------
system_message = """
You are an SQL Assistant.

Your purpose is to help users understand SQL and database concepts.

You can help with:
- Writing SQL queries
- Explaining SQL queries
- Debugging SQL queries
- SELECT, INSERT, UPDATE, and DELETE
- WHERE, ORDER BY, GROUP BY, and HAVING
- Aggregate functions such as COUNT, SUM, AVG, MIN, and MAX
- INNER JOIN, LEFT JOIN, RIGHT JOIN, and other common JOINs
- Subqueries
- Primary keys and foreign keys
- Database relationships
- Normalization
- Basic database design
- MySQL and PostgreSQL

When answering:
1. Explain concepts in simple language.
2. Provide SQL examples when useful.
3. Explain queries clearly.
4. If the user's SQL query contains an error, identify the problem and provide a corrected version.
5. Do not invent the user's database structure. If you need an example table, clearly state that it is an example.

If the user asks something unrelated to SQL or databases, respond:

"Sorry, I can only help with SQL and database-related questions."

Stay focused on SQL and database-related topics.
"""

# -----------------------------
# Initialize Chat History
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage(content=system_message)
    ]

# -----------------------------
# Create Chat Model
# -----------------------------
if api_key:

    chat = ChatOpenAI(
        model_name="gpt-4o",
        temperature=0.5,
        api_key=api_key
    )

    # -----------------------------
    # Display Previous Messages
    # -----------------------------
    for msg in st.session_state.messages:
        if isinstance(msg, HumanMessage):
            with st.chat_message("user"):
                st.write(msg.content)

        elif isinstance(msg, AIMessage):
            with st.chat_message("assistant"):
                st.write(msg.content)

    # -----------------------------
    # User Input
    # -----------------------------
    user_prompt = st.chat_input(
        "Ask me an SQL question..."
        )

    if user_prompt:

        # Add user message
        st.session_state.messages.append(
            HumanMessage(content=user_prompt)
        )

        # Display user message
        with st.chat_message("user"):
            st.write(user_prompt)

        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):

                try:
                    response = chat.invoke(
                        st.session_state.messages
                    )

                    st.write(response.content)

                    # Save response
                    st.session_state.messages.append(
                        AIMessage(content=response.content)
                    )

                except Exception as e:
                    st.error(
                        "Something went wrong. Please check your API key."
                    )

else:
    st.info(
        "Please enter your OpenAI API key above to start chatting."
    )
