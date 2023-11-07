import base64
import tempfile

import openai
from PIL import Image


def b64_encode_image(image_data):
    # TODO: Fix this to and fro
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file_name = temp_file.name
        Image.fromarray(image_data).save(temp_file_name, "PNG")

    with open(temp_file_name, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def image_to_songs(image_data, openai_api_key=None) -> str:
    """
    Directly go from image to songs using GPT4 vision model.
    """

    if openai_api_key:
        old_key_value = openai.api_key
        openai.api_key = openai_api_key

    base64_image = b64_encode_image(image_data)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Here is a drawing made by someone. You have to list 10 songs that could be described by the drawing. First describe the drawing in words and then try listing songs around what you described. Return text properly formatted in markdown."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=1000
        )
    except Exception as e:
        if openai_api_key:
            openai.api_key = old_key_value
        raise e

    return response.choices[0]["message"].content
