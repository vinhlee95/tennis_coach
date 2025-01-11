from pydantic_ai import Agent
from dotenv import load_dotenv

load_dotenv()

agent = Agent(
  model="google-gla:gemini-2.0-flash-exp",
  system_prompt="You are a helpful assistant that can answer questions related to Tennis",
)

result = agent.run_sync("I want to improve my forehand. I have an Eastern grip. Give me links to 5 YouTube video to improve.")

print(result)
