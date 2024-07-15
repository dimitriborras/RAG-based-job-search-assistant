import streamlit as st
from generator import generate_documents
import gspread
from google.oauth2.service_account import Credentials
from google.oauth2 import service_account
import toml

def show_sidebar_content(tab):
    if tab == "Generator":
        # Sidebar content for Generator tab
        st.sidebar.title("API Settings")
        ai_provider_toggle = st.sidebar.radio("Select AI Provider", ("Anthropic 🦜", "OpenAI 🤖"), key="ai_provider_toggle")
        ai_provider = ai_provider_toggle.split()[0]
        api_key = st.sidebar.text_input("Enter your API key:", type="password")

        if not api_key:
            st.sidebar.error("🚨 Please enter a valid API key to use the app.")
            st.stop()

        st.sidebar.warning("⚠️ Heads up: make sure you have a valid API key from either provider and sufficient funds in your account. Otherwise, the app won't work.")

        st.sidebar.subheader("Additional Settings 🔧")
        formality_level = st.sidebar.select_slider("Formality Level for cover letter and email 📝", ["Super Casual", "Casual", "Neutral", "Formal", "Super Formal"], value="Neutral", key="formality_level")
        additional_info = st.sidebar.text_area("Additional Information 💡", height=100, placeholder="Anything else you want the AI to consider or focus on?", key="additional_info")


        st.sidebar.subheader("How to Use 🤖")
        with st.sidebar.expander("Click here to see a quick guide!"):
            st.markdown("""
            - 📝 Copy and paste your resume
            - 📋 Copy and paste the job description you're applying for
            - 🙋‍♂️ Provide a brief bio/intro about yourself
            - 🔧 Pick the formality level for the cover letter and email (default works well for most cases)
            - 💡 Add any additional information you want the AI to consider (optional)
            - 🚀 Click the "Generate Documents" button and let the magic happen!✨
            """)
        # Feedback section common to all tabs
        st.sidebar.subheader("Got Feedback or features you'd find useful? 📮")
        with st.sidebar.form(key='feedback_form'):
            feedback = st.sidebar.text_area("Share your thoughts with me here:", key="feedback")
            submit_feedback = st.form_submit_button(label='Submit Feedback 🙌')
            if submit_feedback:
                # Set up the Google Sheets API using TOML secrets
                try:
                    secrets = {
                    "type": st.secrets["type"],
                    "project_id": st.secrets["project_id"],
                    "private_key_id": st.secrets["private_key_id"],
                    "private_key": st.secrets["private_key"],
                    "client_email": st.secrets["client_email"],
                    "client_id": st.secrets["client_id"],
                    "auth_uri": st.secrets["auth_uri"],
                    "token_uri": st.secrets["token_uri"],
                    "auth_provider_x509_cert_url": st.secrets["auth_provider_x509_cert_url"],
                    "client_x509_cert_url": st.secrets["client_x509_cert_url"],
                    "universe_domain": st.secrets["universe_domain"]
                    }
                    creds = service_account.Credentials.from_service_account_info(
                        secrets,
                        scopes=['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
                    )
                    client = gspread.authorize(creds)
                    # Open the Google Sheet and append the feedback
                    sh = client.open('prototype_feedback').worksheet('Feedback')
                    sh.append_row([feedback])
                    st.sidebar.success("Thanks for your feedback! 🙏")
                except Exception as e:
                    st.sidebar.error(f"Error: {e}")

    elif tab == "Job Explorer":
        # Sidebar content for Job Explorer tab
        st.sidebar.subheader("Job Explorer Settings")
        st.sidebar.text_input("test setting 1", key="job_explorer_setting_1")
        st.sidebar.text_area("test setting 2", key="job_explorer_setting_2")

    elif tab == "Personal Branding Advisor":
        # Sidebar content for Personal Branding Advisor tab
        st.sidebar.subheader("Personal Branding Advisor Settings")
        st.sidebar.text_input("Linkedin profile to analyze", key="advisor_setting_1")
        st.sidebar.text_area("Your job preferences and context", key="advisor_setting_2")

def main():
    st.set_page_config(page_title='JobExp.ai', page_icon='🤖')
    st.title("AI Job Application Assistant")

    # Define tabs
    tabs = st.tabs(["Generator", "Job Explorer", "Personal Branding Advisor"])

    # Display sidebar content based on the selected tab
    if "selected_tab" not in st.session_state:
        st.session_state.selected_tab = "Generator"

    #add the sidebar content here because I dont know how to manage sidebar dynamically according to the selected tab so I need to retrieve variable value like api_key
    with tabs[0]:
        st.session_state.selected_tab = "Generator"
        # Sidebar content for Generator tab
        st.sidebar.title("API Settings")
        ai_provider_toggle = st.sidebar.radio("Select AI Provider", ("Anthropic 🦜", "OpenAI 🤖"), key="ai_provider_toggle")
        ai_provider = ai_provider_toggle.split()[0]
        api_key = st.sidebar.text_input("Enter your API key:", type="password")

        if not api_key:
            st.sidebar.error("🚨 Please enter a valid API key to use the app.")
            st.stop()

        st.sidebar.warning("⚠️ Heads up: make sure you have a valid API key from either provider and sufficient funds in your account. Otherwise, the app won't work.")

        st.sidebar.subheader("Additional Settings 🔧")
        formality_level = st.sidebar.select_slider("Formality Level for cover letter and email 📝", ["Super Casual", "Casual", "Neutral", "Formal", "Super Formal"], value="Neutral", key="formality_level")
        additional_info = st.sidebar.text_area("Additional Information 💡", height=100, placeholder="Anything else you want the AI to consider or focus on?", key="additional_info")
        st.header("Generate Documents")
        # User inputs
        st.subheader("Paste your resume here 📝")
        resume = st.text_area("", height=200, placeholder="Your resume goes here...")

        st.subheader("Paste the job description here 📋")
        job_description = st.text_area("", height=200, placeholder="The job description goes here...")

        st.subheader("Paste your bio/brief intro here 🙋‍♂️")
        bio = st.text_area("", height=100, placeholder="Your bio or brief intro goes here. For example, you can add your LinkedIn summary or a short introduction about yourself.")

        # Define the output section titles
        output_section_titles = {
            "Tailored Resume": "TAILORED RESUME",
            "Tailored Cover Letter": "TAILORED COVER LETTER",
            "Customized Cold Email": "CUSTOMIZED COLD EMAIL"
        }

        if st.button("✨ Generate Docs"):
            # Show loader while generating documents
            with st.spinner("🤖AI is cooking up the docs to help with your application, just a few secs! 👨‍🍳"):
                # Generate outputs
                outputs = generate_documents(resume, job_description, bio, api_key, ai_provider, formality_level, additional_info)

            if outputs:
                for section_title, section_key in output_section_titles.items():
                    if section_key in outputs and outputs[section_key].strip():
                        st.subheader(section_title)
                        st.code(outputs[section_key], language="text")

    with tabs[1]:
        st.session_state.selected_tab = "Job Explorer"
        show_sidebar_content("Job Explorer")
        st.header("Job Explorer")
        st.write("This is where you can add Job Explorers for your app.")
         # User inputs
        st.subheader("Paste your resume here or drag and drop it 📝")
        resume_explorer = st.text_area("", height=200, placeholder="Your resume goes here..")

        st.subheader("Here goes your query to find your job or generate anything about it 📋")
        query_explorer = st.text_area("", height=200, placeholder="Your query...")

    with tabs[2]:
        st.session_state.selected_tab = "Personal Branding Advisor"
        show_sidebar_content("Personal Branding Advisor")
        st.header("Personal Branding Advisor")
        st.write("This is where you can add Personal Branding Advisor-related features for your app.")
         # User inputs
        st.subheader("Best recommandations for your linkedin profile 📝")      


if __name__ == "__main__":
    main()
