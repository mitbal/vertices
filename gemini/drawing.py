import io
import pandas as pd
from PIL import Image
from PIL import Image as PIL_Image

import streamlit as st
from streamlit_drawable_canvas import st_canvas
from vertexai.preview.generative_models import GenerativeModel, Image

st.title('Pelukis Malam')

# Specify canvas parameters in application
drawing_mode = st.sidebar.selectbox(
    "Drawing tool:", ("freedraw", "point", "line", "rect", "circle", "transform")
)

stroke_width = st.sidebar.slider("Stroke width: ", 1, 25, 3)
if drawing_mode == 'point':
    point_display_radius = st.sidebar.slider("Point display radius: ", 1, 25, 3)
stroke_color = st.sidebar.color_picker("Stroke color hex: ")
bg_color = st.sidebar.color_picker("Background color hex: ", "#eee")
bg_image = st.sidebar.file_uploader("Background image:", type=["png", "jpg"])

realtime_update = st.sidebar.checkbox("Update in realtime", True)

# Create a canvas component
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    background_image=PIL_Image.open(bg_image) if bg_image else None,
    update_streamlit=realtime_update,
    height=360,
    drawing_mode=drawing_mode,
    point_display_radius=point_display_radius if drawing_mode == 'point' else 0,
    key="canvas",
)

input_prompt = st.text_input('put your input here', 'Read the text in this image')

if st.button('Run Gemini'):

    pil = PIL_Image.fromarray(canvas_result.image_data)
    img_bytes = io.BytesIO()
    pil.save(img_bytes, format='PNG')
    img_bytes_io = img_bytes.getvalue()
    # st.text(type(img_bytes_io))

    model = GenerativeModel(model_name='gemini-pro-vision')
    response = model.generate_content([input_prompt, Image.from_bytes(img_bytes_io)])

    st.text(response.text)
