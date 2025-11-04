from smolagents import ToolCallingAgent, LiteLLMModel, DuckDuckGoSearchTool, WikipediaSearchTool
import os
from channels.db import database_sync_to_async
from .models import Celebrity, User

# ✅ Async-safe DB fetch
@database_sync_to_async
def get_user_and_celebrity(user_id, celebrity_id):
    """Fetch user and celebrity objects in a thread-safe way for async context."""
    user = User.objects.get(id=user_id)
    celebrity = Celebrity.objects.get(id=celebrity_id)
    return user, celebrity

# ✅ Helper to extract text from streaming deltas
def extract_text_from_delta(delta):
    """Extract incremental text from ChatMessageStreamDelta."""
    text = ""

    if getattr(delta, "content", None):
        text += delta.content

    if getattr(delta, "tool_calls", None):
        for tool_call in delta.tool_calls:
            args = getattr(tool_call, "arguments", None)
            if isinstance(args, dict) and "answer" in args:
                text += args["answer"]
            elif isinstance(args, str):
                text += args
    return text


# ✅ Streaming agent function (no DB access inside)
def agent_chat_stream(user_message: str, instructions: str):
    """
    Simple approach that only streams the tool call arguments
    """
    deepseek_model = LiteLLMModel(
        model_id="deepseek/deepseek-chat",
        api_base="https://api.deepseek.com",
        api_key=os.getenv("DEEPSEEK_API_KEY"),
    )

    agent = ToolCallingAgent(
        model=deepseek_model,
        tools=[DuckDuckGoSearchTool(), WikipediaSearchTool()],
        max_steps=1,
        instructions=instructions,
        stream_outputs=True
    )

    print(f"🔄 Starting simple smolagents streaming...")
    
    full_response = ""
    
    for token in agent.run(user_message, stream=True):
        # Focus only on extracting the answer text from tool call arguments
        if hasattr(token, 'tool_calls') and token.tool_calls:
            for tool_call in token.tool_calls:
                if (hasattr(tool_call, 'function') and 
                    hasattr(tool_call.function, 'arguments') and 
                    tool_call.function.arguments):
                    
                    args = tool_call.function.arguments
                    if args and args != full_response:
                        # This is new content - extract just the text parts
                        new_content = args.replace(full_response, "")
                        
                        # Clean the content - remove JSON syntax, keep only text
                        clean_content = new_content.replace('{"answer": "', '').replace('"}', '').replace('"', '')
                        
                        if clean_content and clean_content not in ['{', '}', ':']:
                            full_response = args
                            print(f"🎯 Text token: '{clean_content}'")
                            yield clean_content

    # If we didn't get proper streaming but have a final answer
    if not full_response:
        # Try to get the final answer from the completed run
        result = agent.run(user_message)
        if result:
            response_text = str(result)
            print(f"📦 Streaming final answer: {response_text}")
            # Stream word by word
            words = response_text.split()
            for word in words:
                yield word + ' '