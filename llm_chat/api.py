from dataclasses import dataclass
import requests
from .session import SessionHistory
import os

OPENAI_ENDPOINT = "https://api.openai.com/v1/chat/completions"

def get_response_openai(
    SessionHistory:SessionHistory,
    **generation_args
) -> list[str]:
    api_key = os.environ.get("OPENAI_API_KEY")
    headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "messages": SessionHistory.json(),
        **generation_args
    }
    r = requests.post(OPENAI_ENDPOINT, json=data, headers=headers, verify=False)

    if r.status_code == 200:
        response = r.json()
        print(response)
        model_output = response['choices'][0]['message']['content']
    else:
        raise Exception(f"Response returned with code {r.status_code}, message: {r.content.decode()}")
    return model_output

def get_response(model_kind: str, SessionHistory:SessionHistory, **kwargs) -> list[str]:
    if model_kind.lower() == "openai":
        return get_response_openai(SessionHistory, kwargs["openai"])
    else:
        raise Exception(f"Model kind {model_kind} not supported")
