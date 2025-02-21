import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, END, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from prompts import figma_ui_agent_prompt


load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
model = "llama-3.3-70b-specdec"

llm = ChatGroq(temperature=0,
               api_key=api_key, 
               model_name=model,
               max_tokens=4096)

figma_ui_prompt = figma_ui_agent_prompt()

