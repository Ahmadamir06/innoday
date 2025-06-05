import os
import json
from pathlib import Path
from langchain.chat_models import ChatAnthropic
from langchain.schema import SystemMessage, HumanMessage
from langchain.prompts import PromptTemplate

# Initialize Claude via LangChain
llm = ChatAnthropic(model="claude-3-sonnet-20240229", temperature=0)

# Load SonarQube JSON
def load_sonarqube_results(json_path):
    with open(json_path, 'r') as f:
        return json.load(f)

# Load all code files from directory
def load_code_files(code_dir):
    code_files = {}
    for file in Path(code_dir).glob("*.py"):  # Adjust extension if needed
        with open(file, 'r') as f:
            code_files[file.name] = f.read()
    return code_files

# Create a prompt from code and its issues
def generate_prompt(code, issues):
    prompt_template = PromptTemplate.from_template(
        """You are an expert debugger that fixes code based on static analysis issues.
            Here is the code:
        ```javascript
        {code}
        And here are the issues from SonarQube:
        {issues}
        Please return the fixed code only, with no explanation."""
        )
    
    return prompt_template.format(code=code, issues=issues)

def get_fixes_from_ai(code, issues):
    prompt = generate_prompt(code, issues)
    messages = [
    SystemMessage(content="You are a helpful AI assistant and an experct coder that fixes code issues."),
    HumanMessage(content=prompt)
    ]
    return llm(messages).content

def fix_all_code(json_path, code_dir):
    sonar_data = load_sonarqube_results(json_path)
    code_files = load_code_files(code_dir)
    # Map SonarQube issues to each file
    issues_by_file = {}
    for issue in sonar_data["issues"]:
        file_path = os.path.basename(issue["component"].split(":")[-1])
        issues_by_file.setdefault(file_path, []).append(issue["message"])

    # Apply fixes
    fixed_files = {}
    for filename, code in code_files.items():
        issues = "\n".join(issues_by_file.get(filename, []))
        if issues:
            fixed_code = get_fixes_from_ai(code, issues)
            fixed_files[filename] = fixed_code
        else:
            fixed_files[filename] = code  # No issues to fix

    return fixed_files