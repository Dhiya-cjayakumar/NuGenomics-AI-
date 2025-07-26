# @title Import necessary libraries  
import os
import asyncio
from google.adk.agents import LlmAgent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.adk.tools import google_search
from google.genai import types
from dotenv import load_dotenv
import warnings

warnings.filterwarnings("ignore")
print("Libraries imported.")

# @title Configure API Keys
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY is missing from your .env file!")

os.environ["GOOGLE_API_KEY"] = api_key
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "False"

print(f"Google API Key set: {'Yes' if api_key else 'No'}")
print("\nEnvironment configured.")

# @title ✅ Handling
main_agent = LlmAgent(
    name="NuGenomicsMainAgent",
    model="gemini-2.0-flash",
    description="Unified NuGenomics AI assistant that handles both support and wellness queries intelligently",
    instruction="""
    You are the main NuGenomics AI Assistant. You handle two types of queries intelligently:

    📋 **FOR SUPPORT QUERIES** (NuGenomics business questions):
    When users ask about NuGenomics services, any program related queries, pricing, costs, EMI options, blood tests, blood reports
    appointments, scheduling, program details, sample collection, reports, timelines, program duration, support related
    or any business-related questions:
    use google search to:
    1. search the nugenomics faq page - https://www.nugenomics.in/faqs/
    2. the page contains all the faq questions in h4 tags and its answer in the adjacent div tab.
    3. so use your intelligence to compare the user query with all the questions (h4 tags) and return its corresponding answer(adjacent div tab)
    analyze the nugenomics faq page https://www.nugenomics.in/faqs/ and return the correct answer(div tag) by matching the user query with the questions (h4 tags) mentioned in the faq page.
    always remember that the user query will always be refering the the program given in the faq page https://www.nugenomics.in/faqs/ and there is only one program
    
    🧬 **FOR WELLNESS QUERIES** (health and genetics questions):
    When users ask about DNA analysis, genetic insights, health risks, metabolism, 
    fitness, nutrition guidance, disease predisposition, or general wellness questions:
    
    1. Use your built-in knowledge and expertise in genetics and wellness
    2. Provide scientifically accurate information about:
       - DNA and genetic testing insights
       - Health risk assessments based on genetics
       - Personalized nutrition and fitness recommendations
       - Metabolic health and genetic factors
       - Disease predisposition and prevention strategies
    3. Always recommend consulting healthcare professionals for medical concerns
    4. Never provide medical diagnoses
    
    🎯 **INTELLIGENT DECISION MAKING**:
    - Analyze each user query to determine if it's support-related or wellness-related
    - For support queries: Use Google Search to go to the nugenomics faq page https://www.nugenomics.in/faqs/ and find the best matching question(h4 tags) to the user's query and return its answer(adjacent div tag)
    - For wellness queries: Use your expertise without searching
    - Be friendly, professional, and accurate in all responses
    """,
    tools=[google_search]  # Only tool needed - used conditionally based on query type
)

# @title Session and Runner Setup
APP_NAME = "nugenomics_unified_agent"
USER_ID = "user_1" 
SESSION_ID = "session_001"

async def setup_and_run():
    """Main async function with single agent architecture"""
    
    # Create session service
    session_service = InMemorySessionService()
    
    # Create session (with await - required for ADK 1.0.0+)
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )
    print(f"✅ Session created: App='{APP_NAME}', User='{USER_ID}', Session='{SESSION_ID}'")
    
    # Create runner with main agent
    runner = Runner(
        agent=main_agent,
        app_name=APP_NAME,
        session_service=session_service
    )
    
    print(f"✅ Runner created for main agent '{runner.agent.name}'")
    

    
    # Interactive loop
    while True:
        try:
            query = input("\n💬 Ask something (or 'quit' to exit): ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
                
            if not query:
                continue
                
            print(f"\n🤖 Processing: {query}")
            result = await run_agent(runner, query)
            print(f"\n✨ Response: {result}")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

async def run_agent(runner: Runner, query: str) -> str:
    """Run the main agent with proper event handling"""
    content = types.Content(role='user', parts=[types.Part(text=query)])
    
    final_text_response = None
    
    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=SESSION_ID, 
        new_message=content
    ):
        if event.is_final_response() and event.content and event.content.parts:
            for part in event.content.parts:
                # Look specifically for text parts
                if hasattr(part, 'text') and part.text and part.text.strip():
                    final_text_response = part.text.strip()
                    break
            
            if final_text_response:
                break
    
    return final_text_response or "No response generated from the agent."

if __name__ == "__main__":
    print("🚀 Starting NuGenomics Unified AI Agent...")
    print("\n📋 Key Features:")
    print("   ✅ Single main agent architecture (no sub-agents)")
    print("   ✅ Intelligent query classification (support vs wellness)")
    print("   ✅ Conditional Google Search for support queries")
    print("   ✅ Built-in wellness expertise for health questions") 
    print("   ✅ Clean, simple, and maintainable design")
    print("   ✅ No function calling limitations or complex routing")
    
    asyncio.run(setup_and_run())
