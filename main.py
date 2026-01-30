"""
Conversational Knowledge Bot - Command Line Interface
Uses Groq LLM, DuckDuckGo Search, and Wikipedia with LangChain Memory
"""

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import AgentType, initialize_agent
from langchain.memory import ConversationBufferMemory
from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper

# Load environment variables
load_dotenv()

# Initialize LLM - Groq (Free, Fast, No CC required)
def initialize_llm():
    """Initialize Groq LLM with free API"""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("Please set GROQ_API_KEY in .env file")

    # Using llama-3.1-8b-instant model (free tier, fast, currently supported)
    llm = ChatGroq(
        groq_api_key=api_key,
        model_name="llama-3.1-8b-instant",  # Fast, currently supported model
        temperature=0.3,  # Lower temperature for more focused responses
        max_tokens=256  # Further reduced to conserve tokens and encourage concise answers
    )
    return llm

# Initialize Tools
def initialize_tools():
    """Initialize free search tools (no API keys needed)"""

    # Wikipedia Tool (Free, no limits)
    wikipedia = WikipediaQueryRun(
        api_wrapper=WikipediaAPIWrapper(
            top_k_results=2,
            doc_content_chars_max=500
        )
    )

    # DuckDuckGo Search Tool (Free, no API key)
    duckduckgo = DuckDuckGoSearchRun()

    tools = [wikipedia, duckduckgo]

    return tools

# Create Agent with Memory
def create_conversational_agent(llm, tools, memory):
    """Create a conversational agent with tools and memory"""

    # Create agent using initialize_agent (compatible with LangChain 0.3.0)
    agent_executor = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,  # Better for web searches
        memory=memory,
        verbose=True,  # Keep verbose for CLI to see what's happening
        handle_parsing_errors=True,
        max_iterations=3,  # Reduced to prevent infinite loops
        early_stopping_method="generate",  # Generate answer if limit reached
        max_execution_time=20,  # 20 seconds timeout
        return_intermediate_steps=False
    )

    return agent_executor

def main():
    """Main function to run the conversational bot"""
    print("=" * 60)
    print("Conversational Knowledge Bot")
    print("Powered by: Groq LLM + DuckDuckGo + Wikipedia + LangChain")
    print("=" * 60)
    print("\nInitializing bot...\n")

    try:
        # Initialize components
        llm = initialize_llm()
        tools = initialize_tools()
        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )

        # Create agent
        agent_executor = create_conversational_agent(llm, tools, memory)

        print("✅ Bot initialized successfully!")
        print("\nType 'quit', 'exit', or 'bye' to end the conversation.\n")
        print("-" * 60)

        # Chat loop
        while True:
            user_input = input("\n👤 You: ").strip()

            if user_input.lower() in ['quit', 'exit', 'bye', 'q']:
                print("\n🤖 Bot: Goodbye! Have a great day!")
                break

            if not user_input:
                continue

            try:
                # Get response from agent
                response = agent_executor.invoke({"input": user_input})
                print(f"\n🤖 Bot: {response.get('output', 'I could not generate a response.')}")

            except Exception as e:
                error_str = str(e)
                if "iteration limit" in error_str.lower() or "agent stopped" in error_str.lower():
                    print(f"\n❌ I took too long to answer. Try rephrasing your question or making it more specific.")
                else:
                    print(f"\n❌ Error: {error_str}")
                    print("Please try rephrasing your question.")

    except ValueError as e:
        print(f"\n❌ Configuration Error: {str(e)}")
        print("\nPlease follow these steps:")
        print("1. Sign up for free at https://console.groq.com/")
        print("2. Get your API key")
        print("3. Create a .env file and add: GROQ_API_KEY=your_key_here")
    except Exception as e:
        print(f"\n❌ Unexpected Error: {str(e)}")

if __name__ == "__main__":
    main()

