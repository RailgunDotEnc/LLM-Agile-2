import firebase_admin
from firebase_admin import db, credentials
import Settings as ST
import json

#jsonExample={"Name of topic": {"Your user name": {"LLM Name": {"History": { "Question 1": "[Question, Response]","Question 2": ["Question II", "Response II"],},"SDLC": -1,"Security": -1}}}}

            

#authenticate to firebase
cred = credentials.Certificate(ST.cred_file)
firebase_admin.initialize_app(cred, {"databaseURL": ST.database_url})

#Helper functions
def filter_users(data, security_lv):
    if 'Test' in data:
        tests = data['Test']
        filtered_tests = {}
        for test_name, test_data in tests.items():
            user_security = test_data.get('Security', 0)  # Assuming default security level is 0 if not specified
            if user_security <= security_lv:
                filtered_tests[test_name] = test_data

        data['Test'] = filtered_tests

    return data

def construct_json(Title, Prompt, Role, SdlcPhase, History):
    new_dict={"Title":Title, "Prompt":Prompt, "Role":Role,"SdlcPhase":SdlcPhase,"History":History}


#Database calls
def getAllPrompts():
    ref = db.reference('/Prompts')
    print(ref)
        # Query to find the object with the title 'NewPromptName'
    query = ref.get().keys()
    return {"keys":list(query)}

def findPrompt(title,security_lv):
    print(title)
    ref = db.reference('/Prompts')
    # Query to find the object with the title 'NewPromptName'
    query = ref.order_by_key().equal_to(title)
    result = query.get()
    result_filtered=filter_users(result,security_lv)
    return result_filtered

def getAllFormats():
    ref = db.reference('/Formats')
    print(ref)
        # Query to find the object with the title 'NewPromptName'
    query = ref.get().keys()
    return {"keys":list(query)}

def findFormat(title):
    ref = db.reference('/Formats')
    query = ref.order_by_key().equal_to(title)
    result = query.get()
    print(result)
    return result

def addPrompt(data):
    print(data)
    # Reference to the root of your database
    ref = db.reference('/')
    jsonfile=json.loads(data)
    ref.child('Prompts').update(jsonfile)
    return f"Saved: {data}"

def removePrompt(username,title,security_lv):
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
