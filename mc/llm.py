import boto3, json
from pydantic import BaseModel, Field
from typing import Optional, List, Union, Literal, Dict

class ClaudeLLM(BaseModel):
    modelId: Literal["anthropic.claude-3-sonnet-20240229-v1:0"] = "anthropic.claude-3-sonnet-20240229-v1:0"

    def generate(self, prompt: Dict, system_prompt: str = None):
        
        bedrock_runtime = boto3.client("bedrock-runtime", region_name="us-west-2")

        if system_prompt: 
            prompt['system'] = system_prompt

        kwargs = {
                "modelId": "anthropic.claude-3-sonnet-20240229-v1:0",
                "contentType": "application/json",
                "accept": "application/json",
                "body": json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 1000,
                    **prompt
                })
            }
        
        response = bedrock_runtime.invoke_model(**kwargs)

        body = json.loads(response.get("body").read())

        return {"role": body['role'], "content": body['content']}


