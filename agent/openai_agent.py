from dotenv import load_dotenv
from langchain.agents import initialize_agent, AgentType
from langchain.schema import HumanMessage
from langchain.tools import tool, Tool
from langchain_openai import ChatOpenAI
import json
import os
from pathlib import Path

# --- Setup ---

load_dotenv()
llm = ChatOpenAI(model="gpt-4", temperature=0)

# --- Core Functions ---

def load_json(path: str) -> dict:
    """Load a JSON file from disk."""
    with open(path, 'r') as f:
        data = json.load(f)
        # Extract only relevant information for LLM: file, line, message, rule
        if "issues" in data:
            simplified_issues = []
            for issue in data["issues"]:
                simplified_issues.append({
                    "file": os.path.basename(issue.get("component", "")),
                    "line": issue.get("line", ""),
                    "message": issue.get("message", ""),
                    "rule": issue.get("rule", "")
                })
            data["issues"] = simplified_issues
        return data

def load_js_files(directory: str) -> dict:
    """Load all .js files from a directory into a dict {filename: content}."""
    code = {}
    for file in Path(directory).glob("*.js"):
        with open(file, 'r') as f:
            code[file.name] = f.read()
    return code

def generate_prompt(code: str, issues: str) -> str:
    """Generate a prompt for the LLM to fix code based on SonarQube issues."""
    return (
        "You are an expert JavaScript developer and debugger.\n"
        "You will fix code based on static analysis issues and refactor code as required.\n\n"
        "Here is the code:\n"
        "javascript\n"
        f"{code}\n\n"
        "And here are the issues from SonarQube:\n"
        f"{issues}\n\n"
        "Return only the full fixed code, no backticks or explanations."
    )

def fix_code_with_llm(code: str, issues: str) -> str:
    """Send code and issues to the LLM and return the fixed code, removing any Markdown backticks."""
    prompt = generate_prompt(code, issues)
    response = llm([HumanMessage(content=prompt)])
    content = response.content.strip()
    # Remove Markdown code block backticks if present
    if content.startswith("```") and content.endswith("```"):
        # Remove the first and last lines (the backticks)
        lines = content.splitlines()
        # If the first line is like ```js or ```javascript, remove it
        if lines[0].strip().startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        content = "\n".join(lines)
    return content

def fix_code_from_sonar(json_path: str, code_dir: str) -> dict:
    """Fix all JS files in code_dir using issues from SonarQube JSON."""
    sonar = load_json(json_path)
    code_files = load_js_files(code_dir)
    # Map issues to filenames
    issues_by_file = {}
    for issue in sonar.get("issues", []):
        file = issue.get("file", "")
        issues_by_file.setdefault(file, []).append(issue["message"])
    # Fix files
    fixed = {}
    for filename, code in code_files.items():
        issues = "\n".join(issues_by_file.get(filename, []))
        if issues:
            print(f"🔧 Fixing: {filename}")
            fixed[filename] = fix_code_with_llm(code, issues)
        else:
            fixed[filename] = code
    return fixed

def write_fixed_files(fixed: dict, output_dir: str = "fixed") -> None:
    """Write fixed files to the output directory."""
    os.makedirs(output_dir, exist_ok=True)
    for filename, content in fixed.items():
        path = os.path.join(output_dir, filename)
        with open(path, "w") as f:
            f.write(content)
        print(f"✅ Saved: {path}")

# --- Tool for Agent ---

@tool
def sonar_fix_tool(tool_input: str) -> str:
    """
    Fix code using SonarQube JSON and source folder.
    tool_input: JSON string with 'json_path', 'code_dir', and optional 'output_dir'.
    """
    try:
        args = json.loads(tool_input)
        json_path = args["json_path"]
        code_dir = args["code_dir"]
        output_dir = args.get("output_dir", "fixed")
    except Exception as e:
        return f"Invalid input: {e}"
    fixed = fix_code_from_sonar(json_path, code_dir)
    write_fixed_files(fixed, output_dir)
    return f"Fixed files written to {output_dir}:\n" + "\n".join(fixed.keys())

# --- Agent Factory ---

def get_code_fixing_agent():
    """Return a LangChain agent for fixing code using SonarQube JSON and source folder."""
    tools = [
        Tool.from_function(
            sonar_fix_tool,
            name="sonar_fix_tool",
            description="Fix code using SonarQube JSON and source folder. Args: json_path, code_dir, output_dir (optional)."
        )
    ]
    return initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
