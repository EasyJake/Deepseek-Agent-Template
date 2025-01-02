# Please install OpenAI SDK first: `pip3 install openai`

from openai import OpenAI
from dotenv import load_dotenv
import os
from Tools import Tool1, Tool2, Tool3

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables
api_key = os.getenv('DEEPSEEK_API_KEY')

client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

def parse_tool_response(response_text):
    """Parse the AI response to extract multiple tool calls"""
    tools = []
    current_tool = {}
    
    for line in response_text.strip().split('\n'):
        if line.startswith('TOOL:'):
            if current_tool:
                tools.append(current_tool)
            current_tool = {'tool': line.replace('TOOL:', '').strip()}
        elif line.startswith('ARGS:'):
            current_tool['args'] = eval(line.replace('ARGS:', '').strip())
        elif line.startswith('REASON:'):
            current_tool['reason'] = line.replace('REASON:', '').strip()
    
    if current_tool:
        tools.append(current_tool)
    
    return tools

def execute_tool(tool_name, args):
    """Execute the specified tool with given arguments"""
    print(f"\n[Tool Execution]")
    print(f"Tool Name: {tool_name}")
    print(f"Arguments: {args}")
    
    tool_mapping = {
        'analyze_crypto_price': Tool1.analyze_crypto_price,
        'generate_trading_strategy': Tool2.generate_trading_strategy,
        'calculate_portfolio_metrics': Tool3.calculate_portfolio_metrics
    }
    
    try:
        if tool_name in tool_mapping:
            if isinstance(args, dict):
                result = tool_mapping[tool_name](**args)
                print(f"Execution Result: {result}")
                return result
            elif isinstance(args, (list, tuple)):
                result = tool_mapping[tool_name](*args)
                print(f"Execution Result: {result}")
                return result
            else:
                result = tool_mapping[tool_name](args)
                print(f"Execution Result: {result}")
                return result
        else:
            return {"status": "error", "message": f"Tool {tool_name} not found"}
    except Exception as e:
        error_result = {
            "status": "error",
            "message": f"Error executing {tool_name}: {str(e)}",
            "args_received": str(args)
        }
        print(f"Execution Error: {error_result}")
        return error_result

def run_agent(user_input):
    """Main function to run the agent"""
    print("\n[User Input]")
    print(f"Query: {user_input}")
    
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": """You are a crypto trading assistant. Analyze what tools would be most appropriate to use from the available tools.
                Current tools:
                - analyze_crypto_price: Analyzes current price and trends for a cryptocurrency
                - generate_trading_strategy: Generates trading strategy based on risk level and budget
                - calculate_portfolio_metrics: Calculates portfolio metrics for a wallet address
                
                You can recommend multiple tools if needed. For each tool, respond in this format:
                TOOL: [tool_name]
                ARGS: [arguments as Python literal]
                REASON: [brief explanation]
                
                Repeat this format for each tool needed."""},
            {"role": "user", "content": user_input},
        ],
        stream=False
    )

    print("\n[AI Response]")
    print(response.choices[0].message.content)
    
    tool_calls = parse_tool_response(response.choices[0].message.content)
    print("\n[Parsed Tool Calls]")
    print(f"Number of tools to execute: {len(tool_calls)}")
    for i, tool_call in enumerate(tool_calls, 1):
        print(f"\nTool Call {i}:")
        print(f"Tool: {tool_call['tool']}")
        print(f"Arguments: {tool_call['args']}")
        print(f"Reason: {tool_call['reason']}")
    
    results = []
    for tool_call in tool_calls:
        result = execute_tool(tool_call['tool'], tool_call['args'])
        results.append({
            'tool': tool_call['tool'],
            'reason': tool_call['reason'],
            'result': result
        })
    
    return results

def main():
    print("\nWelcome to the Crypto Trading Assistant!")
    print("Available tools:")
    print("- analyze_crypto_price: Analyzes current price and trends for a cryptocurrency")
    print("- generate_trading_strategy: Generates trading strategy based on risk level and budget")
    print("- calculate_portfolio_metrics: Calculates portfolio metrics for a wallet address")
    
    while True:
        print("\n" + "="*50)
        user_query = input("\nEnter your query (or 'exit' to quit): ")
        
        if user_query.lower() in ['exit', 'quit', 'q']:
            print("\nThank you for using the Crypto Trading Assistant. Goodbye!")
            break
            
        results = run_agent(user_query)
        
        print("\n[Final Results]")
        for result in results:
            print(f"\nTool: {result['tool']}")
            print(f"Reason: {result['reason']}")
            print(f"Result: {result['result']}")
        
        continue_choice = input("\nWould you like to make another query? (y/n): ")
        if continue_choice.lower() not in ['y', 'yes']:
            print("\nThank you for using the Crypto Trading Assistant. Goodbye!")
            break

if __name__ == "__main__":
    main()