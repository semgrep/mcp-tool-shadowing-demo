.PHONY: all install provision-servers clean-servers list-servers angel devil

# Default target - install dependencies and provision servers
all: install provision-servers

# Install uv dependencies
install:
	@command -v uv >/dev/null 2>&1 || { echo "Installing uv..."; curl -LsSf https://astral.sh/uv/install.sh | sh; }
	uv sync

# Provision both MCP servers
provision-servers: install angel devil

# Add the angel server
angel:
	claude mcp add angel -- uv run angel_server.py

# Add the devil server
devil:
	claude mcp add devil -- uv run devil_server.py

# Clean up both servers from Claude
clean-servers:
	claude mcp remove angel || true
	claude mcp remove devil || true

# List all configured MCP servers
list-servers:
	claude mcp list

# Remove and re-add both servers (useful for updates)
reprovision: clean-servers provision-servers
