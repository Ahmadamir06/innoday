import os
import json
from pathlib import Path
from anthropic import Anthropic
from dotenv import load_dotenv

from dotenv import load_dotenv

# Load environment variables (e.g., ANTHROPIC_API_KEY)
load_dotenv()


client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Load SonarQube JSON
def load_sonarqube_results(json_path):
    with open(json_path, 'r') as f:
        return json.load(f)

# Load all JavaScript code files from directory
def load_code_files(code_dir):
    code_files = {}
    for file in Path(code_dir).glob("*.js"):
        with open(file, 'r') as f:
            code_files[file.name] = f.read()
    return code_files

# Create a prompt from code and its issues
def generate_prompt(code, issues):
    return f"""You are an expert JavaScript developer and debugger.
            You will fix code based on static analysis issues (by SonarQube).

            Here is the code:
            ```javascript
            {code}
            And here are the issues from SonarQube:
            {issues}
            please return only the fixed code with no explanation"""


def get_fixes_from_claude(code, issues):
    prompt = generate_prompt(code, issues)
    response = client.messages.create(
    model="claude-3-sonnet-20240229",
    max_tokens=2048,
    temperature=0.3,
    messages=[
    {"role": "user", "content": prompt}
    ]
    )
    return response.content[0].text # Returns only the message text

def fix_all_code(json_path, code_dir):
    sonar_data = load_sonarqube_results(json_path)
    code_files = load_code_files(code_dir)
    # Map SonarQube issues to each file
    issues_by_file = {}
    for issue in sonar_data["issues"]:
        file_path = os.path.basename(issue["component"].split(":")[-1])
        issues_by_file.setdefault(file_path, []).append(issue["message"])

    # Apply fixes using Claude
    fixed_files = {}
    for filename, code in code_files.items():
        issues = "\n".join(issues_by_file.get(filename, []))
        if issues:
            fixed_code = get_fixes_from_claude(code, issues)
            fixed_files[filename] = fixed_code
        else:
            fixed_files[filename] = code  # No issues to fix

    return fixed_files
