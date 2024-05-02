from flask import Flask,request
import setup
import services
# importing the libs 

app = Flask(__name__) #creating flask application

@app.route('/',methods=['GET']) #create default routing with get method
def Alawao():
    return'Hello This Alawao Bot'

@app.route('/webhook', methods=['GET']) # define route for handel get request of verify token
def verify_token():
    try:
        token = request.args.get('hub.verify_token')  #Meta webhook configuration
        challenge = request.args.get('hub.challenge')
        if token == setup.token and challenge != None: # comparing the token that we store with webhook token
            return challenge
        else:
            return 'Toke Rejected',403 # status code 403 Forbidden
    except Exception as e :
        return str(e) , 403
@app.route('/webhook',methods=['POST']) # handel post request retrieves incoming message from webhook
def received_message():
    try:
        body = request.get_json()
        entry = body['entry'][0]      # access json data with select first element with [0]
        changes = entry['changes'][0]
        value = changes['value']
        message = value['messages'][0]
        number = message['from']
        messageId = message['id']
        contacts = value['contacts'][0]
        name = contacts['profile']['name']
        text = services.get_whatsapp_message(message)  # calling to get user message object
        services.chatbot_manager(text, number, messageId, name) # passing to chatbot manger for take action
        return 'Done' #statues
    except Exception as e: #handling error
        return str(e),403
if __name__ == '__main__':
    app.run(port=8080,debug=True)  #set farrowed port 