import requests

def is_user_message(message):
    """Check if the message is a message from the user"""
    return (message.get('message') and
            message['message'].get('text') and
            not message['message'].get("is_echo"))

#uses PyMessenger to send response to user
def send_message(recipient_id, response, bot):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"


# def send_message(recipient_id, text, PAGE_ACCESS_TOKEN, FB_API_URL):
#     """Send a response to Facebook"""
#     payload = {
#         'message': {
#             'text': text
#         },
#         'recipient': {
#             'id': recipient_id
#         },
#         'notification_type': 'regular'
#     }
#     auth = {
#         'access_token': PAGE_ACCESS_TOKEN
#     }
#     response = requests.post(
#         FB_API_URL,
#         params=auth,
#         json=payload
#     )
#     return response.json()

def get_bot_response(message):
    """This is just a dummy function, returning a variation of what
    the user said. Replace this function with one connected to chatbot."""
    return "This is a dummy response to '{}'".format(message)

def respond(recipient_id, message, bot):
    """Formulate a response to the user and
    pass it on to a function that sends it."""
    response = get_bot_response(message)
    send_message(recipient_id, response, bot)

