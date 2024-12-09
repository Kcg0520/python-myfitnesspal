from flask import Flask, request, abort
from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    TemplateMessage,
    ConfirmTemplate,
    ButtonsTemplate,
    CarouselTemplate,
    CarouselColumn,
    ImageCarouselTemplate,
    ImageCarouselColumn,
    MessageAction,
    URIAction,
    PostbackAction,
    DatetimePickerAction,
    CameraAction,
    CameraRollAction,
    LocationAction
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,PostbackEvent,
    FollowEvent,PostbackContent
)
import myfitnesspal
import matplotlib.pyplot as plt
import numpy as np
app = Flask(__name__)
caltotal=[]
proteintotal=[]
fattotal=[]
carbstotal=[]
sodiumtotal=[]
sugartotal=[]
basicinfo=[]
standard=[]
alltotal=[]
stlist=[]
texttotal=[]
configuration = Configuration(access_token='LVxXjG26WuhUSgarsuaJBzFw0TJoTJGxtM6IIL8YRC2DlYaz1Cb0QXGtBKfVKdkzyUx86bYPlM4pkYrz5vRpVrYHLD77e5et0kQ7xszaptKHWykCOWEHZdUu9XWnOlc4BwEQI94egYUXEm9T9/HQYAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('886804d12908edd8cff134dc251d1b88')
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
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'
                   
@handler.add(PostbackEvent)
def handle_postback(event):
    with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
        
            if event.postback.data == 'breakfast':
                text_message=TextMessage(text='請輸入早餐品項，請開頭輸入我的早餐:作為提示語，早餐可依序描述名稱、品牌')
                line_bot_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[text_message]
                    )
                )
            if event.postback.data == 'lunch':
                text_message=TextMessage(text='請輸入午餐品項，請開頭輸入我的午餐:作為提示語，午餐可依序描述名稱、品牌')
                line_bot_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[text_message]
                    )
                )
            if event.postback.data == 'dinner':
                text_message=TextMessage(text='請輸入晚餐品項，請開頭輸入我的晚餐:作為提示語，晚餐可依序描述名稱、品牌')
                line_bot_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[text_message]
                    )
                )
            if event.postback.data == 'snack':
                text_message=TextMessage(text='請輸入點心品項，請開頭輸入我的點心:作為提示語，點心可依序描述名稱、品牌')
                line_bot_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[text_message]
                    )
                )
            
#初次使用者
@handler.add(FollowEvent)
def handle_follow(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        text_message=TextMessage(text='歡迎使用本聊天機器人，請輸入您的身高以開屎輸入基本資料')

        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[text_message]
            ))
    
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        text=event.message.text
        if event.message.text == '性別':
            buttons_template = ButtonsTemplate(
                title='請選擇您的生理性別',
                text='性別選擇',
                actions=[
                    PostbackAction(label='男', text='男性', data='gender=male'),
                    PostbackAction(label='女', text='女性',data='gender=female')
                    ]
                )
            template_message = TemplateMessage(
                alt_text='Postback Sample',
                template=buttons_template
                
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[template_message]))
        if event.message.text=='男性' or event.message.text=='女性':
            if event.message.text == '男性':
                standardcal=10*int(basicinfo[0])+6.25*int(basicinfo[1])-5*(int(basicinfo[2]))+5
                standard.append(standardcal)
            elif event.message.text == '女性':
                standardcal=10*float(basicinfo[0])+6.25*float(basicinfo[1])-5*float(basicinfo[2])-161
                standard.append(standardcal)
            text_message=TextMessage(text='基本資料輸入完成!可輸入"餐點登錄"以開始記錄您的飲食習慣')
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[text_message]
                )
            )
        
            
        elif '身高' in event.message.text:
            height=''.join(i for i in event.message.text if i.isdigit())
            text_message=TextMessage(text='請接續輸入您的體重(需含我的"體重"此關鍵字)')
            height_message=TextMessage(text='您的身高為'+height+'cm')
            messages_all=[height_message,text_message]
            basicinfo.append(height)
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=messages_all
                )
            )
            
        elif '體重' in event.message.text:
            weight=''.join(i for i in event.message.text if i.isdigit())
            text_message=TextMessage(text='請接續輸入您的年紀(需含我的"年紀"此關鍵字)')
            weight_message=TextMessage(text='您的體重為'+weight+'kg')
            messages_all=[weight_message,text_message]
            basicinfo.append(weight)
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=messages_all
                )
            )
            
        elif '年紀' in event.message.text or '年齡' in event.message.text or '歲' in event.message.text:
            age=''.join(i for i in event.message.text if i.isdigit())
            age_message=TextMessage(text='您的年齡為'+age+'歲')
            text_message=TextMessage(text='輸入成功!請輸入關鍵字"性別"已開啟選擇頁面')
            messages_all=[age_message,text_message]
            basicinfo.append(age)
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=messages_all
            
                )
            )
        #加入預先的設定標準
        # Buttons Template
        elif '餐點登錄' in text:
            url = request.url_root + 'static/Logo.jpg'
            url = url.replace("http", "https")
            app.logger.info("url=" + url)
            buttons_template = ButtonsTemplate(
                thumbnail_image_url=url,
                title='餐點登錄',
                text='今日輸入完成後，可輸入"總表"、"標準"、"分析"以查看今日營養素攝取建議',
                actions=[
                    # URIAction(label='連結', uri='https://www.facebook.com/NTUEBIGDATAEDU'),
                    # PostbackAction(label='回傳值', data='ping', displayText='傳了'),
                    # MessageAction(label='傳"哈囉"', text='哈囉'),
                    # DatetimePickerAction(label="選擇時間", data="時間", mode="datetime"),
                    PostbackAction(label='早餐',data='breakfast',text='請輸入早餐品項，請開頭輸入我的午餐:作為提示語，午餐可依序描述名稱、品牌'),
                    PostbackAction(label='午餐',data='lunch',text='請輸入午餐品項，請開頭輸入我的午餐:作為提示語，午餐可依序描述名稱、品牌'),
                    PostbackAction(label='晚餐',data='dinner',text='請輸入晚餐品項，請開頭輸入我的晚餐:作為提示語，晚餐可依序描述名稱、品牌'),
                    PostbackAction(label='點心',data='snack',text='請輸入點心品項，請開頭輸入我的點心:作為提示語，點心可依序描述名稱、品牌')
                ]
            )
            template_message = TemplateMessage(
                alt_text="This is a buttons template",
                template=buttons_template
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[template_message]
                )
            )

            
       
        elif '早餐' in event.message.text:
            breakfast = text.replace('早餐', '').strip()
            client = myfitnesspal.Client()
            food_items = client.get_food_search_results(breakfast)
            try:
                cals=str(food_items[0].calories)
            except KeyError:
                cals='NA'
            try:    
                protein=str(food_items[0].protein)
            except KeyError:
                protein='NA'
            try:
                fat=str(food_items[0].fat)
            except KeyError:
                fat='NA'
            try:
                carbs=str(food_items[0].carbohydrates)
            except KeyError:
                carbs='NA'
            try:
                sodium=str(food_items[0].sodium)
            except KeyError:
                sodium='NA'
            try:
                sugar=str(food_items[0].sugar)
            except KeyError:
                sugar='NA'
            if cals != 'NA':
                caltotal.append(float(cals))
            if protein != 'NA':
                proteintotal.append(float(protein))
            if fat != 'NA':
                fattotal.append(float(fat))
            if carbs != 'NA':
                carbstotal.append(float(carbs))
            if sodium != 'NA':
                sodiumtotal.append(float(sodium))
            if sugar != 'NA':
                sugartotal.append(float(sugar))
            
            text_message=TextMessage(text='您的早餐為'+breakfast+'\n，營養成分如下:\n熱量:'+cals+'大卡\n蛋白質:'+protein+'g\n脂肪:'+fat+'g\n碳水化合物:'+carbs+'g\n鈉:'+sodium+'mg\n糖:'+sugar+'g')
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[text_message]
                    ))
        elif '午餐' in event.message.text:
            breakfast = text.replace('午餐', '').strip()
            client = myfitnesspal.Client()
            food_items = client.get_food_search_results(breakfast)
            try:
                cals=str(food_items[0].calories)
            except KeyError:
                cals='NA'
            try:    
                protein=str(food_items[0].protein)
            except KeyError:
                protein='NA'
            try:
                fat=str(food_items[0].fat)
            except KeyError:
                fat='NA'
            try:
                carbs=str(food_items[0].carbohydrates)
            except KeyError:
                carbs='NA'
            try:
                sodium=str(food_items[0].sodium)
            except KeyError:
                sodium='NA'
            try:
                sugar=str(food_items[0].sugar)
            except KeyError:
                sugar='NA'
            if cals != 'NA':
                caltotal.append(float(cals))
            if protein != 'NA':
                proteintotal.append(float(protein))
            if fat != 'NA':
                fattotal.append(float(fat))
            if carbs != 'NA':
                carbstotal.append(float(carbs))
            if sodium != 'NA':
                sodiumtotal.append(float(sodium))
            if sugar != 'NA':
                sugartotal.append(float(sugar))
            text_message=TextMessage(text='您的午餐為'+breakfast+'\n，營養成分如下:\n熱量:'+cals+'大卡\n蛋白質:'+protein+'g\n脂肪:'+fat+'g\n碳水化合物:'+carbs+'g\n鈉:'+sodium+'mg\n糖:'+sugar+'g')
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[text_message]
                    ))
        elif '晚餐' in event.message.text:
            breakfast = text.replace('早餐', '').strip()
            client = myfitnesspal.Client()
            food_items = client.get_food_search_results(breakfast)
            try:
                cals=str(food_items[0].calories)
            except KeyError:
                cals='NA'
            try:    
                protein=str(food_items[0].protein)
            except KeyError:
                protein='NA'
            try:
                fat=str(food_items[0].fat)
            except KeyError:
                fat='NA'
            try:
                carbs=str(food_items[0].carbohydrates)
            except KeyError:
                carbs='NA'
            try:
                sodium=str(food_items[0].sodium)
            except KeyError:
                sodium='NA'
            try:
                sugar=str(food_items[0].sugar)
            except KeyError:
                sugar='NA'
            if cals != 'NA':
                caltotal.append(float(cals))
            if protein != 'NA':
                proteintotal.append(float(protein))
            if fat != 'NA':
                fattotal.append(float(fat))
            if carbs != 'NA':
                carbstotal.append(float(carbs))
            if sodium != 'NA':
                sodiumtotal.append(float(sodium))
            if sugar != 'NA':
                sugartotal.append(float(sugar))
          
            text_message=TextMessage(text='您的晚餐為'+breakfast+'\n，營養成分如下:\n熱量:'+cals+'大卡\n蛋白質:'+protein+'g\n脂肪:'+fat+'g\n碳水化合物:'+carbs+'g\n鈉:'+sodium+'mg\n糖:'+sugar+'g')
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[text_message]
                    ))
        elif '點心' in event.message.text:
            breakfast = text.replace('點心', '').strip()
            client = myfitnesspal.Client()
            food_items = client.get_food_search_results(breakfast)
            try:
                cals=str(food_items[0].calories)
            except KeyError:
                cals='NA'
            try:    
                protein=str(food_items[0].protein)
            except KeyError:
                protein='NA'
            try:
                fat=str(food_items[0].fat)
            except KeyError:
                fat='NA'
            try:
                carbs=str(food_items[0].carbohydrates)
            except KeyError:
                carbs='NA'
            try:
                sodium=str(food_items[0].sodium)
            except KeyError:
                sodium='NA'
            try:
                sugar=str(food_items[0].sugar)
            except KeyError:
                sugar='NA'
            if cals != 'NA':
                caltotal.append(float(cals))
            if protein != 'NA':
                proteintotal.append(float(protein))
            if fat != 'NA':
                fattotal.append(float(fat))
            if carbs != 'NA':
                carbstotal.append(float(carbs))
            if sodium != 'NA':
                sodiumtotal.append(float(sodium))
            if sugar != 'NA':
                sugartotal.append(float(sugar))
            text_message=TextMessage(text='點心'+breakfast+'\n，營養成分如下:\n熱量:'+cals+'大卡\n蛋白質:'+protein+'g\n脂肪:'+fat+'g\n碳水化合物:'+carbs+'g\n鈉:'+sodium+'mg\n糖:'+sugar+'g')
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[text_message]
                    ))
        elif '總表' in event.message.text:
            totalcal=str(round(sum(caltotal),2))
            totalprotein=str(round(sum(proteintotal),2))
            totalfat=str(round(sum(fattotal),2))
            totalcarbs=str(round(sum(carbstotal),2))
            totalsodium=str(round(sum(sodiumtotal),2))
            totalsugar=str(round(sum(sugartotal),2))
            alltotal.extend([sum(caltotal),sum(proteintotal),sum(fattotal),sum(carbstotal),sum(sodiumtotal),sum(sugartotal)])
            text_message=TextMessage(text='您今日的總熱量為'+str(alltotal[0])+'大卡\n總蛋白質為'+str(alltotal[1])+'g\n總脂肪為'+totalfat+'g\n總碳水化合物為'+totalcarbs+'g\n總鈉為'+totalsodium+'mg\n總糖分為'+totalsugar+'g')
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[text_message]
                    )) 
            
        elif '標準' in event.message.text:
            standardprotein=0.8*float(basicinfo[1])
            standardfat=0.3*standard[0]/9
            standardcarbs=(standard[0]-standardprotein*4-standardfat*9)/4
            stlist.extend([standard[0],standardprotein,standardfat,standardcarbs,2400,50])
            text_message=TextMessage(text='您的各項營養素標準:\n'+'熱量為'+str(round(standard[0],2))+'大卡\n蛋白質為'+str(round(standardprotein,2))+'g\n脂肪為'+str(round(standardfat,2))+'g\n碳水化合物為'+str(round(standardcarbs,2))+'g\n鈉為'+str(2400)+'mg\n糖分為'+str(50)+'g')
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[text_message]
                    ))
        elif'分析' in event.message.text:
                if alltotal[0]/stlist[0] > 1.3:
                    text_message=('您的熱量嚴重超標!，請修改您的飲食計畫!')
                    texttotal.append(text_message)
                if alltotal[0]/stlist[0] > 1.1 and alltotal[0]/stlist[0] < 1.3:
                    text_message=('您的熱量略微超標!，請注意飲食習慣')
                    texttotal.append(text_message)
                if alltotal[0]/stlist[0] > 0.9 and alltotal[0]/stlist[0] < 1.1:
                    text_message=('您的熱量正常!，請繼續保持')
                    texttotal.append(text_message)
                if alltotal[0]/stlist[0] < 0.9 and alltotal[0]/stlist[0] > 0.7:
                    text_message=('您的熱量略微不足!，請注意飲食習慣')
                    texttotal.append(text_message)
                if alltotal[0]/stlist[0] < 0.7:
                    text_message=('您的熱量嚴重不足!，請修改您的飲食計畫!')
                    texttotal.append(text_message)
                if alltotal[1]/stlist[1] > 1.3:
                    text_message=('您的蛋白質嚴重超標!，請修改您的飲食計畫!')
                    texttotal.append(text_message)
                if alltotal[1]/stlist[1] > 1.1 and alltotal[1]/stlist[1] < 1.3:
                    text_message=('您的蛋白質略微超標!，請注意飲食習慣')
                    texttotal.append(text_message)
                if alltotal[1]/stlist[1] > 0.9 and alltotal[1]/stlist[1] < 1.1:
                    text_message=('您的蛋白質正常!，請繼續保持')
                    texttotal.append(text_message)
                if alltotal[1]/stlist[1] < 0.9 and alltotal[1]/stlist[1] > 0.7:
                    text_message=('您的蛋白質略微不足!，請注意飲食習慣')
                    texttotal.append(text_message)
                if alltotal[1]/stlist[1] < 0.7:
                    text_message=('您的蛋白質嚴重不足!，請修改您的飲食計畫!')
                    texttotal.append(text_message)
                if alltotal[2]/stlist[2] > 1.3:
                    text_message=('您的脂肪嚴重超標!，請修改您的飲食計畫!')
                    texttotal.append(text_message)
                if alltotal[2]/stlist[2] > 1.1 and alltotal[2]/stlist[2] < 1.3:
                    text_message=('您的脂肪略微超標!，請注意飲食習慣')
                    texttotal.append(text_message)
                if alltotal[2]/stlist[2] > 0.9 and alltotal[2]/stlist[2] < 1.1:
                    text_message=('您的脂肪正常!，請繼續保持')
                    texttotal.append(text_message)
                if alltotal[2]/stlist[2] < 0.9 and alltotal[2]/stlist[2] > 0.7:
                    text_message=('您的脂肪略微不足!，請注意飲食習慣')
                    texttotal.append(text_message)
                if alltotal[2]/stlist[2] < 0.7:
                    text_message=('您的脂肪嚴重不足!，請修改您的飲食計畫!')
                    texttotal.append(text_message)
                if alltotal[3]/stlist[3] > 1.3:
                    text_message=('您的碳水化合物嚴重超標!，請修改您的飲食計畫!')
                    texttotal.append(text_message)
                if alltotal[3]/stlist[3] > 1.1 and alltotal[3]/stlist[3] < 1.3:
                    text_message=('您的碳水化合物略微超標!，請注意飲食習慣')
                    texttotal.append(text_message)
                if alltotal[3]/stlist[3] > 0.9 and alltotal[3]/stlist[3] < 1.1:
                    text_message=('您的碳水化合物正常!，請繼續保持')
                    texttotal.append(text_message)
                if alltotal[3]/stlist[3] < 0.9 and alltotal[3]/stlist[3] > 0.7:
                    text_message=('您的碳水化合物略微不足!，請注意飲食習慣')
                    texttotal.append(text_message)
                if alltotal[3]/stlist[3] < 0.7:
                    text_message=('您的碳水化合物嚴重不足!，請修改您的飲食計畫!')
                    texttotal.append(text_message)
                if alltotal[4]/stlist[4] > 1.3:
                    text_message=('您的鈉嚴重超標!，請修改您的飲食計畫!')
                    texttotal.append(text_message)
                if alltotal[4]/2400 > 1.1 and alltotal[4]/2400 < 1.3:
                    text_message=('您的鈉略微超標!，請注意飲食習慣')
                    texttotal.append(text_message)
                if alltotal[4]/2400 > 0.9 and alltotal[4]/2400 < 1.1:
                    text_message=('您的鈉正常!，請繼續保持')
                    texttotal.append(text_message)
                if alltotal[4]/2400 < 0.9 and alltotal[4]/2400> 0.7:
                    text_message=('您的鈉略微不足!，請注意飲食習慣')
                    texttotal.append(text_message)
                if alltotal[4]/stlist[4] < 0.7:
                    text_message=('您的鈉嚴重不足!，請修改您的飲食計畫!')
                    texttotal.append(text_message)
                if alltotal[5]/stlist[5] > 1.3:
                    text_message=('您的糖分嚴重超標!，請修改您的飲食計畫!')
                    texttotal.append(text_message)
                if alltotal[5]/stlist[5] > 1.1 and alltotal[5]/stlist[5] < 1.3:
                    text_message=('您的糖分略微超標!，請注意飲食習慣')
                    texttotal.append(text_message)
                if alltotal[5]/stlist[5] > 0.9 and alltotal[5]/stlist[5] < 1.1:
                    text_message=('您的糖分正常!，請繼續保持')
                    texttotal.append(text_message)
                if alltotal[5]/stlist[5] < 0.9 and alltotal[5]/stlist[5] > 0.7:
                    text_message=('您的糖分略微不足!，請注意飲食習慣')
                    texttotal.append(text_message)
                if alltotal[5]/stlist[5] < 0.7:
                    text_message=('您的糖分嚴重不足!，請修改您的飲食計畫!')
                    texttotal.append(text_message)
                message=TextMessage(text=texttotal[0]+'\n'+texttotal[1]+'\n'+texttotal[2]+'\n'+texttotal[3]+'\n'+texttotal[4]+'\n'+texttotal[5])
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[message]
                        ))
                 
                
  
                
                
            

            
            
  











        

       
if __name__ == "__main__":
    app.run()