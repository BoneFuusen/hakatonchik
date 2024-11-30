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
    allow_origins=["http://localhost:3000"],  # Разрешаем доступ с Front-End
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/uploadjson/")
async def upload_json(file: UploadFile = File(...), textOption: str = Form(...)):
    content = await file.read()
    data = json.loads(content)

    try:
        JsonData.model_validate(data)

        if data["currentMethod"] != "SMS":
            pass
            #NO ADVICES
        else:
            message_on_entry = ""
            message_after_oper = ""
            message_before_vip_oper = ""

            proc = Processor(data)
            df = proc.preprocess()
            prediction = predict(df)
            match prediction[0]:
                case 1:
                    with open("source/message_text.json", "r") as file1:
                        msgjson = json.load(file1)
                        message_on_entry = msgjson["paycontrol"]["base"]["on_entry"]
                        message_after_oper = msgjson["paycontrol"]["base"]["after_oper"]
                        message_before_vip_oper = msgjson["paycontrol"]["base"]["before_vip_oper"]
                case 2:
                    with open("source/message_text.json", "r") as file1:
                        msgjson = json.load(file1)
                        message_on_entry = msgjson["paycontrol"]["sms_reported"]["on_entry"]
                        message_after_oper = msgjson["paycontrol"]["sms_reported"]["after_oper"]
                        message_before_vip_oper = msgjson["paycontrol"]["sms_reported"]["before_vip_oper"]
                case 3:
                    with open("source/message_text.json", "r") as file1:
                        msgjson = json.load(file1)
                        message_on_entry = msgjson["paycontrol"]["is_available_but_not_used"]["on_entry"]
                        message_after_oper = msgjson["paycontrol"]["is_available_but_not_used"]["after_oper"]
                        message_before_vip_oper = msgjson["paycontrol"]["is_available_but_not_used"]["before_vip_oper"]
                case 4:
                    with open("source/message_text.json", "r") as file1:
                        msgjson = json.load(file1)
                        message_on_entry = msgjson["paycontrol"]["no_app"]["on_entry"]
                        message_after_oper = msgjson["paycontrol"]["no_app"]["after_oper"]
                        message_before_vip_oper = msgjson["paycontrol"]["no_app"]["before_vip_oper"]
                case 5:
                    with open("source/message_text.json", "r") as file1:
                        msgjson = json.load(file1)
                        message_on_entry = msgjson["CAP"]["base"]["on_entry"]
                        message_after_oper = msgjson["CAP"]["base"]["after_oper"]
                        message_before_vip_oper = msgjson["CAP"]["base"]["before_vip_oper"]
                case 6:
                    with open("source/message_text.json", "r") as file1:
                        msgjson = json.load(file1)
                        message_on_entry = msgjson["CAP"]["sms_reported"]["on_entry"]
                        message_after_oper = msgjson["CAP"]["sms_reported"]["after_oper"]
                        message_before_vip_oper = msgjson["CAP"]["sms_reported"]["before_vip_oper"]
                case 7:
                    with open("source/message_text.json", "r") as file1:
                        msgjson = json.load(file1)
                        message_on_entry = msgjson["CAP_with_token"]["base"]["on_entry"]
                        message_after_oper = msgjson["CAP_with_token"]["base"]["after_oper"]
                        message_before_vip_oper = msgjson["CAP_with_token"]["base"]["before_vip_oper"]
                case 8:
                    with open("source/message_text.json", "r") as file1:
                        msgjson = json.load(file1)
                        message_on_entry = msgjson["CAP_with_token"]["for_employers_with_a_lot_of_orgs"]["on_entry"]
                        message_after_oper = msgjson["CAP_with_token"]["for_employers_with_a_lot_of_orgs"]["after_oper"]
                        message_before_vip_oper = msgjson["CAP_with_token"]["for_employers_with_a_lot_of_orgs"]["before_vip_oper"]
                case 9:
                    with open("source/message_text.json", "r") as file1:
                        msgjson = json.load(file1)
                        message_on_entry = msgjson["CAP_with_token"]["sms_reported"]["on_entry"]
                        message_after_oper = msgjson["CAP_with_token"]["sms_reported"]["after_oper"]
                        message_before_vip_oper = msgjson["CAP_with_token"]["sms_reported"]["before_vip_oper"]
                case 10:
                    with open("source/message_text.json", "r") as file1:
                        msgjson = json.load(file1)
                        message_on_entry = msgjson["CAP_with_token"]["is_available_but_not_used"]["on_entry"]
                        message_after_oper = msgjson["CAP_with_token"]["is_available_but_not_used"]["after_oper"]
                        message_before_vip_oper = msgjson["CAP_with_token"]["is_available_but_not_used"]["before_vip_oper"]
                case 11:
                    with codecs.open("./source/message_text.json", encoding='utf-8' , mode="r") as file1:
                        msgjson = json.load(file1)
                        #msgjson = codecs.open("./source/message_text.json", encoding='utf-8', mode='r')
                        #print(msgjson)
                        message_on_entry = msgjson["CAP"]["has_an_app_but_not_used"]["on_entry"]
                        #print(message_on_entry)
                        message_after_oper = msgjson["CAP"]["has_an_app_but_not_used"]["after_oper"]
                        message_before_vip_oper = msgjson["CAP"]["has_an_app_but_not_used"]["before_vip_oper"]
                        #print("VADbvadbadbd")

            response = {
                "prediction": int(prediction[0]),
                "message_on_entry": message_on_entry,
                "message_after_oper": message_after_oper,
                "message_before_vip_oper": message_before_vip_oper
            }
            #print(response)
            return response
    except Exception as e:
        print(e)

"""
@app.get("/")
async def get_upload_page():
    return HTMLResponse("""
"""<html>
        <head>
            <title>JSON File Upload</title>
        </head>
        <body>
            <h1>Upload a JSON file</h1>
            <div id="drop_area" style="border: 2px dashed #ccc; width: 300px; height: 100px; text-align: center; padding: 20px;">
                Drop your JSON file here
            </div>
            <script>
                const dropArea = document.getElementById('drop_area');

                dropArea.addEventListener('dragover', (event) => {
                    event.preventDefault();
                    dropArea.style.borderColor = 'blue';
                });

                dropArea.addEventListener('dragleave', () => {
                    dropArea.style.borderColor = '#ccc';
                });

                dropArea.addEventListener('drop', (event) => {
                    event.preventDefault();
                    dropArea.style.borderColor = '#ccc';

                    const files = event.dataTransfer.files;
                    if (files.length) {
                        const formData = new FormData();
                        formData.append('file', files[0]);

                        fetch('/uploadjson/', {
                            method: 'POST',
                            body: formData
                        })
                        .then(response => response.json())
                        .then(data => {
                            alert('Data received: ' + JSON.stringify(data.received_data));
                        })
                        .catch(error => {
                            console.error('Error:', error);
                        });
                    }
                });
            </script>
        </body>
    </html>
    """""")"""
