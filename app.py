import streamlit as st
from langchain_community.llms import Ollama
from langchain.agents import AgentType, initialize_agent, Tool
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
import traceback
from tools import (
    search_products, estimate_shipping, check_promo, 
    compare_prices, get_return_policy
)

# Initialize session state for memory
if 'memory' not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

def create_llm():
    """Create and return the language model."""
    return Ollama(model="mistral", temperature=1.0)

def create_agent_tools():
    """Create and return the list of tools for the agent."""
    return [
        Tool(
            name="SearchProducts",
            func=search_products,
            description="Search for fashion products across multiple e-commerce websites. also provides the url of the product"
        ),
        Tool(
            name="EstimateShipping",
            func=estimate_shipping,
            description="Get shipping estimates including cost and delivery time"
        ),
        Tool(
            name="CheckPromoCode",
            func=check_promo,
            description="Validate and calculate discounted prices with promo codes"
        ),
        Tool(
            name="ComparePrices",
            func=compare_prices,
            description="Compare prices for a product across different stores"
        ),
        Tool(
            name="GetReturnPolicy",
            func=get_return_policy,
            description="Get return policy details for a specific store"
        )
    ]

def initialize_shopping_agent():
    """Initialize and return the shopping agent and its components."""
    llm = create_llm()
    agent_tools = create_agent_tools()

    template = """You are a shopping assistant with access to real-time price data.
        For ANY shopping query:
        1. ALWAYS use SearchProducts first to find matching items
        2. ALWAYS use ComparePrices to compare prices across stores
        3. NEVER give generic advice - always show actual prices
        4. ALWAYS include product links and availability
        
        Previous conversation:
        {chat_history}
        
        Human: {input}
        Assistant: I'll search for these products and if needed will compare prices across different stores."""

    shopping_prompt = PromptTemplate(
        input_variables=["chat_history", "input"],
        template=template
    )
    
    agent = initialize_agent(
        tools=agent_tools,
        llm=llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        memory=st.session_state.memory,
        prompt=shopping_prompt, 
        verbose=True
    )
    
    return agent

def format_response(response: str) -> dict:
    """Format the agent's response for better display."""
    ai_message = response['output']
    
    formatted = {
        'main_response': ai_message,
        'price_comparison': None,
        'shipping': None,
        'promo': None
    }
    
    if "price comparison" in ai_message.lower():
        formatted['price_comparison'] = "Price comparison data here"
        
    if "shipping" in ai_message.lower():
        formatted['shipping'] = "Shipping details here"
        
    if "promo" in ai_message.lower():
        formatted['promo'] = "Promotion details here"
        
    return formatted

def process_query(agent, query: str) -> dict:
    """Process a user query using the shopping agent."""
    try:
        response = agent.invoke(query)
        formatted_response = format_response(response)
        return formatted_response
    except Exception as e:
        print(traceback.format_exc())
        return {'main_response': f"Error: {str(e)}", 'price_comparison': None, 'shipping': None, 'promo': None}

def main():
    st.set_page_config(page_title="AI Shopping Assistant", page_icon="🛍️")
    
    # Application title and description
    st.title("🛍️ AI Shopping Assistant")
    st.markdown("""
    Your personal shopping assistant that can:
    - Search products across multiple stores
    - Compare prices
    - Check shipping estimates
    - Validate promo codes
    - Check return policies
    """)
    
    # Initialize the agent
    agent = initialize_shopping_agent()
    
    # Query input
    query = st.text_input("What would you like to shop for today?")
    
    if st.button("Search"):
        if query:
            with st.spinner("Searching for the best options..."):
                response = process_query(agent, query)
                
                # Add to chat history
                st.session_state.chat_history.append({"role": "user", "content": query})
                st.session_state.chat_history.append({"role": "assistant", "content": response['main_response']})
                
                # Display main response
                st.markdown("### Response:")
                st.write(response['main_response'])
                
                # Display additional information in expandable sections
                if response['price_comparison']:
                    with st.expander("💰 Price Comparison"):
                        st.write(response['price_comparison'])
                        
                if response['shipping']:
                    with st.expander("🚚 Shipping Options"):
                        st.write(response['shipping'])
                        
                if response['promo']:
                    with st.expander("🏷️ Promotion Details"):
                        st.write(response['promo'])
    
    # Display chat history
    st.markdown("### Chat History")
    for message in st.session_state.chat_history:
        role_icon = "🤔" if message["role"] == "user" else "🛍️"
        st.write(f"{role_icon} **{message['role'].title()}:** {message['content']}")
    
    # Clear chat history button
    if st.button("Clear Chat History"):
        st.session_state.chat_history = []
        st.session_state.memory.clear()
        st.experimental_rerun()

if __name__ == "__main__":
    main()
