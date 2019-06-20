from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os
import requests
import pprint
import urllib.request as req
import sys
from bs4 import BeautifulSoup
from apiclient import discovery
#from oauth2client.service_account import ServiceAccountCredentials
#from calendar import GoogleCalendar
#from datetime import datetime, timedelta
#import email.utils
#import traceback
#import httplib2
#import logging

app = Flask(__name__)

#from __future__ import print_function
 
#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body" + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

cnt = 0

#def handle_message(event):
#    line_bot_api.reply_message(
#        event.reply_token,
#        TextSendMessage(text=event.message.text))


@handler.add(MessageEvent, message=TextMessage)

def handle_message(event):
    global cnt
    global sum

    #入力された文字列を格納
    push_text = event.message.text
    reply_text = ""

    #リプライする文字列
    if "今日の天気" in push_text and cnt == 0:
        #tenki.jpの名古屋市のURL
        url0 = "https://tenki.jp/forecast/5/26/5110/23100/"
        url1 = "https://tenki.jp/indexes/dress/5/26/5110/"

        r0 = req.urlopen(url0)
        r1 = req.urlopen(url1)

        soup0 = BeautifulSoup(r0, "lxml")
        soup1 = BeautifulSoup(r1, "lxml")

        #今日・明日の天気の取得
        today = soup0.find(class_ = "today-weather")
        weather0 = today.p.string

        #服装情報の取得
        dress = soup1.find(class_ = "today-weather")

        #気象情報のまとまり
        temp0 = today.div.find(class_ = "date-value-wrap")

        # 服装情報の取得
        dress_info = dress.find_all("p")
        dress_str = dress_info[2].string

        #気温の取得
        temp0 = temp0.find_all("dd")

        #今日の分
        temp_max0 = temp0[0].span.string #最高気温
        temp_max_diff0 = temp0[1].string #最高気温の前日比
        temp_min0 = temp0[2].span.string #最低気温
        temp_min_diff0 = temp0[3].string #最低気温の前日比

        print("今日の名古屋の天気：{}".format(weather0))
        print("最高気温：{}℃ {}".format(temp_max0, temp_max_diff0))
        print("最低気温：{}℃ {}".format(temp_min0, temp_min_diff0))
        print("服装のアドバイス：{}".format(dress_str))

        text0 = "今日の名古屋の天気：{}\n".format(weather0)
        text1 = "最高気温：{}℃ {}\n".format(temp_max0, temp_max_diff0)
        text2 = "最低気温：{}℃ {}\n".format(temp_min0, temp_min_diff0)
        text3 = "服装のアドバイス：{}".format(dress_str)
        reply_text = text0 + text1 + text2 + text3

    elif "明日の天気" in push_text and cnt == 0:
        #tenki.jpの名古屋市のURL
        url0 = "https://tenki.jp/forecast/5/26/5110/23100/"
        url1 = "https://tenki.jp/indexes/dress/5/26/5110/"

        r0 = req.urlopen(url0)
        r1 = req.urlopen(url1)

        soup0 = BeautifulSoup(r0, "lxml")
        soup1 = BeautifulSoup(r1, "lxml")

        tomorrow = soup0.find(class_ = "tomorrow-weather")
        weather1 = tomorrow.p.string

        temp1 = tomorrow.div.find(class_ = "date-value-wrap")
        temp1 = temp1.find_all("dd")

        #服装情報の取得
        dress = soup1.find(class_ = "tomorrow-weather")
        dress_info = dress.find_all("p")
        dress_str = dress_info[2].string

        #明日の分
        temp_max1 = temp1[0].span.string #最高気温
        temp_max_diff1 = temp1[1].string #最高気温の前日比
        temp_min1 = temp1[2].span.string #最低気温
        temp_min_diff1 = temp1[3].string #最低気温の前日比

        print("明日の名古屋の天気：{}".format(weather1))
        print("最高気温：{}℃ {}".format(temp_max1, temp_max_diff1))
        print("最低気温：{}℃ {}".format(temp_min1, temp_min_diff1))
        print("服装のアドバイス：{}".format(dress_str))

        text0 = "明日の名古屋の天気：{}\n".format(weather1)
        text1 = "最高気温：{}℃ {}\n".format(temp_max1, temp_max_diff1)
        text2 = "最低気温：{}℃ {}\n".format(temp_min1, temp_min_diff1)
        text3 = "服装のアドバイス：{}".format(dress_str)
        reply_text = text0 + text1 + text2 + text3

    #elif "今日の予定" in push_text and cnt == 0:
        #calendar = GoogleCalendar()
        #calendar_id = 'sumiyou1997@gmail.com'

        #time_min = datetime.now()
        #time_max = time_min + timedelta(days=1)

        #event = calendar.get_schedule(calendar_id, time_min, time_max)

        #reply_text = "{}\t{}".format(event["start"]["date"], event["summary"])


    elif "電車" in push_text and cnt == 0:
        # 0:JR東海道線 
        # 1:名古屋市営地下鉄東山線
        # 2:名古屋市営地下鉄名城線
        info0 = ""
        info1 = ""
        info2 = ""

        url0 = "https://transit.yahoo.co.jp/traininfo/detail/192/193/"
        url1 = "https://transit.yahoo.co.jp/traininfo/detail/240/0/"
        url2 = "https://transit.yahoo.co.jp/traininfo/detail/241/0/"
        res0 = req.urlopen(url0)
        res1 = req.urlopen(url1)
        res2 = req.urlopen(url2)
        soup0 = BeautifulSoup(res0, "lxml")
        soup1 = BeautifulSoup(res1, "lxml")
        soup2 = BeautifulSoup(res2, "lxml")

        train0 = soup0.select_one("#main > div.mainWrp > div.labelLarge > h1").text
        train1 = soup1.select_one("#main > div.mainWrp > div.labelLarge > h1").text
        train2 = soup2.select_one("#main > div.mainWrp > div.labelLarge > h1").text
        
        print(train0 + "\n")
        print(train1 + "\n")
        print(train2)
        status0 = soup0.select_one("#mdServiceStatus > dl > dt").text
        status1 = soup1.select_one("#mdServiceStatus > dl > dt").text
        status2 = soup2.select_one("#mdServiceStatus > dl > dt").text
        print(status0 + "\n")
        print(status1 + "\n")
        print(status2)

        if not status0 == "[○]平常運転":
            info0 = soup0.select_one("#mdServiceStatus > dl > dd > p").text
            info0 = "\n" + str(info0)
            print(info0)
        if not status1 == "[○]平常運転":
            info1 = soup1.select_one("#mdServiceStatus > dl > dd > p").text
            info1 = "\n" + str(info1)
            print(info1)
        if not status2 == "[○]平常運転":
            info2 = soup2.select_one("#mdServiceStatus > dl > dd > p").text
            info2 = "\n" + str(info2)
            print(info1)

        reply_text4 = str(train0) + "\n" + str(status0) + info0
        reply_text5 = str(train1) + "\n" + str(status1) + info1
        reply_text6 = str(train2) + "\n" + str(status2) + info2
        reply_text = "現在の運行状況です\n" +  reply_text4 + "\n" + reply_text5 + "\n" + reply_text6

    elif "給与登録" in push_text and cnt == 0:
        reply_text = "本日の給与を数字で入力してください"
        cnt = cnt + 1

    elif push_text.isdecimal() == True and cnt == 1:
        f = open('salary.txt', 'r')
        sum = f.read()
        sum = int(sum) + int(push_text)
        f.close()
        f = open('salary.txt', 'w')
        f.write(str(sum) + "\n")
        f.close()
        reply_text = "登録が完了しました！\n今日現在で合計" + str(sum) + "円です\n今日もお疲れ様でした！"
        cnt = 0

    elif push_text.isdecimal() == False and cnt == 1:
        reply_text = "数字だけで入力してください..."

    elif "今月の給料" in push_text and cnt == 0:
        f = open('salary.txt', 'r')
        sum = f.read()
        f.close()
        reply_text = "今日までの給料は" + str(sum) + "円です！"

    else:
        text0 = "使い方\n"
        text1 = "天気が知りたいとき：\n「今日の天気」、「明日の天気」が含まれる文を送信してください\n"
        text2 = "運行状況が知りたいとき：\n「電車」が含まれる文を送信してください\n"
        text3 = "今日の給料を登録したいとき：\n「給与登録」が含まれる文を送信してください\n"
        text4 = "今月の給料を確認したいとき：\n「今月の給料」が含まれる文を送信してください"
        reply_text = text0 + text1 + text2 + text3 + text4

    
    #リプライ部分の記述
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text = reply_text))
    
if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
