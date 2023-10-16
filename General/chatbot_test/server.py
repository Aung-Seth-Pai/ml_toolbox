from flask import Flask
import requests
import os
from os.path import join, dirname
from dotenv import load_dotenv
from botwork import send_message


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app = Flask(__name__)

FB_API_URL = 'https://graph.facebook.com/v2.6/me/messages'
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN")
PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN")

# test server
@app.route('/')
def hello_world():
    return 'Hello, World!'

# def verify_webhook(req):
#     if req.args.get("hub.verify_token") == VERIFY_TOKEN:
#         return req.args.get("hub.challenge")
#     else:
#         return "incorrect"

# def is_user_message(message):
#     """Check if the message is a message from the user"""
#     return (message.get('message') and
#             message['message'].get('text') and
#             not message['message'].get("is_echo"))


# @app.route("/webhook")
# def listen():
#     """This is the main function flask uses to 
#     listen at the `/webhook` endpoint"""
#     if request.method == 'GET':
#         return verify_webhook(request)

#     if request.method == 'POST':
#         payload = request.json
#         event = payload['entry'][0]['messaging']
#         for x in event:
#             if is_user_message(x):
#                 text = x['message']['text']
#                 sender_id = x['sender']['id']
#                 respond(sender_id, text)

#         return "ok"
    
# To locally run the app
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0',port=3000)
