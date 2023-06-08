import requests
from dotenv import dotenv_values

# Load environment variables from .env file
env_vars = dotenv_values()
class AuthAPI:
    def __init__(self, base_url):
        self.base_url = env_vars["AUTH_BASE_URL"]
        self.token = None

    def sign_up(self, username, password):
        url = f"{self.base_url}/signup"
        data = {
            "username": username,
            "password": password
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print("Sign up successful!")
        else:
            print("Sign up failed.")

    def sign_in(self, username, password):
        url = f"{self.base_url}/signin"
        data = {
            "username": username,
            "password": password
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            self.token = response.json().get("token")
            print("Sign in successful!")
        else:
            print("Sign in failed.")

    def logout(self):
        if self.token:
            url = f"{self.base_url}/logout"
            headers = {
                "Authorization": f"Bearer {self.token}"
            }
            response = requests.post(url, headers=headers)
            if response.status_code == 200:
                self.token = None
                print("Logout successful!")
            else:
                print("Logout failed.")
        else:
            print("You are not signed in.")

    def gettoken(self):
        return self.token



if __name__ == "__main__":
    # Example usage
    api = AuthAPI("https://dummyauthapi.com")  # Replace with the actual API base URL

    # Sign up
    api.sign_up("exampleuser", "password123")

    # Sign in
    api.sign_in("exampleuser", "password123")

    # Logout
    api.logout()
