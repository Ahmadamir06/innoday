import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

# Load environment variables
load_dotenv()

# Make sure the key is set
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not set in environment!")

# Initialize chat model
llm = ChatOpenAI(
    openai_api_key=api_key,
    model_name="gpt-4o",  # or "gpt-4", "gpt-3.5-turbo"
    temperature=0.3
)

# Create a test prompt
test_prompt = [
    HumanMessage(content="Write a short Python function that reverses a string.")
]

# Run the model and print the response
response = llm(test_prompt)
print("\n🔁 Response from OpenAI:\n")
print(response.content)