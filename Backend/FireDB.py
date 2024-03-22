import firebase_admin
from firebase_admin import db, credentials
import Settings as ST
import json

#jsonExample={"Name of topic": {"Your user name": {"LLM Name": {"History": { "Question 1": "[Question, Response]","Question 2": ["Question II", "Response II"],},"SDLC": -1,"Security": -1}}}}

            

#authenticate to firebase
cred = credentials.Certificate(ST.cred_file)
firebase_admin.initialize_app(cred, {"databaseURL": ST.database_url})

def construct_json(Title, Prompt, Role, SdlcPhase, History):
    new_dict={"Title":Title, "Prompt":Prompt, "Role":Role,"SdlcPhase":SdlcPhase,"History":History}


def findPrompt(title):
    print(title)
    ref = db.reference('/Prompts')
    # Query to find the object with the title 'NewPromptName'
    query = ref.order_by_key().equal_to(title)
    result = query.get()
    return result

def findFormat(title):
    ref = db.reference('/Formats')
    # Query to find the object with the title 'NewPromptName'
    query = ref.order_by_key().equal_to(title)
    result = query.get()
    return result

def addPrompt(data):
    print(data)
    # Reference to the root of your database
    #NEEDS TO MAKE SURE TITLE DOES NOT EXIST
    ref = db.reference('/')
    jsonfile=json.loads(data)
    ref.child('Prompts').update(jsonfile)
    return f"Saved: {data}"

def removePrompt(username,title):
     # Reference to the 'Prompts' node
    ref = db.reference('/Prompts')

    # Find the prompt with the specified title
    prompt_ref = ref.child(title)
    prompt_data = prompt_ref.get()

    if prompt_data:  # Check if the prompt exists
        if username in prompt_data:
            prompt_ref.child(username).delete()
            return f"Deleted '{username}' from '{title}'"
        else:
            return f"Error: Username '{username}' not found in '{title}'"
    else:
        return f"Error: Prompt '{title}' not found" 

def addFormat(data):
    # Reference to the root of your database
    #NEEDS TO MAKE SURE TITLE DOES NOT EXIST
    ref = db.reference('/')
    ref.child('Formats').update(json.loads(data))
    return f"Saved: {data}"


def removeFormat(username,title):
    # Reference to the 'Formats' node
    ref = db.reference('/Formats')

    # Find the format with the specified title
    format_ref = ref.child(title)
    format_data = format_ref.get()

    if format_data:  # Check if the format exists
        if username in format_data:
            format_ref.child(username).delete()
            return f"Deleted '{username}' from '{title}'"
        else:
            return f"Error: Username '{username}' not found in '{title}'"
    else:
        return f"Error: Format '{title}' not found" 
    
#ADD UPDATE FOR PROMPT AND FORMAT
#SELECT CONVERSTION POINT 
    
#Data Structure
#Result
    #{Model}
    #    {Question}
    #         {Results}
    #{Model}.....
