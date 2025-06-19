import os
import json
import requests
from dotenv import load_dotenv

# 📥 Load environment variables
load_dotenv()

MCP_API_KEY = os.getenv("MCP_API_KEY")
MCP_DISCOVERY_URL = os.getenv("MCP_DISCOVERY_URL")
MCP_TOOL_CALL_URL = os.getenv("MCP_TOOL_CALL_URL")
MCP_PROMPT_URL = os.getenv("MCP_PROMPT_URL")

HEADERS = {
    "Content-Type": "application/json",
}
if MCP_API_KEY:
    HEADERS["X-API-KEY"] = MCP_API_KEY

OLLAMA_API_URL = "http://localhost:11434/v1/chat/completions"
MODEL_NAME = "llama3-groq-tool-use:latest"

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

# 🧠 Call Ollama with tools
def call_ollama_with_tools(messages, functions):
    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "functions": functions,
        "tool_choice": "auto"
    }
    response = requests.post(OLLAMA_API_URL, json=payload)
    response.raise_for_status()
    data = response.json()

    print("🧾 Full Ollama response:", json.dumps(data, indent=2))  # Debug

    choice = data["choices"][0]

    # ✅ Handle tool_calls[] (modern format)
    if "tool_calls" in choice and choice["tool_calls"]:
        tool_call = choice["tool_calls"][0]
        return {
            "function_call": {
                "name": tool_call["function"]["name"],
                "arguments": json.dumps(tool_call["function"].get("arguments", {}))
            }
        }

    # Legacy single call support
    if "tool_call" in choice:
        return {
            "function_call": {
                "name": choice["tool_call"]["name"],
                "arguments": json.dumps(choice["tool_call"].get("arguments", {}))
            }
        }

    # No tool call
    return {"content": choice.get("message", {}).get("content", "")}

# 🧠 Call Ollama to format final answer
def call_ollama_formatting(prompt):
    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(OLLAMA_API_URL, json=payload)
    response.raise_for_status()
    data = response.json()
    return data["choices"][0].get("message", {}).get("content", "")

# 🚀 Main function
def main():
    user_message = "Call the weather tool to get the current weather in Istanbul."

    print("🔎 Fetching tool definitions from MCP...------------------")
    openai_tools = fetch_structured_tools()
    print(openai_tools)

    print("🔎 Fetching prompts from MCP...----------------------")
    prompts_map = fetch_prompts_from_mcp()
    system_prompt = prompts_map.get("structured-tool-system-prompt", "You are a helpful assistant.")
    print(system_prompt)

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]

    print("💬 Sending message to Ollama with tools...")
    first_response = call_ollama_with_tools(messages, openai_tools)
    print(f"first_response: {first_response}")

    if first_response.get("function_call"):
        function_call = first_response["function_call"]
        func_name = function_call["name"]
        arguments = json.loads(function_call["arguments"])
        print(f"📞 Ollama wants to call MCP function: {func_name} with args {arguments}")

        tool_response = call_mcp_function(func_name, arguments)

        final_response_prompt = prompts_map.get("final-response-prompt", "").replace("[TOOL_RESPONSE]", json.dumps(tool_response))
        print("💬 Formatting final response with Ollama...")
        final_response = call_ollama_formatting(final_response_prompt)
        print("\n✅ Final answer from Ollama:")
        print(final_response)
    else:
        print("\n✅ Final answer from Ollama:")
        print(first_response.get("content", "No content"))

# Entry point
if __name__ == "__main__":
    main()
