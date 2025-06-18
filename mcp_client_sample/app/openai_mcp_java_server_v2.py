import os
import openai
import requests
import json

# 🧠 Load your OpenAI key and MCP config
openai.api_key = os.getenv("OPENAI_API_KEY")

MCP_DISCOVERY_URL = "http://localhost:8080/mcp/tools"
MCP_BASE_FUNCTION_URL = "http://localhost:8080/mcp/tools"
MCP_TOOL_CALL_URL = "http://localhost:8080/mcp/call"
MCP_API_KEY = "my-secret-api-key"  # Optional

HEADERS = {
    "Content-Type": "application/json",
}
if MCP_API_KEY:
    HEADERS["X-API-KEY"] = MCP_API_KEY

# 🌐 1. Discover available MCP tools and functions
def fetch_function_definitions_from_mcp():
    response = requests.get(MCP_DISCOVERY_URL, headers=HEADERS)
    if not response.ok:
        raise Exception(f"Failed to fetch MCP tools: {response.status_code} - {response.text}")

    tools = response.json()

    # Transform MCP tool format → OpenAI function format
    openai_functions = []

    for tool in tools:
        tool_name = tool["name"]
        for func in tool.get("functions", []):
            func_name = func["name"]
            func_schema = {
                "name": func_name,
                "description": func.get("description", ""),
                "parameters": func.get("parameters", {})
            }
            openai_functions.append(func_schema)

    return openai_functions

# 🚀 2. Call MCP tool function dynamically
def call_mcp_function(function_name, arguments):
   
    response = requests.post(MCP_TOOL_CALL_URL, headers=HEADERS, json={"tool":function_name,"parameters:":arguments})
    if not response.ok:
        return {"error": f"MCP Error: {response.status_code} - {response.text}"}

    return response.json()

# 🤖 3. Full roundtrip: user message → function → result → LLM
def main():
    user_message = "What's the weather like in Istanbul?"

    # 🔍 Discover tools from MCP
    function_definitions = fetch_function_definitions_from_mcp()

    # 🧠 Step 1: Ask OpenAI with discovered tools
    response = openai.ChatCompletion.create(
        model="gpt-4-0613",
        messages=[{"role": "user", "content": user_message}],
        functions=function_definitions,
        function_call="auto",
    )

    message = response["choices"][0]["message"]

    # ⚙️ Step 2: Call the MCP tool if required
    if message.get("function_call"):
        func_name = message["function_call"]["name"]
        func_args = json.loads(message["function_call"]["arguments"])

        func_response = call_mcp_function(func_name, func_args)

        # 🧠 Step 3: Feed result back to GPT for final reasoning
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

        print("✅ Final answer from GPT:")
        print(final_response["choices"][0]["message"]["content"])
    else:
        print("🤖 GPT Response:")
        print(message["content"])

if __name__ == "__main__":
    main()
