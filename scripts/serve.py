"""
Usage:
  serve.py
"""

import streamlit as st
from docopt import docopt
from muse.models import description_to_songs, image_to_description
from streamlit_drawable_canvas import st_canvas

if __name__ == "__main__":
    args = docopt(__doc__, version="muse 0.1.0")

    st.title("_muse_")

    col1, col2, col3 = st.columns(3)

    with col1:
        drawing_mode = st.selectbox(
            "Drawing tool:", ("freedraw", "line", "rect", "circle", "transform")
        )

        stroke_width = st.slider("Stroke width: ", 1, 25, 3)

    with col2:
        stroke_color = st.color_picker("Stroke color hex: ")

    with col3:
        bg_color = st.color_picker("Background color hex: ", "#eee")

    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color=bg_color,
        height=500,
        drawing_mode=drawing_mode,
        point_display_radius=None,
        key="canvas"
    )

    if st.button("Generate"):
        if canvas_result.image_data is not None:
            description = image_to_description(canvas_result.image_data)

        st.markdown(description_to_songs(description))
