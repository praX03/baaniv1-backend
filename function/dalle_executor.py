import openai
import os
from dotenv import load_dotenv
load_dotenv()
client=openai

def generate_image(prompt, size="1024x1024"):
    image_paths = []
    image_count = 0
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size=size,
        n=1,
        quality="standard",
    )
    # path = os.path.join("./dalle", str(round(time.time() * 1000)) + ".png")
    image_url = response.data[0].url
    # Image.open(requests.get(image_url, stream=True).raw).save(path)
    image_paths.append(image_url)
    print(image_url)
    image_count += 1
    return image_paths[-1]
# if __name__=="__main__":
#     prompt = input("Enter prompt for image")
#     generate_image(prompt)