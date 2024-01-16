import requests
import os

def make_post_linkedin(text, pic=None):
    body = {
        "access_token": os.getenv("LINKEDIN_ACCESS_TOKEN"),
        "linkedin_id": os.getenv("LINKEDIN_ID"),
        "content": text,
    }
 
    url = "https://replyrocket-flask.onrender.com/upload"
 
    try:
        if pic is None:
            response = requests.post(url, data=body, timeout=10000)
            if response.status_code == 200:
                return "Post successful!"
            else:
                return f"Failed to post. Status code: {response.status_code}"
        else:
            with open(pic, "rb") as file:
                files = {"file": file}
                response = requests.post(url, files=files, data=body, timeout=10000)
                if response.status_code == 200:
                    return "Post successful!"
                else:
                    return f"Failed to post. Status code: {response.status_code}"
    except Exception as e:
        return f"An error occurred: {str(e)}"
 