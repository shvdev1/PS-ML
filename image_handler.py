import io
import os
from PIL import Image

from google.genai import types
from google.genai import Client
from google.genai.types import GenerateContentConfig

from utils import env_wrapper
from utils import img2part

from dotenv import load_dotenv
load_dotenv()



HTTP_PROXY = os.environ.get("HTTP_PROXY", None)
if HTTP_PROXY is None:
    raise ValueError("HTTP_PROXY environment variable is not set.")
API_KEY = os.environ.get("GEMINI_API_KEY", None)
if API_KEY is None:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")



def process_image(image_path: str, prompt: str):
    with env_wrapper(HTTP_PROXY, API_KEY) as session:
        
        client = Client(api_key = API_KEY)
        gen_config = types.GenerateContentConfig(
            temperature = 0,
            thinking_config=types.ThinkingConfig(
                thinking_budget = -1,
                include_thoughts = False,
            )
        )
        
        image = Image.open(image_path)
        image_part = img2part(image)
        
        response = client.models.generate_content(
            model = "gemini-2.5-flash",
            config = gen_config,
            contents = [image_part, prompt]
        )
        return response.candidates[0].content.parts[0].text 



if __name__ == "__main__":
    image_path = "test/img/image.png"
    prompt = "Describe the content of the image."
    result = process_image(image_path, prompt)
    print("Generated Output:", result)
