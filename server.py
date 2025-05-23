import os
from fastmcp import FastMCP, Context
from typing import List
import httpx
import json
import asyncio
from utils import get_code_path, get_code, get_all_code_paths, execute_code

WORKSPACE_DIR = os.getcwd()
CODE_STORAGE = os.path.join(WORKSPACE_DIR, "example_codes")
print("Default workspace directory:", WORKSPACE_DIR)

mcp = FastMCP("🛠️🤖 Your Coding Master 🤖🛠️")

@mcp.tool()
async def fetch_and_save_tool_info(ctx: Context, url: str = "https://gofastmcp.com/servers/tools", output_file: str = "tool_info.json"):
    """
    Fetch all information from the given URL and save it to a file.

    Args:
        url (str): The URL to fetch the data from.
        output_file (str): The name of the file to save the data to.
    """
    output_file = os.path.join(CODE_STORAGE, output_file)
    try:
        # Fetch data from the URL
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()  # Raise an error for HTTP issues
        
        # Parse the response content (assuming it's JSON)
        data = response.json()
        
        # Save the data to a file
        with open(output_file, "w") as file:
            json.dump(data, file, indent=4)
        
        print(f"Tool information successfully saved to '{output_file}'.")
    except httpx.RequestError as e:
        print(f"Error fetching data from {url}: {e}")
    except json.JSONDecodeError:
        print("Error decoding the response as JSON.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        

#resource about the code writer of the Coding Master MCP server
@mcp.resource(uri = "config://codewriter", name= "Code Writer Info", description= "Information about the code writer.")
def get_code_writer_profile(ctx: Context) -> dict:
    # Fetch the code writer profile
    profile = {
        "name": "Chaeeun Ryu",
        "linkedin": "https://www.linkedin.com/in/chaeeun-ryu-a39a82234/",
        "version": mcp.settings.version,
        "accessed at": ctx.request_id
    }
    return profile


@mcp.tool()
def write_me_a_mcp_tool(concept: str, ctx: Context) -> str:
    """
    Write an MCP tool based on the concept provided.
    """
    tool_info_path = os.path.join(CODE_STORAGE, "tool_info.json")
    
    if not os.path.exists(tool_info_path):
        # Fetch the data from the URL and save it to a file for the tools document
        asyncio.run(fetch_and_save_tool_info(ctx))
    
    # Read the tool info file
    with open(tool_info_path, "r") as file:
        tool_info = json.load(file)
    
    # Generate the tool based on the concept
    return f"Tool generated for concept: {concept}. Tool info: {tool_info}"

        
@mcp.tool()
def list_codes(directory: str = CODE_STORAGE) -> List[str]:
    """
    List all code files in the specified directory.
    
    Args:
        directory: The directory to search for code files.
    
    Returns:
        A list of code file names (without paths).
    """
    # Get all code file paths
    code_files = get_all_code_paths(directory)
    
    # Extract only the file names from the full paths
    code_names = [os.path.basename(file) for file in code_files]
    
    return code_names

@mcp.tool()
def run_code(code_name: str) -> dict:
    """
    Execute a code file (e.g., Python script, C# project) and return its output.
    For C#, provide the project name (e.g., "EmployeeDirectory" which should resolve to "EmployeeDirectory.csproj").
    
    Args:
        code_name: The name of the code/project (without extension).
    
    Returns:
        A dictionary containing the code content, output, and file name.
    """
    try:
        # get_code_path is now updated to prefer .csproj for C#
        code_path = get_code_path(CODE_STORAGE, code_name)
    except FileNotFoundError as e:
        print(f"Error in run_code (get_code_path): {e}")
        # Ensure a consistent dictionary structure for errors
        return {
            "code": f"File for '{code_name}' not found.", 
            "output": str(e), 
            "code_file_name": f"{code_name} (not found)", 
            "return_code": -1
        }

    # The 'code' field in the result from execute_code will be the content of the file
    # found by get_code_path (e.g., the .csproj XML, or the .py source).
    # If you want to display the associated .cs source code instead when a .csproj is run,
    # you would need to add logic here or in execute_code to find and read it.
    # For now, the 'code' field will be the content of the executed project/script file.
    try:
        result = execute_code(code_path)
        # Optionally, if a .csproj was executed, try to load the corresponding .cs file for display
        if result.get("code_file_name", "").endswith(".csproj"):
            base_cs_name = os.path.splitext(result["code_file_name"])[0] + ".cs"
            path_to_cs_display = os.path.join(os.path.dirname(code_path), base_cs_name)
            if os.path.exists(path_to_cs_display):
                try:
                    with open(path_to_cs_display, "r") as f_cs:
                        result["code_to_display_name"] = base_cs_name
                        result["code_to_display_content"] = f_cs.read()
                        result["code_display_message"] = (f"Executed project '{result['code_file_name']}'. "
                                                          f"Displaying content of associated '{base_cs_name}'.")
                except Exception as e_read_cs:
                    result["code_display_message"] = f"Could not read associated .cs file '{base_cs_name}': {e_read_cs}"
            else:
                result["code_display_message"] = (f"Executed project '{result['code_file_name']}'. "
                                                  f"Associated .cs file '{base_cs_name}' not found for display.")

        return result
    except Exception as e: # Catch any other unexpected errors from execute_code if it didn't return a dict
        print(f"Critical error during execute_code call for '{code_path}': {e}")
        return {
            "code": f"Failed to process {code_path}", 
            "output": f"Execution failed critically: {str(e)}", 
            "code_file_name": os.path.basename(code_path), 
            "return_code": -1
        }





if __name__ == "__main__":
    mcp.run() 