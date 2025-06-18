import os
import json
import requests
from dotenv import load_dotenv

# 📥 Load environment variables
load_dotenv()

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
OLLAMA_API_GENERATE_URL = os.getenv("OLLAMA_API_GENERATE_URL", "http://localhost:11434/api/generate")
OLLAMA_API_CHAT_URL = os.getenv("OLLAMA_API_CHAT_URL", "http://localhost:11434/api/chat")

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
    # Build a readable tool description block
    tool_info_text = ""
    for tool in tools:
        name = tool.get("name", "unknown")
        description = tool.get("description", "No description provided")
        schema = tool.get("inputSchema", "{}").replace("\r\n", "").replace("\n", "").strip()
        
        tool_info_text += f"- {name}: {description}\n  Input schema: {schema}\n\n"

    print("📦 MCP Tools for system prompt:\n")
    print(tool_info_text)
    
    return tool_info_text

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

# 🧠 Step 3: Ask Ollama chat endpoint
def call_ollama_chat(messages):
    response = requests.post(OLLAMA_API_CHAT_URL, json={
        "model": OLLAMA_MODEL,
        "messages": messages,
        "stream": False
    })
    response.raise_for_status()
    return response.json()["message"]["content"]

# For /api/generate endpoint, it expects "prompt" (string), not messages list
def call_ollama_generate(prompt):
    response = requests.post(OLLAMA_API_GENERATE_URL, json={
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    })
    response.raise_for_status()
    data = response.json()  # parse JSON response
    return data.get("response", "")  # return the actual text response

# 🚀 Main agent flow
def main():
    user_message = "What's the weather like in Istanbul?"
    print("🔎 Fetching tool definitions from MCP server...")
    tool_info_text = fetch_function_definitions_from_mcp()

    system_prompt = f"""
You are a helpful and intelligent AI assistant.

You have access to external tools via the Model Context Protocol (MCP). 
To call a tool, respond with a **single line** in the following format:
CALL <function_name> <JSON_arguments>

Use this format exactly. Do **not** include extra text, explanation, or multiple calls.

You may choose from the following available tools:

{tool_info_text}

Guidelines:
- If you can answer the user's query directly using your own knowledge, do so.
- If a tool is needed to fulfill the user's request, respond **only** with the CALL line.
- Ensure the JSON arguments match the input schema for the tool.
- If the tool requires no arguments, pass an empty object: `{{}}`.

Example:
CALL getWeather {{ "cityName": "Istanbul" }}

Stay concise and accurate in tool selection and response formatting.
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]

    print("💬 Sending message to Ollama chat endpoint...")
    reply = call_ollama_chat(messages)
    print(f"🤖 Ollama Response:\n{reply}")

    if reply.strip().startswith("CALL"):
        try:
            _, func_name, json_str = reply.strip().split(" ", 2)
            args = json.loads(json_str)
            print(f"📞 Ollama wants to call MCP function: {func_name} with args {args}")

            tool_response = call_mcp_function(func_name, args)

            system_prompt_tool_response = """
You are a helpful and intelligent AI assistant that receives raw JSON data from external tools via MCP (Model Context Protocol).

Each tool call returns a ToolResponse object in the following format:
{
  "tool": "<function_name>",
  "result": "<JSON string from external API or service>",
  "httpCode": <status_code>
}

Your job is to:
- Parse the `result` field, which is a raw JSON string.
- Understand and extract the key information from it.
- Present the result to the end user in **clear, human-friendly language**.
- Adapt the tone and formatting based on context: the user may be a client, a customer, or a general app user.
- DO NOT repeat the JSON or say "Here is the result." Just present it like you naturally would in conversation or in a report.

Examples:
- If the result is about weather: summarize the temperature, condition, and location naturally.
- If it’s an author profile: share the name, expertise, and notable articles or ratings.
- If no data is found, respond kindly: “Sorry, I couldn’t find any matching results.”

Always aim for clarity, brevity, and friendliness.
"""

            # Prepare message with tool_response as JSON string inside user content
            messages = [
                {"role": "system", "content": system_prompt_tool_response},
                {"role": "user", "content": json.dumps(tool_response)}  # serialize dict to string
            ]

            print("💬 Sending tool response back to Ollama for final user-friendly answer...")
            final_response = call_ollama_generate("\n".join([m["content"] for m in messages]))
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
