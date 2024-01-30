# Import necessary libraries hello world hello again
import streamlit as st
import streamlit_ace as st_ace
import html
import openai

import os
import random
import json
from openai import OpenAI
import subprocess

import time
import shutil
import stat
import pickle
from pathlib import Path
import git

import re

#st.set_page_config(layout="wide")



# Custom CSS to increase the width of the main content area
def set_css_to_increase_width():
    st.markdown(
        """
        <style>
        .reportview-container .main .block-container{
            max-width: 90%;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

set_css_to_increase_width()



# Define the function to get the OpenAI client
def get_openai_client():
    # Access the OpenAI API key from Streamlit secrets
    openai.api_key = st.secrets["OPENAI_API_KEY"]
    
    return openai


# OpenAI client setup

def get_openai_client():
    """
    Create an OpenAI client using the API key provided by the user.
    """
    api_key = st.session_state.get("api_key")
    if api_key:
        return openai.Client(api_key=api_key)
    else:
        return None
        
        
        




# Function to clean up the code
def clean_up_solution(solution, task_statement, code_context):
    client = get_openai_client()
    if client is None:
        st.error("No Minato Key provided.")
        return "Error: No Minato Key."

    if not solution or not task_statement:
        return "Solution or question statement is missing."

    combined_prompt = f"Based of this {code_context} , Task Statement: {task_statement}\n\nSolution:\n{solution}\n\nRefactor the solution to enhance its cleanliness and efficiency:"

    try:
        stream_response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=combined_prompt,
            temperature=0.6,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )

        full_response = f"```\n{stream_response.choices[0].text.strip()}\n```"
        st.markdown(full_response, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return f"Error: {e}"


# Function to diagnose issues in the code
def diagnose_solution_issues(solution, task_statement, code_context):
    client = get_openai_client()
    if client is None:
        st.error("No Minato key provided.")
        return "Error: No Minato  key."

    if not solution or not task_statement:
        return "Solution or Question statement is missing."

    combined_prompt = f"Based of this {code_context}, Task Statement: {task_statement}\n\nSolution:\n{solution}\n\nDiagnose any issues present in the solution and provide explanations for them:"

    try:
        stream_response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=combined_prompt,
            temperature=0.6,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )

        full_response = f"```\n{stream_response.choices[0].text.strip()}\n```"
        st.markdown(full_response, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return f"Error: {e}"





# Function to give almost solution
def almost_solution_issues(solution, task_statement, code_context):
    client = get_openai_client()
    if client is None:
        st.error("No Minato Key provided.")
        return "Error: No Minato Key."

    if not solution or not task_statement:
        return "Solution or question statement or selected_files_paths  is missing."

    combined_prompt = f"Based of this: {code_context} ,  Task Statement: {task_statement}\n\nSolution:\n{solution}\n\nEvaluate the solution to determine if it is nearly correct. Provide guidance on what steps to take next :"

    try:
        stream_response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=combined_prompt,
            temperature=0.6,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )

        full_response = f"```\n{stream_response.choices[0].text.strip()}\n```"
        st.markdown(full_response, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return f"Error: {e}"
        
        

# Define the function to generate a Task based of codebase file
def generate_problems(difficulty, code_context):
    full_response = ""
    message_placeholder = st.empty()

    client = get_openai_client()
    if client is None:
        st.error("No Minato Key provided.")
        return

    combined_prompt = f"Create a {difficulty} level computer science task related to {code_context}, Please suggest a practical task for modifying an existing functionality or adding a new one. " \
                      f"Provide a problem statement."

    try:
        stream_response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=combined_prompt,
            temperature=0.6,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            
        )

        full_response = stream_response.choices[0].text.strip()


        sections = full_response.split('\n\n')

        # Separate labels and contents for each section
        problem_statement_label, problem_statement_content = sections[0].split(':', 1)


        colored_response = f"""
            <p><span style='color: red;'>{problem_statement_label}:</span>{problem_statement_content}</p> <!-- Problem Statement -->

        """
            

        # Store the colored response directly in the session state
        st.session_state['problem'] = colored_response

    except Exception as e:
        st.error(f"An error occurred: {e}")   


#generate task with codebase file
def generate_task(code_context, task):
    client = get_openai_client()
    if client is None:
        st.error("No Minato Key provided.")
        return "Error: No Minato Key."

    if not task:
        return "task statement is missing."

   
    combined_prompt = f"Based of this {code_context} Read carefully the Question: {task}\n\nProvide a explanation output, hint1, and hint2."
    

    try:
        stream_response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=combined_prompt,
            temperature=0.5,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )


        full_response = stream_response.choices[0].text.strip()


        sections = full_response.split('\n\n')

        # Separate labels and contents for each section
        explanation_output_label, explanation_output_content = sections[0].split(':', 1)
        hint1_input_label, hint1_input_content = sections[1].split(':', 1)
        hint2_output_label, hint2_output_content = sections[2].split(':', 1)

        colored_response = f"""
            <p><span style='color: red;'>{explanation_output_label}:</span>{explanation_output_content}</p> <!-- Explanation Output -->
            <p><span style='color: blue;'>{hint1_input_label}:</span>{hint1_input_content}</p> <!-- Hint1 Input -->
            <p><span style='color: green;'>{hint2_output_label}:</span>{hint2_output_content}</p> <!-- Hint2 Output -->
        """ 

        # Store the colored response directly in the session state
        st.session_state['task'] = colored_response

    except Exception as e:
        st.error(f"An error occurred: {e}") 

# Function to add documentation to the provided code
def generate_documentation(code_context):
    client = get_openai_client()
    if client is None:
        st.error("No Minato Key provided.")
        return "Error: No Minato Key."

    if not code_context:
        return "Selected file is missing."
        
    language = determine_language(code_context, "")
    #user_query = "Please enhance this code by adding clear and simple documentation, concise comments, Generate typehinted, descriptive docstrings that make the code easily understandable, making it understandable for both technical and non-technical individuals."
    
    
    user_query = f"Please enhance this code by adding clear and simple documentation, concise comments, and generate typehinted, descriptive docstrings. Make the documentation easily understandable for both technical and non-technical individuals. Please make sure that the response is formatted according to the specific programming language, including code syntax highlighting and relevant code formatting rules."

    
    combined_prompt = (
        f"Read carefully the code:\n{code_context}\n\n"
        f"Enhancement request: {user_query}\n\n"
        "Answer:"
    )

    try:
        stream_response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=combined_prompt,
            temperature=0.6,
            max_tokens=600,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )

        full_response = f"```\n{stream_response.choices[0].text.strip()}\n```"
        
        
        st.markdown(full_response, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return f"Error: {e}"





# Function to give clean code to the provided code
def generate_clean(code_context):
    client = get_openai_client()
    if client is None:
        st.error("No Minato Key provided.")
        return "Error: No Minato Key."

    if not code_context:
        return "Selected file is missing."
        
    language = determine_language(code_context, "")
    user_query = "Please improve this code by ensuring it is clean and efficient. Identify and automatically correct any instances of dead or duplicate code, code smells, overly complex structures, and security vulnerabilities. Additionally, please provide comments explaining each change you make for clarity and understanding."
    
    combined_prompt = (
        f"Read carefully the code:\n{code_context}\n\n"
        f"Enhancement request: {user_query}\n\n"
        "Answer:"
    )

    try:
        stream_response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=combined_prompt,
            temperature=0.6,
            max_tokens=600,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )

        full_response = f"```\n{stream_response.choices[0].text.strip()}\n```"
        st.markdown(full_response, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return f"Error: {e}"

# Function to generate front end code to the provided code
def generate_front(code_context):
    client = get_openai_client()
    if client is None:
        st.error("No Minato Key provided.")
        return "Error: No Minato Key."

    if not code_context:
        return "Selected file is missing."
        
    language = determine_language(code_context, "")
    user_query = "Please examine the provided code and determine if it is suitable for a frontend implementation. If it is, kindly generate the corresponding frontend code. However, if a frontend component is not applicable or necessary for this code, please indicate that no frontend development is required."
    
    combined_prompt = (
        f"Read carefully the code:\n{code_context}\n\n"
        f"Enhancement request: {user_query}\n\n"
        "Answer:"
    )

    try:
        stream_response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=combined_prompt,
            temperature=0.3,
            max_tokens=600,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )

        full_response = f"```\n{stream_response.choices[0].text.strip()}\n```"
        st.markdown(full_response, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return f"Error: {e}"
        

# Function to generate back end code to the provided code
def generate_back(code_context):
    client = get_openai_client()
    if client is None:
        st.error("No Minato Key provided.")
        return "Error: No Minato Key."

    if not code_context:
        return "Selected file is missing."
        
    language = determine_language(code_context, "")
    user_query = "Please examine the provided code and determine if it is suitable for a backend implementation. If it is, kindly generate the corresponding backend code. However, if a backend component is not applicable or necessary for this code, please indicate that no backend development is required."
    
    combined_prompt = (
        f"Read carefully the code:\n{code_context}\n\n"
        f"Enhancement request: {user_query}\n\n"
        "Answer:"
    )

    try:
        stream_response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=combined_prompt,
            temperature=0.4,
            max_tokens=600,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )

        full_response = f"```\n{stream_response.choices[0].text.strip()}\n```"
        
        st.markdown(full_response, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return f"Error: {e}"


@st.cache_data(ttl=3600, show_spinner=False)
def generate_query_response(user_query, code_context):
    try:
    
        client = get_openai_client()
        if client is None:
            return "No Minato Key provided."
        # Determine the language from the code context or user query
        #language = determine_language(code_context, user_query)

        combined_prompt = (
            f"Code Context:\n{code_context}\n\n"
            f"Question: {user_query}\n\n"
            "Answer:"
        )
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=combined_prompt,
            temperature=0.7,
            max_tokens=550,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        # Format the response
        #formatted_response = format_response(response.choices[0].text.strip(), language)
        
        full_response = f"```\n{response.choices[0].text.strip()}\n```"
             
   
        return full_response
    except Exception as e:
        return str(e)

        


def format_response(response, language):
    """
    Formats the response so that each sentence is on a new line.

    Parameters:
    response (str): The response text to be formatted.
    language (str): The language of the code.

    Returns:
    str: The formatted response.
    """
    # Split the response into sentences
    sentences = re.split(r'(?<=[.!?]) +', response)

    # Join the sentences with a newline character
    formatted_response = '\n'.join(sentences)

    # Check if the response is too long for a single line
    if len(formatted_response.split('\n')) > 1 or len(formatted_response) > 80:
        # Multi-line or long response
        return f"\n{formatted_response}\n"
    else:
        # Single-line response, add indentation for better readability
        return f"\n {formatted_response}\n"

        




def determine_language(code_context, user_query):
    """
    Determine the programming language from the code context or user query.

    Parameters:
    code_context (str): The code context or background information.
    user_query (str): The user's query.

    Returns:
    str: The identified language code for formatting.
    """
    # A mapping of keywords to language codes for formatting

    
    language_map = {
        'py': 'python', 'js': 'javascript', 'css': 'css',
        'cpp': 'cpp', 'dart': 'dart', 'java': 'java',
        'sol': 'solidity', 'php': 'php', 'cs': 'csharp',
        'go': 'go', 'rb': 'ruby', 'sql': 'sql',
        'swift': 'swift', 'kt': 'kotlin', 'html': 'html',
        'rs': 'rust', 'ts': 'typescript', 'pl': 'perl',
        'lua': 'lua', 'r': 'r', 'mat': 'matlab',
        'hs': 'haskell', 'sh': 'shell', 'ml': 'ocaml',
        'f#': 'fsharp', 'scala': 'scala', 'groovy': 'groovy',
        'vb': 'visualbasic', 'asm': 'assembly', 'elixir': 'elixir',
        'erl': 'erlang', 'prolog': 'prolog', 'lisp': 'lisp'
    }


    # Logic to determine the language from code_context or user_query
    # This is a placeholder, and you might need a more sophisticated method
    for key, value in language_map.items():
        if key in code_context or key in user_query:
            return value

    # Default to 'text' if no specific language is identified
    return 'text'

def handle_query(user_query, code_context):
    if user_query:
        query_result = generate_query_response(user_query, code_context)
        formatted_query = format_response(f" {user_query}", 'text')
        formatted_response = format_response(f" {query_result}", 'text')
        st.session_state.chat_history.append({"question": formatted_query, "answer": formatted_response})
        return query_result
    return ""
    
   
    
def main():
    
    
    # CSS styling
    st.markdown("""
        <style>
        .chatbox {
            border: 2px solid #008CBA;
            border-radius: 5px;
            padding: 10px;
            margin: 10px 0;
            background-color: #f1f1f1;
        }
        .chat-message {
            font-family: Arial, sans-serif;
            padding: 5px;
            margin: 4px 0;
            border-radius: 5px;
        }
        .user-message {
            background-color: #dff0d8;
            border: 1px solid #d6e9c6;
            color: #3c763d;
        }
        .bot-message {
            background-color: #d9edf7;
            border: 1px solid #bce8f1;
            color: #31708f;
        }
        .message-content {
            white-space: pre-line;
        }
        .question {
            font-weight: bold;
            color: #555;
        }
        .answer {
            font-weight: bold;
            color: #000;
        }
        </style>
    """, unsafe_allow_html=True)

    with st.expander("Configuration"):
        # Additional section for Discord and Email
        st.markdown("""
            - [🤑 Get Minato Free Credit](https://discord.gg/pNvPGqWfyX)

        """)
        
        st.markdown("""
    <h2>
        <span style="color: #2874A6; font-weight: bold; font-size: 24px;">Please add your Minato Key</span>
    </h2>
    """, unsafe_allow_html=True)
    
        api_key = st.text_input("Enter your Minato Key", type="password")
        if api_key:
            st.session_state["api_key"] = api_key
        else:
            st.warning("Please enter your Minato Key.")
            
    
    st.markdown("""
        Focus on enhancing an existing <span style="color: #2874A6; font-weight: bold;">Codebase</span> 
        by addressing <span style="color: #28B463; font-weight: bold;">Interactive</span> and 
        <span style="color: #CB4335; font-weight: bold;">Practical Real-World</span> Problems.
        """, unsafe_allow_html=True)
        
        
    # Initialize session state for chat history
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
        
                       
    def on_rm_error(func, path, exc_info):
        # Remove read-only attributes and retry
        os.chmod(path, stat.S_IWRITE)
        os.unlink(path)

    def clear_directory(directory):
        if os.path.exists(directory):
            for _ in range(5):  # Retry loop
                try:
                    shutil.rmtree(directory, onerror=on_rm_error)
                    os.makedirs(directory)
                    return
                except Exception as e:
                    print(f"Attempt to clear directory failed: {e}")
                    time.sleep(1)  # Wait a bit for any locks to be released
        else:
            os.makedirs(directory)  # Create directory if it doesn't exist

        raise Exception(f"Unable to clear the directory: {directory}")
        
    
    # Function to clone git repository


    def clone_git_repo(repo_url, destination):
        try:
        
            # Clear the destination directory before cloning
            clear_directory(destination)
            
            git.Repo.clone_from(repo_url, destination)
            return "Repository cloned successfully."
        except Exception as e:
            return f"Error cloning repository: {e}"
            
            
    def generate_tree_structure(startpath):
        tree = []
        for root, dirs, files in os.walk(startpath):
            level = root.replace(startpath, '').count(os.sep)
            indent = ' ' * 4 * (level)
            tree.append('{}{}/'.format(indent, os.path.basename(root)))
            subindent = ' ' * 4 * (level + 1)
            for f in files:
                tree.append('{}{}'.format(subindent, f))
        return "\n".join(tree)



    def list_files_recursively(directory):
        all_files = {}
        for root, dirs, files in os.walk(directory):
            for file in files:
                relative_path = os.path.relpath(os.path.join(root, file), directory)
                all_files[relative_path] = os.path.join(root, file)
        return all_files

    def filter_files(search_query, file_list):
        if not search_query:
            return file_list
        return [file for file in file_list if search_query.lower() in file.lower()]


    # Streamlit UI st.subheader("🌌: Clone Git Repository")
    

    repo_url = st.text_input("STEP 1 Enter the link to any GitHub repo")
    destination = "path/to/clone"  # You might consider making this a user input

    if st.button("Clone Repository"):
        message = clone_git_repo(repo_url, destination)
        st.write(message)

    with st.expander("View Repository Structure"):
        repo_structure = generate_tree_structure(destination)

        st_ace.st_ace(repo_structure, language='text', theme='github', height=300)


    

    # Recursive function to list all files in a directory and its subdirectories
    def list_files_recursively(directory):
        all_files = []
        for root, _, files in os.walk(directory):
            for file in files:
                all_files.append(os.path.join(root, file))
        return all_files

    if 'current_path' not in st.session_state:
        st.session_state['current_path'] = destination

    st.text("STEP 2:Please select the file you want to work with.")

    # Listing all files in the repository
    repo_files = []
    if os.path.exists(destination):
        repo_files = list_files_recursively(destination)


    # Selectbox for single file selection
    selected_files_paths = st.selectbox("Select a File to Display", repo_files, format_func=lambda x: os.path.relpath(x, destination))




    code_context = ""
    if selected_files_paths:
    
        file_name = os.path.basename(selected_files_paths)
        # Open the selected file
        with open(selected_files_paths, "r") as file:
            # Read the file content


            file_content = file.read()
        file_extension = file_name.split('.')[-1]
        

        
        language_map = {
        'py': 'python', 'js': 'javascript', 'css': 'css',
        'cpp': 'cpp', 'dart': 'dart', 'java': 'java',
        'sol': 'solidity', 'php': 'php', 'cs': 'csharp',
        'go': 'go', 'rb': 'ruby', 'sql': 'sql',
        'swift': 'swift', 'kt': 'kotlin', 'html': 'html',
        'rs': 'rust', 'ts': 'typescript', 'pl': 'perl',
        'lua': 'lua', 'r': 'r', 'mat': 'matlab',
        'hs': 'haskell', 'sh': 'shell', 'ml': 'ocaml',
        'f#': 'fsharp', 'scala': 'scala', 'groovy': 'groovy',
        'vb': 'visualbasic', 'asm': 'assembly', 'elixir': 'elixir',
        'erl': 'erlang', 'prolog': 'prolog', 'lisp': 'lisp'
        }
       
        language = language_map.get(file_extension, 'text')

        # Use an expander for theme and editor options
        with st.expander("Customize Editor"):
            # Theme selection
            theme = st.selectbox(
                'Select Theme',
                ('ambiance', 'chaos', 'chrome', 'clouds', 'clouds_midnight', 'cobalt', 'crimson_editor', 'dawn', 'dracula', 
                 'dreamweaver', 'eclipse', 'github', 'gob', 'gruvbox', 'idle_fingers', 'iplastic', 'katzenmilch', 'kr_theme', 
                 'kuroir', 'merbivore', 'merbivore_soft', 'mono_industrial', 'monokai', 'nord_dark', 'pastel_on_dark', 
                 'solarized_dark', 'solarized_light', 'sqlserver', 'terminal', 'textmate', 'tomorrow', 'tomorrow_night', 
                 'tomorrow_night_blue', 'tomorrow_night_bright', 'tomorrow_night_eighties', 'twilight', 'vibrant_ink', 'xcode'),
                index=30)  # Default to 'tomorrow_night_blue'

            # Editor keybinding selection
            keybinding = st.selectbox(
                'Select Keybinding',
                ('ace', 'vim', 'emacs', 'sublime', 'vscode', 'textmate'),
                index=4)  # Default to 'vscode'
                
        st_ace.st_ace(language=language, value=file_content, keybinding=keybinding, theme=theme, key=f"ace-editor-{file_content}", readonly=True, height=300)

        # Append file content to code_context for further processing
        #code_context += f"\n\nFile Content:\n{file_content}"
        code_context += f"\n\nFile Name: {file_name}\nFile Extension: .{file_extension}\nFile Content:\n{file_content}"






    # Flags to track which button has been pressed
    documentation_clicked = False
    clean_clicked = False
    front_clicked = False
    back_clicked = False

    # Creating a row of columns for the buttons
    col_run, col_diagnose, col_clean , col_back = st.columns(4)

    with col_run:
        documentation_clicked = st.button(' Get Documentation')

    with col_diagnose:
        clean_clicked = st.button("Make this Code Clean")

    with col_clean:
        front_clicked = st.button("Build Front-End")
    
    with col_back:
        back_clicked = st.button("Build Back-End")


    # Display output if 'Almost Solution' button was clicked
    if documentation_clicked:

        
        documentation = generate_documentation(code_context)

        
    # Display diagnosis if 'What's wrong with my solution?' button was clicked
    
    if clean_clicked:
        
        clean = generate_clean(code_context)
        

    # Display cleaned code if 'Make my solution clean' button was clicked
    if front_clicked:

        front = generate_front(code_context)

    # Display cleaned code if 'Make my solution clean' button was clicked
    if back_clicked:
        back = generate_back(code_context)


    query_col, button_col = st.columns([0.9, 0.1])

    with query_col:
        user_query = st.text_area("", value=st.session_state.get('user_query', ''), 
                                  placeholder="Type your question here...", key="query_input", height=100)

    with button_col:
        if st.button("🔍", key="query_submit_button"):
            if user_query:
                handle_query(user_query, code_context)
                with st.spinner('Waiting for response...'):
                    response = handle_query(user_query, code_context)
                    st.session_state.response = response


    # Display the response
    if 'response' in st.session_state and st.session_state.response:
        st.markdown(f"*Minato:*\n{st.session_state.response}")
        
    with st.expander("Chat History"):

        for chat in st.session_state.chat_history:
            st.markdown(chat['question'], unsafe_allow_html=True)
            st.markdown(chat['answer'], unsafe_allow_html=True)

        if st.button("Clear History", key="clear_history_button"):
            st.session_state.chat_history = []
            
            
            
            
            
            
    # let make it interactive         
            

    col1, col2 = st.columns(2)

    with col1:


        st.markdown("""
    <h2>
        <span style="color: #2874A6; font-weight: bold; font-size: 24px;">Tasks</span>
    </h2>
    """, unsafe_allow_html=True)

        selected_files_paths = st.selectbox("Select the same File from the Editor on the top", repo_files, format_func=lambda x: os.path.relpath(x, destination))
        task = st.text_area("Describe your task here")

        if st.button("Generate Hints"):
            generate_task(code_context, task)    
    
        # Display the challenge if it's stored in the session state
        if 'task' in st.session_state:
            st.markdown(st.session_state['task'], unsafe_allow_html=True)

            
        # Computer Science Problems in an expander
        with st.expander("Generate Task Problems "):
            difficulty = st.selectbox("Select Difficulty Level", ["Beginner", "Intermediate", "Hard", "Expert"], key='difficulty')

            selected_files_paths = st.selectbox("Select a File to Work", repo_files, format_func=lambda x: os.path.relpath(x, destination))
        


            if st.button("Generate Related Problems"):
                generate_problems(difficulty, code_context)

            # Display the challenge if it's stored in the session state
            if 'problem' in st.session_state:
                st.markdown(st.session_state['problem'], unsafe_allow_html=True)



    with col2:


        st.markdown("""
    <h2>
        <span style="color: #2874A6; font-weight: bold; font-size: 24px;">Solution Area</span>
    </h2>
    """, unsafe_allow_html=True)

        # Use an expander for theme and editor options
        with st.expander("Customize Editor"):
            # Theme selection
            theme = st.selectbox(
                'Select Theme',
                ('ambiance', 'chaos', 'chrome', 'clouds', 'clouds_midnight', 'cobalt', 'crimson_editor', 'dawn', 'dracula', 
                 'dreamweaver', 'eclipse', 'github', 'gob', 'gruvbox', 'idle_fingers', 'iplastic', 'katzenmilch', 'kr_theme', 
                 'kuroir', 'merbivore', 'merbivore_soft', 'mono_industrial', 'monokai', 'nord_dark', 'pastel_on_dark', 
                 'solarized_dark', 'solarized_light', 'sqlserver', 'terminal', 'textmate', 'tomorrow', 'tomorrow_night', 
                 'tomorrow_night_blue', 'tomorrow_night_bright', 'tomorrow_night_eighties', 'twilight', 'vibrant_ink', 'xcode'),
                index=33)  # Default to 'tomorrow_night_blue'

            # Editor keybinding selection
            keybinding = st.selectbox(
                'Select Keybinding',
                ('ace', 'vim', 'emacs', 'sublime', 'vscode', 'textmate'),
                index=3)  # Default to 'vscode'
                
            language= st.selectbox(
                'Select Language',
                ('python', 'javascript', 'css',
    'cpp', 'dart', 'java',
    'solidity', 'php', 'csharp',
    'go', 'ruby', 'sql',
    'swift', 'kotlin', 'html',
    'rust', 'typescript', 'perl',
    'lua', 'r', 'matlab',
    'haskell', 'shell', 'ocaml',
    'fsharp', 'scala', 'groovy',
    'visualbasic', 'assembly', 'elixir',
    'erlang', 'prolog', 'lisp'),
                index=0)
                
                
                
        # ACE editor
        code = st_ace.st_ace(language=language, keybinding=keybinding, theme=theme, placeholder="Write your code here...", height=400, key='code')

        solution = code

        st.caption('Click first on  :blue[Apply] before _Run code_  and others :sunglasses:')

        # Flags to track which button has been pressed
        almost_clicked = False
        diagnose_clicked = False
        clean_clicked = False

        # Creating a row of columns for the buttons
        col_run, col_diagnose, col_clean = st.columns(3)

        with col_run:
            almost_clicked = st.button(' Almost There??')

        with col_diagnose:
            diagnose_clicked = st.button("Solution Checking")

        with col_clean:
            clean_clicked = st.button("Clean Solution")

        # Display output if 'Almost Solution' button was clicked
        if almost_clicked:

            task_statement = st.session_state.get('task', '')
            almost = almost_solution_issues(solution, task_statement, code_context)
            
        # Display diagnosis if 'What's wrong with my solution?' button was clicked
        
        if diagnose_clicked:
            task_statement = st.session_state.get('task', '')
            diagnosis = diagnose_solution_issues(solution, task_statement, code_context)
            

        # Display cleaned code if 'Make my solution clean' button was clicked
        if clean_clicked:
            task_statement = st.session_state.get('task', '')
            cleaned_solution = clean_up_solution(solution, task_statement, code_context)
            
  

if __name__ == "__main__":
    main()





# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
