import json


#How to add Prompt to database ##########################################################################################--
#Variable
Pusername="Daniel Morandi"
Ptitle="Apple Test Question"
Pprompt="What color is an apple"
PSLC=-1
Psecurity=-1

jsonPromptExample={Ptitle: 
                    {Pusername:{
                        "Prompt":Pprompt,
                        models:{"gemini":
                            {"model_history":{
                                 "Question_1":["What color is an apple","red"],
                                 "Question_2":["What was the first question","What color is an apple"]}
                             },
                        "gpt":
                            {"model_history":{
                                 "Question_1":["What color is an apple","red"],
                                 "Question_2":["What was the first question","What color is an apple"]}
                             }
                             
                        },
                        "SDLC": PSLC,
                        "Security": Psecurity
                        }
                    }
                }
#Http call
http=f"http://100.68.81.165:364/api/AddPrompt?api_key=4652424&Data={jsonPromptExample}"
    
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
http=f"http://100.68.81.165:364/api/AddFormat?api_key=4652424&Data={jsonFormatExample}}}"


#Rest of https request ##########################################################################################
#Find all prompts based on security level
PromptTitle="Apple Test Question"
Security=1
http=f"http://100.68.81.165:364/api/FindPrompt?api_key=4652424&Title={PromptTitle}&Security={Security}"

#Find All formats
FormatTitle="This is a title"
http=f"http://100.68.81.165:364/api/FindFormat?api_key=4652424&Title={FormatTitle}"


#Remove Prompt Title based on ur own name
Username="Daniel Morandi"
Title="Apple Test Question"
http=f"http://100.68.81.165:364/api/RemovePrompt?api_key=4652424&Username={Username}&Title={Title}"

#Remove Format Title based on ur own name
Username="Daniel Morandi"
Title="This is a title"
http=f"http://100.68.81.165:364/api/RemoveFormat?api_key=4652424&Username={Username}&Title={Title}"


#How to Request from model ########################################################################################

#Without History
model="gpt"
prompt="What color is an apple"
http=f"http://192.168.0.200:364/api/Model?api_key=4652424&Model={model}&Prompt={prompt}"

#With History
model="gpt"
prompt="What color is an apple"
history="{%22Question_1%22:[%22What%20color%20is%20an%20apple%22,%22red%22]}"
http=f"http://192.168.0.200:364/api/Model?api_key=4652424&Model={model}&Prompt={prompt}&History={history}"



#Files you need to make for api to work ##########################################################################
#Settings.py
#-----------------------------
#authenticate to firebase
cred_file=""
database_url=""

# Setup API keys
GOOGLE_API_KEY=""
OPENAI_API_KEY = ""
CLUADE_API_KEY = ""
PRIVATE_GPT_PATH = '/Users/ubadahsaleh/Desktop/Multi-LLM-Agile-Assistant/PrivateGPT'
#-----------------------------

#credentils.json
#Get from firebase. Ask guidi

