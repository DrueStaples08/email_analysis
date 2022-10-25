from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
from bs4 import BeautifulSoup
import mailparser
import pandas as pd
import re



def extract_email():
    all_emails = []
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        result = service.users().messages().list(maxResults=350, userId='me').execute()
        messages = result.get('messages')
        count = 0
        # iterate through all the messages
        for msg in messages:
            # Get the message from its id
            txt = service.users().messages().get(userId='me', id=msg['id']).execute()
            # Use try-except to avoid any Errors
            try:
                # Get value of 'payload' from dictionary 'txt'
                payload = txt['payload']
                headers = payload['headers']
                # Look for Subject and Sender Email in the headers
                for d in headers:
                    if d['name'] == 'Subject':
                        subject = d['value']
                    if d['name'] == 'From':
                        sender = d['value']
                count += 1
                # # The Body of the message is in Encrypted format. So, we have to decode it.
                # # Get the data and decode it with base 64 decoder.
                parts = payload.get('parts')[0]
                # print(parts)
                data = parts['body']['data']
                data = data.replace("-","+").replace("_","/")
                decoded_data = base64.b64decode(data)
                # Now, the data obtained is in html. So, we will parse 
                # it using the html parser
                soup = BeautifulSoup(decoded_data , "html.parser")
                text = soup.get_text()
                text_split = re.split(" ", text)
                all_emails.append(text_split)
                print('EMAIL', count)
            except:
                pass
    except HttpError as error:
        print(f'An error occurred: {error}')
        pass
    return all_emails




# if __name__ == '__main__':
#     ee = extract_email()
#     print(ee)
