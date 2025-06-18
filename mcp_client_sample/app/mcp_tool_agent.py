import os
import json
import requests
import openai
from dotenv import load_dotenv  # Optional: only needed if you use .env file

# 📥 Load environment variables from a .env file (if using python-dotenv)
load_dotenv()

# 🔐 Load API keys from environment variables (recommended for security)
openai.api_key = os.getenv("OPENAI_API_KEY")
MCP_API_KEY = os.getenv("MCP_API_KEY")  # Optional API key for your MCP server

# 🌐 MCP server endpoints
MCP_DISCOVERY_URL = os.getenv("MCP_DISCOVERY_URL")
MCP_TOOL_CALL_URL = os.getenv("MCP_TOOL_CALL_URL")

# 🧾 Common headers for requests
HEADERS = {
    "Content-Type": "application/json",
}
if MCP_API_KEY:
    HEADERS["X-API-KEY"] = MCP_API_KEY  # Optional header if your server requires authentication

# 📡 Step 1: Fetch available tool functions from MCP server
def fetch_function_definitions_from_mcp():
    try:
        response = requests.get(MCP_DISCOVERY_URL, headers=HEADERS, timeout=5)
        response.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"❌ Error fetching MCP tools: {str(e)}")

    tools = response.json()
    print(f"🔎 Fetched Tools:{tools}")
    openai_functions = []
    for tool in tools:
        tool_name = tool.get("name", "unknown")
        for func in tool.get("functions", []):
            openai_functions.append({
                "name": func.get("name", ""),
                "description": func.get("description", ""),
                "parameters": func.get("parameters", {})
            })

    return openai_functions

# ⚙️ Step 2: Call a specific tool on the MCP server
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

# 🧠 Step 3: Full end-to-end roundtrip: user → tool → result → LLM
def main():
    user_message = "What's the weather like in Istanbul?"

    # 🔍 Discover tools from MCP
    print("🔎 Fetching tool definitions from MCP server...")
    function_definitions = fetch_function_definitions_from_mcp()

    # 🧠 Ask OpenAI model with function definitions
    print("💬 Sending user message to GPT with tool definitions...")
    response = openai.ChatCompletion.create(
        model="gpt-4-0613",  # Supports function calling
        messages=[{"role": "user", "content": user_message}],
        functions=function_definitions,
        function_call="auto",
    )

    message = response["choices"][0]["message"]

    # 🔁 Check if GPT wants to call a tool
    if message.get("function_call"):
        func_name = message["function_call"]["name"]
        func_args = json.loads(message["function_call"]["arguments"])

        print(f"📞 GPT wants to call MCP function: {func_name} with args {func_args}")

        # 🧪 Call the tool via MCP
        func_response = call_mcp_function(func_name, func_args)

        # 🧠 Feed result back into GPT for reasoning
        print("🔁 Sending tool response back to GPT for reasoning...")
        final_response = openai.ChatCompletion.create(
            model="gpt-4-0613",
            messages=[
                {"role": "user", "content": user_message},
                message,
                {
                    "role": "function",
                    "name": func_name,
                    "content": json.dumps(func_response)
                }
            ],
        )

        # ✅ Final answer from GPT
        print("\n✅ Final answer from GPT:")
        print(final_response["choices"][0]["message"]["content"])

    else:
        # 🤖 GPT answered without needing a tool
        print("\n🤖 GPT Response:")
        print(message["content"])

# 🚀 Entry point
if __name__ == "__main__":
    main()
