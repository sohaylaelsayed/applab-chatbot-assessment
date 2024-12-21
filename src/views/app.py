import streamlit as st
import requests
import os

def main():
    st.title("Document Chatbot Assistant")
    st.write("Upload PDF document file and ask our Chatbot assistant.")

    # Tabs for File Upload and Chatbot
    tab1, tab2 = st.tabs(["Document Upload", "Chatbot"])

    # File Upload Tab
    with tab1:
        st.header("PDF Document Upload")
        uploaded_file = st.file_uploader("Choose a PDF document", type=["pdf"])

        if uploaded_file is not None:
            st.write("Document uploaded successfully:", uploaded_file.name)

            # Display a button to trigger upload
            if st.button("Upload and Process the target document"):
                st.write("Uploading ...")

                # Define API endpoint URL
                api_url = "http://127.0.0.1:8000/api/v1/data/upload"

                try:
                    # Stream the file to the backend
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    response = requests.post(api_url, files=files)

                    if response.status_code == 200:
                        st.success("Target document uploaded and processed successfully!")
                        # st.json(response.json())  # Display response JSON
                    else:
                        st.error(f"Failed to upload file: {response.status_code}")
                        st.write(response.text)
                except Exception as e:
                    st.error(f"An error occurred: {e}")

    with tab2:
        st.header("Chatbot")
        st.write("Ask questions to the chatbot assistant..")

        # Initialize session state to store chat history if it doesn't exist
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []

        user_query = st.text_input("Enter your query:", "")

        if st.button("Ask"):
            if user_query.strip():
                st.write("Processing query...")

                # Add the user's query to the chat history
                st.session_state.chat_history.append(f"You: {user_query}")

                # Define API endpoint URL for the chatbot
                chatbot_api_url = "http://127.0.0.1:8000/api/v1/nlp/index/search"

                try:
                    # Prepare payload for chatbot API
                    payload = {"text": user_query, "limit": 1}
                    response = requests.post(chatbot_api_url, json=payload)

                    if response.status_code == 200:
                        # Extract the relevant response text (from "results")
                        data = response.json()
                        chatbot_reply = data["results"][0] if "results" in data else "No relevant data found."

                        # Add the chatbot's response to the chat history
                        st.session_state.chat_history.append(f"Bot: {chatbot_reply}")

                        # Display success and the chatbot's response text
                        st.success("Query processed successfully!")
                    else:
                        st.error(f"Failed to process query: {response.status_code}")
                        st.write(response.text)
                except Exception as e:
                    st.error(f"An error occurred: {e}")
            else:
                st.warning("Please enter a query before sending.")

        # Display the chat history
        if st.session_state.chat_history:
            for message in st.session_state.chat_history:
                st.write(message)
                
if __name__ == "__main__":
    main()
