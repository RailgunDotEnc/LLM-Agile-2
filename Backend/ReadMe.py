import json
#How API keys work
webkey="xyz"
userkey="12345abcde"
apikey=webkey+userkey
#apikey=xyz12345abcde
#The key is split into currently 3 parts
#Part 1 xyz: This just makes sure that there is company access and is a legal key. This key will be added automatically by the website
#Part 2 12345: This is going to be a unique number based on user. If we have time and are done with everything else, we can add a verificaiton that the user exist.
#Part 3 abcde: This has 5 versions from abcde, bcdef, ...., This indicates the security level and the filtration of the dataset

#Add this to Settings.py
default_key="xyz"
key_levels=["abcde","bcdef","cdefg","defgh","efghi"]

#How to add Prompt to database ##########################################################################################--
#Variable
Pusername="Daniel Morandi"
Ptitle="Apple Test Question"
Pprompt="What color is an apple"
PSLC=-1
Psecurity=-1


jsonPromptExample={"Ptitle":    #Title header
                    {"Pusername":{ 
                        "Prompt":"What color is an apple", 
                        "models":{  
                                    "gemini": 
                                    {"model_history":{
                                        "Question_1":["What color is an apple","red"],
                                        "Question_2":["What was the first question","What color is an apple"]}
                                    },
                                    "gpt":
                                        {"model_history":{
                                            "Question_1":["What color is an apple","red"],
                                            "Question_2":["What was the first question","What color is an apple"]}
                                        },
                                    "claude" : 
                                     {"model_history":{
                                        "Question_1":["What color is an apple","red"],
                                        "Question_2":["What was the first question","What color is an apple"]}
                                    }
                        },
                        "SDLC": "PSLC",
                        "Security": "Psecurity"                                          
                        }
                    }
                }

#IP Addresses and ports##########################################################################################
ip="70.153.136.26"
port="333"
###This calls ping for server testing with no api key
htpp=f"http://{ip}:{port}"
###This calls ping for server testing with api key
http=f"http://{ip}:{port}/?api_key={apikey}"

##########################################################################################

#Http call to add prompt data
http=f"http://{ip}:{port}/api/AddPrompt?api_key={apikey}&Data={jsonPromptExample}"

#How to add Format ##########################################################################################
Fusername="Daniel Morandi"
Title="This is a title"
Fformat="In the structure of a table"
jsonFormatExample={
                Title:{
                    Fusername:Fformat
                    }
                }
#Http call
http=f"http://{ip}:{port}/api/AddFormat?api_key={apikey}&Data={jsonFormatExample}"


#Rest of https request ##########################################################################################
#Find all prompts: only returns titles
http=f"http://{ip}:{port}/api/ScanAllPrompts?api_key={apikey}"
#Find all formats: only returns titles
http=f"http://{ip}:{port}/api/ScanAllFormats?api_key={apikey}"

#Find all prompts for title based on security level
PromptTitle="Apple Test Question"
http=f"http://{ip}:{port}/api/FindPrompt?api_key={apikey}&Title={PromptTitle}"

#Find All formats for title
FormatTitle="This is a title"
http=f"http://{ip}:{port}/api/FindFormat?api_key={apikey}&Title={FormatTitle}"


#Remove Prompt Title based on ur own name
Username="Daniel Morandi"
Title="Apple Test Question"
http=f"http://{ip}:{port}/api/RemovePrompt?api_key={apikey}&Username={Username}&Title={Title}"

#Remove Format Title based on ur own name
Username="Daniel Morandi"
Title="This is a title"
http=f"http://{ip}:{port}/api/RemoveFormat?api_key={apikey}&Username={Username}&Title={Title}"


#How to Request from model ########################################################################################

#Without History
model="gpt"
prompt="What color is an apple"
http=f"http://{ip}:{port}/api/Model?api_key={apikey}&Model={model}&Prompt={prompt}"

#With History
model="gpt"
prompt="What color is an apple"
history=history={"model_history":{"Question_1":["What color is an apple","red"],
"Question_2":["What was the first question","What color is an apple"]}}

http=f"http://{ip}:{port}/api/Model?api_key={apikey}&Model={model}&Prompt={prompt}&History={history}"

#Hot to Request from Jira ##########################################################################################
#Get these from Jira
issue_key="FP-1"
email=""
api_token=""

http=f"http://{ip}:{port}/api/get_story?api_key={apikey}&issue_key={issue_key}&email={email}&api_token={api_token}"

project_key="FP"
email=""
api_token=""
http=f"http://{ip}:{port}/api/get_story_list?api_key={apikey}&project_key={project_key}&email={email}&api_token={api_token}"
#Files you need to make for api to work ##########################################################################
#Settings.py
#-----------------------------
#Security
default_key="xyz"
key_levels=["abcde","bcdef","cdefg","defgh","efghi"]

#authenticate to firebase
cred_file=""
database_url=""

# Setup API keys
GOOGLE_API_KEY=""
OPENAI_API_KEY = ""
CLUADE_API_KEY = ""

#Port
Port="364"
#----------------------------
#credentils.json
#Get from firebase. Ask guidi

