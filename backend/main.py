import os
import random
import string

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, END, START
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver

from agent_services.prompts import figma_ui_agent_prompt, figma_theme_agent_prompt
from agent_services.figma_ui_agent import FigmaUIAgent
from agent_services.figma_theme_agent import FigmaThemeAgent

def generate_random_code() -> str:
    """
    Generate a random alphanumeric code with a length of 8
    Returns:
        str: Random alphanumeric code
    """
    characters = string.ascii_letters + string.digits  # combines letters and numbers
    return ''.join(random.choice(characters) for _ in range(8))


load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
model = os.getenv("MODEL_Z")

llm = ChatGroq(temperature=0,
               api_key=api_key, 
               model_name=model,
               max_tokens=8000)

figma_ui_prompt = figma_ui_agent_prompt()
figma_theme_prompt = figma_theme_agent_prompt()

figma_ui_agent = FigmaUIAgent(figma_ui_prompt, llm)
figma_theme_agent = FigmaThemeAgent(figma_theme_prompt, llm)


memory = MemorySaver()

unique_id = generate_random_code()
print(f"Unique ID: {unique_id}")
config = {
        "recursion_limit": 10,
        "thread_id": "main_thread",
        "checkpoint_id": unique_id,
        "checkpoint_ns": "test_implementation"
}

class OverallState(TypedDict):
    messages: Annotated[list, add_messages]


figma_graph = StateGraph(OverallState)
figma_graph.add_node("figma_ui_agent", figma_ui_agent.chat)
figma_graph.add_node("figma_theme_agent", figma_theme_agent.chat)


figma_graph.add_edge(START, "figma_ui_agent")
# figma_graph.add_edge("figma_ui_agent", "figma_theme_agent")
figma_graph.add_edge("figma_ui_agent", END)


complete_graph = figma_graph.compile(checkpointer=memory)

def call_agent_workflow(prompt):
    events = complete_graph.stream({
        "messages": [HumanMessage(content=prompt)],
    }, config)

    for event in events:
        # print(event)
        print('===============')
        # if 'figma_theme_agent' in event:
        #     response = event['figma_theme_agent']['messages'].content
        #     print(response)
        #     print('===============')
        response = event['figma_ui_agent']['messages'].content

    return response
