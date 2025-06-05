from openai_agent import get_code_fixing_agent, write_fixed_files


agent = get_code_fixing_agent()
result = agent.run("Fix the code using SonarQube issues in file agent/SQ.json and folder ./appdemo/src")
print(result)
# write_fixed_files(fixed_code)