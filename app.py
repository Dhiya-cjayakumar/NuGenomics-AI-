from flask import Flask, request, jsonify, send_from_directory
import asyncio
import os
from flask import render_template
from agentapp.agentsingle import setup_and_run, run_agent, main_agent  # your ADK async agent code
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from typing import Optional

runner: Optional[Runner] = None

app = Flask(__name__)

APP_NAME = "nugenomics_unified_agent"
USER_ID = "user_1"
SESSION_ID = "session_001"

# Create session and runner once, on startup
session_service = InMemorySessionService()
runner = None

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

async def init_runner():
    global runner
    await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
    runner = Runner(agent=main_agent, app_name=APP_NAME, session_service=session_service)

loop.run_until_complete(init_runner())


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/query', methods=['POST'])
def query():
    data = request.get_json()
    user_query = data.get('query', '')
    if not user_query:
        return jsonify({'response': 'Please provide a query.'}), 400
    
    async def process_query():
        if runner is None:
            raise RuntimeError("Runner not ready")
        return await run_agent(runner, user_query)
        
        

    response = loop.run_until_complete(process_query())
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
