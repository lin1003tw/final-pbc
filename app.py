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
        message = event.message.text
        result = location(message)
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=result))


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
                        data='B&bar'
                    ),
                    PostbackTemplateAction(
                        label='旅館',
                        display_text='旅館',
                        data='B&hotel'
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template_message)
    elif event.postback.data[0:1] == "B":
        place_type = event.postback.data[2:]
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage('請輸入捷運站名'))


	
# 蕭-爬googlemap,選出15個選項
import googlemaps
import pandas as pd
import time
google_key = 'AIzaSyB74lRYR0Y-8FGxnFAoW0V8Wv6GEcKmbr8' # fill in your google map api key
gmaps = googlemaps.Client(key=google_key)

# In[61]:

from io import BytesIO
from PIL import Image
def time_transform(row):
    if pd.isna(row):
        return {}
    return row['weekday_text']

def image_transform(row):
    b = row[0]['photo_reference']
    photo = gmaps.places_photo(photo_reference = b, max_width=800, max_height=800)
    photo
    f = BytesIO()
    for chunk in gmaps.places_photo(photo_reference = b, max_width=800, max_height=800):
        if chunk:
            f.write(chunk)
    image = Image.open(f)
    return image


# In[62]:


def find_sex_place(query: str, query_type: str, place_type: str):
    if query_type == 'station':
        ids = []
        results = []
        # Geocoding an address
        geocode_result = gmaps.geocode(query)
        loc = geocode_result[0]['geometry']['location']
        query_result = gmaps.places_nearby(type='bar',location=loc, radius=1000)
        results.extend(query_result['results'])
        while query_result.get('next_page_token'):
            time.sleep(2)
            query_result = gmaps.places_nearby(page_token=query_result['next_page_token'])
            results.extend(query_result['results'])
        #print(f'Number of bars in {query}: {len(results)} (maximum: 60)')
        for place in results:
            ids.append(place['place_id'])
        stores_info = []
        ids = list(set(ids)) 
        for id in ids:
            stores_info.append(gmaps.place(place_id=id, language='zh-TW')['result'])
        #print(f'Total number of bars: {len(stores_info)}')
        taipei_bar = pd.DataFrame.from_dict(stores_info)
        taipei_bar['score'] = taipei_bar['rating'] * taipei_bar['user_ratings_total']
        bar_df = taipei_bar.sort_values('score', ascending=False).head(15)
        bar_df['營業時間'] = bar_df['opening_hours'].apply(time_transform)
        bar_df['圖片'] = bar_df['photos'].apply(image_transform)
        
        ids = []
        results = []
        query_result = gmaps.places_nearby(type='lodging',location=loc, radius=1000)
        results.extend(query_result['results'])
        while query_result.get('next_page_token'):
            time.sleep(2)
            query_result = gmaps.places_nearby(page_token=query_result['next_page_token'])
            results.extend(query_result['results'])
        #print(f'Number of hotels in {query}: {len(results)} (maximum: 60)')
        for place in results:
            ids.append(place['place_id'])
        stores_info = []
        ids = list(set(ids)) 
        for id in ids:
            stores_info.append(gmaps.place(place_id=id, language='zh-TW')['result'])
        #print(f'Total number of hotels: {len(stores_info)}')
        taipei_hotel = pd.DataFrame.from_dict(stores_info)
        taipei_hotel['score'] = taipei_hotel['rating'] * taipei_hotel['user_ratings_total']
        hotel_df = taipei_hotel.sort_values('score', ascending=False).head(15)
        hotel_df['營業時間'] = hotel_df['opening_hours'].apply(time_transform)
        hotel_df['圖片'] = hotel_df['photos'].apply(image_transform)
    else:
        stores_info = gmaps.places(query, language='zh-TW', type='bar')['results']
        #print(f'Total number of bars: {len(stores_info)}')
        taipei_bar = pd.DataFrame.from_dict(stores_info)
        taipei_bar['score'] = taipei_bar['rating'] * taipei_bar['user_ratings_total']
        bar_df = taipei_bar.sort_values('score', ascending=False).head(15)
        bar_df['營業時間'] = bar_df['opening_hours'].apply(time_transform)
        bar_df['圖片'] = bar_df['photos'].apply(image_transform)
        
        stores_info = gmaps.places(query, language='zh-TW', type='lodging')['results']
        #print(f'Total number of hotels: {len(stores_info)}')
        taipei_hotel = pd.DataFrame.from_dict(stores_info)
        taipei_hotel['score'] = taipei_hotel['rating'] * taipei_hotel['user_ratings_total']
        hotel_df = taipei_hotel.sort_values('score', ascending=False).head(15)
        hotel_df['營業時間'] = hotel_df['opening_hours'].apply(time_transform)
        hotel_df['圖片'] = hotel_df['photos'].apply(image_transform)
        
    if place_type == 'A&bar':
        return bar_df
    elif place_type == 'A&hotel':
        return hotel_df
    return pd.concat([bar_df, hotel_df])


# In[63]:
a = find_sex_place(query = result[1], query_type = 'station', place_type = result[0])
a.head(5)

#妤文
def star_count(rating_num): #依評價顯示星星的函數
    if rating_num >= 4.5:
        "contents":[ 
              {
                "type": "icon",
                "size": "xs",
                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
              }*5,
              {
                "type": "text",
                "text": "5.0",
                "size": "xs",
                "color": "#8c8c8c",
                "margin": "md",
                "flex": 0
              }
            ]
    elif 3.5 <= rating_num < 4.5:
        "contents":[ 
              {
                "type": "icon",
                "size": "xs",
                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
              }*4,
              {
                "type": "icon",
                "size": "xs",
                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png"
              },
              {
                "type": "text",
                "text": "4.0",
                "size": "xs",
                "color": "#8c8c8c",
                "margin": "md",
                "flex": 0
              }
            ]            
    elif 2.5 <= rating_num < 3.5:
        "contents":[ 
              {
                "type": "icon",
                "size": "xs",
                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
              }*3,
              {
                "type": "icon",
                "size": "xs",
                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png"
              }*2,
              {
                "type": "text",
                "text": "3.0",
                "size": "xs",
                "color": "#8c8c8c",
                "margin": "md",
                "flex": 0
              }
            ]
    elif 1.5 <= rating_num < 2.5:
        "contents":[ 
              {
                "type": "icon",
                "size": "xs",
                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
              }*2,
              {
                "type": "icon",
                "size": "xs",
                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png"
              }*3,
              {
                "type": "text",
                "text": "2.0",
                "size": "xs",
                "color": "#8c8c8c",
                "margin": "md",
                "flex": 0
              }
            ]
    elif rating_num < 1.5:
        "contents":[ 
              {
                "type": "icon",
                "size": "xs",
                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
              }*1,
              {
                "type": "icon",
                "size": "xs",
                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png"
              }*4,
              {
                "type": "text",
                "text": "1.0",
                "size": "xs",
                "color": "#8c8c8c",
                "margin": "md",
                "flex": 0
              }
            ]
		
def callback():
# get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
# get request body as text body = request.get_data(as_text=True) app.logger.info("Request body: " + body) # handle webhook body try:     handler.handle(body, signature) except InvalidSignatureError:     abort(400) return 'OK'
# 訊息傳遞區塊
# 基本上程式編輯都在這個function
@handler.add(MessageEvent, message=TextMessage)
def order_reply(rank): #選擇訂房方式
    message = text = event.message.text
    if re.match('我要訂房',message)
        flex_message = TextSendMessage(text='請選擇訂房方式',
                            quick_reply=QuickReply(items=[
                                QuickReplyButton(action=MessageAction(label="電話預訂", text=output.iloc[rank]['formatted_phone_number'])),
                                QuickReplyButton(action=MessageAction(label="線上預訂", text=output.iloc[rank]['website'])),
                            ]))
        line_bot_api.reply_message(event.reply_token, flex_message)
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))
        
@handler.add(MessageEvent, message=TextMessage)
def three_handle_message_1(event): #推薦三個旅館/酒吧
    output = find_sex_place(query=result[1], query_type='station', place_type=result[0]),
    message = text=event.message.text
     #if re.match('告訴我秘密',message):
         # Flex Message Simulator網頁：https://developers.line.biz/console/fx/
         #flex_message = FlexSendMessage(
             #alt_text='行銷搬進大程式',
    contents={
    "type": "carousel",
    "contents": [
    { 
      "type": "bubble", #旅館01
      "size": "micro",
      "hero": {
        "type": "image", #https://xdasu.com/2018/06/08/python-%e4%bd%bf%e7%94%a8google-map-api6-%e5%8f%96%e5%be%97%e7%85%a7%e7%89%87/
        "url": output.iloc[0]['圖片'], #主圖01*
        "size": "full",
        "aspectMode": "cover",
        "aspectRatio": "320:213"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": output.iloc[0]['name'], #飯店名
            "weight": "bold",
            "size": "sm",
            "wrap": True
          },
          {
            "type": "box",
            "layout": "baseline",
            "contents": star_num(output.iloc[0]['rating']) #評價
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "text": "地址："+str(output.iloc[0]['formatted_address']), 
                    "wrap": True,
                    "color": "#8c8c8c",
                    "size": "xs",
                    "flex": 5
                  }
                ]
              },
              {
                "type": "text",
                "text": output.iloc[0]['business_status'], #營業狀態
                "wrap": True,
                "color": "#8c8c8c",
                "size": "xs",
                "flex": 5
              },
              {
                "type": "text",
                "text": "營業時間"+str(output.iloc[0]['營業時間']), #營業時間01*
                "wrap": True,
                "color": "#8c8c8c",
                "size": "xs",
                "flex": 5
              }
              
            ]
          }
        #兩個按鈕
        "footer": { 
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
              {
                "type": "button",
                "style": "link",
                "height": "sm",
                "action": {
                  "type": "uri",
                  "label": "看更多",
                  "uri": "https://linecorp.com" #網址01*
                }
              },
              {
                "type": "button",
                "style": "link",
                "height": "sm",
                "action": {
                  "type": "message",
                  "label": "我要訂房",
                  "text": "訂房方式", #跳出訂房方式:線上/電話
                  "data":result[0], output.iloc[0]['name'] 
		  order_reply(0)
                }
              }
            ],
            "flex": 0
          }          
        ],
        "spacing": "sm",
        "paddingAll": "13px"
      }
    },
    #旅館02
    {
      "type": "bubble",
      "size": "micro",
      "hero": {
        "type": "image",
        "url": output.iloc[1]['圖片'], #主圖02
        "size": "full",
        "aspectMode": "cover",
        "aspectRatio": "320:213"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": output.iloc[1]['name'],
            "weight": "bold",
            "size": "sm",
            "wrap": True
          },
          {
            "type": "box",
            "layout": "baseline",
            "contents":star_num(output.iloc[1]['rating'])
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "text": "地址："+str(output.iloc[1]['formatted_address']),
                    "wrap": True,
                    "color": "#8c8c8c",
                    "size": "xs",
                    "flex": 5
                  }
                ]
              },
              {
                "type": "text",
                "text":output.iloc[1]['business_status'],
                "wrap": True,
                "color": "#8c8c8c",
                "size": "xs",
                "flex": 5
              },
              {
                "type": "text",
                "text": "營業時間"+str(output.iloc[1]['營業時間']),
                "wrap": True,
                "color": "#8c8c8c",
                "size": "xs",
                "flex": 5
              }
            ]
          }
        #兩個按鈕
         "footer": { 
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
              {
                "type": "button",
                "style": "link",
                "height": "sm",
                "action": {
                  "type": "uri",
                  "label": "看更多",
                  "uri": "https://linecorp.com"
                }
              },
              {
                "type": "button",
                "style": "link",
                "height": "sm",
                "action": {
                  "type": "message",
                  "label": "我要訂房",
                  "text": "我要訂房" #跳出訂房方式:線上/電話
                  "data":result[0], output.iloc[1]['name'] 
                  order_reply(1)
                }
              }
            ],
            "flex": 0
      }
        ],
        "spacing": "sm",
        "paddingAll": "13px"
      }
    },
    #旅館03
    {
      "type": "bubble",
      "size": "micro",
      "hero": {
        "type": "image",
        "url": output.iloc[2]['圖片'], #主圖03
        "size": "full",
        "aspectMode": "cover",
        "aspectRatio": "320:213"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": output.iloc[2]['name'],
            "weight": "bold",
            "size": "sm"
            "wrap": True
          },
          {
            "type": "box",
            "layout": "baseline",
            "contents": star_num(output.iloc[2]['rating']) 
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "text": "地址："+str(output.iloc[2]['formatted_address']),
                    "wrap": True,
                    "color": "#8c8c8c",
                    "size": "xs",
                    "flex": 5
                  }
                ]
              },
              {
                "type": "text",
                "text": output.iloc[2]['business_status'],
                "wrap": True,
                "color": "#8c8c8c",
                "size": "xs",
                "flex": 5
              },
              {
                "type": "text",
                "text": "營業時間"+str(output.iloc[2]['營業時間']),
                "wrap": True,
                "color": "#8c8c8c",
                "size": "xs",
                "flex": 5
              }
            ]
          }
        ],
        "spacing": "sm",
        "paddingAll": "13px"
      },
    #兩個按鈕
     "footer": {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
          {
            "type": "button",
            "style": "link",
            "height": "sm",
            "action": {
              "type": "uri",
              "label": "看更多",
              "uri": "https://linecorp.com"
            }
          },
          {
            "type": "button",
            "style": "link",
            "height": "sm",
            "action": {
              "type": "message",
              "label": "我要訂房",
              "text": "我要訂房" #跳出訂房方式:線上/電話
              "data":result[0], output.iloc[2]['name'] 
              order_reply(2)
              
            }
          }
        ],
        "flex": 0
      }
    }
    ]
} #json
         line_bot_api.reply_message(event.reply_token, flex_message)
         result = event.postback.data
'''
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
        line_bot_api.push_message('Ud6ce2036c8854221694d3f33b3b796c3', TemplateSendMessage(
            alt_text = '給一組心情選項',
            template = ButtonsTemplate(
                text = '這間飯店給你的感覺偏向？',
                action = [
                    PostbackTemplateAction(
                        label = mood_dict[times],
                        text = '', #看有沒有要回覆訊息
                        mood_review_h = 0
                    ),
                    PostbackTemplateAction(
                        label = mood_dict[times + 1],
                        text = '', #看有沒有要回覆訊息
                        mood_review_h = 1
                    ),
                    PostbackTemplateAction(
                        label = '略過',
                        text = '', #看有沒有要回覆訊息
                        mood_review_h = 999
                    ),
                ]
            )
        )

        if mood_review_h < 6: # if 要評論， mood_review 只會有0-5的 int
            hotel_list[hotel][1][mood_review_h][0] += 1
            answer_more_than_one += 1
            # 使用者編號下的貢獻分數加一，還沒寫

elif where == 1: # 只去了酒吧

# 三組心情選項
    for times in range(0, 4, 2): # range 內的數字要跟著心情有幾種調整
        line_bot_api.push_message('Ud6ce2036c8854221694d3f33b3b796c3', TemplateSendMessage(
            alt_text = '給一組心情選項',
            template = ButtonsTemplate(
                text = '這間酒吧給你的感覺偏向？',
                action = [
                    PostbackTemplateAction(
                        label = mood_dict[times],
                        text = '', #看有沒有要回覆訊息
                        mood_review_h = times 
                    ),
                    PostbackTemplateAction(
                        label = mood_dict[times + 1],
                        text = '', #看有沒有要回覆訊息
                        mood_review_h = times + 1
                    ),
                    PostbackTemplateAction(
                        label = '略過',
                        text = '', #看有沒有要回覆訊息
                        mood_review_h = 999
                    ),
                ]
            )
        )


        if mood_review_b < 6: # if 要評論， mood_review 只會有0-5的 int
            bar_list[bar][1][mood_review_b][0] += 1
            answer_more_than_one += 1
            # 使用者編號下的貢獻分數加一，還沒寫


else: # 去了飯店＋酒吧

# 三組心情選項
    for times in range(0, 4, 2): # range 內的數字要跟著心情有幾種調整
        line_bot_api.push_message('Ud6ce2036c8854221694d3f33b3b796c3', TemplateSendMessage(
            alt_text = '給一組心情選項',
            template = ButtonsTemplate(
                text = '這間飯店給你的感覺偏向？',
                action = [
                    PostbackTemplateAction(
                        label = mood_dict[times],
                        display_text = '', #看有沒有要回覆訊息
                        mood_review_h = times
                    ),
                    PostbackTemplateAction(
                        label = mood_dict[times + 1],
                        text = '', #看有沒有要回覆訊息
                        mood_review_h = times + 1
                    ),
                    PostbackTemplateAction(
                        label = '略過',
                        text = '', #看有沒有要回覆訊息
                        mood_review_h = 999
                    ),
                ]
            )
        )

        if mood_review_h < 6: # if 要評論， mood_review 只會有0-5的 int
            hotel_list[hotel][1][mood_review_h][0] += 1
            answer_more_than_one += 1
            # 使用者編號下的貢獻分數加一，還沒寫

# 三組心情選項
    for times in range(0, 4, 2): # range 內的數字要跟著心情有幾種調整
        line_bot_api.push_message('Ud6ce2036c8854221694d3f33b3b796c3', TemplateSendMessage(
            alt_text = '給一組心情選項',
            template = ButtonsTemplate(
                text = '這間酒吧給你的感覺偏向？',
                action = [
                    PostbackTemplateAction(
                        label = mood_dict[times],
                        text = '', #看有沒有要回覆訊息
                        mood_review_h = times
                    ),
                    PostbackTemplateAction(
                        label = mood_dict[times + 1],
                        text = '', #看有沒有要回覆訊息
                        mood_review_h = times + 1
                    ),
                    PostbackTemplateAction(
                        label = '略過',
                        text = '', #看有沒有要回覆訊息
                        mood_review_h = 999
                    ),
                ]
            )
        )


        if mood_review_b < 6: # if 要評論， mood_review 只會有0-5的 int
            bar_list[bar][1][mood_review_b][0] += 1
            answer_more_than_one += 1
            # 使用者編號下的貢獻分數加一，還沒寫

if answer_more_than_one >= 1:
    line_bot_api.push_message('Ud6ce2036c8854221694d3f33b3b796c3',TextSendMessage(text='感謝您的回答'))
else:
    line_bot_api.push_message('Ud6ce2036c8854221694d3f33b3b796c3',TextSendMessage(text='下次記得評論喔！'))
'''
# 主程式
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
