# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 21:16:35 2021
@author: Ivan
版權屬於「行銷搬進大程式」所有，若有疑問，可聯絡ivanyang0606@gmail.com
Line Bot聊天機器人
第四章 選單功能
按鈕樣板TemplateSendMessage
"""
# 載入LineBot所需要的套件
import os
from tryfunction import *
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

import re
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

# 訊息傳遞區塊
##### 基本上程式編輯都在這個function #####


@handler.add(FollowEvent)
def handle_follow(event):
    buttons_template_message = TemplateSendMessage(
        alt_text='這個看不到',
        template=ButtonsTemplate(
            thumbnail_image_url='https://www.posist.com/restaurant-times/wp-content/uploads/2017/04/neon-170182_1920-768x510.jpg',
            title='今晚去哪瑟瑟',
            text='幫你找到最適合的酒吧或旅館，度過激情四射的夜生活！',
            actions=[
                MessageAction(
                    label='點我開始！',
                    text='開始'
                )
            ]
        )
    )
    line_bot_api.reply_message(event.reply_token, buttons_template_message)


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == "開始":
        flex_message = TextSendMessage(text='請選擇此刻的心情吧~',
                                       quick_reply=QuickReply(items=[
                                           QuickReplyButton(action=PostbackAction(
                                               label="歡樂", text="歡樂", data='A&歡樂')),
                                           QuickReplyButton(action=PostbackAction(
                                               label="憂鬱", text="憂鬱", data='A&憂鬱')),
                                           QuickReplyButton(action=PostbackAction(
                                               label="低調", text="低調", data='A&低調')),
                                           QuickReplyButton(action=PostbackAction(
                                               label="奢侈", text="奢侈", data='A&奢侈')),
                                           QuickReplyButton(action=PostbackAction(
                                               label="活力", text="活力", data='A&活力')),
                                           QuickReplyButton(action=PostbackAction(
                                               label="慵懶", text="慵懶", data='A&慵懶'))
                                       ]))
        line_bot_api.reply_message(event.reply_token, flex_message)
    else:
        carousel_template_message = TemplateSendMessage(
            alt_text='免費教學影片',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://cdn2.ettoday.net/images/5540/d5540806.jpg',
                        title='台北福華大飯店',
                        text='02 2700 2323',
                        actions=[
                            URIAction(
                                label='綫上訂房',
                                uri='https://tw.hotels.com/ho114106/tai-bei-fu-hua-da-fan-dian-tai-bei-tai-wan/?chkin=2022-09-06&chkout=2022-09-07&x_pwa=1&rfrr=HSR&pwa_ts=1654770961068&referrerUrl=aHR0cHM6Ly90dy5ob3RlbHMuY29tL0hvdGVsLVNlYXJjaA%3D%3D&useRewards=false&rm1=a2&regionId=3518&destination=%E5%8F%B0%E5%8C%97%2C+%E5%8F%B0%E7%81%A3&destType=MARKET&neighborhoodId=6063187&selected=13054&sort=RECOMMENDED&top_dp=3100&top_cur=TWD&MDPDTL=HTL.13054.20220906.20220907.DDT.89.CID.9899498146.AUDID.&mdpcid=HCOM-TW.META.HPA.HOTEL-CORESEARCH-desktop.HOTEL&gclid=CjwKCAjwtIaVBhBkEiwAsr7-c-QThpo6BUTyrodJncOltyRCG0ndHMyjl9db-nCkZ-F4W4I7DAthtxoCQ2gQAvD_BwE&mctc=10&semdtl=&userIntent=&selectedRoomType=200189906&selectedRatePlan=204547410&expediaPropertyId=13054'
                            ),
                            URIAction(
                                label='帶我去',
                                uri='https://goo.gl/maps/ZpdjAN6FEsSUBm6Y9'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://res.klook.com/image/upload/fl_lossy.progressive,q_85/c_fill/v1611214373/hotel/aktqhvjiypw9d6barcz0.jpg',
                        title='台北遠東香格里拉',
                        text='02 2378 8888',
                        actions=[
                            URIAction(
                                label='綫上訂房',
                                uri='https://tw.hotels.com/ho134169/tai-bei-yuan-dong-xiang-ge-li-la-tai-bei-tai-wan/?chkin=2022-06-23&chkout=2022-06-24&x_pwa=1&rfrr=HSR&pwa_ts=1654770952031&referrerUrl=aHR0cHM6Ly90dy5ob3RlbHMuY29tL0hvdGVsLVNlYXJjaA%3D%3D&useRewards=false&rm1=a2&regionId=3518&destination=%E5%8F%B0%E5%8C%97%2C+%E5%8F%B0%E7%81%A3&destType=MARKET&neighborhoodId=6063187&selected=14153&sort=RECOMMENDED&top_dp=4500&top_cur=TWD&MDPDTL=HTL.14153.20220623.20220624.DDT.14.CID.9899498146.AUDID.&mdpcid=HCOM-TW.META.HPA.HOTEL-CORESEARCH-desktop.HOTEL&gclid=CjwKCAjwtIaVBhBkEiwAsr7-c_CL2-VZ5-s5PIZjTNy2PkIrRiK_dA75gA3xyX4rqLICJzBJyFyX0hoC2cYQAvD_BwE&mctc=10&semdtl=&userIntent=&selectedRoomType=202163329&selectedRatePlan=240224907&expediaPropertyId=14153'
                            ),
                            URIAction(
                                label='帶我去',
                                uri='https://goo.gl/maps/GjV7P5GU6KAdyvCw7'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://img.ltn.com.tw/Upload/news/600/2021/08/27/3652747_1_1.jpg',
                        title='福容大飯店 台北一館',
                        text='02 2701 9266',
                        actions=[
                            URIAction(
                                label='綫上訂房',
                                uri='https://tw.hotels.com/ho308819/fu-rong-da-fan-dian-tai-bei-yi-guan-tai-bei-tai-wan/?chkin=2022-09-06&chkout=2022-09-07&x_pwa=1&rfrr=HSR&pwa_ts=1654771257650&referrerUrl=aHR0cHM6Ly90dy5ob3RlbHMuY29tL0hvdGVsLVNlYXJjaA%3D%3D&useRewards=false&rm1=a2&regionId=3518&destination=%E5%8F%B0%E5%8C%97%2C+%E5%8F%B0%E7%81%A3&destType=MARKET&neighborhoodId=6063187&selected=2436987&sort=RECOMMENDED&top_dp=3238&top_cur=TWD&MDPDTL=HTL.13054.20220906.20220907.DDT.89.CID.9899498146.AUDID.&mdpcid=HCOM-TW.META.HPA.HOTEL-CORESEARCH-desktop.HOTEL&gclid=CjwKCAjwtIaVBhBkEiwAsr7-c-QThpo6BUTyrodJncOltyRCG0ndHMyjl9db-nCkZ-F4W4I7DAthtxoCQ2gQAvD_BwE&mctc=10&semdtl=&userIntent=&selectedRoomType=356771&selectedRatePlan=201498430&expediaPropertyId=2436987'
                            ),
                            URIAction(
                                label='帶我去',
                                uri='https://g.page/fullonhoteltaipei?share'
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(
            event.reply_token, carousel_template_message)


@handler.add(PostbackEvent)
def handle_postback(event):
    if event.postback.data[0:1] == "A":
        mood = event.postback.data[2:]
        buttons_template_message = TemplateSendMessage(
            alt_text='這個看不到',
            template=ButtonsTemplate(
                thumbnail_image_url='https://yhangry.com/wp-content/uploads/2021/11/Wine-1.jpg',
                title='今晚想去哪裡色色？',
                text='請選擇類型',
                actions=[
                    PostbackTemplateAction(
                        label='酒吧',
                        display_text='酒吧',
                        data='B&'+mood+'bar'
                    ),
                    PostbackTemplateAction(
                        label='旅館',
                        display_text='旅館',
                        data='B&'+mood+'hotel'
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template_message)
    elif event.postback.data[0:1] == "B":
        place_type = event.postback.data[4:]
        result = event.postback.data[2:].split('&')
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage('請輸入捷運站名'))


# 主程式
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
