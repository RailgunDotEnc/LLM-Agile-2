import FireDB as DB
import Models as MD
import uvicorn
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
def check_key(api_key: str, security_level: int):
    # Implement your key checking logic here
    # Return True if the key is valid for the given security level, False otherwise
    if security_level == 1 and api_key == "KEY_FOR_SECURITY_LEVEL_1":
        return True
    elif security_level == 2 and api_key == "KEY_FOR_SECURITY_LEVEL_2":
        return True
    elif security_level == 3 and api_key == "KEY_FOR_SECURITY_LEVEL_3":
        return True
    elif security_level == 4 and api_key == "KEY_FOR_SECURITY_LEVEL_4":
        return True
    elif security_level == 5 and api_key == "KEY_FOR_SECURITY_LEVEL_5":
        return True
    else:
        return False

#api_key=4652424&Title=Test
#Find Prompt
#NEEDS SECURITY LEVEL CHECK
#REPLACE API KEY WITH SECURITY LEVEL
@app.get("/")
async def ping(request: Request):
    return {"message":"Pingged"}

@app.get("/api/FindPrompt")
async def bard_call(request: Request,api_key: str, Title: str):
    # if api_key=="4652424":
    if check_key(api_key, security_level):
        message=DB.findPrompt(Title)
        return message
    else:
        return {"message":"Acess Error"}

@app.get("/api/FindFormat")
async def bard_call(request: Request,api_key: str, Title: str):
    # if api_key=="4652424":
    if check_key(api_key, security_level):
        message=DB.findFormat(Title)
        return message
    else:
        return {"message":"Acess Error"}
    
@app.get("/api/AddPrompt")
async def bard_call(request: Request,api_key: str, Title: str,Security:int, Description: str, Role: str, SdlcPhase: int, Models: str, Results: str):
    # if api_key=="4652424":
    if check_key(api_key, security_level):
        message=DB.addPrompt(Title,Security, Description, Role, SdlcPhase, Models, Results)
        return message
    else:
        return {"message":"Acess Error"}

@app.get("/api/AddFormat")
async def bard_call(request: Request,api_key: str, Title: str, Description: str):
    # if api_key=="4652424":
    if check_key(api_key, security_level):
        message=DB.addFormat(Title, Description)
        return {"status":message}
    else:
        return {"message":"Acess Error"}
    
@app.get("/api/RemovePrompt")
async def bard_call(request: Request,api_key: str, Title: str):
    # if api_key=="4652424":
    if check_key(api_key, security_level):
        message=DB.removePrompt(Title)
        return {"status":message}
    else:
        return {"message":"Acess Error"}

@app.get("/api/RemoveFormat")
async def bard_call(request: Request,api_key: str, Title: str):
    # if api_key=="4652424":
    if check_key(api_key, security_level):
        message=DB.removeFormat(Title)
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