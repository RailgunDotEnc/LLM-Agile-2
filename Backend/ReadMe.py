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

jsonPromptExample={"Ptitle": 
                    {"Pusername":{
                        "Prompt":Pprompt,
                        "models":{  "gemini":
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
http=f"http://100.68.81.165:364/api/AddPrompt?api_key={apikey}&Data={jsonPromptExample}"

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
http=f"http://100.68.81.165:364/api/AddFormat?api_key={apikey}&Data={jsonFormatExample}}}"


#Rest of https request ##########################################################################################
#Find all prompts based on security level
PromptTitle="Apple Test Question"
Security=1
http=f"http://100.68.81.165:364/api/FindPrompt?api_key={apikey}&Title={PromptTitle}"

#Find All formats
FormatTitle="This is a title"
http=f"http://100.68.81.165:364/api/FindFormat?api_key={apikey}&Title={FormatTitle}"


#Remove Prompt Title based on ur own name
Username="Daniel Morandi"
Title="Apple Test Question"
http=f"http://100.68.81.165:364/api/RemovePrompt?api_key={apikey}&Username={Username}&Title={Title}"

#Remove Format Title based on ur own name
Username="Daniel Morandi"
Title="This is a title"
http=f"http://100.68.81.165:364/api/RemoveFormat?api_key={apikey}&Username={Username}&Title={Title}"


#How to Request from model ########################################################################################

#Without History
model="gpt"
prompt="What color is an apple"
http=f"http://192.168.0.200:364/api/Model?api_key={apikey}&Model={model}&Prompt={prompt}"

#With History
model="gpt"
prompt="What color is an apple"
history="{%22Question_1%22:[%22What%20color%20is%20an%20apple%22,%22red%22]}"
http=f"http://192.168.0.200:364/api/Model?api_key={apikey}&Model={model}&Prompt={prompt}&History={history}"



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

