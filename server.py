import os
import glob
from fastmcp import FastMCP, Context
from pathlib import Path
from typing import List
import subprocess
import platform 
import requests
import json

WORKSPACE_DIR = os.getcwd()
CODE_STORAGE = os.path.join(WORKSPACE_DIR, "example_codes")
print("Default workspace directory:", WORKSPACE_DIR)

mcp = FastMCP("🛠️🤖 Your Coding Master 🤖🛠️")

def get_code_path(code_name: str) -> str:
    """
    Get the path to the code file based on the code name.
    Tries to find .csproj for C# targets, then uses glob.
    
    Args:
        code_name: The name of the code file (without extension).
    
    Returns:
        The full path to the code file.
    """
    # Attempt to find a .csproj file first for the given code_name
    # This makes it the preferred target if both .cs and .csproj exist for a C# program
    csproj_path = os.path.join(CODE_STORAGE, f"{code_name}.csproj")
    if os.path.exists(csproj_path):
        print(f"Prioritizing .csproj file for '{code_name}': {csproj_path}")
        return csproj_path

    # Original glob search as a fallback or for other file types
    search_pattern = os.path.join(CODE_STORAGE, f"{code_name}.*")
    matching_files = glob.glob(search_pattern)
    
    if matching_files:
        # You could add more sophisticated sorting here if needed,
        # e.g., to prefer .py over other less common executables if found by glob.
        # For now, taking the first match after the .csproj check.
        print(f"Found matches with glob: {matching_files}, choosing: {matching_files[0]}")
        return matching_files[0]
    else:
        raise FileNotFoundError(f"No file found with name '{code_name}' or associated project file in {CODE_STORAGE}")


def get_code(code_path: str)-> str:
    """
    Read the content of a code file.
    
    Args:
        code_path: The path to the code file.
    
    Returns:
        The content of the code file as a string.
    """
    with open(code_path, "r") as f:
        return f.read()

def get_all_code_paths(storage_dir: str = CODE_STORAGE) -> List[str]:
    """
    Get the paths to all code files in the specified storage directory.
    
    Args:
        storage_dir: The directory where code files are stored.
    
    Returns:
        A list of full paths to all code files in the directory.
    """
    # List all files in the directory
    code_files = [
        os.path.join(storage_dir, file)
        for file in os.listdir(storage_dir)
        if os.path.isfile(os.path.join(storage_dir, file))
    ]
    
    return code_files


def execute_code(code_path: str):
    """
    Execute the code and returns the dictionary containing output of the code, 
    content of the code file (e.g., .py, .csproj), file name, and return code.

    Args:
        code_path (str): Full path to the code file to execute (e.g., .py, .csproj).

    Returns:
        dictionary: {"code": content_of_code_path_file, "output": execution_output, "code_file_name": original_base_name, "return_code": int}
    """
    if not os.path.exists(code_path):
        raise FileNotFoundError(f"The file '{code_path}' does not exist.")
    
    # Read the content of the file being processed (e.g., the .py script, or the .csproj XML)
    try:
        with open(code_path, "r") as file:
            code_content = file.read()
    except Exception as e:
        # If we can't even read the file that code_path points to.
        return {
            "code": f"Error reading file: {os.path.basename(code_path)} - {e}", 
            "output": f"Cannot execute, failed to read file: {os.path.basename(code_path)}", 
            "code_file_name": os.path.basename(code_path), 
            "return_code": -1
        }
            
    code_file_name = os.path.basename(code_path) # e.g., "EmployeeDirectory.csproj"
    _, file_extension = os.path.splitext(code_path)
    
    command_to_execute: List[str] = []
    working_dir: str | None = None 
    
    exec_kwargs = {
        "capture_output": True,
        "text": True,
        "check": False
    }

    try:
        if file_extension == ".py":
            print(f"Executing Python script: {code_path}")
            command_to_execute = ["python3", code_path]
            working_dir = os.path.dirname(os.path.abspath(code_path))

        elif file_extension == ".java":
            # (Your existing Java logic - ensure it's robust)
            java_source_dir = os.path.dirname(os.path.abspath(code_path))
            class_name = os.path.splitext(code_file_name)[0]
            compile_command = ["javac", code_path]
            print(f"Compiling Java: {' '.join(compile_command)}")
            compile_result = subprocess.run(compile_command, capture_output=True, text=True, check=False, cwd=java_source_dir)
            if compile_result.returncode != 0:
                error_output = f"Java compilation failed (in {java_source_dir}):\n--- STDOUT ---\n{compile_result.stdout.strip()}\n--- STDERR ---\n{compile_result.stderr.strip()}"
                return {"code": code_content, "output": error_output, "code_file_name": code_file_name, "return_code": compile_result.returncode}
            command_to_execute = ["java", "-cp", java_source_dir, class_name]
            working_dir = java_source_dir

        # === NEW C# HANDLING: TARGET .csproj FILES ===
        elif file_extension == ".csproj":
            print(f"Executing C# project: {code_path}")
            command_to_execute = ["dotnet", "run", "--project", code_path]
            # It's good practice to set the working directory to the project file's directory
            working_dir = os.path.dirname(os.path.abspath(code_path))
        
        # === MODIFIED .cs HANDLING: Inform user to use .csproj ===
        elif file_extension == ".cs":
            print(f"Direct .cs file execution attempted for: {code_path}")
            error_message = (f"Direct execution of .cs files ('{code_file_name}') is not supported by this script "
                             "due to previous environment inconsistencies. Please create a corresponding "
                             f"'.csproj' file (e.g., '{os.path.splitext(code_file_name)[0]}.csproj') and "
                             "ensure it's configured correctly. Then, target the .csproj file for execution.")
            return {
                "code": code_content, # Content of the .cs file
                "output": error_message,
                "code_file_name": code_file_name,
                "return_code": -1
            }

        elif file_extension == ".c":
            # (Your existing C logic - ensure it's robust)
            source_dir = os.path.dirname(os.path.abspath(code_path))
            executable_name = os.path.splitext(code_file_name)[0]
            executable_path = os.path.join(source_dir, executable_name)
            compile_command = ["gcc", code_path, "-o", executable_path]
            print(f"Compiling C: {' '.join(compile_command)}")
            compile_result = subprocess.run(compile_command, capture_output=True, text=True, check=False, cwd=source_dir)
            if compile_result.returncode != 0:
                error_output = f"C compilation failed:\n--- STDOUT ---\n{compile_result.stdout.strip()}\n--- STDERR ---\n{compile_result.stderr.strip()}"
                return {"code": code_content, "output": error_output, "code_file_name": code_file_name, "return_code": compile_result.returncode}
            command_to_execute = [executable_path]
            working_dir = source_dir

        elif file_extension in [".cpp", ".c++", ".cc"]:
            # (Your existing C++ logic - ensure it's robust)
            source_dir = os.path.dirname(os.path.abspath(code_path))
            executable_name = os.path.splitext(code_file_name)[0]
            executable_path = os.path.join(source_dir, executable_name)
            compile_command = ["g++", code_path, "-o", executable_path]
            print(f"Compiling C++: {' '.join(compile_command)}")
            compile_result = subprocess.run(compile_command, capture_output=True, text=True, check=False, cwd=source_dir)
            if compile_result.returncode != 0:
                error_output = f"C++ compilation failed:\n--- STDOUT ---\n{compile_result.stdout.strip()}\n--- STDERR ---\n{compile_result.stderr.strip()}"
                return {"code": code_content, "output": error_output, "code_file_name": code_file_name, "return_code": compile_result.returncode}
            command_to_execute = [executable_path]
            working_dir = source_dir
        else:
            raise ValueError(f"Unsupported file extension for execution: {file_extension} (from file: {code_path})")
        
        if not command_to_execute: # Should be caught by specific handlers or ValueError
             return {"code": code_content, "output": "Internal error: No command formulated for execution.", "code_file_name": code_file_name, "return_code": -1}

        print(f"Executing command: {' '.join(command_to_execute)}")
        if working_dir:
            print(f"In working directory: {working_dir}")
            exec_kwargs["cwd"] = working_dir
            
        execution_result = subprocess.run(command_to_execute, **exec_kwargs)
        
        output_log_parts = []
        if execution_result.stdout:
            output_log_parts.append("--- STDOUT ---")
            output_log_parts.append(execution_result.stdout.strip())
        if execution_result.stderr:
            output_log_parts.append("--- STDERR ---")
            output_log_parts.append(execution_result.stderr.strip())
        
        final_output = "\n".join(output_log_parts)
        if not final_output.strip(): # Check if effectively empty
            if execution_result.returncode == 0:
                final_output = "(No output on stdout or stderr)"
            else:
                final_output = f"(No output on stdout or stderr, execution failed with return code {execution_result.returncode})"
        
        if execution_result.returncode != 0:
            print(f"Execution of '{code_file_name}' failed with return code {execution_result.returncode}.")
        
        return {
            "code": code_content, # Content of the file specified by code_path (e.g., .py, .csproj)
            "output": final_output,
            "code_file_name": code_file_name, # e.g., "EmployeeDirectory.csproj"
            "return_code": execution_result.returncode
        }
    except FileNotFoundError as e:
        error_msg = f"Command not found (e.g., dotnet, python3, gcc) or file missing during execution: {str(e)}"
        print(error_msg)
        return {"code": code_content, "output": error_msg, "code_file_name": code_file_name, "return_code": -1}
    except ValueError as e: # Catches the ValueError from unsupported extensions
        print(str(e))
        return {"code": code_content, "output": str(e), "code_file_name": code_file_name, "return_code": -1}
    except Exception as e:
        error_msg = f"An unexpected error occurred in execute_code for '{code_file_name}': {type(e).__name__} - {str(e)}"
        print(error_msg)
        return {"code": code_content, "output": error_msg, "code_file_name": code_file_name, "return_code": -1}

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
        response = await requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP issues
        
        # Parse the response content (assuming it's JSON)
        data = await response.json()
        
        # Save the data to a file
        with open(output_file, "w") as file:
            json.dump(data, file, indent=4)
        
        response = await ctx.sample(
            messages=f"Read the following data about writing tools for the mcp server: {data}",
            system_prompt="You are an expert Python programmer developing MCP Server. Provide concise, working code examples without explanations.",
            temperature=0.7,
            max_tokens=300
        )
        
        print(f"Tool information successfully saved to '{output_file}'.")
    except requests.exceptions.RequestException as e:
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
def write_me_a_mcp_tool(conecept: str, ctx: Context) -> str:
    
    if os.path.exists(os.path.join(CODE_STORAGE, "tool_info.json")):
        pass
    else:
        "Fetching the data from the URL and saving it to a file for the tools document."
        fetch_and_save_tool_info()    
        
        return write_me_a_mcp_tool(ctx)
    
    return
        
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
        code_path = get_code_path(code_name)
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