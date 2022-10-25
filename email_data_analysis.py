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
        # results = service.users().labels().list(userId='me').execute()
        # labels = results.get('labels', [])

        # print('SERVICE', labels)
        result = service.users().messages().list(maxResults=350, userId='me').execute()
        # print('RESULTS!!!', result)

        messages = result.get('messages')
        # print('MESSAGES!!', messages)

        # messages is a list of dictionaries where each dictionary contains a message id.
    
        count = 0
        # iterate through all the messages
        for msg in messages:

            # Get the message from its id
            txt = service.users().messages().get(userId='me', id=msg['id']).execute()
            # print(txt)
  
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
                # print(data)
                data = data.replace("-","+").replace("_","/")
                # print(data)
                decoded_data = base64.b64decode(data)
                # print(decoded_data)

                # Now, the data obtained is in lxml. So, we will parse 
                # it with BeautifulSoup library
                soup = BeautifulSoup(decoded_data , "html.parser")
                # print(soup)
                # soup = BeautifulSoup(decoded_data, 'html_parser')
                # body = soup.body()
                # print(body)
                text = soup.get_text()
                # print(text)


                text_split = re.split(" ", text)
                # print(text_split)
                all_emails.append(text_split)
                # text_list = parse_text(text)
                # print(text_list)

                # mail = mailparser.parse_from_string(text)
                # # print(mail.text_plain)
                # print(mail.main_partial)
  
                # Printing the subject, sender's email and message
                # print(decoded_data)
                # print("Subject: ", subject)
                # print("From: ", sender)
                # print("Message: ", body)
                print('EMAIL', count)
            except:
                pass



    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')

    return all_emails

def parse_text(single_email):
    res = []
    # single_email = single_email.split(['/', '', '/n', '/r'])
    # single_email = re.split('/', ' ', '/n', '/r', single_email)
    res.append(single_email)
    # res = res.split('/')
    return res

def create_dataframe(all_emails):
    df = pd.DataFrame(all_emails)
    return df



# if __name__ == '__main__':
#     ee = extract_email()
#     print(ee)
