import streamlit as st

st.title(":material/chat: Meet the Chat Elements")

# 1. Displaying Static Messages
with st.chat_message("user"):
    st.write("Hello! Can you explain what Streamlit is?")

with st.chat_message("assistant"):
    st.write("Streamlit is an open-source Python framework for building data apps.")
    st.bar_chart([10, 20, 30, 40]) # You can even put charts inside chat messages!

with st.chat_message("user"):
    st.write("Let's introduce all the participants...")
for item in ('user','assistant','ai','human', 'person', 'persona'):
    with st.chat_message(item):
        st.write(f"I'm a/an {item}")

with st.chat_message("human", avatar = ':material/emoji_people:' ):
    st.write("I'm a human people")

# 2. Chat Input
prompt = st.chat_input("Type a message here...")

# 3. Reacting to Input
if prompt:
    # Display the user's new message
    with st.chat_message("user"):
        st.write(prompt)
    
    # Display a mock assistant response
    with st.chat_message("assistant"):
        st.write(f"You just said:\n\n '{prompt}' \n\n(I don't have memory yet!)")