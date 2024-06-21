from django.shortcuts import render, HttpResponse,redirect
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import json
# from .Text_process import data
# from .Text_process import openaiCode as ai
from .Text_process import LangChain as lc
# from .Text_process import runnableChainNestedIntent as lc
from django.http import HttpResponse
# from .Image_process import Pipeline as pp
# from .Image_process import Pipeline_matching as pp
import sys as pp
# from .Image_process import Yolo_Tags as yt
# import django.conf.settings
# import pyaudio
# import speech_recognition as sr
import requests
import random
import string
import re
# from chat_app.models import Products
# name =""

def index(request):
    return render(request, "home.html")

@csrf_exempt
def produceMessage(request):
    if request.method=="POST":
        print("produceMessage Called!")
        name = request.POST['name']
        return HttpResponse(json.dumps({'status':200,'message': "message send successfully!"}), content_type='application/json')
    return HttpResponse(json.dumps({'status':400,'error': "error"}), content_type='application/json')

@csrf_exempt
def getUserInfo(request):
    response_data = {}

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    print("User IP is : "+ip)
    response_data['User IP'] = ip

    user_agent = request.META.get('HTTP_USER_AGENT', '')
    if 'Windows' in user_agent:
        response_data['OS'] = "Windows"
    elif 'Mac' in user_agent:
        response_data['OS'] = "Mac"
    elif 'Linux' in user_agent:
        response_data['OS'] = "Linux"
    else:
        response_data['OS'] = "Unknown"

    response_data['System Name'] = request.get_host()
    response = HttpResponse(json.dumps(response_data), content_type="application/json")
    return response

@csrf_exempt
def setcookie(request,key="user-name",name="first Name"):
    response = HttpResponse("Cookie Set")
    response.set_cookie(key, name)
    print("cookie key : ",key)
    print("cookie Name : ",name)
    return response


@csrf_exempt
def userSession(request,userId="without use id"):
    print(userId)
    request.session['user_name'] = "Mr. Jamnani"
    user_name = request.session.get('user_name')
    print(user_name)
    return render(request, 'temp.html',{"user_name":user_name,"id":userId})

@csrf_exempt
def chat_view(request): #Loading page(Firest Page)
    '''Main page load, returens html page.'''
    theme="light"
    try:
        theme=request.COOKIES['theme']
    except:
        print("error in cookie read")
        # setcookie(request,"theme",theme)
        # pass
    # global name
    if request.method=="POST":
        name = request.POST['name']
        print("cookie value",name)
        # return redirect("/screen")
        return redirect("/scookie/"+name)
    print(theme)
    if theme=='light':
        imgSVG="imgs/moon.svg"
    else:
        imgSVG="imgs/sun.svg"
    print(imgSVG)
    # return render(request, 'index.html',{"theme":{"css":"css/"+theme+"-theme.css",'img': imgSVG}})
    return HttpResponse(json.dumps({"status":200,"message":"chatbot run successfull"}), content_type='application/json')



@csrf_exempt
def chat_screen_view(request):
    theme="light"
    try:
        email=request.COOKIES['user-name']
        try:
            theme=request.COOKIES['theme']
        except:
            pass
    except:
        return redirect(chat_view)

    # print(userId)
    name = email.split(".")[0].title()
    print("Page load User Name = ", name)
    return render(request, 'chat_screen.html',{"name":name,"email":email,"theme":{"css":"css/"+theme+"-theme.css",'img':"imgs/moon.svg" if theme=='light' else "imgs/sun.svg"}})

def getProducts(request, query):
    products = [{"id":data.productId,"name":data.productName,"image":data.displayImage,"price":data.price,"currency":data.currency} for data in Products.objects.raw(query)]
    return products,products

# lc.set_cate_list(data)
@csrf_exempt
def send_message(request): # User Question and Answer to front end connection point
    print('send message function is called')
    if request.method == 'POST':
        sender = request.POST['sender']
        isImage = request.POST['isImage']
        tMsg = request.POST['tagMsg']
        hist = request.POST['history']

        # reply = {
        #     "text":[],
        #     "all_img":{
        #         "fix_img":[{"id":data.productId,"name":data.productName,"image":data.displayImage,"price":data.price,"currency":data.currency} for data in Products.objects.raw("SELECT * FROM chat_app_products where productId < 4;")[:4]],
        #         "img":[{"id":data.productId,"name":data.productName,"image":data.displayImage,"price":data.price,"currency":data.currency} for data in Products.objects.all()[4:]]
        #         }
        # }
        # return HttpResponse(json.dumps({'status':200,'time':datetime.now().isoformat(),'sender': sender, 'content': reply, "detail_data":reply}), content_type='application/json')
        if tMsg != "":
            hist = hist[:-2]+',"reply":"'+tMsg+'"}"'

        print("History:",hist,"-"*20,">")
        client_ip = request.META.get('REMOTE_ADDR')
        imgName = sender+"_"+datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        content = request.POST['content']

        print("content:",content,"+"*20,">")

        if eval(isImage):
            print("Image called","-"*50)
            imag = request.FILES["image"]
            with open("static/imgs/uploads/"+str(imgName)+".png", "wb") as image_file:
                image_file.write(imag.read())

            if 'match' in content.lower() or 'pair' in content.lower():
                print("Match call")
                img_path = "static/imgs/uploads/"+str(imgName)+".png"
                img_response,param_text,model_tags = pp.pipeline("static/imgs/uploads/"+imgName+".png")
                print(model_tags)
                gptReply,timestamp,detail_data = gptReply,timestamp,detail_data = lc.intent("Suggest me Pair product for given Attributes:"+str(model_tags),sender)
                # ai.match(model_tags,sender,client_ip,hist,data)
                #match(text,sender,client_ip,hist,data)
                # data.show()
                pass
            elif 'tag' in content.lower() or 'attribute' in content.lower() or 'feature' in content.lower():
                param_text ="This is Image tags"
                img_path = "static/imgs/uploads/"+str(imgName)+".png"
                # text = pp.Yolo_Tags(img_path)
                response = pp.Yolo_Tags(img_path)
                print("Response :::::::::: ", response)
                text=""
                for tag_lst in response:
                    att = tag_lst.split(":")[1].split(",")
                    text = "<b>"+att[-5]+":</b>"
                    text += "<li>"+tag_lst.split(":")[0]+"</li>"
                    for attrb in att[:-5]:
                        text += "<li>"+attrb+"</li>"
                    clr = ",".join(att[-3:])
                    text += "<li><div style='display:inline-block;height:20px;width:50px;border:1px solid black;background-color:rgb"+clr.strip()+"'></div></li>"
                    text += "<br>"

                if 'description' in content.lower() or 'detail' in content.lower():
                    desc = ai.desc(response[0],sender,client_ip,hist,data)#content,sender,client_ip,hist,data
                    print("Descript",desc,"="*100)
                    text += "<span style='text-align:justify'>"+desc+"</span>"
                reply,timestamp,detail_data = json.dumps({"text": [text]}),datetime.now().strftime("%Y-%m-%d %H:%M:%S"),str(text)
                print("input tags")
            else :
                img_response,param_text,mode_tags = pp.pipeline("static/imgs/uploads/"+imgName+".png")
                print("ans","="*10,img_response)
                # print("ans of pram text","="*10,param_text)
                del param_text[0]['crop_img']
                # print("ans of pram text","="*10,param_text)
                keyword_str = str(mode_tags[0][0])+": "+", ".join(mode_tags[0][1:])
                print("keywords from image :",keyword_str)
                try:
                    recom_img = data.show(keyword_str,1)
                    img_response[0][0][1] = recom_img
                except Exception as e:
                    print("error at ",e)
                # reply,timestamp,detail_data = json.dumps({"all_img": img_response}),datetime.now().strftime("%Y-%m-%d %H:%M:%S"),str("static/imgs/uploads/"+imgName+".png")
                # reply,timestamp,detail_data = json.dumps({"all_img": img_response}),datetime.now().strftime("%Y-%m-%d %H:%M:%S"),keyword_str
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                textMessages=[]
                imgss  = {"fix_img":img_response[:4],"img":img_response[4:]}
                reply = {"text":textMessages,"all_img":imgss}
                detail_data = {"text":textMessages,"all_img":"imgss"}
                # timestamp = "2024-02-21 10:07:48"
                print(reply,timestamp,detail_data)
                return HttpResponse(json.dumps({'status':200,'time':timestamp,'sender': sender, 'content': reply, "detail_data":detail_data}), content_type='application/json')

        else:
            # reply,timestamp,detail_data = ai.intent(content,sender,client_ip,hist,data) ## personal api use
            gptReply,timestamp,detail_data = lc.intent(content,sender) ## personal api use
            # reply,timestamp,detail_data = data.show(content,sender),datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"text search" ## personal api use
            # gptReply,timestamp,detail_data = 'Recommendation: ["Flower_name":["rose roses"], "Colour":["White"]]',"2024-02-21 10:07:48",'Recommendation: ["Flower_name":["rose roses"], "Colour":["White"]]'
        print("reply ","==="*10,gptReply)
        print("detail_data ","==="*10,detail_data)
        print("time stemp ",timestamp)

        #It will find the reconnedation pattern in GPT generated text message user Regex
        gptReply = str(gptReply).replace("\\", "")
        pattern = r'SELECT\s+.*?\s+FROM\s+.*?(?:;|$)'
        match = re.search(pattern, gptReply)

        if match:
            textReply=  match.group()

            print("TExt rexply by Regex : ", textReply)
            # products = fetchProduct(request,textReply)
            products = getProducts(request,textReply)
            print("Product len",len(products[0]),len(products[1]),products)
            if products=="Error" or len(products)==0:
                print("product not found")
                reply = json.dumps({"text":["Product Not Found"]})
                detail_data = "Product Not Found"
                # timestamp = "2024-02-21 10:07:48"
                return HttpResponse(json.dumps({'status':200,'time':timestamp,'sender': sender, 'content': reply, "detail_data":detail_data}), content_type='application/json')
            otherProduct = []
            for p in products[1]:
                if p not in products[0]:
                    otherProduct.append(p)
            print("other Products","*********"*10,otherProduct)
            textMessages  = [i for i in gptReply.split(textReply) if len(i.strip())>0] # It will find or split text except Recommendation pattern
            # textMessages = ["this is first message", "This is second message"]
            imgss  = {"fix_img":products[0],"img":otherProduct}
            reply = {"text":textMessages,"all_img":imgss}
            detail_data = {"text":textReply,"all_img":"imgss"}
            # timestamp = "2024-02-21 10:07:48"
            print("Final output reply:",reply)
            return HttpResponse(json.dumps({'status':200,'time':timestamp,'sender': sender, 'content': reply, "detail_data":detail_data}), content_type='application/json')
        
        # Split Question like in Curious with Shopping
        match = re.search(r'\[.*?\]', gptReply)
        # print()
        if match:
            q = match.group()
            ans = [gptReply.replace(q,"").strip(),q.split(":")[1].strip()[:-1]]
        else:
            ans = [gptReply]
        reply = {"text":ans,"all_img":{}}
        detail_data = {"text":ans,"all_img":"imgss"}
        return HttpResponse(json.dumps({'status':200,'time':timestamp,'sender': sender, 'content': reply, "detail_data":detail_data}), content_type='application/json')
    return HttpResponse(json.dumps({'status':400,'error': "error"}), content_type='application/json')

@csrf_exempt
def updateProduct(request):
    if request.method =="POST":
        inputData  = {
            "updateBy":request.POST["updateBy"],
            "attibutes":request.POST["attibutes"],
            "updateAttributes":request.POST["updateAttributes"],

        }
        
        print("update Product",inputData)
        if inputData['updateBy']=="filter":
            if inputData["updateAttributes"].split("=")[0]=="Price":
                r = inputData["updateAttributes"].split("=")
                if 'range(' in inputData["updateAttributes"]:
                    fltr = {r[0]:{"gte":float(r[1].split(",")[0].split('(')[1]),"lte":float(r[1].split(",")[1][:-1]),}}
                else:
                    fltr = {"term":  { r[0]: r[1] }}#Issue

        gptReply = str(inputData["attibutes"]).replace("\\", "")
        pattern = r'Recommendation:\{.*?\}'
        match = re.search(pattern, gptReply)

        if match:
            textReply=  match.group()

            print("new TExt rexply by Regex : ", textReply)
            if inputData['updateBy']=="filter":
                print("product filtering")
                products = fetchProduct(request,textReply,{"filter":fltr})
            elif inputData['updateBy']=="Shuffle":
                print("Product Shuffleing")
                products = fetchProduct(request,textReply,{"Shuffle":10})

            if products=="Error" or len(products)==0:
                print("product not found")
                reply = json.dumps({"text":["Product Not Found"]})
                detail_data = "Product Not Found"
                return HttpResponse(json.dumps({'status':200,'content': reply, "detail_data":detail_data}), content_type='application/json')
            otherProduct = []
            for p in products[1]:
                if p not in products[0]:
                    otherProduct.append(p)
            imgss  = {"fix_img":products[0],"img":otherProduct}
            reply = {"text":"","all_img":imgss}
            detail_data = {"text":"","all_img":"imgss"}
            # timestamp = "2024-02-21 10:07:48"
            print("Final output reply:",reply)
            return HttpResponse(json.dumps({'status':200,'content': reply, "detail_data":detail_data}), content_type='application/json') 
        return HttpResponse(json.dumps({'status':200,'msg':"Stored Sucessfuly! but filter not worked"}), content_type='application/json')
    return HttpResponse(json.dumps({'status':400,'msg':"Stored Sucessfuly!"}), content_type='application/json')

@csrf_exempt
def feedback(request): # Feedbacks from user for reply and likes for product connection point
    if request.method == 'POST':
        store = request.POST['store']
        username = request.POST['username']

        if store == "feedback":
            log_entry = {"feedback_time":request.POST['feedback_time'],"username":username,"feedback_options":request.POST['feedback_options'],"feedback_text":request.POST['feedback_text']}
        elif store == "like":
            log_entry = {"img_options":request.POST['img_options'] ,"img_time":request.POST['img_time'],"username":username,"img_link":request.POST['img_link'],"record_time":datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

        print(store+'_log.log',log_entry,"\n")
        # with open("logs/"+store+'_log.log', 'a') as log_file:
        #     log_file.write(json.dumps(log_entry) + '\n')
        return HttpResponse(json.dumps({'status':200,'msg':"Stored Sucessfuly!"}), content_type='application/json')
    return HttpResponse(json.dumps({'status':400,'error': "feeback write errir : not in post method"}), content_type='application/json')

@csrf_exempt
def getFeedbackForm(request):
    theme="light"
    try:
        theme=request.COOKIES['theme']
    except:
        pass
    # if request.method == 'POST':

    #     name=request.COOKIES['user-name']
    #     data = {
    #         "email":name,
    #         "q1":request.POST['satisfiedRange'],
    #         "q2":request.POST['relevantDetail'],
    #         "q3":request.POST['misinterpretedImage'],
    #         "q4":request.POST['startRate'],
    #         "q5":request.POST['technicalIssue'],
    #         "q6":request.POST['experience'],
    #         "q7":request.POST['feedback_text'],
    #         "q8":request.POST['comment']
    #     }

    #     print("Post mathod is called",data)
    #     print('feedbackform_log.log',data,"\n")
    #     with open("logs/"+'feedbackform_log.log', 'a') as log_file:
    #         log_file.write(json.dumps(data) + '\n')
    #     # return redirect(request, 'index.html')
    #     return redirect('chat')
    return render(request, 'feedBack.html',{"name":"name","theme":{"css":"css/"+theme+"-theme.css",'img':"imgs/moon.svg" if theme=='light' else "imgs/sun.svg"}})
    # return render(request, 'chat_screen.html',{"name":'name'})


# r=sr.Recognizer()
# r.energy_threshold=4000
# @csrf_exempt
# def recordVoice(request):
    if request.method == 'POST':
        name=request.COOKIES['user-name']
        data = {"email":name}
        print("Function recoding called")
        with sr.Microphone() as source:
            audio=r.listen(source)
        try:
            # print("Speech was:" + r.recognize_google(audio,language='en-IN'))
            return HttpResponse(json.dumps({'status':200,'text':r.recognize_google(audio,language='en-IN')}), content_type='application/json')
        except LookupError:
            return HttpResponse(json.dumps({'status':400,'error': "Call record Issue : api not working"}), content_type='application/json')
        # return HttpResponse(json.dumps({'status':200,'msg':"Stored Sucessfuly!"}), content_type='application/json')
    return HttpResponse(json.dumps({'status':400,'error': "Call record Issue : not in post method"}), content_type='application/json')