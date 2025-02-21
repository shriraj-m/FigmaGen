from langchain_core.messages import SystemMessage, HumanMessage

"""
This agent is responsible for giving the previous agent's design a theme and color palette.
Args:
    system_prompt: The system prompt for the agent.
    llm: The language model to use for the agent.
Returns:
    Agent's response, which should be an updated version of the previous agent's Figma UI design JSON object.
"""

class FigmaThemeAgent:
    def __init__(self, _system_prompt, _chat_instance):
        self.system_prompt = _system_prompt
        self.chat_instance = _chat_instance

    def chat(self, state):
        message = state["messages"][-1].content
        print(message)
        
        response = self.chat_instance.invoke([
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=message)
        ])

        return {
            "messages": response
        }


