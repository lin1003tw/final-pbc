# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 21:16:35 2021
@author: Ivan
版權屬於「行銷搬進大程式」所有，若有疑問，可聯絡ivanyang0606@gmail.com

Line Bot聊天機器人
第一章 Line Bot申請與串接
Line Bot機器人串接與測試
"""
#載入LineBot所需要的套件
import os
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('9pIVzQsUEI08RidYJzOwaZPDLNbneY9dIDHddgvx5MZu2PJkWH6nz9kue7wt56SNxogCf+p5D+WpmW0nrHZ1vY5LRnOytVROJ+8m0Q/cXMoRzi+8ZvkWuNeGokAYcOZhu4c/1M/fJTA7raGxPtV91wdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('21d57c590dcdfe2564cc65574fdc8724')

line_bot_api.push_message('Ud6ce2036c8854221694d3f33b3b796c3', TextSendMessage(text='你可以開始了'))


# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

 
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

 
#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####

# 
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = text = event.message.text
    if re.match('開始', message):
        buttons_template_message = TemplateSendMessage(
            alt_text='這個看不到',
            template=ButtonsTemplate(
                title='Menu',
                text='請選擇類型',
                actions=[
                    PostbackTemplateAction(
                        label='酒吧',
                        text='酒吧'
                        data='A&酒吧'
                    ),
                    PostbackTemplateAction(
                        label='旅館',
                        text='旅館'
                        data='A&旅館'
                    ),
                    PostbackTemplateAction(
                        label='全都要',
                        text='全都要'
                        data='A&全都要'
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template_message)
    elif message == '酒吧' or message == '旅館' or message == '全都要':
        bar_or_hotel = event.postback.data[2:]
        flex_message = TextSendMessage(text='請輸入台北市的任意地區（區或街道），或點擊下列的快捷鍵選擇地區',  # （暫時只能做到有選項，無法自由填入）
                                       quick_reply=QuickReply(items=[
                                            QuickReplyButton(action=PostbackAction(
                                                label="中正區", text="中正區", data='B&' + bar_or_hotel + '&中正區')),
                                            QuickReplyButton(action=PostbackAction(
                                                label="萬華區", text="萬華區", data='B&' + bar_or_hotel + '&萬華區')),
                                            QuickReplyButton(action=PostbackAction(
                                                label="大同區", text="大同區", data='B&' + bar_or_hotel + '&大同區')),
                                            QuickReplyButton(action=PostbackAction(
                                                label="中山區", text="中山區", data='B&' + bar_or_hotel + '&中山區')),
                                            QuickReplyButton(action=PostbackAction(
                                                label="松山區", text="松山區", data='B&' + bar_or_hotel + '&松山區')),
                                            QuickReplyButton(action=PostbackAction(
                                                label="大安區", text="大安區", data='B&' + bar_or_hotel + '&大安區')),
                                            QuickReplyButton(action=PostbackAction(
                                                label="信義區", text="信義區", data='B&' + bar_or_hotel + '&信義區')),
                                            QuickReplyButton(action=PostbackAction(
                                                label="內湖區", text="內湖區", data='B&' + bar_or_hotel + '&內湖區')),
                                            QuickReplyButton(action=PostbackAction(
                                                label="南港區", text="南港區", data='B&' + bar_or_hotel + '&南港區')),
                                            QuickReplyButton(action=PostbackAction(
                                                label="士林區", text="士林區", data='B&' + bar_or_hotel + '&士林區')),
                                            QuickReplyButton(action=PostbackAction(
                                                label="北投區", text="北投區", data='B&' + bar_or_hotel + '&北投區')),
                                            QuickReplyButton(action=PostbackAction(
                                                label="文山區", text="文山區", data='B&' + bar_or_hotel + '&文山區')),
                                       ]))
        line_bot_api.reply_message(event.reply_token, flex_message)
    else:
        result = event.postback.data[2:].split('&')
	
# 蕭

# 妤

# 効 Review Part
# input

# 心情標籤 Dict
mood_dict ={0:'歡樂', 1:'憂鬱', 2:'低調', 3:'奢侈', 4:'活力', 5:'慵懶'}

# 以每間 hotels & bars 編號，建list
# 心情類別[評論數(預設為0),心情編號(0-5)] list
mood_list = []

for mood in range(6): # 假設有六種心情
    mood_list.append([0, mood])

# hotels 1371間，編號0-1370
hotel_list = []

for hotel in range(1514):
	hotel_list.append([hotel, mood_list])

# bars 1513間，編號0-1512
bar_list = []

for bar in range(1514):
	bar_list.append([bar, mood_list])

# 三個變數都是系統要自動記錄

where = int(input()) # 0 for hotels(預設), 1 for bars, others for both，系統要在使用者去了飯店或酒吧後紀錄他去了哪裡
hotel = int(input()) # hotel 編號，系統紀錄使用者去了哪間飯店
bar = int(input()) # bar 編號，系統紀錄使用者去了哪間酒吧，沒去就隨便紀



# operation 評論紀錄系統
answer_more_than_one = 0
mood_review_h = 999
mood_review_b = 999
line_bot_api.push_message('Ud6ce2036c8854221694d3f33b3b796c3',TextSendMessage(text='評論可以拿優惠券喔'))

# 因為Line Bot 有限制選項數目，所以拆成兩倆＋略過，共三組選項問使用者
if where == 0: # 只去了飯店

# 三組心情選項
    for times in range(0, 4, 2): # range 內的數字要跟著心情有幾種調整
        confirm_template_message = TemplateSendMessage(
            alt_text = '給一組心情選項',
            template = ConfirmTemplate(
                text = '這間飯店給你的感覺偏向？',
                action = [
                    PostbackAction(
                        label = mood_dict[times],
                        display_text = '', #看有沒有要回覆訊息
                        mood_review_h = 0
                    ),
                    PostbackAction(
                        label = mood_dict[times + 1],
                        display_text = '', #看有沒有要回覆訊息
                        mood_review_h = 1
                    ),
                    PostbackAction(
                        label = '略過',
                        display_text = '', #看有沒有要回覆訊息
                        mood_review_h = 999
                    ),
                ]
            )
        )

        if mood_review_h < 6: # if 要評論， mood_review 只會有0-5的 int
            hotel_list[hotel][1][mood_review_h][0] += 1
            answer_more_than_one += 1
            # 使用者編號下的貢獻分數加一，還沒寫
        '''else:
            line_bot_api.push_message('Ud6ce2036c8854221694d3f33b3b796c3',TextSendMessage(text='剛剛錯過了W hotel 免費入住一晚兌換券，真可惜')) # 也可以什麼都不講'''

elif where == 1: # 只去了酒吧

# 三組心情選項
    for times in range(0, 4, 2): # range 內的數字要跟著心情有幾種調整
        confirm_template_message = TemplateSendMessage(
            alt_text = '給一組心情選項',
            template = ConfirmTemplate(
                text = '這間酒吧給你的感覺偏向？',
                action = [
                    PostbackAction(
                        label = mood_dict[times],
                        display_text = '', #看有沒有要回覆訊息
                        mood_review_h = times 
                    ),
                    PostbackAction(
                        label = mood_dict[times + 1],
                        display_text = '', #看有沒有要回覆訊息
                        mood_review_h = times + 1
                    ),
                    PostbackAction(
                        label = '略過',
                        display_text = '', #看有沒有要回覆訊息
                        mood_review_h = 999
                    ),
                ]
            )
        )


        if mood_review_b < 6: # if 要評論， mood_review 只會有0-5的 int
            bar_list[bar][1][mood_review_b][0] += 1
            answer_more_than_one += 1
            # 使用者編號下的貢獻分數加一，還沒寫
        '''else:
            line_bot_api.push_message('Ud6ce2036c8854221694d3f33b3b796c3',TextSendMessage(text='你剛剛錯過了免費調酒兌換券，真可惜')) # 也可以什麼都不講'''

else: # 去了飯店＋酒吧

# 三組心情選項
    for times in range(0, 4, 2): # range 內的數字要跟著心情有幾種調整
        confirm_template_message = TemplateSendMessage(
            alt_text = '給一組心情選項',
            template = ConfirmTemplate(
                text = '這間飯店給你的感覺偏向？',
                action = [
                    PostbackAction(
                        label = mood_dict[times],
                        display_text = '', #看有沒有要回覆訊息
                        mood_review_h = times
                    ),
                    PostbackAction(
                        label = mood_dict[times + 1],
                        display_text = '', #看有沒有要回覆訊息
                        mood_review_h = times + 1
                    ),
                    PostbackAction(
                        label = '略過',
                        display_text = '', #看有沒有要回覆訊息
                        mood_review_h = 999
                    ),
                ]
            )
        )

        if mood_review_h < 6: # if 要評論， mood_review 只會有0-5的 int
            hotel_list[hotel][1][mood_review_h][0] += 1
            answer_more_than_one += 1
            # 使用者編號下的貢獻分數加一，還沒寫
        '''else:
            line_bot_api.push_message('Ud6ce2036c8854221694d3f33b3b796c3',TextSendMessage(text='剛剛錯過了W hotel 免費入住一晚兌換券，真可惜')) # 也可以什麼都不講'''

# 三組心情選項
    for times in range(0, 4, 2): # range 內的數字要跟著心情有幾種調整
        confirm_template_message = TemplateSendMessage(
            alt_text = '給一組心情選項',
            template = ConfirmTemplate(
                text = '這間酒吧給你的感覺偏向？',
                action = [
                    PostbackAction(
                        label = mood_dict[times],
                        display_text = '', #看有沒有要回覆訊息
                        mood_review_h = times
                    ),
                    PostbackAction(
                        label = mood_dict[times + 1],
                        display_text = '', #看有沒有要回覆訊息
                        mood_review_h = times + 1
                    ),
                    PostbackAction(
                        label = '略過',
                        display_text = '', #看有沒有要回覆訊息
                        mood_review_h = 999
                    ),
                ]
            )
        )


        if mood_review_b < 6: # if 要評論， mood_review 只會有0-5的 int
            bar_list[bar][1][mood_review_b][0] += 1
            answer_more_than_one += 1
            # 使用者編號下的貢獻分數加一，還沒寫
        '''else:
            line_bot_api.push_message('Ud6ce2036c8854221694d3f33b3b796c3',TextSendMessage(text='你剛剛錯過了免費調酒兌換券，真可惜')) # 也可以什麼都不講'''

if answer_more_than_one >= 1:
    line_bot_api.push_message('Ud6ce2036c8854221694d3f33b3b796c3',TextSendMessage(text='感謝您的回答'))
else:
    line_bot_api.push_message('Ud6ce2036c8854221694d3f33b3b796c3',TextSendMessage(text='下次記得評論喔！'))

# 主程式
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
