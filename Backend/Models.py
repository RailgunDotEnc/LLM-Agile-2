import textwrap
import requests
from IPython.display import Markdown, display
import google.generativeai as genai
from IPython.display import Markdown
import torch
import asyncio
from anthropic import AsyncAnthropic
from transformers import AutoTokenizer, AutoModelForCausalLM
import openai
import json
from Settings import *

#Key Settup
#GOOGLE_API_KEY=""
#OPENAI_API_KEY = ""
#CLUADE_API_KEY = ""
#PRIVATE_GPT_PATH = ''


def model_manager(Model_name,prompt,model_history):
    if Model_name=="gemini":
        Result=gemini_chat(prompt,model_history)
    elif Model_name=="gpt":
        Result=gpt_chat(prompt,model_history)
    elif Model_name=="claude":
        Result=claude_chat(prompt, model_history)
    elif Model_name=="llama":
        Result=LLAMA(prompt, model_history)
    else:
        Result={"Error":"Model not found"}
    return Result

#########################################################################################################


# Global variables
conversation_history = []

# Initialize OpenAI client
openai.api_key = OPENAI_API_KEY

#########################################################################################################

def get_history(model_history):
    data = json.loads(model_history)
    return data

#########################################################################################################

def add_log(response, prompt, model):
    data = get_history()
    prompt = "Question " + str(len(data[model]) + 1) + " : " + prompt
    data[model][prompt] = response

    return json.dump(data, indent=4) 

#########################################################################################################

# Load the tokenizer and model
#tokenizer = AutoTokenizer.from_pretrained(PRIVATE_GPT_PATH)
#model = AutoModelForCausalLM.from_pretrained(PRIVATE_GPT_PATH)

#def private_gpt(prompt, max_length=50):
    # Tokenize the input prompt
#    input_ids = tokenizer.encode(prompt, return_tensors='pt')
    
    # Generate a sequence of tokens following the prompt
#    output = model.generate(input_ids, max_length=max_length, num_return_sequences=1)

    # Decode the output tokens to a string
#    text = tokenizer.decode(output[0], skip_special_tokens=True)

    # Display the text
#   display(Markdown(textwrap.indent(text, '> ')))

#########################################################################################################

def gemini(prompt,model_history):
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    if len(model_history)!=0:
        new_prompt="Past Converstation: \n"
    else:
        new_prompt=""
    for key in model_history.keys():
        new_prompt=f"{new_prompt}User Question: {model_history[key][0]}\n"
        new_prompt=f"{new_prompt}Your Response: {model_history[key][1]}\n"
    new_prompt=f"{new_prompt}\nAnswer the following: {prompt}"
    response = model.generate_content(new_prompt)
    #model_history = json.dumps(get_history(model_history)) + prompt+response
    return response.text

def gemini_chat(prompt,model_history):
    message={"gemini":{}}
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
    response={"response":gemini(prompt, model_history)}
    new_model_history["model_history"].update(model_history)
    new_model_history["model_history"].update({f"Question_{key_num+1}": [prompt,response["response"]]})
    message["gemini"].update(response)
    message["gemini"].update(new_model_history)
    return message

#########################################################################################################

def gpt(prompt,model_history):
    # Concatenate prompts and previous responses for context
    if len(model_history)!=0:
        new_prompt="Past Converstation: \n"
    else:
        new_prompt=""
    for key in model_history.keys():
        new_prompt=f"{new_prompt}User Question: {model_history[key][0]}\n"
        new_prompt=f"{new_prompt}Your Response: {model_history[key][1]}\n"
    new_prompt=f"{new_prompt}\nAnswer the following: {prompt}"
    print(new_prompt)
    # Generate response using the OpenAI API
    response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",  
        prompt=new_prompt,
        max_tokens=150
    )
    return response["choices"][0]["text"].strip()

def gpt_chat(prompt,model_history):
    print(model_history)
    message={"gpt":{}}
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
    response={"response":gpt(prompt, model_history)}
    new_model_history["model_history"].update(model_history)
    new_model_history["model_history"].update({f"Question_{key_num+1}": [prompt,response["response"]]})
    message["gpt"].update(response)
    message["gpt"].update(new_model_history)
    return message

#########################################################################################################

anthropic = AsyncAnthropic()
async def run_claude(prompt,model_history):
    anthropic = AsyncAnthropic(api_key=CLUADE_API_KEY)
    completion = await anthropic.completions.create(
        model="claude-2.1",
        max_tokens_to_sample=300,
        prompt=prompt,
    )
    return completion.completion+"\n"

# Helper Function for Async
def claude(prompt,model_history):
    if len(model_history)!=0:
        new_prompt="Past Converstation: \n"
    else:
        new_prompt=""
    for key in model_history.keys():
        new_prompt=f"{new_prompt}User Question: {model_history[key][0]}\n"
        new_prompt=f"{new_prompt}Your Response: {model_history[key][1]}\n"
    new_prompt=f"{new_prompt}\nAnswer the following: {prompt}"
    print(new_prompt)
    return asyncio.run(run_claude(new_prompt))

def claude_chat(prompt,model_history):
    print(model_history)
    message={"claude":{}}
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
    response={"response":claude(prompt, model_history)}
    new_model_history["model_history"].update(model_history)
    new_model_history["model_history"].update({f"Question_{key_num+1}": [prompt,response["response"]]})
    message["claude"].update(response)
    message["claude"].update(new_model_history)
    return message

#########################################################################################################

#https://huggingface.co/CohereForAI/c4ai-command-r-v01
def LLAMA(prompt):
    model_id = "CohereForAI/c4ai-command-r-v01"
    tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True)

    # Format message with the command-r chat template
    messages = [{"role": "user", "content": (json.dumps(get_history())+prompt)}]
    input_ids = tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=True, return_tensors="pt")
    ## <BOS_TOKEN><|START_OF_TURN_TOKEN|><|USER_TOKEN|>prompt<|END_OF_TURN_TOKEN|><|START_OF_TURN_TOKEN|><|CHATBOT_TOKEN|>

    gen_tokens = model.generate(
        input_ids, 
        max_new_tokens=100, 
        do_sample=True, 
        temperature=0.3,
        )

    gen_text = tokenizer.decode(gen_tokens[0])
    return gen_text

def LLAMA_chat(prompt):
    response = LLAMA(prompt)
    add_log(response, prompt, model="LLAMA")
    return response

#########################################################################################################

#Test Gemini
# print(gemini_chat("Tell me a joke about computers"))
# print(gemini_chat("Tell me another joke about computer"))
# print(gemini_chat("What was the first joke about computers that you told me?"))
# print(gemini_chat("Tell me something about alex"))

#Test GPT3.5
# print(gpt_chat("Tell me a joke about computers"))
# print(gpt_chat("Tell me another joke about computer"))
# print(gpt_chat("What was the first joke about computers that you told me?"))

# Test Cluade - overloads quickly, cant keep much history
# print(claude_chat("Tell me a joke about computers"))
# print(claude_chat("Tell me another joke about computer"))
# print(claude_chat("What was the first joke about computers that you told me?"))
# print(claude_chat("Tell me something about alex"))

#Test Hugging Face (Model wont run since i dont have enough memory :(. )
# print(LLAMA_chat("Tell me a joke about computers"))
# print(LLAMA_chat("Tell me another joke about computer"))
# print(LLAMA_chat("What was the first joke about computers that you told me?"))
# print(LLAMA_chat("Tell me something about alex"))

# Test Private GPT
# private_gpt("Tell me a story about a magic backpack.")
# print(private_gpt("Tell me a joke about computers"))
# print(private_gpt("Tell me another joke about computer"))
# print(private_gpt("What was the first joke about computers that you told me?"))


# =============================================================================
# {
#     "GPT": {
#         "Question 1 : Tell me a joke about computers": "Here's a silly computer joke: \n\nWhy was the computer cold?\nIt left its Windows open!",
#         "Question 2 : Tell me another joke about computer": "algorithms\n\nSure! What did the computer say when it saw a bug in its program? \"It's not a bug, it's a feature!\"",
#         "Question 3 : What was the first joke about computers that you told me?": "The first joke I told you was \"Why was the computer cold? It left its Windows open!\""
#     },
#     "Claude": {
#         "Question 1 : Tell me a joke about computers": " Here's a silly computer joke: \n\nWhy was the computer cold?\nIt left its Windows open!\n"
#     },
#     "Gemini": {
#         "Question 1 : Tell me a joke about computers": "Why was the computer cold? \nIt left its Windows open!",
#         "Question 2 : Tell me another joke about computer": "What did the computer say when it saw a bug in its program?\n\n\"It's not a bug, it's a feature!\"",
#         "Question 3 : What was the first joke about computers that you told me?": "Why was the computer cold? It left its Windows open!",
#         "Question 4 : Tell me something about alex": "Alex is a large language model trained by Google. The model is capable of understanding and generating human-like text, and it has been used in a variety of applications, including chatbots, language translation, and text summarization.\n\nHere are some additional details about Alex:\n\n* Alex is trained on a massive dataset of text and code. This data includes books, articles, websites, and other types of text.\n* Alex is able to understand the meaning of text and to generate text that is both coherent and informative.\n* Alex is still under development, but it is already one of the most powerful language models in the world.\n\nHere are some examples of how Alex can be used:\n\n* Alex can be used to create chatbots that can engage in natural language conversations with humans.\n* Alex can be used to translate text from one language to another.\n* Alex can be used to summarize text, making it easier for people to quickly understand the main points of a document.\n\nAlex is a powerful tool that has the potential to revolutionize the way we interact with computers. As the model continues to develop, we can expect to see even more innovative and groundbreaking applications for its use."
#     },
#     "LLAMA": {},
#     "PrivateGPT":{}
# }
# =============================================================================