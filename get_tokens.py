"""
One-time script to get Gmail OAuth2 access + refresh tokens.
Run this once, then copy the printed values into your environment.
"""

from google_auth_oauthlib.flow import InstalledAppFlow

CLIENT_ID     = "YOUR_GOOGLE_CLIENT_ID"
CLIENT_SECRET = "YOUR_GOOGLE_CLIENT_SECRET"

flow = InstalledAppFlow.from_client_config(
    {
        "installed": {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }
    },
    scopes=["https://www.googleapis.com/auth/gmail.send"],
)

creds = flow.run_local_server(port=0)

print("\n--- Copy these into your environment ---")
print(f"GMAIL_ACCESS_TOKEN={creds.token}")
print(f"GMAIL_REFRESH_TOKEN={creds.refresh_token}")
print("----------------------------------------")
