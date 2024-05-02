import requests # for request from whatsapp API 
import setup
import json #passing data as json
import time


def get_whatsapp_message(message): # function for extracts the content  from whatsapp message
    if 'type' not in message:
        text = 'Message type is not recognized'
        return text
    typeMessage = message['type']
    if typeMessage == 'text':
        text = message['text']['body'] # if type is text message retrieves the text content body
    elif typeMessage == 'button':
        text = message['button']['text'] # if type is button retrieves the text content of button
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'list_reply': 
        text = message['interactive']['list_reply']['title']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'button_reply':
        text = message['interactive']['button_reply']['title']
    else:
        text = 'Message not processed'
    
    return text

def send_whatsapp_message(data): # send massage using whatsapp api  
    try:
        whatsapp_token = setup.whatsapp_token #token url
        whatsapp_url = setup.whatsapp_url # authentication url
        headers = {'Content-Type': 'application/json', #send data in json format data with the access token
                'Authorization': 'Bearer ' + whatsapp_token}
        print("Message Sent", data)
        response = requests.post(whatsapp_url, 
                                headers=headers, 
                                data=data)
        
        if response.status_code == 200: # check status code if 200 successful
            return 'Message sent', 200 
        else:
            return 'An error occurred while sending the message', response.status_code #handling error
    except Exception as e:
        return str(e), 403 # forbidden
    
def text_Message(number, text): #the json format
    data = json.dumps(  #convert python objects to json string
            {
                "messaging_product": "whatsapp",    
                "recipient_type": "individual",
                "to": number,
                "type": "text",
                "text": {
                    "body": text
                }
            }
    )
    return data

def buttonReply_Message(number, options, body, footer, prefix_id,messageId): # construct JSON data for sending a button reply message
    buttons = []
    for i, option in enumerate(options):
        buttons.append(
            {
                "type": "reply",
                "reply": {
                    "id": prefix_id + "_btn_" + str(i+1),
                    "title": option
                }
            }
        )

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "buttons": buttons
                }
            }
        }
    )
    return data

def listReply_Message(number, options, body, footer, prefix_id, messageId):
    rows = []
    for i, option in enumerate(options):
        rows.append(
            {
                "id": prefix_id + "_row_" + str(i+1),
                "title": option,
                "description": ""
            }
        )

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "button": "Options",
                    "sections": [
                        {
                            "title": "Sections",
                            "rows": rows
                        }
                    ]
                }
            }
        }
    )
    return data

def replyReaction_Message(number, messageId, emoji):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "reaction",
            "reaction": {
                "message_id": messageId,
                "emoji": emoji
            }
        }
    )
    return data

def replyText_Message(number, messageId, text):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "context": { "message_id": messageId },
            "type": "text",
            "text": {
                "body": text
            }
        }
    )
    return data

def markRead_Message(messageId):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id": messageId
        }
    )
    return data

def drop_list_Message(number, options, body, footer, prefix_id, messageId):
    rows = []
    for i, option in enumerate(options):
        rows.append(
            {
                "id": prefix_id + "_row_" + str(i + 1),
                "title": option,
                "description": ""
            }
        )

    interactive_data = {
        "type": "list",
        "header": {"type": "text", "text": body},
        "body": {"text":"الرجاء اختيار الخدمة المطلوبة من الاختيارات"},
        "footer": {"text": footer},
        "action": {
            "button": "الاختيارات",
            "sections": [
                {"title": "services Selection", "rows": rows}
            ]
        }
    }

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": interactive_data
        }
    )
    return data


def chatbot_manager(text, number, messageId, name):
    text = text.lower() # Message sent by the user
    greetings = ["مرحبا", "اهلا", "السلام عليكم","hi"]
    list = []
    print("User message: ", text)

    markRead = markRead_Message(messageId)
    list.append(markRead)
    time.sleep(2)
    if any(greeting in text for greeting in greetings):
        body = "اهلا بك في Alawao 👋 "
        footer = "Alowao Team"
        options = ["خدمةالعملاء", "طلب جديد"]
        prefix_id = "services"        
        replyButtonData = drop_list_Message(number, options, body, footer, prefix_id, messageId)
        replyReaction = replyReaction_Message(number, messageId, "🤗")
        list.append(replyReaction)
        list.append(replyButtonData)
        
    elif "خدمةالعملاء" in text:
        body = " 📞 سوف نتوصل معك في اقرب وقت او يمكنك التواصل معنا عبر الرقم الموحد"
        footer = "Alowao Team"
        options = ["(888) 880-5510"]
        replyButtonData = buttonReply_Message(number, options, body, footer, "sed1",messageId)
        replyReaction = replyReaction_Message(number, messageId, "⏳")
        list.append(replyReaction)
        list.append(replyButtonData)
        
    elif "طلب جديد" in text:
        body = "💻 للطلبات يمكنك زيارة موقعنا"
        footer = "Alowao Team"
        options = ["https://alawao.com/"]
        replyButtonData = buttonReply_Message(number, options, body, footer, "sed1",messageId)
        replyReaction = replyReaction_Message(number, messageId, "🚀")
        list.append(replyReaction)
        list.append(replyButtonData)
        
    elif "سلام" in text:
        data = text_Message(number, "مع السلامة 👋")
        replyReaction = replyReaction_Message(number, messageId, "👋")
        list.append(data)
        
    elif "نعم" in text:
        body = "مرحبا كيف يمكنني مساعدتك 👋 ؟"
        footer = "Alowao Team"
        options = ["خدمةالعملاء", "طلب جديد"]
        replyButtonData = buttonReply_Message(number, options, body, footer, "sed1",messageId)
        replyReaction = replyReaction_Message(number, messageId, "🤗")
        list.append(replyReaction)
        list.append(replyButtonData)
        
    elif "" in text :
        data = text_Message(number, "عذرًا، لم أفهمك. هل ترغب في عرض الخيارات؟")
        list.append(data)
    else:
        data = text_Message(number, " عذرًا، لم أفهم ما قلته مع السلامة 👋")
        replyReaction = replyReaction_Message(number, messageId, "👋")
        list.append(data)
            
    for item in list: #collecting responses in a list and iterating over them to send individually
        send_whatsapp_message(item)
        
def replace_start(s): #handling country code
    number = s[2:]
    if s.startswith("20"):
        return "2" + number
    else:
        return s
