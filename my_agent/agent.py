from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import os

# Define the node function that will handle the conversation
def conversation_node(state: MessagesState):
    """Single node that processes conversation using OpenAI GPT-4o with markdown output"""
    # Initialize the OpenAI model
    model = ChatOpenAI(model="gpt-4o", temperature=0.7)
    
    # Create system message to ensure markdown output
    system_message = SystemMessage(content="""You are a helpful AI assistant. Always format your responses in markdown to ensure proper rendering in the frontend UI. Use markdown formatting for:

- **Bold text** for emphasis
- *Italic text* for subtle emphasis
- `Code snippets` for technical terms
- ```code blocks``` for multi-line code
- # Headers for structure
- - Bullet points for lists
- 1. Numbered lists for steps
- > Blockquotes for important information
- [Links](url) for references
- Tables for structured data

Ensure your responses are well-formatted and visually appealing using markdown syntax.""")
    
    # Combine system message with conversation history
    messages = [system_message] + state["messages"]
    
    # Generate response using the model with the entire message history
    response = model.invoke(messages)
    
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
