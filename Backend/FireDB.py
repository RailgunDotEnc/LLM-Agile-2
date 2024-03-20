import firebase_admin
from firebase_admin import db, credentials
import Settings as ST

#authenticate to firebase
cred = credentials.Certificate(ST.cred_file)
firebase_admin.initialize_app(cred, {"databaseURL": ST.database_url})


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

def addPrompt(title,Security, Description, Role, SdlcPhase, Models, Results):
    # Reference to the root of your database
    #NEEDS TO MAKE SURE TITLE DOES NOT EXIST
    ref = db.reference('/')
    new_prompt_test = {
    title: { 
        'Description': Description,
        'Security':Security,
        'Role': Role,
        'SdlcPhase': SdlcPhase,
        'Models': Models,
        'Results': Results
    }
    }
    ref.child('Prompts').update(new_prompt_test)
    return f"Saved: {title}:\nSecurity: {Security}\nDescription: {Description}\nRole: {Role}\nSdlcPhase: {SdlcPhase}\nModels: {Models}\nResults: {Results}"

def removePrompt(title):
    # Reference to the 'Prompts' node
    ref = db.reference('/Prompts')

    # Query to find the object with the title 'NewPromptName'
    query = ref.order_by_key().equal_to(title)
    result = query.get()

    # Remove if the object exists
    if result:
        for key in result.keys():
            ref.child(key).delete()
        return "Deleted: " + title
    else:
        return "Error could not find "+title

def addFormat(title,Description):
    # Reference to the root of your database
    #NEEDS TO MAKE SURE TITLE DOES NOT EXIST
    ref = db.reference('/')
    new_format_test = {
    title: { 
        'Description': Description,
    }
    }
    ref.child('Formats').update(new_format_test)
    return f"Saved: {title}\nDescription: {Description}\n"


def removeFormat(title):
    # Reference to the 'Format' node
    ref = db.reference('/Formats')

    # Query to find the object with the title 'NewFormatName'
    query = ref.order_by_key().equal_to(title)
    result = query.get()

    # Remove if the object exists
    if result:
        for key in result.keys():
            ref.child(key).delete()
        return "Deleted: " + title
    else:
        return "Error could not find "+title
    
#ADD UPDATE FOR PROMPT AND FORMAT
#SELECT CONVERSTION POINT 
    
#Data Structure
#Result
    #{Model}
    #    {Question}
    #         {Results}
    #{Model}.....
