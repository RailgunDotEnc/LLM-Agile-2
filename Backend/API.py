import FireDB as DB
import Models as MD
import uvicorn
import requests
import base64
from fastapi import FastAPI,  Request

import socket
#Test functions
#addPrompt("NewPromptName",new_prompt['NewPromptName']['Description'],new_prompt['NewPromptName']['Role'],new_prompt['NewPromptName']['SdlcPhase'])
#removePrompt("NewPromptName")

#addFormat("NewFormatName",new_format['NewFormatName']['Description'])
#removeFormat("NewFormatName")
    
app = FastAPI()
#KEY FOR SECURITY LEVEL 1
#KEY FOR SECRUTIY LEVEL 2
#FRONT_END OWNS KEY


#api_key=4652424&Title=Test
#Find Prompt
#NEEDS SECURITY LEVEL CHECK
#REPLACE API KEY WITH SECURITY LEVEL
@app.get("/")
async def ping(request: Request):
    return {"message":"Pingged"}

@app.get("/api/FindPrompt")
async def bard_call(request: Request,api_key: str, Title: str, Security:int):
    if api_key=="4652424":
        message=DB.findPrompt(Title)
        return message
    else:
        return {"message":"Acess Error"}

@app.get("/api/FindFormat")
async def bard_call(request: Request,api_key: str, Title: str):
    if api_key=="4652424":
        message=DB.findFormat(Title)
        return message
    else:
        return {"message":"Acess Error"}
    
@app.get("/api/AddPrompt")###########
async def bard_call(request: Request,api_key: str, Data:str):
    if api_key=="4652424":
        message=DB.addPrompt(Data)
        return message
    else:
        return {"message":"Acess Error"}

@app.get("/api/AddFormat")###############
async def bard_call(request: Request,api_key: str, Data: str):
    if api_key=="4652424":
        message=DB.addFormat(Data)
        return {"status":message}
    else:
        return {"message":"Acess Error"}
    
@app.get("/api/RemovePrompt")
async def bard_call(request: Request,api_key: str,Username:str, Title: str):
    if api_key=="4652424":
        message=DB.removePrompt(Username, Title)
        return {"status":message}
    else:
        return {"message":"Acess Error"}

@app.get("/api/RemoveFormat")
async def bard_call(request: Request,api_key: str,Username:str, Title: str):
    if api_key=="4652424":
        message=DB.removeFormat(Username, Title)
        return {"status":message}
    else:
        return {"message":"Acess Error"}
    
@app.get("/api/Model")
async def bard_call(request: Request,api_key: str,Model:str, Prompt: str, History:str= "none"):
    if api_key=="4652424":
        message=MD.model_manager(Model,Prompt,History)
        return message
    else:
        return {"Error":"Acess Error"}


if __name__ == '__main__':
    host_name = socket.gethostname()
    IP_address=socket.gethostbyname(host_name)
    print("Using IP:", IP_address)
    uvicorn.run("API:app", host=IP_address, port=364, workers=4)

# jira
def get_encoded_credentials(email: str, api_token: str) -> str:
    credentials = f"{email}:{api_token}"
    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    return encoded_credentials

def make_get_request(url: str, headers: dict, params: dict) -> requests.Response:
    response = requests.get(url, headers=headers, params=params)
    return response