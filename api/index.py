from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from api.chatgpt import ChatGPT

import os

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))
working_status = os.getenv("DEFALUT_TALKING", default = "true").lower() == "true"


app = Flask(__name__)
chatgpt = ChatGPT()

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
    if event.message.type != "text":
        return

    if event.message.text == "說話":
        working_status = True
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="我可以說話囉，歡迎來跟我互動 ^_^ "))
        return

    if event.message.text == "閉嘴":
        working_status = False
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="好的，我乖乖閉嘴 > <，如果想要我繼續說話，請跟我說 「說話」 > <"))
        return
    if event.message.text == "我同意":
        working_status = False
        line_bot_api.reply_message(
            event.reply_token,
            TextMessage(text ="可以跟我說說你的故事嗎?"))
        working_status =True
        return
    task = False  
    if working_status:
        if task== False:
            reply_arr =[]
            text1 = "看起來你是我們需要的客戶呢，讓我們一起超渡灰飛煙滅吧!"
            text2 = "但...超渡需要付出一些代價的...不過不用擔心!我們不需要金錢，只要您向我們分享您的情緒，我們便能將情緒蒐集，您便能獲得靈堂所需的祭品，當集齊七個祭品，就是舉行超度儀式的時刻!"
            text3 ="試著選一個關鍵詞來寫一封分手信吧!請不要發出去，只有你我知道，請選擇一個關鍵詞:熱烈的 平淡的 深刻的 以我們有過XX的戀情，來開頭"
            chatgpt.add_msg(f"HUMAN:{event.message.text} 根據這個故事先安慰我 並詢問他在這短感情中學到了什麼?\n")
            reply_msg = chatgpt.get_response().replace("AI:", "", 1)
            chatgpt.add_msg(f"AI:{reply_msg}\n")
            reply_arr.append( TextSendMessage(reply_msg) )
            reply_arr.append( TextSendMessage(text1) )
            reply_arr.append( TextSendMessage(text2) )
            reply_arr.append( TextSendMessage(text3) )
            line_bot_api.reply_message(
                event.reply_token,
                reply_arr)
            task = True
        else:
            reply_arr1 =[]
            text4 = "你成功集到第一周的祭品了!但著個祭品還很脆弱，穩定的方法就是不要與超度的對象聯繫~這非常重要"
            chatgpt.add_msg(f"HUMAN:{event.message.text} 根據這個故事先安慰我 ")
            reply_msg = chatgpt.get_response().replace("AI:", "", 1)
            reply_arr1.append( TextSendMessage(reply_msg) )
            reply_arr1.append( TextSendMessage(text4) )
            chatgpt.add_msg(f"AI:{reply_msg}\n")
            line_bot_api.reply_message(
                event.reply_token,
                reply_arr1)

if __name__ == "__main__":
    app.run()
