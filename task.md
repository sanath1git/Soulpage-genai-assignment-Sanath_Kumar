Task 2: Conversational Knowledge Bot (LangChain +
Tools + Memory)
Problem Statement:
Build a Conversational Knowledge Bot that can:
● Remember previous conversations
● Search external data (Wikipedia or any free API)
● Give contextual and factual answers
Objective:
Assess how well you can integrate tools, memory, and conversational flow in LangChain.
Steps:
1. Use LangChain’s ConversationChain or AgentExecutor with a memory component
(e.g., ConversationBufferMemory).
2. Add a tool for web search (e.g., SerpAPI, DuckDuckGo API, or a static JSON
knowledge base).
3. Ensure the bot can:
○ Answer factual queries (e.g., “Who is the CEO of OpenAI?”)
○ Continue the conversation with context (e.g., “Where did he study?”).
4. Deploy it locally as a Streamlit chat UI or command-line chat loop.
Deliverables:
● GitHub repository with:
○ Code + requirements.txt
○ README describing tools, memory design, and sample chat logs
● Optional: Short screencast showing live interaction

Common Submission Instructions for All Tasks
● Create a GitHub repository named:
Soulpage-genai-assignment-yourname
● Include:
○ README.md (with setup, architecture, and example usage)
○ requirements.txt (libraries with versions)
○ main.py or notebook file
○ Optional: demo screenshots or video link
● Push the code to your public GitHub and share the repository link.
● Bonus points for clean, modular code and good documentation.