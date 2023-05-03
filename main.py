from flask_ngrok import run_with_ngrok
from flask import Flask, request
import det
# 載入 LINE Message API 相關函式庫
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage,TextSendMessage, ImageSendMessage, StickerSendMessage, LocationSendMessage, QuickReply, QuickReplyButton, MessageAction
# 載入 json 標準函式庫，處理回傳的資料格式
import json

app = Flask(__name__)

@app.route("/", methods=['POST'])

def linebot():
    body = request.get_data(as_text=True)                    # 取得收到的訊息內容
    try:
        json_data = json.loads(body)                         # json 格式化訊息內容
        access_token = 'OmnjvUyiZboktlKCJIeSF3mdWC3OMKnsuX7E3cgc1dX31bwOHWIiZXXGPmHAvYy8i2mqLuOUoRwN4aVF8agLEDkHg7ZDWxdbUAZ3YM3B7+m/QR3xTYojes+K9Qc0o9k6hIcq6oG8rsJu6AzVI1TW9AdB04t89/1O/w1cDnyilFU='
        secret = '5a9bf8bb5d2f72508cccb9953347423e'
        line_bot_api = LineBotApi(access_token)              # 確認 token 是否正確
        handler = WebhookHandler(secret)                     # 確認 secret 是否正確
        signature = request.headers['X-Line-Signature']      # 加入回傳的 headers
        handler.handle(body, signature)                      # 綁定訊息回傳的相關資訊
        msg = json_data['events'][0]['message']['text']      # 取得 LINE 收到的文字訊息
        tk = json_data['events'][0]['replyToken']            # 取得回傳訊息的 Token
        if(msg == "start"):
          a =  det.fall_detection(0)
          message = [
                TextSendMessage( #傳文字
                text = "發生跌倒"
                ),
                ImageSendMessage( #傳圖片
                    original_content_url=a,
                    preview_image_url=a
                )]
          #line_bot_api.reply_message(tk,TextSendMessage("發生跌倒 "))
          line_bot_api.reply_message(tk, message)
        else:
          line_bot_api.reply_message(tk,TextSendMessage(msg))  # 回傳訊息
        print(msg, tk)                                       # 印出內容
    except:
        print(body)                                          # 如果發生錯誤，印出收到的內容
    return 'OK'                 # 驗證 Webhook 使用，不能省略
if __name__ == "__main__":
  run_with_ngrok(app)           # 串連 ngrok 服務
  app.run()
  # port = int(os.environ.get('PORT', 5000))
  # app.run(host='0.0.0.0', port=port)