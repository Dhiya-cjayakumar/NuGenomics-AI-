# NuGenomics AI Assistant 

A smart, modern AI agent for **NuGenomics** powered by the **Google Agent Development Kit (ADK)**. This project intelligently handles both **customer support** queries and **genetic wellness** questions, dynamically routing each to the appropriate logic using ADK-native capabilities.

---

##  Project Overview

This AI assistant is designed to:

-  **Handle Support Queries** — Fetches real answers from NuGenomics’ [FAQ page](https://www.nugenomics.in/faqs/) using Google Search.
-  **Handle Wellness Queries** — Answers using AI's built-in understanding of genetics, DNA, fitness, and health.
-  **Dynamic Routing** — Decides which tool or response method to use based on user query, **without hardcoded if-else logic**.

---

##  Components Breakdown

### 1. **Main Agent Logic (`agentsingle.py`)**

- Uses Google ADK's `Agent` class with clear `instruction` to:
  - Use `google_search` for support questions.
  - Answer health/wellness queries directly.
- Tool: `run(query)` is passed as a Tool to the agent.

---

### 2. **Google Search Integration**

- Integrated using ADK’s `google_search` tool.
- Used to extract FAQ answers by querying NuGenomics’ FAQ page (instead of direct scraping).
- Keeps responses up-to-date and accurate.
- Used the browsers web developer tools to see the underlying HTML structure of the page to find the questions (<h4>) and their answers (adjacent <div>)

---

### 3. **Asynchronous Session Management**

- Uses `InMemorySessionService` for managing sessions.
- ADK’s `Runner` executes the agent’s response flow.
- Sessions and runners are created **asynchronously** to improve performance and flexibility.

---

### 4. **Flask Backend (`app.py`)**

- ✅ Serves a clean HTML frontend via `/`
- ✅ Provides an API at `/api/query` to accept user input and return agent responses
- ✅ Uses `asyncio` to initialize the agent session and runner

---

### 5. **Frontend (`index.html`)**

-  Simple and clean HTML UI
-  Lets users type a question and receive real-time AI responses

---

### 6. **Testing (`tests/test_agent.py`)**

- ✅ Built with `pytest` and `pytest-asyncio`
- ✅ Includes mocks for:
  - Agent session
  - Runner responses
- ✅ Tests:
  - Empty/invalid responses
  - Correct final output parsing
  - Session creation behavior

---

##  How the AI Works

###  Agent Initialization

- API key (`GOOGLE_API_KEY`) loaded from `.env` file
- `Agent` instantiated with:
  - Tool: `run(query)`
  - Model: `gemini-2.0-flash`
  - Clear, role-based instructions for dual-purpose use

### ⚙️ Session + Runner

```python
session_service = InMemorySessionService()
runner = Runner(agent=nugenomics_agent, ...)
Fixed APP_NAME, USER_ID, and SESSION_ID

Session used to manage interaction history

📨 Agent Message Flow
User submits query

Query converted to types.Content

Runner processes the message

Agent either:

Calls run() tool (for support)

Replies from built-in knowledge (for wellness)

### Testing
Run all tests:

bash
Copy
Edit
pytest
Features:

Mocked tools and runners

Tests async event flows

Handles edge cases gracefully

 Tech Stack 
Component	Tech Used
Language	Python 3.10
AI Framework	Google ADK
Backend	Flask
Frontend	HTML + JavaScript
Testing	Pytest + AsyncIO
Session Storage	InMemorySessionService (ADK)

# Project Structure
bash
Copy
Edit
my_adk_nugenomics/
├── app.py                      # Flask backend
├── .env                        # Environment config (DO NOT COMMIT)
├── requirements.txt            # Python dependencies
├── agentapp/
│   ├── agentsingle.py          # Main agent logic
│   └── tests/
│       └── test_agent.py       # Pytest suite
└── templates/
    └── index.html              # Frontend interface
 Setup & Run
1. Install dependencies:
bash
Copy
Edit
pip install -r requirements.txt
2. Create a .env file:
env
Copy
Edit
GOOGLE_API_KEY=your_api_key_here
3. Run the server:
bash
Copy
Edit
python app.py
4. Open in browser:
Visit http://localhost:5000 and ask away!

✅ Key Features
✅ Dual-purpose agent (support + wellness)

✅ Dynamic routing without if-else rules

✅ Real-time agent response handling

✅ Test coverage for reliability

✅ Modular structure (easy to extend)

Author
Dhiya C Jayakumar

License
MIT License
