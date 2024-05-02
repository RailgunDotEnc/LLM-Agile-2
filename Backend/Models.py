import google.generativeai as genai
import anthropic
from transformers import AutoTokenizer, AutoModelForCausalLM
from openai import OpenAI
import json
import Settings as ST
import openai 
from pgpt_python.client import PrivateGPTApi


#Call from API
client = OpenAI(api_key = ST.OPENAI_API_KEY)
def model_manager(Model_name,prompt,model_history):
    if Model_name=="gemini":
        Result=gemini_chat(prompt,model_history)
    elif Model_name=="gpt":
        Result=gpt_chat(prompt,model_history)
    elif Model_name=="claude":
        Result=claude_chat(prompt, model_history)
    elif Model_name=="llama":
        Result=LLAMA_chat(prompt, model_history)
    else:
        Result={"Error":"Model not found"}
    return Result

#########################################################################################################
#Helper functions

def get_history(model_history):
    data = json.loads(model_history)
    return data


def add_log(response, prompt, model):
    data = get_history()
    prompt = "Question " + str(len(data[model]) + 1) + " : " + prompt
    data[model][prompt] = response

    return json.dump(data, indent=4) 

def unpack_history(model_history):
    message={"model":{}}
    new_model_history={"model_history":{}}
    if model_history=="none":
        model_history={}
        key_num=0
    else:
        model_history= json.loads(model_history)
        max_question_num = -1  # Initialize to a low number
        for key in model_history.keys():
            question_num = int(key.split("_")[1])  # Extract the question number
            if question_num > max_question_num:
                max_question_num = question_num
        key_num=max_question_num
    return message,new_model_history,key_num,model_history

def prompt_reformatting(model_history,prompt):
    if len(model_history)!=0:
        new_prompt="Past Converstation: \n"
    else:
        new_prompt=""
    for key in model_history.keys():
        new_prompt=f"{new_prompt}User Question: {model_history[key][0]}\n"
        new_prompt=f"{new_prompt}Your Response: {model_history[key][1]}\n"
    new_prompt=f"{new_prompt}\nAnswer the following: {prompt}"
    return new_prompt

def repack_history(new_model_history,model_history,key_num,prompt,response,message):
    new_model_history["model_history"].update(model_history)
    new_model_history["model_history"].update({f"Question_{key_num+1}": [prompt,response["response"]]})
    message["model"].update(response)
    message["model"].update(new_model_history)
    return message
##########################################################################################################
#Gemini Model code
def gemini(prompt):
    #Prompt comes in as string
    genai.configure(api_key=ST.GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    #Return string
    return response.text

#Formatting prompts for Gemini
def gemini_chat(prompt,model_history):
    #Unpacking history form API for set blank if empty
    message,new_model_history,key_num,model_history=unpack_history(model_history)
    #Reformat prompt with prompt history
    new_prompt=prompt_reformatting(model_history,prompt)
    #Request from Gemini
    response={"response":gemini(new_prompt)}
    #Reformat response to send back
    message=repack_history(new_model_history,model_history,key_num,prompt,response,message)
    return message

#########################################################################################################
#gpt Model code
def gpt(prompt):
    #Prompt comes in as string
    system = [{"role": "system", "content": "You are HappyBot."}]
    user = [{"role": "user", "content": prompt}]
    chat_completion = client.chat.completions.create(
    messages = system + user,
    model="gpt-3.5-turbo",
    max_tokens=25, top_p=0.9,
    )
    #Return string
    return chat_completion.choices[0].message.content

def gpt_chat(prompt, model_history):
    #Unpacking history form API for set blank if empty
    message, new_model_history, key_num, model_history = unpack_history(model_history)
    #Reformat prompt with prompt history
    new_prompt = prompt_reformatting(model_history, prompt)
    #Request from Gpt
    response = {"response": gpt(new_prompt)}
    #Reformat response to send back
    message = repack_history(new_model_history, model_history, key_num, prompt, response, message)
    return message

#########################################################################################################


# Helper Function
def claude(prompt):
    #Prompt comes in as string
    client  = anthropic.Anthropic(api_key=ST.CLUADE_API_KEY)
    message = client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": prompt}
    ]
)
    #Return string
    return f"{message.content[0].text}"

def claude_chat(prompt,model_history):
    #Unpacking history form API for set blank if empty
    message,new_model_history,key_num,model_history=unpack_history(model_history)
    #Reformat prompt with prompt history
    new_prompt=prompt_reformatting(model_history,prompt)
    #Request from Claude
    response={"response":claude(new_prompt)}
    #Reformat response to send back
    message=repack_history(new_model_history,model_history,key_num,prompt,response,message)
    return message

#########################################################################################################


#Calls to Private GPT
def LLAMA(prompt, context):
    #Prompt comes in as string
    client = PrivateGPTApi(base_url="http://localhost:8001")
    prompt_result = client.contextual_completions.prompt_completion(
        prompt = prompt,
        use_context=context,
        include_sources=context,
    )
    #Return string
    return prompt_result.choices[0].message.content

#LLAMA formatting  
def LLAMA_chat(prompt,model_history):
    #Unpacking history form API for set blank if empty
    message,new_model_history,key_num,model_history=unpack_history(model_history)
    #Reformat prompt with prompt history
    new_prompt=prompt_reformatting(model_history,prompt)
    #Request from LLAMA
    response = {"response":LLAMA(new_prompt, ST.context)}
    #Reformat response to send back
    message=repack_history(new_model_history,model_history,key_num,prompt,response,message)
    return message

#Feature to add files to LLama documents
def LLAMA_ingest_text(inText, tname):
    client = PrivateGPTApi(base_url="http://localhost:8001")
    text_to_ingest = inText

    ingested_text_doc_id = (
        client.ingestion.ingest_text(file_name=tname, text=text_to_ingest)
        .data[0]
        .doc_id
    )

#########################################################################################################

