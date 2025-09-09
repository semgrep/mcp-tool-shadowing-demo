#!/usr/bin/env python

import asyncio

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

app = Server("angel-server")


@app.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="totally_cool_legit_tool",
            description="A totally cool and legitimate tool that performs amazing operations.",
            inputSchema={
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            },
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name == "totally_cool_legit_tool":
        return [types.TextContent(type="text", text="hello from angel server")]
    else:
        raise ValueError(f"Unknown tool: {name}")


def main():
    asyncio.run(async_main())


async def async_main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    main()
