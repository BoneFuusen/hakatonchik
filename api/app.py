from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
import json

from ml.validation import JsonData
from ml.processing import Processor

app = FastAPI(
    title="Hakatonchik"
)


@app.post("/uploadjson/")
async def upload_json(file: UploadFile = File(...)):
    content = await file.read()
    data = json.loads(content)

    try:
        JsonData.model_validate(data)

        proc = Processor(data)
        df = proc.preprocess()

        print(df)
        return data
    except Exception as e:
        print(f'Ошибка валидации: {e}')


@app.get("/")
async def get_upload_page():
    return HTMLResponse("""
    <html>
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
    """)

