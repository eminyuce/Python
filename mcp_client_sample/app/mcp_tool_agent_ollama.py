import os
import json
import requests
from dotenv import load_dotenv

# 📥 Load environment variables
load_dotenv()

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434/api/generate")

MCP_API_KEY = os.getenv("MCP_API_KEY")
MCP_DISCOVERY_URL = os.getenv("MCP_DISCOVERY_URL")
MCP_TOOL_CALL_URL = os.getenv("MCP_TOOL_CALL_URL")

HEADERS = {
    "Content-Type": "application/json",
}
if MCP_API_KEY:
    HEADERS["X-API-KEY"] = MCP_API_KEY

# 📡 Step 1: Fetch available tool functions
def fetch_function_definitions_from_mcp():
    try:
        response = requests.get(MCP_DISCOVERY_URL, headers=HEADERS, timeout=5)
        response.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"❌ Error fetching MCP tools: {str(e)}")

    tools = response.json()
    print(f"🔎 Fetched Tools:{tools}")
    descriptions = []
    for tool in tools:
        tool_name = tool.get("name")
        for func in tool.get("functions", []):
            desc = f"- Function: {func.get('name')}, Description: {func.get('description')}, Parameters: {json.dumps(func.get('parameters'))}"
            descriptions.append(desc)
    return "\n".join(descriptions)

# ⚙️ Step 2: Call MCP Function
def call_mcp_function(function_name, arguments):
    try:
        payload = {
            "tool": function_name,
            "parameters": arguments
        }
        response = requests.post(MCP_TOOL_CALL_URL, headers=HEADERS, json=payload, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": f"❌ MCP Error: {str(e)}"}

# 🧠 Step 3: Ask Ollama (simulating tool calling with prompt engineering)
def call_ollama_chat(messages):
    response = requests.post(OLLAMA_API_URL, json={
        "model": OLLAMA_MODEL,
        "messages": messages,
        "stream": False
    })
    response.raise_for_status()
    returnJson = response.json();
    return returnJson["message"]["content"]

# 🚀 Main agent flow
def main():
    user_message = "What's the weather like in Istanbul?"
    print("🔎 Fetching tool definitions from MCP server...")
    tool_info_text = fetch_function_definitions_from_mcp()

    system_prompt = f"""
You are a helpful AI assistant. You can call external tools via MCP by replying in the following format:
CALL <function_name> <JSON arguments>

Available functions:
{tool_info_text}

If you can answer directly, do so. If a tool is needed, output only one line starting with CALL.
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]

    print("💬 Sending message to Ollama...")
    reply = call_ollama_chat(messages)
    print(f"🤖 Ollama Response:\n{reply}")

    if reply.strip().startswith("CALL"):
        try:
            _, func_name, json_str = reply.strip().split(" ", 2)
            args = json.loads(json_str)
            print(f"📞 Ollama wants to call MCP function: {func_name} with args {args}")

            tool_response = call_mcp_function(func_name, args)

            # Return the tool result back to Ollama for final response
            messages.append({"role": "assistant", "content": reply})
            messages.append({
                "role": "function",
                "name": func_name,
                "content": json.dumps(tool_response)
            })

            final_response = call_ollama_chat(messages)
            print("\n✅ Final answer from Ollama:")
            print(final_response)

        except Exception as e:
            print(f"❌ Failed to parse or execute tool call: {e}")
    else:
        print("\n✅ Final answer from Ollama:")
        print(reply)

# Entry point
if __name__ == "__main__":
    main()
