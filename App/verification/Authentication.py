import base64
import requests
from requests_toolbelt import MultipartEncoder
from App.verification.Preprocess import makeDirectoryDeleteAndCreate, deleteDirectory
from dotenv import dotenv_values
from PIL import Image
import io
import json
# Load environment variables from .env file
env_vars = dotenv_values()


class AuthAPI:
    def __init__(self):
        self.base_url = env_vars["AUTH_BASE_URL"]
        self.token = None
        self.userName = None
        self.userEmail = None

    def sign_up(self, username, email, password, signatures):
        url = f"{self.base_url}/signup"

        # Convert dictionary to JSON
        json_data = json.dumps({"username": username, "email": email, "password": password})
        files = {}
        for idx, img in enumerate(signatures):
            files[f"file{idx+1}"] = (f"tempSign{idx+1}.png", open(img, "rb"), "image/png")


        # Create a multipart/form-data object
        multipart_data = MultipartEncoder(
            fields={
                "userDetails": str(json_data),
                **files
            }
        )

        headers = {
            "Content-Type":  multipart_data.content_type
        }

        print(multipart_data)
        response = requests.post(url, data=multipart_data.to_string(), headers=headers)
        if response.status_code == 200:
            print(response.json().get("message"))
            return True
        else:
            print(response.json().get("message"))
            return False

    def sign_in(self, username, password):
        url = f"{self.base_url}/signin"
        data = {
            "username": username,
            "password": password
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            responseJson = response.json()
            self.userName = responseJson.get('username')
            self.userEmail = responseJson.get('email')
            SIGNATURE_SAVE_PATH = "verification//application_data//" + self.userName
            SIGNATURE_VERIFY_SAVE_PATH = SIGNATURE_SAVE_PATH + "//verification_images"
            makeDirectoryDeleteAndCreate(SIGNATURE_SAVE_PATH)
            makeDirectoryDeleteAndCreate(SIGNATURE_VERIFY_SAVE_PATH)
            makeDirectoryDeleteAndCreate(SIGNATURE_SAVE_PATH + "//new_sign")

            for idx, img in enumerate(responseJson.get('userSignature')):
                img = base64.b64decode(img)
                # Create a BytesIO object and load the image
                image_buffer = io.BytesIO(img)
                image = Image.open(image_buffer)
                image.save(SIGNATURE_VERIFY_SAVE_PATH + "/" + str(idx) + ".png")

            self.token = "bezkoder=" + response.cookies.get("bezkoder")
            print("Sign in Successfully")
            return True

        else:
            print(response.json().get("message"))
            return False

    def logout(self):
        if self.token:
            url = f"{self.base_url}/signout"
            # headers = {
            #     "Authorization": f"Bearer {self.token}"
            # }
            response = requests.post(url)
            if response.status_code == 200:
                self.clearUserDir()
                self.token = None
                self.userName = None
                self.userEmail = None
                print("Logout successful!")
            else:
                print("Logout failed.")
        else:
            print("You are not signed in.")

    def gettoken(self):
        return self.token

    def getUserName(self):
        return self.userName

    def clearUserDir(self):
        deleteDirectory("verification//application_data//" + self.userName)


if __name__ == "__main__":
    # Example usage
    api = AuthAPI()  # Replace with the actual API base URL

    # Sign in
    api.sign_in("victorvasanth18@gmail.com", "12345678")

    # Logout
    api.logout()
