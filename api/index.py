from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from api.chatgpt import ChatGPT

import os

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))
working_status = os.getenv("DEFALUT_TALKING", default = "true").lower() == "true"
received_story =False


app = Flask(__name__)
chatgpt = ChatGPT()

def handle_agreement(event):
    global working_status
    if event.message.text =="我同意":
        working_status = False
        line_bot_api.reply_message(
            event.reply_token,
            TextMessage(text="可以跟我說說你的故事嗎2?"))
        working_status = True
        return
    
def process_initial_response(event, chatgpt, line_bot_api):
    reply_arr = []
    text1 = "看起來你是我們需要的客戶呢，讓我們一起超渡灰飛煙滅吧!"
    text2 = "但...超渡需要付出一些代價的...不過不用擔心!我們不需要金錢，只要您向我們分享您的情緒，我們便能將情緒蒐集，您便能獲得靈堂所需的祭品，當集齊七個祭品，就是舉行超度儀式的時刻!"
    text3 = "試著選一個關鍵詞來寫一封分手信吧!請不要發出去，只有你我知道，請選擇一個關鍵詞:熱烈的 平淡的 深刻的 以我們有過XX的戀情，來開頭"
    chatgpt.add_msg(f"HUMAN:{event.message.text} 現在想請你扮演一個腳色，繁體中文回答對話形式：不要是方法或是條列的建議，用像是朋友一樣的交流、一句的對話，和他一直聊天，陪伴他，偶爾也可以互虧，讓聊天不要那麼沉悶，人設是：葬儀師、個性坦率、厭世、說話方式直接，由於自己本身歷過多段被分手的愛情，從中學到很多關於如何處理自己內在傷痛得經驗，因此想運用自己的情史幫助他人，用對話聊天的方式讓被分手的人發覺自己的內在存在但不知道或是不願意面對的傷痛。根據這個故事用以上的人設先安慰我 並用剛剛的人設詢問他在這短感情中學到了什麼?\n")
    reply_msg = chatgpt.get_response().replace("AI:", "", 1)
    chatgpt.add_msg(f"AI:{reply_msg}\n")
    reply_arr.append(TextSendMessage(reply_msg))
    reply_arr.append(TextSendMessage(text1))
    reply_arr.append(TextSendMessage(text2))
    reply_arr.append(TextSendMessage(text3))
    # 給予第一個回應
    line_bot_api.reply_message(event.reply_token, reply_arr)
    received_story = True  # 設置為已收到故事的狀態
    



def process_user_story(event, chatgpt, line_bot_api):
    reply_arr1 = []
    text4 = "你成功集到第一周的祭品了!但著個祭品還很脆弱，穩定的方法就是不要與超度的對象聯繫~這非常重要"
    chatgpt.add_msg(f"HUMAN:{event.message.text} 現在想請你扮演一個腳色，繁體中文回答對話形式：不要是方法或是條列的建議，用像是朋友一樣的交流、一句的對話，和他一直聊天，陪伴他，偶爾也可以互虧，讓聊天不要那麼沉悶，人設是：葬儀師、個性坦率、厭世、說話方式直接，由於自己本身歷過多段被分手的愛情，從中學到很多關於如何處理自己內在傷痛得經驗，因此想運用自己的情史幫助他人，用對話聊天的方式讓被分手的人發覺自己的內在存在但不知道或是不願意面對的傷痛。 ")
    reply_msg = chatgpt.get_response().replace("AI:", "", 1)
    reply_arr1.append(TextSendMessage(reply_msg))
    reply_arr1.append(TextSendMessage(text4))
    chatgpt.add_msg(f"AI:{reply_msg}\n")
    line_bot_api.reply_message(event.reply_token, reply_arr1)

# domain root
@app.route('/')
def home():
    return 'Hello, World!'

@app.route("/webhook", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global working_status 
    global received_story
    if event.message.type != "text":
        return
   
    if event.message.text == "我同意":
        handle_agreement(event)
        
    
    elif working_status:  
        if not received_story:
            process_initial_response(event, chatgpt, line_bot_api)
            received_story =True
            
    if received_story:
        process_user_story(event, chatgpt, line_bot_api)

if __name__ == "__main__":
    app.run()
