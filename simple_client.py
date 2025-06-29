import requests
import json

# --- API Configuration ---
BASE_URL = "http://localhost:8000"

# --- User credentials for demonstration ---
TEST_EMAIL = "client_test@example.com"
TEST_PASSWORD = "supersecretpassword"

# --- 1. Create a New User ---
print("--- Attempting to Create a New User ---")
create_user_url = f"{BASE_URL}/api/v1/users/"
user_data = {
    "email": TEST_EMAIL,
    "password": TEST_PASSWORD
}

try:
    response = requests.post(create_user_url, json=user_data)
    response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
    print("User created successfully!")
    print("Response:", response.json())
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 400 and "already exists" in e.response.text:
        print(f"User '{TEST_EMAIL}' already exists, proceeding to login.")
    else:
        print(f"Error creating user: {e}")
        print("Response:", e.response.json() if e.response.text else e.response.text)
except requests.exceptions.ConnectionError as e:
    print(f"Error connecting to API: {e}. Is your Uvicorn server running?")
    exit() # Exit if we can't connect

# --- 2. Log In and Get an Access Token ---
print("\n--- Attempting to Log In and Get Access Token ---")
token_url = f"{BASE_URL}/api/v1/token"
login_data = {
    "username": TEST_EMAIL, # For OAuth2 password flow, username is typically email
    "password": TEST_PASSWORD,
    "grant_type": "password"
}

# requests.post for x-www-form-urlencoded uses 'data' parameter
# requests.post for application/json uses 'json' parameter
response = requests.post(token_url, data=login_data)
try:
    response.raise_for_status()
    token_response = response.json()
    access_token = token_response.get("access_token")
    token_type = token_response.get("token_type")
    print("Login successful! Token received.")
    # print("Token Response:", token_response) # Uncomment to see full token response
except requests.exceptions.HTTPError as e:
    print(f"Error logging in: {e}")
    print("Response:", e.response.json() if e.response.text else e.response.text)
    access_token = None
    token_type = None

if access_token:
    # --- 3. Access a Protected Endpoint (Get Current User Info) ---
    print("\n--- Attempting to Access Protected User Info ---")
    users_me_url = f"{BASE_URL}/api/v1/users/me/"
    headers = {
        "Authorization": f"{token_type} {access_token}"
    }

    response = requests.get(users_me_url, headers=headers)
    try:
        response.raise_for_status()
        print("Successfully accessed protected endpoint!")
        print("Current User Info:", response.json())
    except requests.exceptions.HTTPError as e:
        print(f"Error accessing protected endpoint: {e}")
        print("Response:", e.response.json() if e.response.text else e.response.text)
else:
    print("\nCould not get access token, skipping protected endpoint access.")

print("\n--- Script finished ---")