#!/usr/bin/env python3
"""
Windsurf MCP provisioning script.
Reads existing Windsurf configuration and adds/updates angel-server and devil-server.
"""

import json
import os
import shutil
from pathlib import Path


def get_windsurf_config_path():
    """Get the path to the Windsurf MCP configuration file."""
    home = Path.home()
    config_path = home / ".codeium" / "windsurf" / "mcp_config.json"
    return config_path


def backup_config(config_path):
    """Create a backup of the existing configuration."""
    if config_path.exists():
        backup_path = config_path.with_suffix(".json.backup")
        shutil.copy2(config_path, backup_path)
        print(f"Created backup: {backup_path}")
        return backup_path
    return None


def load_existing_config(config_path):
    """Load existing Windsurf configuration or create a new one."""
    if config_path.exists():
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                print(f"Loaded existing configuration from {config_path}")
                return config
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error reading existing config: {e}")
            print("Creating new configuration...")
    
    return {"mcpServers": {}}


def add_mcp_servers(config, project_path):
    """Add angel-server and devil-server to the configuration."""
    servers = {
        "a-devil-server": {
            "command": "uv",
            "args": ["run", "--project", str(project_path), "devil-server"],
            "cwd": str(project_path)
        },
        "an-angel-server": {
            "command": "uv",
            "args": ["run", "--project", str(project_path), "angel-server"],
            "cwd": str(project_path)
        },
    }
    
    # Ensure mcpServers exists
    if "mcpServers" not in config:
        config["mcpServers"] = {}
    
    # Remove old conflicting entries if they exist
    conflicting_keys = ["angel", "adevil"]
    for key in conflicting_keys:
        if key in config["mcpServers"]:
            print(f"Removing conflicting server: {key}")
            del config["mcpServers"][key]
    
    # Add or update the servers
    for server_name, server_config in servers.items():
        config["mcpServers"][server_name] = server_config
        print(f"Added/updated {server_name}")
    
    return config


def save_config(config, config_path):
    """Save the configuration to the Windsurf config file."""
    # Ensure the directory exists
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"Configuration saved to {config_path}")


def main():
    """Main provisioning function."""
    # Get current project directory
    project_path = Path.cwd().resolve()
    print(f"Project path: {project_path}")
    
    # Get Windsurf config path
    config_path = get_windsurf_config_path()
    print(f"Windsurf config path: {config_path}")
    
    # Create backup
    backup_path = backup_config(config_path)
    
    try:
        # Load existing configuration
        config = load_existing_config(config_path)
        
        # Add MCP servers
        config = add_mcp_servers(config, project_path)
        
        # Save configuration
        save_config(config, config_path)
        
        print("\nWindsurf MCP servers provisioned successfully!")
        print("Servers added:")
        print("  - angel-server")
        print("  - devil-server")
        
    except Exception as e:
        print(f"Error during provisioning: {e}")
        if backup_path and backup_path.exists():
            print(f"Backup available at: {backup_path}")
        raise


if __name__ == "__main__":
    main()