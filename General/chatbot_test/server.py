from flask import Flask, request
import requests
import random
import os
from os.path import join, dirname
from dotenv import load_dotenv
from botwork import is_user_message, get_message, send_message, respond

from pymessenger.bot import Bot

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app = Flask(__name__)

# FB_API_URL = 'https://graph.facebook.com/v2.6/me/messages'
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN")
PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN")
bot = Bot(PAGE_ACCESS_TOKEN)

# # test server
# @app.route('/')
# def hello_world():
#     return 'Hello, World!'

def verify_fb_token(req):
    if req.args.get("hub.verify_token") == VERIFY_TOKEN:
        return req.args.get("hub.challenge")
    else:
        return 'Invalid verification token'



@app.route("/policy", methods=["GET"])
def policy():
    return "THIS IS TEST POLICY"

@app.route("/webhook", methods=["GET", "POST"])
def listen():
    """This is the main function flask uses to 
    listen at the `/webhook` endpoint"""
    if request.method == 'GET':
        print("Authenticating.....")
        return verify_fb_token(request)

    if request.method == 'POST':
        payload = request.get_json() # object and entry as keys of payload
        print(payload)
        for event in payload['entry']:
            # if user sent message
            if "messaging" in event.keys():
                
                messaging = event['messaging']
                for message in messaging:
                    if message.get('message'):
                        #Facebook Messenger ID for user so we know where to send response back to
                        recipient_id = message['sender']['id']
                        # if user sends text
                        if message['message'].get('text'):
                            if is_user_message(message):
                                text = message['message']['text']
                                print(text)
                                # respond(recipient_id, text, bot)   
                                # bot.send_text_message(recipient_id, text)
                                return "OK"          
                        #if user sends us a GIF, photo,video, or any other non-text item
                        if message['message'].get('attachments'):
                            print("MESSAGE IS NON_TEXT")
                            return "NON TEXT"
                            # response_sent_nontext = get_message()
                            # respond(recipient_id, response_sent_nontext, bot)
            else:
                pass  
        return "ok"
    

# To locally run the app
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0',port=5000)
