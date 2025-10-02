import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

client_id = os.environ['CLIENT_ID']
client_secret = os.environ['CLIENT_SECRET']
tenant_id = os.environ['TENANT_ID']
user_email = os.environ['USER_EMAIL']

# Get access token
token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
token_data = {
    "grant_type": "client_credentials",
    "client_id": client_id,
    "client_secret": client_secret,
    "scope": "https://graph.microsoft.com/.default"
}
token_r = requests.post(token_url, data=token_data)
token_r.raise_for_status()
access_token = token_r.json().get("access_token")

# Upload file to OneDrive
upload_url = f"https://graph.microsoft.com/v1.0/users/{user_email}/drive/root:/Documents/AutoUpload/Tinh Thần Biến.txt:/content"
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "text/plain"
}
file_content = "Chào bạn, đây là tệp Tinh Thần Biến được gửi từ Graph API."
upload_r = requests.put(upload_url, headers=headers, data=file_content)
upload_r.raise_for_status()

# Send email notification
email_url = f"https://graph.microsoft.com/v1.0/users/{user_email}/sendMail"
headers_email = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}
email_data = {
    "message": {
        "subject": "Xác nhận upload OneDrive",
        "body": {
            "contentType": "Text",
            "content": "Tệp Tinh Thần Biến.txt đã được upload thành công vào thư mục Documents/AutoUpload trên OneDrive."
        },
        "toRecipients": [
            {
                "emailAddress": {
                    "address": user_email
                }
            }
        ]
    },
    "saveToSentItems": "true"
}
email_r = requests.post(email_url, headers=headers_email, data=json.dumps(email_data))
email_r.raise_for_status()
print("Upload and email notification completed successfully.")
