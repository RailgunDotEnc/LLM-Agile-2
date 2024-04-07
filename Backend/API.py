import FireDB as DB
import Models as MD
import uvicorn
from fastapi import FastAPI,  Request
from fastapi.middleware.cors import CORSMiddleware
import socket
import Settings as ST
#Test functions
#addPrompt("NewPromptName",new_prompt['NewPromptName']['Description'],new_prompt['NewPromptName']['Role'],new_prompt['NewPromptName']['SdlcPhase'])
#removePrompt("NewPromptName")
origins = [
    "http://localhost:3000/",  # Adjust this to the domain of your frontend application
    # Add other allowed origins as needed
]

#addFormat("NewFormatName",new_format['NewFormatName']['Description'])
#removeFormat("NewFormatName")
#API Key Manager
#Example key: xyz12345abcde
def check_Key(key):
    print(key[0:3],ST.default_key)
    print(key[8:13],ST.key_levels[0])
    if not (key[0:3]==ST.default_key):
        return -2
    elif key[8:13]==ST.key_levels[0]:
        return 1
    elif key[8:13]==ST.key_levels[1]:
        return 2
    elif key[8:13]==ST.key_levels[2]:
        return 3
    elif key[8:13]==ST.key_levels[3]:
        return 4
    elif key[8:13]==ST.key_levels[4]:
        return 5
    else:
        return -1
    
        

app = FastAPI()
#KEY FOR SECURITY LEVEL 1
#KEY FOR SECRUTIY LEVEL 2
#FRONT_END OWNS KEY
                                                         

#
#Find Prompt
#NEEDS SECURITY LEVEL CHECK
#REPLACE API KEY WITH SECURITY LEVEL
@app.get("/")
async def ping(request: Request, api_key: str):
    level=check_Key(api_key)
    if level==-2:
        message="Access not allowed"
    elif level==-1:
        message="LV -1: public access"
    elif level==1:
        message="LV 1: access"
    elif level==2:
        message="LV 2: access"
    elif level==3:
        message="LV 3: access"
    elif level==4:
        message="LV 4: access"
    elif level==5:
        message="LV 5: access"
    return {"message":message}

@app.get("/api/FindPrompt")
async def bard_call(request: Request,api_key: str, Title: str):
    if check_Key(api_key)!=-2:
        message=DB.findPrompt(Title,check_Key(api_key))
        return message
    else:
        return {"message":"Acess Error"}

@app.get("/api/FindFormat")
async def bard_call(request: Request,api_key: str, Title: str):
    if check_Key(api_key)!=-2:
        message=DB.findFormat(Title,check_Key(api_key))
        return message
    else:
        return {"message":"Acess Error"}
    
@app.get("/api/AddPrompt")###########
async def bard_call(request: Request,api_key: str, Data:str):
    if check_Key(api_key)!=-2:
        message=DB.addPrompt(Data)
        return message
    else:
        return {"message":"Acess Error"}

@app.get("/api/AddFormat")###############
async def bard_call(request: Request,api_key: str, Data: str):
    if check_Key(api_key)!=-2:
        message=DB.addFormat(Data)
        return {"status":message} 
    else:
        return {"message":"Acess Error"}
    
@app.get("/api/RemovePrompt")
async def bard_call(request: Request,api_key: str,Username:str, Title: str):
    if check_Key(api_key)!=-2:
        message=DB.removePrompt(Username, Title,check_Key(api_key))
        return {"status":message} 
    else:
        return {"message":"Acess Error"}   

@app.get("/api/RemoveFormat")
async def bard_call(request: Request,api_key: str,Username:str, Title: str):
    if check_Key(api_key)!=-2:
        message=DB.removeFormat(Username, Title)
        return {"status":message} 
    else:
        return {"message":"Acess Error"}  
    
@app.get("/api/Model")
async def bard_call(request: Request,api_key: str,Model:str, Prompt: str, History:str= "none"):
    if check_Key(api_key)!=-2:
        message=MD.model_manager(Model,Prompt,History)
        return message
    else:
        return {"Error":"Acess Error"}  


if __name__ == '__main__':
    host_name = socket.gethostname()
    IP_address=socket.gethostbyname(host_name)
    print("Using IP:", IP_address)
    uvicorn.run("API:app", host=IP_address, port=364, workers=4) 