from openai_agent import fix_all_code, write_fixed_files


fixed_code = fix_all_code("agent/SQ.json", "appdemo/src")  
write_fixed_files(fixed_code)