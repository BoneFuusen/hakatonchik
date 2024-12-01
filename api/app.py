from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
import json
from fastapi.middleware.cors import CORSMiddleware
from ml.validation import JsonData
from ml.processing import Processor
from ml.prediction import predict
import codecs

app = FastAPI(
    title="Hakatonchik"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/uploadjson/")
async def upload_json(file: UploadFile = File(...), textOption: str = Form(...)):
    content = await file.read()
    data = json.loads(content)
    data["mobileApp"] = int(data["mobileApp"])
    try:
        JsonData.model_validate(data)

        if data["currentMethod"] != "SMS":
            message_on_entry = "Данный пользователь уже использует один из оптимальных способов подписания документов - рекомендация не требуется"
            message_after_oper = "Данный пользователь уже использует один из оптимальных способов подписания документов - рекомендация не требуется"
            message_before_vip_oper = "Данный пользователь уже использует один из оптимальных способов подписания документов - рекомендация не требуется"
            response = {
                "prediction": -1,
                "message_on_entry": message_on_entry,
                "message_after_oper": message_after_oper,
                "message_before_vip_oper": message_before_vip_oper
            }
            return response
        else:
            message_on_entry = ""
            message_after_oper = ""
            message_before_vip_oper = ""

            proc = Processor(data)
            df = proc.preprocess()
            prediction = predict(df)
            print(prediction)
            match prediction[0]:
                case 1:
                    with codecs.open("./source/message_text.json", encoding='utf-8' , mode="r") as file1:
                        msgjson = json.load(file1)
                        message_on_entry = msgjson["paycontrol"]["base"]["on_entry"]
                        message_after_oper = msgjson["paycontrol"]["base"]["after_oper"]
                        message_before_vip_oper = msgjson["paycontrol"]["base"]["before_vip_oper"]
                case 2:
                    with codecs.open("./source/message_text.json", encoding='utf-8' , mode="r") as file1:
                        msgjson = json.load(file1)
                        message_on_entry = msgjson["paycontrol"]["sms_reported"]["on_entry"]
                        message_after_oper = msgjson["paycontrol"]["sms_reported"]["after_oper"]
                        message_before_vip_oper = msgjson["paycontrol"]["sms_reported"]["before_vip_oper"]
                case 3:
                    with codecs.open("./source/message_text.json", encoding='utf-8' , mode="r") as file1:
                        msgjson = json.load(file1)
                        message_on_entry = msgjson["paycontrol"]["is_available_but_not_used"]["on_entry"]
                        message_after_oper = msgjson["paycontrol"]["is_available_but_not_used"]["after_oper"]
                        message_before_vip_oper = msgjson["paycontrol"]["is_available_but_not_used"]["before_vip_oper"]
                case 4:
                    with codecs.open("./source/message_text.json", encoding='utf-8' , mode="r") as file1:
                        msgjson = json.load(file1)
                        message_on_entry = msgjson["paycontrol"]["no_app"]["on_entry"]
                        message_after_oper = msgjson["paycontrol"]["no_app"]["after_oper"]
                        message_before_vip_oper = msgjson["paycontrol"]["no_app"]["before_vip_oper"]
                case 5:
                    with codecs.open("./source/message_text.json", encoding='utf-8' , mode="r") as file1:
                        msgjson = json.load(file1)
                        message_on_entry = msgjson["CAP"]["base"]["on_entry"]
                        message_after_oper = msgjson["CAP"]["base"]["after_oper"]
                        message_before_vip_oper = msgjson["CAP"]["base"]["before_vip_oper"]
                case 6:
                    with codecs.open("./source/message_text.json", encoding='utf-8' , mode="r") as file1:
                        msgjson = json.load(file1)
                        message_on_entry = msgjson["CAP"]["sms_reported"]["on_entry"]
                        message_after_oper = msgjson["CAP"]["sms_reported"]["after_oper"]
                        message_before_vip_oper = msgjson["CAP"]["sms_reported"]["before_vip_oper"]
                case 7:
                    with codecs.open("./source/message_text.json", encoding='utf-8' , mode="r") as file1:
                        msgjson = json.load(file1)
                        message_on_entry = msgjson["CAP_with_token"]["base"]["on_entry"]
                        message_after_oper = msgjson["CAP_with_token"]["base"]["after_oper"]
                        message_before_vip_oper = msgjson["CAP_with_token"]["base"]["before_vip_oper"]
                case 8:
                    with codecs.open("./source/message_text.json", encoding='utf-8' , mode="r") as file1:
                        msgjson = json.load(file1)
                        message_on_entry = msgjson["CAP_with_token"]["for_employers_with_a_lot_of_orgs"]["on_entry"]
                        message_after_oper = msgjson["CAP_with_token"]["for_employers_with_a_lot_of_orgs"]["after_oper"]
                        message_before_vip_oper = msgjson["CAP_with_token"]["for_employers_with_a_lot_of_orgs"]["before_vip_oper"]
                case 9:
                    with codecs.open("./source/message_text.json", encoding='utf-8' , mode="r") as file1:
                        msgjson = json.load(file1)
                        message_on_entry = msgjson["CAP_with_token"]["sms_reported"]["on_entry"]
                        message_after_oper = msgjson["CAP_with_token"]["sms_reported"]["after_oper"]
                        message_before_vip_oper = msgjson["CAP_with_token"]["sms_reported"]["before_vip_oper"]
                case 10:
                    with codecs.open("./source/message_text.json", encoding='utf-8' , mode="r") as file1:
                        msgjson = json.load(file1)
                        message_on_entry = msgjson["CAP_with_token"]["is_available_but_not_used"]["on_entry"]
                        message_after_oper = msgjson["CAP_with_token"]["is_available_but_not_used"]["after_oper"]
                        message_before_vip_oper = msgjson["CAP_with_token"]["is_available_but_not_used"]["before_vip_oper"]
                case 11:
                    with codecs.open("./source/message_text.json", encoding='utf-8' , mode="r") as file1:
                        msgjson = json.load(file1)
                        message_on_entry = msgjson["CAP"]["has_an_app_but_not_used"]["on_entry"]
                        message_after_oper = msgjson["CAP"]["has_an_app_but_not_used"]["after_oper"]
                        message_before_vip_oper = msgjson["CAP"]["has_an_app_but_not_used"]["before_vip_oper"]

            response = {
                "prediction": int(prediction[0]),
                "message_on_entry": message_on_entry,
                "message_after_oper": message_after_oper,
                "message_before_vip_oper": message_before_vip_oper
            }
            return response
        
        
    except Exception as e:
        print(e)
