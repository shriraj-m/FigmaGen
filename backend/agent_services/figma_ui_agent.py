from langchain_core.messages import SystemMessage, HumanMessage

"""
This agent is responsible for creating a Figma UI design based on a prompt.

Args:
    system_prompt: The system prompt for the agent.
    llm: The language model to use for the agent.
Returns:
    Agent's response, which should be a Figma UI design JSON object.
"""

class FigmaUIAgent:
    def __init__(self, _system_prompt, _chat_instance):
        self.system_prompt = _system_prompt
        self.chat_instance = _chat_instance

    def chat(self, state):
        user_message = state["messages"]
        
        if isinstance(user_message, str):
            user_message = user_message
        elif isinstance(user_message, list):
            # Get the last message if it's a list
            user_message = user_message[-1].content if isinstance(user_message[-1], HumanMessage) else user_message[-1]

        # Generate the Figma design
        response = self.chat_instance.invoke([
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=user_message)
        ])

        return {
            "messages": response
        }


