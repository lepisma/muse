import os
import tempfile

import openai
import replicate
from PIL import Image


def image_to_description(image_data, replicate_api_token=None) -> str | None:
    """
    Convert image data to textual description.
    """

    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file_name = temp_file.name
        Image.fromarray(image_data).save(temp_file_name, "PNG")

    try:
        with open(temp_file_name, "rb") as fp:
            client = replicate.Client(api_token=replicate_api_token)
            return client.run(
                "salesforce/blip:2e1dddc8621f72155f24cf2e0adbde548458d3cab9f00c0139eea840d0ac4746",
                input={"image": fp}
            )
    except Exception:
        os.unlink(temp_file_name)
        return None


def description_to_songs(description: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": """
            You are getting a description of drawing made by someone via an
            image captioning model. You have to clean the description of
            sentences like 'drawing of', etc. and show that. Then you have to
            list 10 songs that follow the description. Return text properly
            formatted in markdown.

            Now, the image captioning descriptions will be provided by the
            user.
            """},
            {"role": "user", "content": description}
        ]
    )
    return response.choices[0]["message"].content
