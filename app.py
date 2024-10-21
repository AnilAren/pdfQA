import streamlit as st 

# Importing the PDF QA service

st.title("Project Central Hub 😊")

def main():
    st.header("Select the Service You Need")
    
    selected_option = st.selectbox("Choose a Service:", [
        "Select a service",
        "PDF Question Answering (QA)",
        "ChatBot"
    ], index=0)


    if selected_option == "PDF Question Answering (QA)":
        from pdfqa import main as pdf_qa_main
        
        pdf_qa_main()  
    elif selected_option == "ChatBot":
        st.warning("This feature is still under construction. Please check back later! 😊")
    else:
        st.warning("Please select a service to proceed.")

if __name__ == '__main__':
    main()
