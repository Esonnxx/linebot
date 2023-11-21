from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
from api.chatgpt import ChatGPT
from apscheduler.schedulers.background import BackgroundScheduler
from linebot.models.events import FollowEvent, MessageEvent, TextMessage

import os





line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))
working_status = os.getenv("DEFALUT_TALKING", default = "true").lower() == "true"
received_story =False
isArgreed = False
day4State = False
day5State =False
weekendState =False
week2day1State = False
day9State = False
readyState = False
day10State = False
day11State =False
day12State =False
day13State = False
day14State = False
chit_chat_State = False


app = Flask(__name__)
# 存储用户ID的列表
user_ids = set()
message_interval_minutes = 1

# 定义要发送的消息内容
message_text = '今天是第三天晚上， 希望你今天充滿仇恨 由於你昨天實施善行，因此你獲得發洩仇恨的機會，請前往報仇靈堂！ 入口：選單右上角(報仇靈堂連結) 如果你回得來，🗝茫'
chatgpt = ChatGPT()
scheduler = BackgroundScheduler()
def send_message_to_users():
    for user_id in user_ids:
        message = TextSendMessage(text=message_text)
        line_bot_api.push_message(user_id, message)

# 设置定时任务，每5分钟执行一次
scheduler.add_job(send_message_to_users, 'interval', minutes=message_interval_minutes)


def handle_agreement(event):
    global working_status
    if event.message.text =="我同意":
        reply_arr =[]
        image_url = "https://i.ibb.co/4fJ9kv9/week1-1.jpg"  # 請替換成你的圖片 URL
        image_message = ImageSendMessage(
            original_content_url=image_url,
            preview_image_url=image_url
        )
        text="看來你是我們需要的客戶呢，撰寫一封分手信，作為分手的一方，將你沒機會說的及對自己的期望或優點寫下，在最後用<我是...的人，我要迎接更好的自己>做結尾。注意!不能被別人看到，也絕不能跟別人說關鍵詞：熱烈的 平淡的 深刻的"
        reply_arr.append(image_message)
        reply_arr.append(TextSendMessage(text))

        line_bot_api.reply_message(
            event.reply_token,
            reply_arr)
        working_status = True
        
def handle_writeLetter(event):
    global working_status
    if event.message.text =="寫分手信":
        """line_bot_api.reply_message(
            event.reply_token,
            TextMessage(text="試著選一個關鍵詞來寫一封分手信吧!請不要發出去，只有你我知道，請選擇一個關鍵詞:熱烈的 平淡的 深刻的 以我們有過XX的戀情，來開頭"))"""
        # 發送圖片訊息
        image_url = "https://i.ibb.co/4fJ9kv9/week1-1.jpg"  
        image_message = ImageSendMessage(
            original_content_url=image_url,
            preview_image_url=image_url
        )
        line_bot_api.reply_message(event.reply_token, image_message)
        working_status = True
def handle_day2(event):
    global working_status
    url = "http://benevolence.page.s3-website-ap-northeast-1.amazonaws.com/"
    if event.message.text =="第二天療程":
        message_text = "今天是第二天，我們需要完成四十九天的等待與儀式。要多做善行以維持天平的穩定，試試到善行靈堂看看吧~入口：選單左上角(善行靈堂連結)有任何問題都可以問我🗝仇愁得報(建議晚上使用)想進行第三天療程請打<第三天療程>{}".format(url)
        line_bot_api.reply_message(
            event.reply_token,TextMessage(text=message_text)
        )
        # 發送圖片訊息
        image_url = "https://i.ibb.co/0XS57YS/image.jpg"  
        image_message = ImageSendMessage(
            original_content_url=image_url,
            preview_image_url=image_url
        )
        line_bot_api.push_message(event.source.user_id, image_message)
        working_status = True
def handle_day3(event):
    global working_status
    url = "http://benevolence.page.s3-website-ap-northeast-1.amazonaws.com/"
    if event.message.text =="第三天療程":
        message_text = "今天是第三天晚上， 希望你今天充滿仇恨 由於你昨天實施善行，因此你獲得發洩仇恨的機會，請前往報仇靈堂！ 入口：選單右上角(報仇靈堂連結) 如果你回得來，🗝茫'想進行第四天療程請打<第四天療程>{}".format(url)
        line_bot_api.reply_message(
            event.reply_token,TextMessage(text=message_text)
        )
         # 發送圖片訊息
        image_url = "https://i.ibb.co/xsxkJsV/image.jpg"  
        image_message = ImageSendMessage(
            original_content_url=image_url,
            preview_image_url=image_url
        )
        line_bot_api.push_message(event.source.user_id, image_message)
        working_status = True
def handle_day4(event):
    global working_status
    if event.message.text =="第四天療程":
        message_text = "今天是第四天，都說養成習慣需要21天，你這3天就習慣我的存在了嗎？好好好，開個玩笑，昨天的儀式感覺如何呀？"
        line_bot_api.reply_message(
            event.reply_token,TextMessage(text=message_text)
        )
        working_status = True

def handle_day5(event):
    global working_status
    reply_arr =[]
    if event.message.text =="第五天療程":
        text = "今天是第五天，相信你的感情也有一些的沉澱，是時候為這四天做一個總結!!"
        text1 = "關鍵詞：熱烈的 平淡的 深刻的 請您挑選出一個符合您現在感受的關鍵詞並填入信件的開頭，起筆二篇分手信{關鍵詞}我"
        reply_arr.append(TextSendMessage(text))
        reply_arr.append(TextSendMessage(text1))
        line_bot_api.reply_message(
            event.reply_token,reply_arr)
        working_status = True
def handle_weekend(event):
    global working_status
    reply_arr =[]
    if event.message.text =="假日療程":
        text = "今天是我的休假日，但我還是會陪你的，今天有什麼想說的嗎？單身這幾天的你有什麼感覺？"
        reply_arr.append(TextSendMessage(text))
        line_bot_api.reply_message(
            event.reply_token,reply_arr)
        working_status = True

def handle_week2day1(event):
    global working_status
    reply_arr =[]
    if event.message.text =="第二週療程":
        text = "恭喜！順利進入第二階段，愛情應該沒有這麼容易被釋懷吧？"
        reply_arr.append(TextSendMessage(text))
        line_bot_api.reply_message(
            event.reply_token,reply_arr)
        working_status = True

def handle_day9(event):
    global working_status
    reply_arr =[]
    if event.message.text =="第九天療程":
        text = "啊~9這個數字好啊！情緒是很有趣的東西，有時後就像兩個自己在吵架呢..你準備在這個絕佳時機獲得第二周的法器了嗎?"
        reply_arr.append(TextSendMessage(text))
        line_bot_api.reply_message(
            event.reply_token,reply_arr)
        working_status = True

def handle_readySection(event):
    global working_status
    reply_arr =[]
    if event.message.text =="我準備好了":
        text = "看來你已經準備好了，那我出一個任務給你，請寫一個奠文"
        text1 = "關鍵詞：憤怒、傷心、不解請您挑選出一個符合您現在感受的關鍵詞並填入開頭，以第一人稱我，起筆二周奠文我感到{關鍵詞}開頭"
        reply_arr.append(TextSendMessage(text))
        reply_arr.append(TextSendMessage(text1))
        line_bot_api.reply_message(
            event.reply_token,reply_arr)
        working_status = True

def handle_day10(event):
    global working_status
    reply_arr =[]
    if event.message.text =="第十天療程":
        text = "今天第十天了，希望你那邊天氣好，天氣好的時候做善行效果更加，請移駕至善行靈堂，開啟您充滿善意的一天吧~"
        reply_arr.append(TextSendMessage(text))
        line_bot_api.reply_message(
            event.reply_token,reply_arr)
        working_status = True
def handle_day11(event):
    global working_status
    reply_arr =[]
    if event.message.text =="第十一天療程":
        text = "今天是第十一天，本周的任務還剩下2/3 看來你已經準備好了，那我在出一個任務給你，請寫一個奠文 關鍵詞：憤怒、傷心、不解請您挑選出一個符合您現在感受的關鍵詞並填入開頭，以第二人稱你，起筆二周奠文你感到{關鍵詞}開頭"
        reply_arr.append(TextSendMessage(text))
        line_bot_api.reply_message(
            event.reply_token,reply_arr)
        working_status = True

def handle_day12(event):
    global working_status
    reply_arr =[]
    if event.message.text =="第十二天療程":
        text = "其實有一個問題一直想要問問你，你覺得自己是個甚麼樣的人呢？"
        reply_arr.append(TextSendMessage(text))
        line_bot_api.reply_message(
            event.reply_token,reply_arr)
        working_status = True
def handle_day13(event):
    global working_status
    reply_arr =[]
    if event.message.text =="第十三天療程":
        text = "推進到第13天了呀，希望你那邊已經天黑了，夜晚時儀式的法力會有利，今天的報仇靈堂，為您敞開大門~如果你回得來，請說一聲大仇初報"
        reply_arr.append(TextSendMessage(text))
        line_bot_api.reply_message(
            event.reply_token,reply_arr)
        working_status = True

def handle_day14(event):
    global working_status
    reply_arr =[]
    if event.message.text =="第十四天療程":
        text = "今天是第十四天，本周的任務還剩下1/3 請幫我寫一個奠文。關鍵詞：憤怒、傷心、不解請您挑選出一個符合您現在感受的關鍵詞並填入開頭，以第三人稱你，起筆二周奠文你感到{關鍵詞}開頭"
        reply_arr.append(TextSendMessage(text))
        line_bot_api.reply_message(
            event.reply_token,reply_arr)
        working_status = True


    
def process_initial_response(event, chatgpt, line_bot_api):
    reply_arr = []
    #text1 = "看起來你是我們需要的客戶呢，讓我們一起超渡灰飛煙滅吧!"
    #text2 = "但...超渡需要付出一些代價的...不過不用擔心!我們不需要金錢，只要您向我們分享您的情緒，我們便能將情緒蒐集，您便能獲得靈堂所需的祭品，當集齊七個祭品，就是舉行超度儀式的時刻! 請打寫分手信"
    chatgpt.add_msg(f"{event.message.text} 根據以上這段故事，先安慰我並用人設詢問我在這短感情中學到了什麼?")
    reply_msg = chatgpt.get_response().replace("AI:", "", 1)
    chatgpt.add_msg(f"AI:{reply_msg}\n")
    reply_arr.append(TextSendMessage(reply_msg))
    
    # 給予第一個回應
    line_bot_api.reply_message(event.reply_token, reply_arr)
     
    


def process_chit_chat(event, chatgpt, line_bot_api):
    chatgpt.add_msg(f"{event.message.text} 根據以上這段故事 跟我閒聊")
    reply_msg = chatgpt.get_response().replace("AI:", "", 1)

    msg= [TextSendMessage(text=reply_msg)]

    line_bot_api.reply_message(event.reply_token, msg)


def process_user_story(event, chatgpt, line_bot_api):
    reply_arr1 = []
    text = "做的好!你成功得到了一個情緒罐 。這是開啟超度靈堂所需的祭品，當集齊七個祭品，就是舉行超度儀式的時刻!"
    chatgpt.add_msg(f"{event.message.text} 根據以上這段故事，用對話聊天的方式詢問我在這段感情學到了什麼。")
    reply_msg = chatgpt.get_response().replace("AI:", "", 1)
    image_url = "https://i.ibb.co/xDCgRvx/1.jpg" 
    image_message = ImageSendMessage(
        original_content_url=image_url,
        preview_image_url=image_url
    )
    reply_arr1.append(TextSendMessage(reply_msg))
    reply_arr1.append(TextSendMessage(text))
    reply_arr1.append(image_message)
    chatgpt.add_msg(f"AI:{reply_msg}\n")
    line_bot_api.reply_message(event.reply_token, reply_arr1)

def process_day4_message(event, chatgpt, line_bot_api):
    reply_arr = []
    text= "如果有不了解的，可以到幫助中心尋求協助入口:選單左下角(連結)"
    text1= "如果想進行第五天療程 請打<第五天療程>"
    chatgpt.add_msg(
        f"{event.message.text} 根據以上回答，回應我對儀式的感受")
    reply_msg = chatgpt.get_response().replace("AI:", "", 1)
    reply_arr.append(TextSendMessage(reply_msg))
    reply_arr.append(TextSendMessage(text))
    reply_arr.append(TextSendMessage(text1))
    line_bot_api.reply_message(event.reply_token, reply_arr)
def process_day5_message(event, chatgpt, line_bot_api):
    reply_arr = []
    text = "如果想進行假日療程 請打<假日療程>"
    chatgpt.add_msg(
        f"{event.message.text} 根據以上回答，以正面的方式回應我，並在最後跟我說我是一個什麼樣的人及鼓勵我可以迎接更好的的自己")
    reply_msg = chatgpt.get_response().replace("AI:", "", 1)
    reply_arr.append(TextSendMessage(reply_msg))
    reply_arr.append(TextSendMessage(text))
    line_bot_api.reply_message(event.reply_token, reply_arr)
def process_weekend_message(event, chatgpt, line_bot_api):

    reply_arr = []
    text = "如果想進行接下來的療程 請打<第二週療程>"
    chatgpt.add_msg(
        f"{event.message.text} 根據以上回答，以正面的方式回應我，並陪我聊聊天")
    reply_msg = chatgpt.get_response().replace("AI:", "", 1)
    reply_arr.append(TextSendMessage(reply_msg))
    reply_arr.append(TextSendMessage(text))
    line_bot_api.reply_message(event.reply_token, reply_arr)

def process_week2day1_message(event, chatgpt, line_bot_api):
    reply_arr = []
    text = "如果想進行接下來的療程 請打<第九天療程>"
    chatgpt.add_msg(
        f"{event.message.text} 根據以上回答，以正面的方式回應我，並陪我聊聊天")
    reply_msg = chatgpt.get_response().replace("AI:", "", 1)
    reply_arr.append(TextSendMessage(reply_msg))
    reply_arr.append(TextSendMessage(text))
    line_bot_api.reply_message(event.reply_token, reply_arr)

def process_day9_message(event, chatgpt, line_bot_api):
    reply_arr = []
    text = "嗯～我感受不到你的情緒，你<準備>獲得第二個法器了嗎? 準備好請打<我準備好了>"
    chatgpt.add_msg(
        f"{event.message.text} 根據以上回答 以正面的方式回應我 並陪我聊聊天")
    reply_msg = chatgpt.get_response().replace("AI:", "", 1)
    reply_arr.append(TextSendMessage(reply_msg))
    reply_arr.append(TextSendMessage(text))
    line_bot_api.reply_message(event.reply_token, reply_arr)

def process_ready_message(event, chatgpt, line_bot_api):
    reply_arr = []
    text = "若你能接受現在的自己，我們就可以準備下一階段的療程了喔 準備好請打<第十天療程>"
    chatgpt.add_msg(
        f"{event.message.text} 根據以上回答 以正面的方式回應我 並陪我聊聊天")
    reply_msg = chatgpt.get_response().replace("AI:", "", 1)
    reply_arr.append(TextSendMessage(reply_msg))
    reply_arr.append(TextSendMessage(text))
    line_bot_api.reply_message(event.reply_token, reply_arr)

def process_day10_message(event, chatgpt, line_bot_api):
    reply_arr = []
    text = "如果你準備好了 我們隨時可以進入下一階段的療程了喔 準備好請打<第十一天療程>"
    chatgpt.add_msg(
        f"{event.message.text} 根據以上回答 以正面的方式回應我")
    reply_msg = chatgpt.get_response().replace("AI:", "", 1)
    reply_arr.append(TextSendMessage(reply_msg))
    reply_arr.append(TextSendMessage(text))
    line_bot_api.reply_message(event.reply_token, reply_arr)
def process_day11_message(event, chatgpt, line_bot_api):
    reply_arr = []
    text = "如果你準備好了 我們隨時可以進入下一階段的療程了喔 準備好請打<第十二天療程>"
    chatgpt.add_msg(
        f"{event.message.text} 根據以上回答 以正面的方式回應我")
    reply_msg = chatgpt.get_response()
    reply_arr.append(TextSendMessage(reply_msg))
    reply_arr.append(TextSendMessage(text))
    line_bot_api.reply_message(event.reply_token, reply_arr)

def process_day12_message(event, chatgpt, line_bot_api):
    reply_arr = []
    text = "如果你準備好了 我們隨時可以進入下一階段的療程了喔 準備好請打<第十三天療程>"
    chatgpt.add_msg(
        f"{event.message.text} 根據以上回答 以正面的方式回應我")
    reply_msg = chatgpt.get_response()
    reply_arr.append(TextSendMessage(reply_msg))
    reply_arr.append(TextSendMessage(text))
    line_bot_api.reply_message(event.reply_token, reply_arr)

def process_day13_message(event, chatgpt, line_bot_api):
    reply_arr = []
    text = "如果你準備好了 我們隨時可以進入下一階段的療程了喔 準備好請打<第十四天療程>"
    chatgpt.add_msg(
        f"{event.message.text} 根據以上回答 以正面的方式回覆")
    reply_msg = chatgpt.get_response()
    reply_arr.append(TextSendMessage(reply_msg))
    reply_arr.append(TextSendMessage(text))
    line_bot_api.reply_message(event.reply_token, reply_arr)

def process_day14_message(event, chatgpt, line_bot_api):
    reply_arr = []
    text = "如果你準備好了 我們隨時可以進入下一階段的療程了喔 準備好請打<第十五天療程>"
    chatgpt.add_msg(
        f"{event.message.text} 根據以上回答 以正面的方式回應我")
    reply_msg = chatgpt.get_response()
    reply_arr.append(TextSendMessage(reply_msg))
    reply_arr.append(TextSendMessage(text))
    line_bot_api.reply_message(event.reply_token, reply_arr)



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

# 处理关注事件
@line_handler.add(FollowEvent)
def handle_follow(event):
    user_id = event.source.user_id
    user_ids.add(user_id)
@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global working_status 
    global received_story
    global isArgreed
    global day4State
    global day5State
    global  weekendState
    global week2day1State
    global day9State
    global readyState
    global day10State
    global day11State
    global day12State
    global day13State
    global day14State
    global chit_chat_State
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
       
    elif event.message.text == "第二天療程":
        handle_day2(event)
        working_status = True
        chit_chat_State =False
        
    elif event.message.text == "第三天療程":
        handle_day3(event)
        working_status = True
    elif event.message.text == "第四天療程":
        handle_day4(event)
        working_status = True
        day4State = True
    elif event.message.text == "第五天療程":
        handle_day5(event)
        working_status = True
        day5State = True
    elif event.message.text == "假日療程":
        handle_weekend(event)
        working_status = True
        weekendState = True
    elif event.message.text == "第二週療程":
        weekendState = False
        handle_week2day1(event)
        working_status = True
        week2day1State = True
    elif event.message.text == "第九天療程":
        week2day1State = False
        handle_day9(event)
        working_status = True
        day9State= True

    elif event.message.text == "我準備好了":
        day9State = False
        handle_readySection(event)
        working_status = True
        readyState= True
    elif event.message.text == "第十天療程":
        readyState = False
        handle_day10(event)
        working_status = True
        day10State= True
    elif event.message.text == "第十一天療程":
        day10State = False
        handle_day11(event)
        working_status = True
        day11State= True
    elif event.message.text == "第十二天療程":
        day11State = False
        handle_day12(event)
        working_status = True
        day12State= True

    elif event.message.text == "第十三天療程":
        day12State = False
        handle_day13(event)
        working_status = True
        day13State= True

    elif event.message.text == "第十四天療程":
        day13State = False
        handle_day14(event)
        working_status = True
        day14State= True


    

    if working_status and isArgreed:
        process_user_story(event, chatgpt, line_bot_api)
        received_story = False
        isArgreed =False
        
    if  working_status and received_story:
        process_user_story(event, chatgpt, line_bot_api)
        received_story = False
        chit_chat_State =True
    
    if working_status and chit_chat_State:
        process_chit_chat(event, chatgpt, line_bot_api)
    

    if working_status and day4State:
        process_day4_message(event, chatgpt, line_bot_api)
        day4State =False
    if working_status and day5State:
        process_day5_message(event, chatgpt, line_bot_api)
        day5State =False
    if working_status and weekendState:
        process_weekend_message(event, chatgpt, line_bot_api)
    if working_status and week2day1State:
        process_week2day1_message(event, chatgpt, line_bot_api)
    if working_status and day9State:
        process_day9_message(event, chatgpt, line_bot_api)
    if working_status and readyState:
        process_ready_message(event, chatgpt, line_bot_api)
    if working_status and day10State:
        process_day10_message(event, chatgpt, line_bot_api)
    if working_status and day11State:
        process_day11_message(event, chatgpt, line_bot_api)
    if working_status and day12State:
        process_day12_message(event, chatgpt, line_bot_api)
    if working_status and day13State:
        process_day13_message(event, chatgpt, line_bot_api)
    if working_status and day14State:
        process_day14_message(event, chatgpt, line_bot_api)



          
   
if __name__ == "__main__":
    app.run()
