import streamlit as st
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai
import os
from PIL import Image
import io

# Load environment variables from .env file
load_dotenv()

# Configure the API key
api_key = os.getenv("GOOGLE_GEMINI_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_GEMINI_API_KEY not found in .env file. Please add it.")

# Configure the API
genai.configure(api_key=api_key)

# Prompt
system_prompt = """
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

  Your task is to assist healthcare professionals by delivering highly accurate and timely medical image analyses.
"""

geenaraton_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Safety settings
safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
]

# Layout
st.set_page_config(page_title="Diagnostic Analytics", page_icon=":microscope:", layout="wide")

# Create columns
col1, col2, col3 = st.columns([1, 2, 1])

# Center the second image in the center column
with col2:
    st.image("medical1.png", width=400)
    col_left, col_right = st.columns([1, 3])

    with col_left:
        st.image("growup.png", width=200)

    with col_right:
        st.markdown('<h1 style="color: blue;">Medical Diagnostic Analytics</h1>', unsafe_allow_html=True)
        st.write("AI-powered medical image analysis system. Upload an image or take a picture to get started.")

# Add camera input
camera_image = st.camera_input("Click to take a picture for analysis")

if camera_image is not None:
    # Process the captured image
    image_data = camera_image.getvalue()

    # Convert byte data to an image
    image = Image.open(io.BytesIO(image_data))

    # Convert the image back to bytes in JPEG format
    image_bytes = io.BytesIO()
    image.save(image_bytes, format='JPEG')
    image_bytes.seek(0)
    image_dict = {
        "mime_type": camera_image.type,
        "data": image_bytes.read()
    }

    # Generate response based on the captured image
    response = model.generate_content([system_prompt, image_dict])
    st.write(response.text)

    # Display the captured image after analysis
    st.image(image, caption="Captured Image for Analysis", use_column_width=True)

# Add file uploader
uploaded_file = st.file_uploader("Or upload medical images for analysis", type=["jpg", "jpeg", "png"])
submit_button = st.button("Generate image analysis from uploaded file")

# Create a Gemini model
model = genai.GenerativeModel(model_name="gemini-1.5-flash", generation_config=geenaraton_config, safety_settings=safety_settings)

if submit_button:
    if uploaded_file is not None:
        # Process the uploaded image
        image_data = uploaded_file.getvalue()

        # Convert byte data to an image
        image = Image.open(io.BytesIO(image_data))

        # Convert the image back to bytes in JPEG format
        image_bytes = io.BytesIO()
        image.save(image_bytes, format='JPEG')
        image_bytes.seek(0)
        image_dict = {
            "mime_type": uploaded_file.type,
            "data": image_bytes.read()
        }

        # Generate response for the uploaded image
        response = model.generate_content([system_prompt, image_dict])
        st.write(response.text)

        # Display the uploaded image
        st.image(image, caption="Uploaded Image", use_column_width=True)
    else:
        st.warning("Please upload an image or take a picture before submitting.")



# import streamlit as st
# from pathlib import Path
# from dotenv import load_dotenv
# import google.generativeai as genai
# import os
# from PIL import Image
# import io

# # Load environment variables from .env file
# load_dotenv()

# # Configure the API key
# api_key = os.getenv("GOOGLE_GEMINI_API_KEY")
# if not api_key:
#     raise ValueError("GOOGLE_GEMINI_API_KEY not found in .env file. Please add it.")

# # Configure the API
# genai.configure(api_key=api_key)

# # Prompt
# system_prompt = """
#   You are an advanced AI medical image analysis system, specialized in
#   Your responsibilities include:
#   1. Detailed Image Examination:
#   - Carefully analyze each medical image to detect potential abnormalities
#   - Tumors (benign or malignant)
#   - Fractures and bone abnormalities
#   - Infections or inflammatory conditions
#   - Organ enlargement or shrinkage
#   - Vascular abnormalities
#   - Pathological changes in soft tissues
#   - Detect both subtle and significant changes, ensuring that even small abnormalities are identified for further review.

#   2. Condition Detection:
#   - Apply domain-specific knowledge to recognize conditions such as
#   - Cardiovascular diseases
#   - Respiratory conditions
#   - Neurological disorders
#   - Musculoskeletal issues
#   - Tumor classification and staging
#   - Utilize advanced imaging techniques like MRI, CT scans, and X-rays to provide accurate diagnostics.

#   3. Collaboration with Healthcare Professionals:
#   - Work alongside radiologists and physicians to deliver timely and accurate reports.
#   - Assist in developing treatment plans based on the analysis and findings.

#   4. Continuous Learning and Improvement:
#   - Update algorithms and techniques using the latest research and technological advancements in medical imaging.
#   - Participate in training sessions and workshops to refine analysis skills and stay current with medical imaging practices.

#   5. Quality Assurance:
#   - Ensure high sensitivity to guarantee no serious conditions are overlooked.
#   - Maintain high specificity to reduce false positives and avoid unnecessary anxiety.
#   - Ensure the analysis is consistent with current medical standards.

#   6. Ethical Considerations:
#   - Provide a neutral and unbiased assessment, ensuring fairness in diagnosis.
#   - Make sure the diagnosis does not provide overly alarming results.

#   Your task is to assist healthcare professionals by delivering highly accurate and timely medical image analyses.
# """

# geenaraton_config = {
#     "temperature": 1,
#     "top_p": 0.95,
#     "top_k": 40,
#     "max_output_tokens": 8192,
#     "response_mime_type": "text/plain",
# }

# # Safety settings
# safety_settings = [
#     {
#         "category": "HARM_CATEGORY_HARASSMENT",
#         "threshold": "BLOCK_MEDIUM_AND_ABOVE",
#     },
#     {
#         "category": "HARM_CATEGORY_HATE_SPEECH",
#         "threshold": "BLOCK_MEDIUM_AND_ABOVE",
#     },
#     {
#         "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
#         "threshold": "BLOCK_MEDIUM_AND_ABOVE",
#     },
#     {
#         "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
#         "threshold": "BLOCK_MEDIUM_AND_ABOVE",
#     },
# ]

# # Layout
# st.set_page_config(page_title="Diagnostic Analytics", page_icon=":microscope:", layout="wide")

# # Create columns
# col1, col2, col3 = st.columns([1, 2, 1])

# # Center the second image in the center column
# with col2:
#     st.image("medical1.png", width=400)
#     col_left, col_right = st.columns([1, 3])

#     with col_left:
#         st.image("growup.png", width=200)

#     with col_right:
#         st.markdown('<h1 style="color: blue;">Medical Diagnostic Analysis</h1>', unsafe_allow_html=True)
#         st.write("AI-powered medical image analysis system. Upload an image to get started.")

# # Add camera input
# camera_image = st.camera_input("Take a picture for analysis")

# # Add file uploader
# uploaded_file = st.file_uploader("Or upload medical images for analysis", type=["jpg", "jpeg", "png"])
# submit_button = st.button("Generate image analysis")

# # Create a Gemini model
# model = genai.GenerativeModel(model_name="gemini-1.5-flash", generation_config=geenaraton_config, safety_settings=safety_settings)

# if submit_button:
#     # Check if an image is taken from the camera
#     if camera_image is not None:
#         # Process the camera image
#         image_data = camera_image.getvalue()

#         # Convert byte data to an image
#         image = Image.open(io.BytesIO(image_data))

#         # Convert the image back to bytes in JPEG format
#         image_bytes = io.BytesIO()
#         image.save(image_bytes, format='JPEG')
#         image_bytes.seek(0)
#         image_dict = {
#             "mime_type": camera_image.type,
#             "data": image_bytes.read()
#         }

#         # Generate response for the camera image
#         response = model.generate_content([system_prompt, image_dict])
#         st.write(response.text)

#         # Display the captured image
#         st.image(image, caption="Captured Image", use_container_width=True, width=100)

#     # Check if a file is uploaded
#     elif uploaded_file is not None:
#         # Process the uploaded image
#         image_data = uploaded_file.getvalue()

#         # Convert byte data to an image
#         image = Image.open(io.BytesIO(image_data))

#         # Convert the image back to bytes in JPEG format
#         image_bytes = io.BytesIO()
#         image.save(image_bytes, format='JPEG')
#         image_bytes.seek(0)
#         image_dict = {
#             "mime_type": uploaded_file.type,
#             "data": image_bytes.read()
#         }

#         # Generate response for the uploaded image
#         response = model.generate_content([system_prompt, image_dict])
#         st.write(response.text)

#         # Display the uploaded image
#         st.image(image, caption="Uploaded Image", use_container_width=True, width=300)
#     else:
#         st.warning("Please upload an image or take a picture before submitting.")


# # import streamlit as st
# # from pathlib import Path
# # from dotenv import load_dotenv
# # import google.generativeai as genai
# # import os
# # from PIL import Image
# # import io

# # # Load environment variables from .env file
# # load_dotenv()

# # # Configure the API key
# # api_key = os.getenv("GOOGLE_GEMINI_API_KEY")
# # if not api_key:
# #     raise ValueError("GOOGLE_GEMINI_API_KEY not found in .env file. Please add it.")

# # # Configure the API
# # genai.configure(api_key=api_key)

# # # Prompt
# # system_prompt = """
# #   You are an advanced AI medical image analysis system, specialized in
# #   Your responsibilities include:
# #   1. Detailed Image Examination:
# #   - Carefully analyze each medical image to detect potential abnormalities
# #   - Tumors (benign or malignant)
# #   - Fractures and bone abnormalities
# #   - Infections or inflammatory conditions
# #   - Organ enlargement or shrinkage
# #   - Vascular abnormalities
# #   - Pathological changes in soft tissues
# #   - Detect both subtle and significant changes, ensuring that even small abnormalities are identified for further review.

# #   2. Condition Detection:
# #   - Apply domain-specific knowledge to recognize conditions such as
# #   - Cardiovascular diseases
# #   - Respiratory conditions
# #   - Neurological disorders
# #   - Musculoskeletal issues
# #   - Tumor classification and staging
# #   - Utilize advanced imaging techniques like MRI, CT scans, and X-rays to provide accurate diagnostics.

# #   3. Collaboration with Healthcare Professionals:
# #   - Work alongside radiologists and physicians to deliver timely and accurate reports.
# #   - Assist in developing treatment plans based on the analysis and findings.

# #   4. Continuous Learning and Improvement:
# #   - Update algorithms and techniques using the latest research and technological advancements in medical imaging.
# #   - Participate in training sessions and workshops to refine analysis skills and stay current with medical imaging practices.

# #   5. Quality Assurance:
# #   - Ensure high sensitivity to guarantee no serious conditions are overlooked.
# #   - Maintain high specificity to reduce false positives and avoid unnecessary anxiety.
# #   - Ensure the analysis is consistent with current medical standards.

# #   6. Ethical Considerations:
# #   - Provide a neutral and unbiased assessment, ensuring fairness in diagnosis.
# #   - Make sure the diagnosis does not provide overly alarming results.

# #   Your task is to assist healthcare professionals by delivering highly accurate and timely medical image analyses.
# # """

# # geenaraton_config = {
# #     "temperature": 1,  # temperature controls the randomness of the output
# #     "top_p": 0.95,  # top p uses nucleus sampling selecting tokens from top 25% of the cumulative probability distribution
# #     "top_k": 40,  # selects the top 40 tokens from the probability distribution
# #     "max_output_tokens": 8192,  # max_output_tokens specifies the maximum number of tokens in the output
# #     "response_mime_type": "text/plain",  # response_mime_type specifies the format of the response
# # }

# # # Safety settings
# # safety_settings = [
# #     {
# #         "category": "HARM_CATEGORY_HARASSMENT",
# #         "threshold": "BLOCK_MEDIUM_AND_ABOVE",
# #     },
# #     {
# #         "category": "HARM_CATEGORY_HATE_SPEECH",
# #         "threshold": "BLOCK_MEDIUM_AND_ABOVE",
# #     },
# #     {
# #         "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
# #         "threshold": "BLOCK_MEDIUM_AND_ABOVE",
# #     },
# #     {
# #         "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
# #         "threshold": "BLOCK_MEDIUM_AND_ABOVE",
# #     },
# # ]

# # # Layout
# # st.set_page_config(page_title="Diagnostic Analytics", page_icon=":microscope:", layout="wide")

# # # Create columns
# # col1, col2, col3 = st.columns([1, 2, 1])

# # # Center the second image in the center column
# # with col2:
# #     st.image("medical1.png", width=400)
# #     # Create a two-column layout for the logo and title
# #     col_left, col_right = st.columns([1, 3])  # Adjust column sizes as needed

# #     # Add logo in the left column
# #     with col_left:
# #         st.image("growup.png", width=200)  # Adjust path and width as necessary

# #     # Add title and description in the right column
# #     with col_right:
# #         st.markdown('<h1 style="color: blue;">Medical Diagnostic Analytics</h1>', unsafe_allow_html=True)
# #         st.write("AI-powered medical image analysis system. Upload an image to get started.")


# # uploaded_file = st.file_uploader("Please upload the medical images for analysis", type=["jpg", "jpeg", "png"])
# # submit_button = st.button("Generate image analysis")

# # # Create a Gemini model
# # model = genai.GenerativeModel(model_name="gemini-1.5-flash", generation_config=geenaraton_config, safety_settings=safety_settings)

# # if submit_button:
# #     if uploaded_file is not None:
# #         # Process the image
# #         image_data = uploaded_file.getvalue()

# #         # Convert byte data to an image
# #         image = Image.open(io.BytesIO(image_data))

# #         # Convert the image back to bytes in JPEG format
# #         image_bytes = io.BytesIO()
# #         image.save(image_bytes, format='JPEG')  # Ensure the image is stored as JPEG
# #         image_bytes.seek(0)  # Rewind the BytesIO object
# #         image_dict = {
# #             "mime_type": uploaded_file.type,  # Mime type of the uploaded file
# #             "data": image_bytes.read()  # Use bytes read from the BytesIO object
# #         }

# #         # Making our prompt ready
# #         prompt_parts = [
# #             system_prompt,
# #             image_dict,  # Use the image dictionary here
# #             "describe the image in detail",
# #             system_prompt,
# #         ]

# #         # Generate a response based on the prompt and image
# #         response = model.generate_content(prompt_parts)
# #         print(response.text)

# #         st.write(response.text)

# #         # Display the uploaded image with specified width
# #         st.image(image, caption="Uploaded Image", use_container_width=True, width=300)  # Set width as desired

# #         # Generate content using the model again, if needed
# #         response = model.generate_content([system_prompt, image_dict])

# #         # Display the generated content
# #         st.write(response.text)
# #     else:
# #         st.warning("Please upload an image before submitting.")
