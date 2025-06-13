import asyncio
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

async def simple_chat_test():
    load_dotenv()
    
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        print("❌ GROQ_API_KEY not found")
        return
    
    print("🧪 Testing basic LLM functionality...")
    
    try:
        llm = ChatGroq(
            model="qwen-qwq-32b",
            api_key=groq_api_key,
            temperature=0.7
        )
        
        # Test basic functionality
        response = llm.invoke("Hello, can you tell me about Python?")
        print(f"✅ LLM Response: {response.content}")
        
        # Interactive chat
        print("\n🎯 Basic chat mode (type 'exit' to quit):")
        while True:
            user_input = input("\nYou: ").strip()
            if user_input.lower() in ['exit', 'quit']:
                break
            
            try:
                response = llm.invoke(user_input)
                print(f"Assistant: {response.content}")
            except Exception as e:
                print(f"❌ Error: {e}")
                
    except Exception as e:
        print(f"❌ Setup error: {e}")

if __name__ == "__main__":
    asyncio.run(simple_chat_test())