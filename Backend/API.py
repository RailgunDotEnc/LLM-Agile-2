#Import from other files
import FireDB as DB
import Models as MD
import Settings as ST
import Jira as JI

#Import from Settigns
import uvicorn
from fastapi import FastAPI,  Request
from fastapi.middleware.cors import CORSMiddleware
import socket

#Setting up variables
origins = [
    "http://localhost:3000/",  # Adjust this to the domain of your frontend application
    # Add other allowed origins as needed
]
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Adjust as needed for your API
    allow_headers=["Authorization", "Content-Type"],  # Adjust as needed for your API
)       


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
    
                                                  

##############################################################################################################################################################################################################################################
#Test ping
@app.get("/")
async def ping(request: Request, api_key: str= "none"):
    if api_key=="none":
        return {"ping":"No api key used"}
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
    return {"ping":message}

##############################################################################################################################################################################################################################################
#Firebase calls
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

##############################################################################################################################################################################################################################################
#LLM calls
@app.get("/api/Model")
async def bard_call(request: Request,api_key: str,Model:str, Prompt: str, History:str= "none"):
    if check_Key(api_key)!=-2:
        message=MD.model_manager(Model,Prompt,History)
        return message
    else:
        return {"Error":"Acess Error"}  

##############################################################################################################################################################################################################################################
#Jira calls
@app.get("/api/get_story")
async def bard_call(request: Request,api_key: str,issue_key:str,email:str, api_token:str):
    if check_Key(api_key)!=-2:
        #Adding Jira class
        jira_api = JI.JiraAPI(email, api_token, ST.jira_domain)
        message=str(jira_api.get_story(issue_key))
        return {"jira":message}
    else:
        return {"Error":"Acess Error"}  

@app.get("/api/get_story_list")
async def bard_call(request: Request,api_key: str,project_key:str,email:str, api_token:str):
    if check_Key(api_key)!=-2:
        jira_api = JI.JiraAPI(email, api_token, ST.jira_domain)
        message=jira_api.get_story_list(project_key)
        return {"jira":message}
    else:
        return {"Error":"Acess Error"}  

##############################################################################################################################################################################################################################################
# Program start
if __name__ == '__main__':
    host_name = socket.gethostname()
    IP_address=socket.gethostbyname(host_name)
    print("Using IP:", IP_address)
    uvicorn.run("API:app", host=IP_address, port=ST.Port, workers=4) 