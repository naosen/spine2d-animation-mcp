#!/bin/bash
# SPINE2D Animation MCP Server Installation Script

set -e  # Exit on any error

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
MCP_SETTINGS_PATH="$HOME/Library/Application Support/Code/User/globalStorage/rooveterinaryinc.roo-cline/settings/mcp_settings.json"
CLAUDE_SETTINGS_PATH="$HOME/Library/Application Support/Claude/claude_desktop_config.json"

echo "========================================="
echo "SPINE2D Animation MCP Server Installation"
echo "========================================="

# Check Python installation
if command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
    echo "✅ Python 3 is installed."
else
    echo "❌ Python 3 is not installed. Please install Python 3 and try again."
    exit 1
fi

# Create storage directory
mkdir -p "$SCRIPT_DIR/storage"
mkdir -p "$SCRIPT_DIR/storage/characters"
mkdir -p "$SCRIPT_DIR/storage/animations"
mkdir -p "$SCRIPT_DIR/storage/rigs"
mkdir -p "$SCRIPT_DIR/storage/exports"
echo "✅ Storage directories created."

# Install Python dependencies
echo "Installing Python dependencies..."
$PYTHON_CMD -m pip install -r "$SCRIPT_DIR/requirements.txt"
echo "✅ Python dependencies installed."

# Make sure main.py is executable
chmod +x "$SCRIPT_DIR/src/main.py"
echo "✅ Made main.py executable."

# MCP server configuration
SERVER_NAME="spine2d-animation"
SERVER_COMMAND="$PYTHON_CMD"
SERVER_ARGS="$SCRIPT_DIR/src/main.py --storage $SCRIPT_DIR/storage"

# Create a function to update MCP settings
update_mcp_settings() {
    local settings_path=$1
    
    if [ ! -f "$settings_path" ]; then
        # Create new settings file with our server
        echo "{
  \"mcpServers\": {
    \"$SERVER_NAME\": {
      \"command\": \"$SERVER_COMMAND\",
      \"args\": [\"$SERVER_ARGS\"],
      \"disabled\": false,
      \"alwaysAllow\": []
    }
  }
}" > "$settings_path"
        echo "✅ Created new MCP settings file at $settings_path"
    else
        # Check if jq is installed
        if ! command -v jq &>/dev/null; then
            echo "⚠️ jq is not installed. Manual configuration required."
            echo "Please add the following configuration to $settings_path:"
            echo "{
  \"mcpServers\": {
    \"$SERVER_NAME\": {
      \"command\": \"$SERVER_COMMAND\",
      \"args\": [\"$SERVER_ARGS\"],
      \"disabled\": false,
      \"alwaysAllow\": []
    }
  }
}"
            return
        fi
        
        # Backup the original file
        cp "$settings_path" "${settings_path}.backup"
        
        # Add our server to the existing config
        local temp_file="${settings_path}.temp"
        jq ".mcpServers.\"$SERVER_NAME\" = {
            \"command\": \"$SERVER_COMMAND\",
            \"args\": [\"$SERVER_ARGS\"],
            \"disabled\": false,
            \"alwaysAllow\": []
        }" "$settings_path" > "$temp_file"
        
        mv "$temp_file" "$settings_path"
        echo "✅ Updated MCP settings file at $settings_path"
    fi
}

# Configure VS Code MCP settings
echo "Configuring MCP settings for VS Code..."
VS_CODE_DIR="$(dirname "$MCP_SETTINGS_PATH")"
if [ ! -d "$VS_CODE_DIR" ]; then
    mkdir -p "$VS_CODE_DIR"
fi
update_mcp_settings "$MCP_SETTINGS_PATH"

# Ask about Claude Desktop configuration
read -p "Do you want to configure this MCP server for Claude Desktop as well? (y/n): " configure_claude

if [ "$configure_claude" = "y" ] || [ "$configure_claude" = "Y" ]; then
    echo "Configuring MCP settings for Claude Desktop..."
    CLAUDE_DIR="$(dirname "$CLAUDE_SETTINGS_PATH")"
    if [ ! -d "$CLAUDE_DIR" ]; then
        mkdir -p "$CLAUDE_DIR"
    fi
    update_mcp_settings "$CLAUDE_SETTINGS_PATH"
fi

echo "========================================="
echo "✅ Installation complete!"
echo "========================================="
echo ""
echo "The SPINE2D Animation MCP server is now installed."
echo "It provides the following tools:"
echo ""
echo "1. import_psd - Upload and process a PSD file"
echo "2. setup_character - Automatically rig the character"
echo "3. generate_animation - Create animation from text description"
echo "4. preview_animation - Get a preview of the animation"
echo "5. export_animation - Export the final animation"
echo ""
echo "To use the server, restart VS Code and/or Claude."
echo "Then you can use commands like:"
echo ""
echo "- 'Import my character from character.psd'"
echo "- 'Animate my character to wave happily'"
echo "- 'Create a jumping animation for my character with sparkles'"
echo ""
echo "========================================="