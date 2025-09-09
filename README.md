# mcp-tool-shadowing-demo
a demonstration of tool shadowing behavior in the Model Context Protocol.

## prerequisites

Project requires `uv`. See installation instructions:
https://github.com/astral-sh/uv?tab=readme-ov-file#installation

The makefile `install` instruction will install UV with the OSX/Linux instructions and then run `uv sync`.


## usage

The makefile will install the servers for Claude Code locally for this directory. To demonstrate collision behavior, run `make angel`, request `totally_cool_legit_tool` and note the behavior, then run `make devil` and rerun Claude Code with the same prompt and observe the difference.

