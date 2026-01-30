# Conversational Knowledge Bot

A powerful conversational AI bot that remembers context, searches the web, and provides factual answers using **100% FREE services**.

## 🌟 Features

- **💬 Conversational Memory**: Remembers previous conversations and provides contextual responses
- **🔍 Web Search**: Searches DuckDuckGo for current information
- **📚 Wikipedia Integration**: Fetches detailed information from Wikipedia
- **🎨 Dual Interface**: Both Streamlit UI and command-line interface
- **💰 100% Free**: Uses only free services with no credit card required

## 🛠️ Tech Stack

| Component | Service | Cost | Notes |
|-----------|---------|------|-------|
| **LLM** | Groq | FREE | Free tier, no CC, generous limits |
| **Web Search** | DuckDuckGo | FREE | No API key, unlimited |
| **Wikipedia** | Wikipedia API | FREE | Public API, no limits |
| **Framework** | LangChain | FREE | Open source |
| **UI** | Streamlit | FREE | Open source |
| **Python Libs** | All packages | FREE | PyPI open source |

## 🏗️ Architecture

### Memory Design
- **ConversationBufferMemory**: Stores entire conversation history
- **Memory Key**: `chat_history` - accessible to the agent for context
- **Persistent Session**: Memory maintained throughout the conversation

### Tools
1. **Wikipedia Tool**
   - Uses `WikipediaQueryRun` with `WikipediaAPIWrapper`
   - Top 2 results, 1000 chars max per result
   - Best for: Historical facts, biographies, detailed information

2. **DuckDuckGo Search Tool**
   - Uses `DuckDuckGoSearchRun`
   - No API key required
   - Best for: Current events, recent information, general queries

### Agent Flow
```
User Query → Agent (CONVERSATIONAL_REACT) → Decide Tool → Execute Search → Process Result → Generate Response
                ↓
         Memory Context
```

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Step 1: Clone the Repository
```bash
git clone <your-repo-url>
cd soulpage_task
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Set Up API Key

1. Visit [Groq Console](https://console.groq.com/)
2. Sign up for a free account (no credit card required)
3. Generate an API key
4. Create a `.env` file in the project root:

```bash
GROQ_API_KEY=your_groq_api_key_here
```

## 🚀 Usage

### Option 1: Streamlit UI (Recommended)

**Windows:**
```cmd
run_streamlit.bat
```

**Mac/Linux:**
```bash
# Activate venv first
source venv/bin/activate
streamlit run app.py
```

Then open your browser to the displayed URL (usually http://localhost:8501)

### Option 2: Command Line Interface

**Windows:**
```cmd
run_cli.bat
```

**Mac/Linux:**
```bash
# Activate venv first
source venv/bin/activate
python main.py
```

## 💬 Sample Chat Logs

### Example 1: Basic Query with Context
```
👤 You: Who is the CEO of OpenAI?

🤖 Bot: Sam Altman is the CEO of OpenAI.

👤 You: Where did he study?

🤖 Bot: Sam Altman studied computer science at Stanford University. 
       However, he dropped out in 2005 to co-found Loopt.
```

### Example 2: Wikipedia Search
```
👤 You: Tell me about the Eiffel Tower

🤖 Bot: The Eiffel Tower is a wrought-iron lattice tower on the Champ 
       de Mars in Paris, France. It was designed by Gustave Eiffel and 
       completed in 1889. Standing at 330 meters tall, it was the world's 
       tallest structure until 1930.
```

### Example 3: Current Events (Web Search)
```
👤 You: Who is the CEO of Apple?

🤖 Bot: Tim Cook is the CEO of Apple. He has been serving as the CEO 
       since 2011, succeeding Steve Jobs.

👤 You: Who is his mother?

🤖 Bot: I'm not aware of publicly available information about Tim Cook's 
       mother. Tim Cook keeps his personal life private.
```

## 🧪 Testing

Run the bot with these test queries:
1. **Factual Query**: "Who is the CEO of OpenAI?"
2. **Contextual Follow-up**: "Where did he study?"
3. **Wikipedia Query**: "Tell me about Python programming language"
4. **Web Search**: "Who is the CEO of Perplexity?"
5. **Memory Test**: "What did I ask you earlier?"

   <img width="1918" height="953" alt="Screenshot 2026-01-30 140130" src="https://github.com/user-attachments/assets/12eed399-5d38-4479-bf19-e8fca452c4fd" />


## 📁 Project Structure

```
soulpage_task/
├── app.py                 # Streamlit UI application
├── main.py               # Command-line interface
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
├── .gitignore           # Git ignore rules
├── README.md            # This file
├── run_streamlit.bat    # Windows launcher for Streamlit
├── run_cli.bat         # Windows launcher for CLI
├── setup.bat           # Windows setup script
└── setup.sh            # Mac/Linux setup script
```

## 🔧 Configuration

### LLM Settings
- **Model**: `llama-3.1-8b-instant` (Groq's free tier)
- **Temperature**: 0.5 (balanced creativity/accuracy)
- **Max Tokens**: 512 (optimized for responses)

### Memory Settings
- **Type**: ConversationBufferMemory
- **Return Messages**: True
- **Memory Key**: chat_history

### Agent Settings
- **Type**: CONVERSATIONAL_REACT_DESCRIPTION
- **Max Iterations**: 5 (allows thorough searches)
- **Timeout**: 40 seconds
- **Verbose**: False (clean output in Streamlit)

## 🎯 Key Features Explained

### 1. Memory Integration
The bot uses LangChain's `ConversationBufferMemory` to:
- Store all previous messages
- Provide context to the agent
- Enable follow-up questions
- Maintain conversation coherence

### 2. Tool Selection
The agent intelligently selects tools based on:
- Query type (factual vs. current)
- Information availability
- Context requirements

### 3. Error Handling
- Graceful API failures
- Parsing error recovery
- User-friendly error messages
- Debug mode with expandable details

## 🌐 Free Services Used

### Why These Services?

1. **Groq** - Fastest free LLM inference
   - No credit card required
   - Generous rate limits
   - High-quality Llama 3.1 models

2. **DuckDuckGo** - Privacy-focused search
   - No API key needed
   - Unlimited searches
   - No tracking

3. **Wikipedia** - Reliable knowledge base
   - Free public API
   - No rate limits for reasonable use
   - High-quality factual content

4. **LangChain** - Industry-standard framework
   - Excellent documentation
   - Active community
   - Built-in tools and memory

5. **Streamlit** - Modern UI framework
   - Easy to build
   - Beautiful interfaces
   - Real-time updates

## 🐛 Troubleshooting

### Issue: "GROQ_API_KEY not found"
**Solution**: Make sure you've created a `.env` file with your API key

### Issue: "Module not found"
**Solution**: 
1. Create a virtual environment: `python -m venv venv`
2. Activate it: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
3. Install dependencies: `pip install -r requirements.txt`

### Issue: Search tools not working
**Solution**: Check your internet connection; both tools require web access

### Issue: Rate limit errors
**Solution**: The Groq free tier has daily limits. The bot automatically uses `llama-3.1-8b-instant` which has generous limits.

## 🚀 Future Enhancements

- [ ] Add more tools (Calculator, Weather API)
- [ ] Implement conversation export
- [ ] Add voice input/output
- [ ] Support multiple languages
- [ ] Add conversation summarization
- [ ] Integrate more free LLM providers

## 📝 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

Created as part of the Soulpage GenAI Assignment

## 🙏 Acknowledgments

- Groq for free LLM inference
- LangChain for the excellent framework
- DuckDuckGo for free search API
- Wikipedia for open knowledge
- Streamlit for the UI framework

---

**Note**: All services used in this project are free and require no credit card. The Groq API key is free to obtain and use.

