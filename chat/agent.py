
from smolagents import ToolCallingAgent, LiteLLMModel,DuckDuckGoSearchTool,WikipediaSearchTool
import os
from .models import Celebrity,User


def agent_chat(user_message: str,id: int,celebrity_id:int) -> str:
    celebrity = Celebrity.objects.get(id=celebrity_id)
    user=User.objects.get(id=id)
    instructions = celebrity.description+f". You are chatting with {user.username}. use his name in the conversation. if a user use language other than english respond in that language. "
       
    deepseek_model = LiteLLMModel(
            model_id="deepseek/deepseek-chat",
            api_base="https://api.deepseek.com",
            api_key=os.getenv("DEEPSEEK_API_KEY"),
    )
        

        # Create agent
    agent = ToolCallingAgent(
            model=deepseek_model,
            tools=[DuckDuckGoSearchTool(),WikipediaSearchTool()],
            max_steps=1,
            instructions=instructions
    )

        # Run the agent
    return agent.run(user_message)
