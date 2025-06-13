import asyncio
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from mcp_use import MCPAgent, MCPClient

async def simple_mcp_test():
    load_dotenv()
    
    # Check API key
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("❌ GROQ_API_KEY not found!")
        return
    
    os.environ["GROQ_API_KEY"] = api_key
    print(f"✅ API Key loaded: {api_key[:15]}...")

    # Use only Playwright (most reliable MCP server)
    config = {
        "mcpServers": {
            "playwright": {
                "command": "npx",
                "args": ["-y", "@playwright/mcp@latest"],
                "env": {"DISPLAY": ":0"}
            }
        }
    }
    
    # Save config temporarily
    import json
    with open("temp_mcp.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print("🔧 Testing MCP with Playwright only...")
    
    try:
        # Initialize components
        client = MCPClient.from_config_file("temp_mcp.json")
        print("✅ MCP Client created")
        
        llm = ChatGroq(model="qwen-qwq-32b", temperature=0.1)
        print("✅ LLM created")
        
        agent = MCPAgent(
            llm=llm,
            client=client,
            max_steps=5,
            memory_enabled=False  # Disable memory to simplify
        )
        print("✅ MCP Agent created")
        
        # Test queries
        print("\n🧪 Testing MCP Tool Usage:")
        print("=" * 50)
        
        test_cases = [
            ("Math test (no tools needed)", "What is 5 + 3?"),
            ("Web browsing test (should use MCP)", "Browse the website https://httpbin.org/json and tell me what you see"),
        ]
        
        for test_name, query in test_cases:
            print(f"\n📝 {test_name}")
            print(f"Query: {query}")
            print("🔄 Processing...")
            
            try:
                start_time = asyncio.get_event_loop().time()
                response = await asyncio.wait_for(agent.run(query), timeout=30)
                end_time = asyncio.get_event_loop().time()
                
                print(f"⏱️  Response time: {end_time - start_time:.2f}s")
                print(f"📤 Response: {response}")
                
                # Analyze response for MCP usage indicators
                if any(word in response.lower() for word in ['browsed', 'website', 'page', 'html', 'content', 'json']):
                    print("🔧 ✅ LIKELY used MCP tools!")
                else:
                    print("💭 ❌ Likely direct LLM response")
                    
            except asyncio.TimeoutError:
                print("⏰ Timeout - MCP tools might be slow/broken")
            except Exception as e:
                print(f"❌ Error: {e}")
                if "tool" in str(e).lower():
                    print("🔧 Tool-related error - MCP is being called but failing")
                
            print("-" * 50)
        
        # Interactive mode if tests pass
        print("\n🎯 Interactive mode (type 'exit' to quit):")
        while True:
            user_input = input("\n🧑 You: ").strip()
            if user_input.lower() in ['exit', 'quit']:
                break
                
            try:
                response = await agent.run(user_input)
                print(f"🤖 Assistant: {response}")
            except Exception as e:
                print(f"❌ Error: {e}")
                
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        print("\n💡 Common issues:")
        print("  - Node.js not installed: npm --version")
        print("  - Playwright not available: npx @playwright/mcp@latest")
        print("  - Network/firewall blocking MCP servers")
    finally:
        try:
            if 'client' in locals():
                await client.close_all_sessions()
            # Clean up temp file
            if os.path.exists("temp_mcp.json"):
                os.remove("temp_mcp.json")
        except:
            pass

if __name__ == "__main__":
    print("🚀 Simple MCP Test")
    print("This will test if MCP tools are actually working")
    print("=" * 60)
    asyncio.run(simple_mcp_test())