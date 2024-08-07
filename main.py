import streamlit as st
import os

from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
import google.generativeai as genai
from streamlit_option_menu import option_menu

# Load environment variables
load_dotenv()
genai.configure(api_key=st.secrets("API_KEY"))

# Set up Streamlit page configuration
st.set_page_config(page_title="LabelLens", page_icon='🔎')

page_bg = """
<style>
[data-testid='stAppViewContainer'] {
    background-image: url("https://images.pexels.com/photos/18069157/pexels-photo-18069157/free-photo-of-an-artist-s-illustration-of-artificial-intelligence-ai-this-image-depicts-the-process-used-by-text-to-image-diffusion-models-it-was-created-by-linus-zoll-as-part-of-the-visualising-ai.png?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1");
    background-size: cover;
}
[data-testid="stHeader"] {
background-color: rgba(0,0,0,0);
}
</style>
"""

# Apply the styling using st.markdown
#st.markdown(page_bg, unsafe_allow_html=True)

# Initialize session state
if 'img_history' not in st.session_state:
    st.session_state['img_history'] = []
if 'img_srchistory' not in st.session_state:
    st.session_state['img_srchistory'] = []

# Sidebar menu for navigation
selected = option_menu(
    menu_title=None,
    options=["HOME", "LENS LABEL", "CHAT HISTORY", "CREDITS"],
    icons=['house', 'search', 'chat', 'person'],
    default_index=0,
    menu_icon='cast',
    orientation="horizontal",
    styles="""
    <style>
        .option-menu {
            width: 200px; /* Set the desired width */
            margin-right: 20px; /* Set the desired spacing */
        }
    </style>
    """
)

prompt_template = """
You are an expert in nutrition and health assessment. I will provide you with an image that contains labels of various food items. Your task is to analyze the image based on these labels and provide the following:
1. **Health Score**: Provide a health score for the food items based on common nutritional guidelines. You can use a scale from 0 to 100, where 0 is extremely unhealthy and 100 is very healthy. Explain the basis of the score in terms of nutritional value, calorie content, and any other relevant factors.
2. **Recommendation**: Based on the health score, give a recommendation on whether the food items in the image are advisable to eat or not. Provide a brief explanation for your recommendation, considering aspects like overall health impact, potential benefits, and risks.
---
**Image**: [Insert the image here]
**Labels in the Image**: [List the labels or describe the contents of the image here]
---
Please provide a detailed response including the health score and recommendation, along with the rationale behind your evaluation.
"""

def vscontent(input_text, image):
    """Generate content using the vision model."""
    response = vision_model.generate_content([input_text, image], stream=True)
    return response

def imageinlocals(image, key):
    if 'image' in locals():
        try:
            input_text = st.chat_input("Shoot questions to start getting information about the label", key=key)
            if input_text:
                response = vscontent(input_text + prompt_template, image)
                response.resolve()

                # Append to history
                st.session_state['img_history'].append(("YOU", input_text))
                st.session_state['img_history'].append(("IMAGE_BOT", response.text))

                st.balloons()
                st.markdown(f"**Generated text:** {response.text}")

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

        st.warning("THE CHAT HISTORY WILL BE LOST ONCE THE SESSION EXPIRES")

if selected == "HOME":
    

    st.markdown("""# <span style='color:#FFFFFF'>Welcome to My Streamlit App *Lens Label 🍏🔎*</span>""", unsafe_allow_html=True)

    st.markdown("""### <span style='color:lightblue'>Powered by Gemini-PRO LLM API from Google</span>""", unsafe_allow_html=True)

    st.markdown("""## <span style='color:orange'>Introduction</span>""", unsafe_allow_html=True)

    st.markdown(""" > ##### <span style='color:lightgreen'>Lens Label is designed to help you make healthier food choices by providing detailed health scores for scanned food labels.</span>""", unsafe_allow_html=True)

    st.markdown("""## <span style='color:#FFF5EE'>What is Lens Label?</span>""", unsafe_allow_html=True)

    st.markdown("""
    <div style='font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif; font-size: 18px;'>
        Lens Label is your personal health assistant in the grocery aisle! 🍏
        <br>
        📲 Simply scan the food labels of products, and Lens Label will analyze the nutritional information.
        <br>
        🏷️ It provides a health score, helping you understand the nutritional value and make informed choices.
        <br>
        🚀 With features like detailed ingredient analysis and comparison, it ensures you pick the healthiest options available.
        <br>
        💼 Keep track of your scanned items and maintain a healthy diet effortlessly. 🌟
        <br>
        
    </div>
    """, unsafe_allow_html=True)

    st.header(" ")
    st.success("Navigate to the LensLabel tab for detailed insights.")

    

if selected == "LENS LABEL":
    vision_model = genai.GenerativeModel('gemini-1.5-flash')


    with st.expander("Scan FOOD LABELS"):
          st.markdown("""## <span style='color:#FFF5EE'>Scan Food Labels</span>""", unsafe_allow_html=True)
          st.markdown("""
            <div style='font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif; font-size: 18px;'>
                Lens Label offers multiple ways to scan food labels:
                <br>
                1. 📁 Upload an Image: Upload a picture of the food label directly from your device.
                <br>
                2. 🌐 Enter a URL: Provide a URL of the food label image for analysis.
                <br>
                3. 📸 Use Camera: Take a live picture of the food label using your device's camera.
                <br>
               
            </div>
            """, unsafe_allow_html=True)
          


    with st.container():
        st.header("")
        st.header("")
          # Option to choose between file upload, URL input, and camera capture
        tab1, tab2, tab3 = st.tabs(["Upload an Image", "Enter Image URL", "USE CAMERA"])

        with tab1:
            st.header("Upload Image")
            st.header("")
            uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

            if uploaded_file:
                try:
                    # Convert uploaded file to PIL Image
                    image = Image.open(uploaded_file)
                    st.image(image, caption='Uploaded Image', use_column_width=True)
                    st.session_state['img_srchistory'].append(("SOURCE", "Uploaded Image"))
                    imageinlocals(image, key="upload")
                except Exception as e:
                    st.error(f"Error loading uploaded image: {str(e)}")

        with tab2:
            st.header("Provide Image URL")
            st.header("")
            try:
                image_url = st.text_input("Enter Image URL:", key="image_url_input")
            except Exception as e:
                st.error(f"Error loading image URL input: {str(e)}")
            if image_url:
                try:
                    response = requests.get(image_url)
                    if response.status_code == 200:
                        # Convert image URL to PIL Image
                        image = Image.open(BytesIO(response.content))
                        st.image(image, caption='Image from URL', use_column_width=True)
                        st.session_state['img_srchistory'].append(("SOURCE", "Image URL"))
                        imageinlocals(image, key="url")
                    else:
                        st.error(f"Failed to retrieve image from URL. Status code: {response.status_code}")
                except Exception as e:
                    st.error(f"Error loading image from URL: {str(e)}")

        with tab3:
            st.title("Webcam Image Capture")
            st.header("")
            captured_image = st.camera_input("Capture an image:", key="camera_input")
            if captured_image:
                try:
                    # Convert the captured image to PIL Image
                    image = Image.open(captured_image)
                    st.image(image, caption='Captured Image', use_column_width=True)

                    # Update image search history
                    st.session_state['img_srchistory'].append(("CAMERA", "Captured Image"))
                    imageinlocals(image, key="camera")
                except Exception as e:
                    st.error(f"Error processing captured image: {str(e)}")         
          
          


if selected == "CHAT HISTORY":
    if st.button("Show Image Chat History", use_container_width=True):
        # Define history sections and their corresponding emojis
        history_sections = [
            ('img_history', "Image Chat History:", "🤖"),
            ('img_srchistory', "Image Source History:", "📸")
        ]

        for history_type, header_text, emoji in history_sections:
            history = st.session_state.get(history_type, [])

            if history:
                st.subheader(header_text)
                # Use a set to track seen entries and avoid redundancy
                seen_entries = set()

                for role, text in history:
                    entry_id = (role, text)
                    if entry_id not in seen_entries:
                        role_prefix = emoji if role in ["YOU", "SOURCE"] else "🤖"
                        st.markdown(f"**{role} {role_prefix}**: {text}")
                        seen_entries.add(entry_id)
            else:
                st.error(f"{header_text} is empty. Start interacting to build the history.")


if selected == 'CREDITS':
    
            st.balloons()
            st.title("CRAFTED BY :")
            st.subheader("AMARNATH SILIVERI")

        # Define your styles
            st.markdown("""
        <style>
        .social-icons {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 20px;
        }

        .social-icon {
            text-align: center;
        }
        </style>
        """, unsafe_allow_html=True)

        # Create a container for social icons
            st.markdown("""
        <div class="social-icons">
        <div class="social-icon">
            <a href="https://www.github.com/SilverStark18" target="_blank" rel="noreferrer">
            <img src="https://raw.githubusercontent.com/danielcranney/readme-generator/main/public/icons/socials/github.svg" width="32" height="32" alt="GitHub" />
            </a>
            <p>GitHub</p>
        </div>

        <div class="social-icon">
            <a href="http://www.instagram.com/itz..amar." target="_blank" rel="noreferrer">
            <img src="https://raw.githubusercontent.com/danielcranney/readme-generator/main/public/icons/socials/instagram.svg" width="32" height="32" alt="Instagram" />
            </a>
            <p>Instagram</p>
        </div>

        <div class="social-icon">
            <a href="http://www.linkedin.com/in/amarnath-siliveri18" target="_blank" rel="noreferrer">
            <img src="https://raw.githubusercontent.com/danielcranney/readme-generator/main/public/icons/socials/linkedin.svg" width="32" height="32" alt="LinkedIn" />
            </a>
            <p>LinkedIn</p>
        </div>

        <div class="social-icon">
            <a href="https://medium.com/@amartalks25603" target="_blank" rel="noreferrer">
            <img src="https://raw.githubusercontent.com/danielcranney/readme-generator/main/public/icons/socials/medium.svg" width="32" height="32" alt="Medium" />
            </a>
            <p>Medium</p>
        </div>

        <div class="social-icon">
            <a href="https://www.x.com/Amarsiliveri" target="_blank" rel="noreferrer">
            <img src="https://raw.githubusercontent.com/danielcranney/readme-generator/main/public/icons/socials/twitter.svg" width="32" height="32" alt="Twitter" />
            </a>
            <p>Twitter</p>
        </div>

        <div class="social-icon">
            <a href="https://www.threads.net/@itz..amar." target="_blank" rel="noreferrer">
            <img src="https://raw.githubusercontent.com/danielcranney/readme-generator/main/public/icons/socials/threads.svg" width="32" height="32" alt="Threads" />
            </a>
            <p>Threads</p>
        </div>
        </div>
        """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.success(" Stay in the loop and level up your knowledge with every follow! ")
            st.success("Do you see icons , click to follow  on SOCIAL")

