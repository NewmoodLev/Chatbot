from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import boto3
import json
import logging

# ตั้งค่า logging
logging.basicConfig(level=logging.ERROR, filename='error.log')

# กำหนดค่า AWS
aws_region = 'us-east-1'
model_id = 'amazon.titan-text-premier-v1:0'

# สร้าง client สำหรับ AWS Bedrock, S3 และ Translate
bedrock_client = boto3.client('bedrock-runtime', region_name=aws_region)
s3_client = boto3.client('s3', region_name=aws_region)
translate_client = boto3.client('translate', region_name=aws_region)

app = Flask(__name__)
CORS(app)

# Knowledge Base
knowledge_base = {}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/Chatbot-bankok', methods=['POST'])
def chatbot():
    user_input = request.json.get('inputText')

    # ดึงข้อมูล Knowledge Base จาก S3
    global knowledge_base
    knowledge_base = fetch_knowledge_base_from_s3()

    # ค้นหาคำตอบใน Knowledge Base
    response = find_answer_in_knowledge_base(user_input)

    # ถ้าไม่พบใน Knowledge Base ก็เรียกใช้ Bedrock
    if response == "ฉันไม่แน่ใจเกี่ยวกับเรื่องนั้น.":
        response = get_response_from_bedrock(user_input)

    # แปลคำตอบเป็นภาษาไทย
    translated_response = translate_text(response, "en", "th")
    if translated_response is None:
        return jsonify(reply="เกิดข้อผิดพลาดในการแปลข้อความ")

    # ประมวลผลคำตอบก่อนส่งกลับ
    processed_response = process_response(translated_response)

    return jsonify(reply=processed_response)

def fetch_knowledge_base_from_s3():
    try:
        bucket_name = 'depa-demo'
        knowledge_base = {}

        # ดึงรายการไฟล์ใน S3 Bucket
        response = s3_client.list_objects_v2(Bucket=bucket_name)

        if 'Contents' in response:
            for item in response['Contents']:
                file_key = item['Key']
                
                # อ่านข้อมูลจากไฟล์ JSON
                if file_key.endswith('.json'):
                    file_response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
                    data = file_response['Body'].read().decode('utf-8')
                    knowledge_base.update(json.loads(data))

        return knowledge_base

    except Exception as e:
        logging.error(f"เกิดข้อผิดพลาดในการดึง Knowledge Base จาก S3: {e}")
        return {}

def find_answer_in_knowledge_base(question):
    return knowledge_base.get(question, "ฉันไม่แน่ใจเกี่ยวกับเรื่องนั้น.")

def get_response_from_bedrock(user_input):
    try:
        response = bedrock_client.invoke_model(
            modelId=model_id,
            body=json.dumps({
                "inputText": user_input,
                "textGenerationConfig": {
                    "temperature": 0.5,
                    "topP": 0.7,
                    "maxTokenCount": 512,
                    "stopSequences": ["User:"]
                }
            }),
            contentType='application/json',
        )

        output = json.loads(response['body'].read().decode('utf-8'))

        if "results" in output and len(output["results"]) > 0:
            return output['results'][0]['outputText']
        else:
            return "ไม่มีผลลัพธ์"

    except Exception as e:
        logging.error(f"เกิดข้อผิดพลาดในการเรียก Bedrock: {e}")
        return f"ขอโทษค่ะ เกิดข้อผิดพลาดในการตอบกลับ: {str(e)}"

def translate_text(text, source_language, target_language):
    try:
        response = translate_client.translate_text(
            Text=text,
            SourceLanguageCode=source_language,
            TargetLanguageCode=target_language
        )
        return response['TranslatedText']
    except Exception as e:
        logging.error(f"เกิดข้อผิดพลาดในการแปล: {e}")
        return None

def process_response(response):
    formatted_response = f"\n\n{response.strip()}\n\n"
    return formatted_response

if __name__ == '__main__':
    app.run(debug=True)
