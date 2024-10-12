import boto3
import json
import uuid

def chat_with_agent(agent_id, agent_alias_id, input_text, enable_trace=False, end_session=False):
    # สร้าง session สำหรับ AWS
    session = boto3.Session()
    bedrock_client = session.client('bedrock-agent-runtime')

    # สร้าง session ID ใหม่
    session_id = str(uuid.uuid4())

    # กำหนด session state
    session_state = {
        "files": [],
        "invocationId": str(uuid.uuid4()),
        "knowledgeBaseConfigurations": [{
            "knowledgeBaseId": "QXUP3CDZQZ",
            "retrievalConfiguration": {
                "vectorSearchConfiguration": {
                    "filter": {
                        "andAll": [
                            {
                                "equals": {"key": "exampleField", "value": "exampleValue"}
                            },
                            {
                                "equals": {"key": "anotherField", "value": "anotherValue"}
                            }
                        ]
                    },
                    "numberOfResults": 5,
                    "overrideSearchType": "exact"
                }
            }
        }],
        "returnControlInvocationResults": [{
            "apiResult": {
                "actionGroup": "default",
                "apiPath": "/example/path",
                "confirmationState": "CONFIRMED",
                "httpMethod": "GET",
                "httpStatusCode": 200,
                "responseBody": {
                    "body": {"text": "sample response"}
                },
                "responseState": "SUCCESS"
            }
        }],
        "sessionAttributes": {}
    }

    # เรียกใช้ Bedrock Agent Runtime
    response = bedrock_client.invoke_agent(
        agentId=agent_id,
        agentAliasId=agent_alias_id,
        sessionId=session_id,
        inputText=input_text,
        enableTrace=enable_trace,
        endSession=end_session,
        memoryId="exampleMemoryId",
        sessionState=session_state
    )

    # ดึงผลลัพธ์จาก response
    response_body = json.loads(response['body'].read().decode('utf-8'))
    return response_body

if __name__ == "__main__":
    agent_id = 'WPQFZLO1AE'  # Agent ID
    agent_alias_id = 'ME2UD9JNJF'  # Agent Alias ID
    input_text = input("คุณ: ")

    response = chat_with_agent(agent_id, agent_alias_id, input_text)
    print("AI: ", response.get('outputText', ''))
