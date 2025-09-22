from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
import os

# Define the node function that will handle the conversation
def conversation_node(state: MessagesState):
    """Single node that processes conversation using OpenAI GPT-4o"""
    # Initialize the OpenAI model
    model = ChatOpenAI(model="gpt-4o", temperature=0.7)
    
    # Generate response using the model with the entire message history
    response = model.invoke(state["messages"])
    
    # Return the response as a new message (it should already be an AIMessage)
    return {"messages": [response]}

# Construct the graph using MessagesState
workflow = StateGraph(MessagesState)

# Add the single conversation node
workflow.add_node("conversation_agent", conversation_node)

# Set up the flow: START -> conversation_agent -> END
workflow.add_edge(START, "conversation_agent")
workflow.add_edge("conversation_agent", END)

# Compile the graph
graph = workflow.compile()
