import os
import json
from pathlib import Path
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

# Load environment variables (e.g., OPENAI_API_KEY)
load_dotenv()

# Create OpenAI Chat Model
llm = ChatOpenAI(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    model_name="gpt-4o",
    temperature=0.3,
    max_tokens=2048
)

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
    return f"""You are an expert Python developer and debugger.
        You will fix code based on static analysis issues and refactor code as required.

        Here is the code:
        ```javascript
        {code}

        And here are the issues from SonarQube:
        {issues}

        Please return only the fixed code file with no explanation, backticks or markdown formatting."""


def get_fixes_from_openai(code, issues):
    prompt = generate_prompt(code, issues)
    response = llm([HumanMessage(content=prompt)])
    print(f"\n🔧 Fix from LLM:\n{response.content}\n")
    return response.content


def fix_all_code(json_path, code_dir):
    sonar_data = load_sonarqube_results(json_path)
    code_files = load_code_files(code_dir)

    # Organize issues by filename
    issues_by_file = {}
    for issue in sonar_data["issues"]:
        file_path = os.path.basename(issue["component"].split(":")[-1])
        issues_by_file.setdefault(file_path, []).append(issue["message"])

    fixed_files = {}
    for filename, code in code_files.items():
        issues = "\n".join(issues_by_file.get(filename, []))
        print(f"\n📂 Processing: {filename}")
        if issues:
            fixed_code = get_fixes_from_openai(code, issues)
            fixed_files[filename] = fixed_code
        else:
            fixed_files[filename] = code  # No changes needed

    return fixed_files

def write_fixed_files(fixed_files: dict, output_dir: str = "./fixed"):
    os.makedirs(output_dir, exist_ok=True)
    for filename, content in fixed_files.items():
        output_path = os.path.join(output_dir, filename)
        with open(output_path, "w") as f:
            f.write(content)
        print(f"✅ Saved fixed file: {output_path}")