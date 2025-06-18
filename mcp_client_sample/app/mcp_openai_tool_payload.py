import os
import json
import requests
from dotenv import load_dotenv
import openai

# 📥 Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4-0613")  # or gpt-3.5-turbo-0613

MCP_API_KEY = os.getenv("MCP_API_KEY")
MCP_DISCOVERY_URL = os.getenv("MCP_DISCOVERY_URL")
MCP_TOOL_CALL_URL = os.getenv("MCP_TOOL_CALL_URL")
MCP_PROMPT_URL = os.getenv("MCP_PROMPT_URL")

HEADERS = {
    "Content-Type": "application/json",
}
if MCP_API_KEY:
    HEADERS["X-API-KEY"] = MCP_API_KEY

openai.api_key = OPENAI_API_KEY

# 📡 Fetch prompts from MCP
def fetch_prompts_from_mcp():
    try:
        response = requests.get(MCP_PROMPT_URL, headers=HEADERS, timeout=5)
        response.raise_for_status()
        prompts = response.json()
        return {p["name"]: p["content"] for p in prompts if "name" in p and "content" in p}
    except requests.RequestException as e:
        raise RuntimeError(f"❌ Error fetching MCP prompts: {str(e)}")

# 📡 Fetch structured tools in OpenAI-compatible format
def fetch_structured_tools():
    try:
        url = f"{MCP_DISCOVERY_URL}?format=openai"
        response = requests.get(url, headers=HEADERS, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise RuntimeError(f"❌ Error fetching MCP tools: {e}")

# ⚙️ Call MCP tool
def call_mcp_function(function_name, arguments):
    try:
        payload = {"tool": function_name, "parameters": arguments}
        response = requests.post(MCP_TOOL_CALL_URL, headers=HEADERS, json=payload, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": f"❌ MCP Error: {str(e)}"}

# 🧠 Call OpenAI with tools
def call_openai_with_tools(messages, functions):
    response = openai.ChatCompletion.create(
        model=OPENAI_MODEL,
        messages=messages,
        functions=functions,
        function_call="auto"
    )
    return response["choices"][0]["message"]

# 🧠 Call OpenAI to format final answer
def call_openai_formatting(prompt):
    response = openai.ChatCompletion.create(
        model=OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]



# 🚀 Main function
def main():
    user_message = "What's the weather like in Istanbul?"
    print("🔎 Fetching tool definitions from MCP...")
    openai_tools = fetch_structured_tools()

    print("🔎 Fetching prompts from MCP...")
    prompts_map = fetch_prompts_from_mcp()
    system_prompt = prompts_map.get("structured-tool-system-prompt", "You are a helpful assistant.")

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]

    print("💬 Sending message to OpenAI with tools...")
    first_response = call_openai_with_tools(messages, openai_tools)

    if first_response.get("function_call"):
        function_call = first_response["function_call"]
        func_name = function_call["name"]
        arguments = json.loads(function_call["arguments"])
        print(f"📞 OpenAI wants to call MCP function: {func_name} with args {arguments}")

        tool_response = call_mcp_function(func_name, arguments)

        final_response_prompt = prompts_map.get("final-response-prompt", "").replace("[TOOL_RESPONSE]", json.dumps(tool_response))
        print("💬 Formatting final response with OpenAI...")
        final_response = call_openai_formatting(final_response_prompt)
        print("\n✅ Final answer from OpenAI:")
        print(final_response)
    else:
        print("\n✅ Final answer from OpenAI:")
        print(first_response.get("content", "No content"))

# Entry point
if __name__ == "__main__":
    main()
