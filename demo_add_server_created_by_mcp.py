#!/usr/bin/env python3

import asyncio
import json
from typing import Any, Sequence
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio


server = Server("add-numbers-server")


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    List available tools.
    Each tool specifies its arguments using JSON Schema validation.
    """
    return [
        types.Tool(
            name="add_numbers",
            description="Add two numbers together",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "First number to add"
                    },
                    "b": {
                        "type": "number", 
                        "description": "Second number to add"
                    }
                },
                "required": ["a", "b"]
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict[str, Any] | None
) -> list[types.TextContent]:
    """
    Handle tool execution requests.
    Tools can modify server state and notify clients of changes.
    """
    if name != "add_numbers":
        raise ValueError(f"Unknown tool: {name}")
    
    if not arguments:
        raise ValueError("Missing arguments")
    
    # Extract the two numbers
    a = arguments.get("a")
    b = arguments.get("b")
    
    if a is None or b is None:
        raise ValueError("Both 'a' and 'b' parameters are required")
    
    # Perform the addition
    result = a + b
    
    return [
        types.TextContent(
            type="text",
            text=f"The sum of {a} and {b} is {result}"
        )
    ]


async def main():
    # Run the server using stdin/stdout streams
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="add-numbers-server",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())