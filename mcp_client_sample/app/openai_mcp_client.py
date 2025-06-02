import os
import openai
import requests

openai.api_key = os.getenv("OPENAI_API_KEY")

# Define function specifications for OpenAI
function_definitions = [
    {
        "name": "get_weather",
        "description": "Get the weather for a location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "City name"},
            },
            "required": ["location"],
        },
    },
    {
        "name": "lookup_user",
        "description": "Retrieve user info by userId",
        "parameters": {
            "type": "object",
            "properties": {
                "userId": {"type": "string", "description": "User ID"},
            },
            "required": ["userId"],
        },
    },
]

def call_mcp_server(function_name, arguments):
    """Call the Spring Boot MCP server endpoints."""
    if function_name == "get_weather":
        location = arguments.get("location")
        response = requests.get(f"http://localhost:8080/mcp/getWeather", params={"location": location})
    elif function_name == "lookup_user":
        user_id = arguments.get("userId")
        response = requests.get(f"http://localhost:8080/mcp/lookupUser", params={"userId": user_id})
    else:
        return {"error": f"Unknown function: {function_name}"}
    
    return response.json()

def main():
    user_message = "What's the weather like in New York?"
    
    # Step 1: Ask GPT
    response = openai.ChatCompletion.create(
        model="gpt-4-0613",
        messages=[{"role": "user", "content": user_message}],
        functions=function_definitions,
        function_call="auto",
    )
    
    message = response["choices"][0]["message"]
    
    # Step 2: Check if GPT wants to call a function
    if message.get("function_call"):
        func_name = message["function_call"]["name"]
        import json
        func_args = json.loads(message["function_call"]["arguments"])
        
        # Call MCP server
        func_response = call_mcp_server(func_name, func_args)
        
        # Step 3: Send function result back to GPT to get final answer
        final_response = openai.ChatCompletion.create(
            model="gpt-4-0613",
            messages=[
                {"role": "user", "content": user_message},
                message,
                {
                    "role": "function",
                    "name": func_name,
                    "content": str(func_response)
                }
            ],
        )
        
        print("Final answer from GPT:")
        print(final_response["choices"][0]["message"]["content"])
    else:
        print("GPT response:")
        print(message["content"])

if __name__ == "__main__":
    main()
