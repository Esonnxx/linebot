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
isArgreed = False


app = Flask(__name__)
chatgpt = ChatGPT()

def handle_agreement(event):
    global working_status
    if event.message.text =="我同意":
        line_bot_api.reply_message(
            event.reply_token,
            TextMessage(text="可以跟我說說你的故事嗎1"))
        working_status = True
        
def handle_writeLetter(event):
    global working_status
    if event.message.text =="寫分手信":
        line_bot_api.reply_message(
            event.reply_token,
            TextMessage(text="試著選一個關鍵詞來寫一封分手信吧!請不要發出去，只有你我知道，請選擇一個關鍵詞:熱烈的 平淡的 深刻的 以我們有過XX的戀情，來開頭"))
        working_status = True
        
    
def process_initial_response(event, chatgpt, line_bot_api):
    reply_arr = []
    text1 = "看起來你是我們需要的客戶呢，讓我們一起超渡灰飛煙滅吧!"
    text2 = "但...超渡需要付出一些代價的...不過不用擔心!我們不需要金錢，只要您向我們分享您的情緒，我們便能將情緒蒐集，您便能獲得靈堂所需的祭品，當集齊七個祭品，就是舉行超度儀式的時刻! 請打寫分手信"
    chatgpt.add_msg(f"{event.message.text} 根據以上這段故事，先安慰我並用人設詢問我在這短感情中學到了什麼?。請你扮演一個人設是：葬儀師、個性坦率、厭世、說話方式直接 \n")
    reply_msg = chatgpt.get_response().replace("AI:", "", 1)
    chatgpt.add_msg(f"AI:{reply_msg}\n")
    reply_arr.append(TextSendMessage(reply_msg))
    reply_arr.append(TextSendMessage(text1))
    reply_arr.append(TextSendMessage(text2))
    # 給予第一個回應
    line_bot_api.reply_message(event.reply_token, reply_arr)
      # 設置為已收到故事的狀態
    



def process_user_story(event, chatgpt, line_bot_api):
    reply_arr1 = []
    text4 = "你成功集到第一周的祭品了!但著個祭品還很脆弱，穩定的方法就是不要與超度的對象聯繫~這非常重要"
    chatgpt.add_msg(f"{event.message.text} 根據以上這段故事，用對話聊天的方式詢問我在這段感情學到了什麼。請你扮演一個人設是：葬儀師、個性坦率、厭世、說話方式直接，但請不要跟我表示你的人設")
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
    global isArgreed
    if event.message.type != "text":
        return
   
    if event.message.text == "我同意":
        handle_agreement(event)
        working_status =True
        isArgreed =True
        #
        
    
    elif event.message.text == "寫分手信":
        handle_writeLetter(event)
        working_status = True
        received_story = True
        #process_user_story(event, chatgpt, line_bot_api)
    

    if working_status and isArgreed:
        process_initial_response(event,chatgpt ,line_bot_api)
        isArgreed =False
        
    if  working_status and received_story:
        process_user_story(event, chatgpt, line_bot_api)
          
    #if received_story:
        #process_user_story(event, chatgpt, line_bot_api)

if __name__ == "__main__":
    app.run()
