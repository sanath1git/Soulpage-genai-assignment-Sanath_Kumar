"""
Conversational Knowledge Bot - Streamlit UI
Task: LangChain + Tools + Memory
"""

import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import AgentType, initialize_agent
from langchain.memory import ConversationBufferMemory
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool
from duckduckgo_search import DDGS

load_dotenv()

st.set_page_config(
    page_title="Conversational Knowledge Bot",
    page_icon="🤖",
    layout="centered"
)


def get_llm():
    """Initialize Groq LLM"""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        st.error("❌ GROQ_API_KEY not found in .env file")
        st.stop()

    return ChatGroq(
        groq_api_key=api_key,
        model_name="llama-3.1-8b-instant",
        temperature=0.5,
        max_tokens=512
    )


def search_web(query: str) -> str:
    """DuckDuckGo web search with better results"""
    try:
        with DDGS(timeout=15) as ddgs:
            results = list(ddgs.text(query, max_results=6))

            if results:
                output = []
                for i, r in enumerate(results[:4], 1):
                    title = r.get('title', '')
                    body = r.get('body', '')
                    if body:
                        body = body[:350].strip()
                    output.append(f"Result {i}: {title}\n{body}")

                return "\n\n".join(output)
            return "No search results found."
    except Exception as e:
        return f"Search unavailable: {str(e)}"


def search_wiki(query: str) -> str:
    """Wikipedia search"""
    try:
        wiki = WikipediaQueryRun(
            api_wrapper=WikipediaAPIWrapper(
                top_k_results=2,
                doc_content_chars_max=1000
            )
        )
        return wiki.run(query)
    except Exception as e:
        return f"Wikipedia error: {str(e)}"


def get_tools():
    """Get search tools"""
    return [
        Tool(
            name="WebSearch",
            func=search_web,
            description=(
                "Searches the web for current information. Use this for questions about:\n"
                "- Company CEOs and executives (e.g., 'Perplexity AI CEO', 'OpenAI CEO')\n"
                "- Recent news and events\n"
                "- Startups and tech companies\n"
                "Input: A search query like 'Perplexity AI CEO' or 'CEO of Tesla'\n"
                "Output: Multiple search results with titles and descriptions. Read them to find the answer."
            )
        ),
        Tool(
            name="Wikipedia",
            func=search_wiki,
            description=(
                "Searches Wikipedia for factual information. Use this for:\n"
                "- Well-known people and historical figures\n"
                "- Established companies\n"
                "- Scientific concepts and general knowledge\n"
                "Input: Topic name like 'Apple Inc' or 'Sam Altman'\n"
                "Output: Detailed Wikipedia article content"
            )
        )
    ]


def create_agent(llm, tools, memory):
    """Create conversational agent with memory"""
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
        memory=memory,
        verbose=False,
        handle_parsing_errors=True,
        max_iterations=5,
        early_stopping_method="generate",
        max_execution_time=40,
        return_intermediate_steps=False,
        agent_kwargs={
            "prefix": (
                "You are a helpful AI assistant with access to web search and Wikipedia. "
                "When asked about a CEO or founder, always use WebSearch to find current information. "
                "Read the search results carefully and extract the person's name from the results. "
                "For company names like 'Perplexity', try searching 'Perplexity AI CEO' or 'Perplexity company CEO'. "
                "Provide direct, concise answers based on the information you find."
            )
        }
    )
    return agent


def main():
    st.title("🤖 Conversational Knowledge Bot")
    st.caption("Powered by: Groq LLM + DuckDuckGo + Wikipedia + LangChain")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "memory" not in st.session_state:
        st.session_state.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )

    if "agent" not in st.session_state:
        llm = get_llm()
        tools = get_tools()
        st.session_state.agent = create_agent(llm, tools, st.session_state.memory)

    with st.sidebar:
        st.header("💡 Sample Questions")
        st.markdown("""
        - Who is the CEO of OpenAI?
        - Where did he study?
        - Who founded Tesla?
        - Tell me about Python
        """)

        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.session_state.memory = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True
            )
            llm = get_llm()
            tools = get_tools()
            st.session_state.agent = create_agent(llm, tools, st.session_state.memory)
            st.rerun()

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask me anything..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Searching..."):
                try:
                    result = st.session_state.agent.invoke({"input": prompt})
                    raw_answer = result.get("output", "")

                    if not raw_answer:
                        answer = "I'm sorry, I couldn't find an answer to your question. Please try rephrasing it."
                    else:
                        answer = raw_answer

                        if "Final Answer:" in answer:
                            answer = answer.split("Final Answer:")[-1].strip()

                        reasoning_prefixes = ['Question:', 'Thought:', 'Action:', 'Action Input:', 'Observation:']
                        lines = answer.split('\n')

                        content_start_idx = 0
                        for i, line in enumerate(lines):
                            line_stripped = line.strip()
                            if any(line_stripped.startswith(prefix) for prefix in reasoning_prefixes):
                                content_start_idx = i + 1
                            elif line_stripped and not any(line_stripped.startswith(prefix) for prefix in reasoning_prefixes):
                                break

                        if content_start_idx > 0 and content_start_idx < len(lines):
                            answer = '\n'.join(lines[content_start_idx:]).strip()

                        if not answer or len(answer) < 10:
                            answer = raw_answer

                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})

                except Exception as e:
                    error_msg = f"Error: {str(e)}"
                    st.error(error_msg)
                    with st.expander("🔍 Debug Details"):
                        st.code(str(e))
                    st.session_state.messages.append({"role": "assistant", "content": "Sorry, I encountered an error. Please try again."})


if __name__ == "__main__":
    main()
