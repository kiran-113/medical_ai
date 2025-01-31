import streamlit as st
from pathlib import Path
import google.generativeai as genai
import os
from PIL import Image
import io

# Set page configuration at the very beginning
st.set_page_config(page_title="Diagnostic Analytics", page_icon=":microscope:", layout="wide")

# Configure the API key
api_key = os.getenv("GOOGLE_GEMINI_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_GEMINI_API_KEY not found in .env file. Please add it.")


# Configure the API
genai.configure(api_key=api_key)

# Prompt
system_prompt ="""
  You are an advanced AI medical image analysis system, specialized in
  Your responsibilities include:
  1. Detailed Image Examination:
  - Carefully analyze each medical image to detect potential abnormalities
  - Tumors (benign or malignant)
  - Fractures and bone abnormalities
  - Infections or inflammatory conditions
  - Organ enlargement or shrinkage
  - Vascular abnormalities
  - Pathological changes in soft tissues
  - Detect both subtle and significant changes, ensuring that even small abnormalities are identified for further review.

  2. Condition Detection:
  - Apply domain-specific knowledge to recognize conditions such as
  - Cardiovascular diseases
  - Respiratory conditions
  - Neurological disorders
  - Musculoskeletal issues
  - Tumor classification and staging
  - Utilize advanced imaging techniques like MRI, CT scans, and X-rays to provide accurate diagnostics.

  3. Collaboration with Healthcare Professionals:
  - Work alongside radiologists and physicians to deliver timely and accurate reports.
  - Assist in developing treatment plans based on the analysis and findings.

  4. Continuous Learning and Improvement:
  - Update algorithms and techniques using the latest research and technological advancements in medical imaging.
  - Participate in training sessions and workshops to refine analysis skills and stay current with medical imaging practices.

  5. Quality Assurance:
  - Ensure high sensitivity to guarantee no serious conditions are overlooked.
  - Maintain high specificity to reduce false positives and avoid unnecessary anxiety.
  - Ensure the analysis is consistent with current medical standards.

  6. Ethical Considerations:
  - Provide a neutral and unbiased assessment, ensuring fairness in diagnosis.
  - Make sure the diagnosis does not provide overly alarming results.

  7. AI Confidence Scoring:
  - Assign confidence levels to findings based on certainty and evidence.
  - Indicate areas requiring further human review.

  8. Comparative Analysis:
  - Compare with past medical images to detect progression or regression.
  - Highlight changes over time to aid in long-term diagnosis.

  9. Anomaly Detection:
  - Identify rare or unknown patterns requiring specialist attention.
  - Flag unusual cases for deeper investigation.

  10. Patient Report Generation:
  - Summarize findings in a human-readable medical report.
  - Provide actionable insights for doctors and patients.

  Your task is to assist healthcare professionals by delivering highly accurate and timely medical image analyses.
"""

# Apply button styling
st.markdown(
    """<style>
    .stButton>button {
        background-color: #008CBA;
        color: white;
        font-size: 16px;
        border-radius: 10px;
        padding: 10px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #005F73;
    }
    </style>""",
    unsafe_allow_html=True,
)

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

# Create columns
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.image("medical1.png", width=400)
    col_left, col_right = st.columns([1, 3])

    with col_left:
        st.image("growup.png", width=200)

    with col_right:
        st.markdown('<h1 style="color: blue;">Medical Diagnostic Analytics</h1>', unsafe_allow_html=True)
        st.write("AI-powered medical image analysis system. Upload an image or take a picture to get started.")

# File uploader button only
uploaded_file = st.file_uploader("Browse files", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

if st.button("Open Camera"):
    camera_image = st.camera_input("Click to take a picture for analysis")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file or 'camera_image' in locals():
    image_source = uploaded_file if uploaded_file else camera_image

    if image_source is not None:  # Ensure image_source is not None
        image_data = image_source.getvalue()
        image = Image.open(io.BytesIO(image_data))
        st.image(image, caption="Selected Image", use_container_width=True)

        if st.button("Submit for Analysis"):
            image_bytes = io.BytesIO()
            image.save(image_bytes, format='JPEG')
            image_bytes.seek(0)
            image_dict = {"mime_type": image_source.type, "data": image_bytes.read()}

            model = genai.GenerativeModel(model_name="gemini-1.5-flash", generation_config=generation_config, safety_settings=safety_settings)
            response = model.generate_content([system_prompt, image_dict])
            st.write(response.text)
    else:
        st.warning("Please upload a file or take a picture before submitting.")
else:
    st.info("Please upload an image or use the camera to take a photo for analysis.")

