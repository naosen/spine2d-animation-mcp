# SPINE2D Animation MCP Server

This Model Context Protocol (MCP) server provides tools for creating SPINE2D animations from PSD character files using natural language descriptions.

## Overview

The SPINE2D Animation MCP server allows you to:
1. Import PSD character files
2. Automatically rig characters
3. Generate animations using natural language descriptions
4. Preview animations
5. Export animations in various formats

## Requirements

- Python 3.6+
- Required Python packages (installed automatically):
  - Flask
  - Pydantic
  - Pillow
  - PSD-Tools
  - OpenAI (for natural language processing)
  - Requests
  - Python-dotenv

## Installation

1. Clone this repository
2. Run the installation script:
```bash
./install.sh
```

The installation script will:
- Create necessary storage directories
- Install Python dependencies
- Configure MCP settings for VS Code
- Optionally configure MCP settings for Claude Desktop

## Usage

After installation, restart VS Code and/or Claude. You can then use the following tools through the MCP server:

### Import PSD Character

Upload and process a PSD file:

```
Use: "Import my character from character.psd"
```

Parameters:
- `file_path`: Path to the PSD file

### Setup Character

Automatically rig a character that has been imported:

```
Use: "Set up rigging for my character"
```

Parameters:
- `character_id`: Character ID from import_psd

### Generate Animation

Create an animation from a text description:

```
Use: "Create a happy waving animation for my character"
Use: "Make my character jump with excitement"
Use: "Animate my character to run scared with sparkle effects"
```

Parameters:
- `character_id`: Character ID
- `description`: Animation description (e.g., "wave happily")

### Preview Animation

Get a preview of the animation:

```
Use: "Show me a preview of the waving animation"
```

Parameters:
- `character_id`: Character ID
- `animation_id`: Animation ID

### Export Animation

Export the final animation:

```
Use: "Export the jumping animation as a GIF"
```

Parameters:
- `character_id`: Character ID
- `animation_id`: Animation ID
- `format`: Export format (json, png, gif)

## Project Structure

```
spine2d-animation-mcp/
├── README.md             # This file
├── requirements.txt      # Python dependencies
├── install.sh            # Installation script
├── src/
│   ├── main.py           # Entry point
│   ├── server.py         # MCP server implementation
│   ├── psd_parser.py     # PSD parsing module
│   ├── animation_generator.py  # Animation generation module
│   └── spine2d_integration.py  # SPINE2D integration module
└── storage/              # Created during installation
    ├── characters/       # Imported character data
    ├── animations/       # Generated animations
    ├── rigs/             # Character rigs
    └── exports/          # Exported animations
```

## How It Works

1. **PSD Import**: The server parses a PSD file, extracts layers, and organizes them into a character structure.
2. **Character Rigging**: The server analyzes the character structure and automatically creates bones, IK constraints, and skin attachments.
3. **Animation Generation**: Natural language descriptions are parsed to extract animation type, emotion, and intensity. The server then applies these to animation templates.
4. **Animation Preview**: The server generates a preview of the animation in GIF format.
5. **Animation Export**: The server exports the animation in the requested format (JSON, PNG, or GIF).

## Limitations

1. The automatic rigging system is based on layer names and structure, which may require specific naming conventions for optimal results.
2. The animation templates are predefined, so complex custom animations may require manual adjustment.
3. The natural language processing is simplified in this implementation and may not capture all nuances of complex descriptions.

## Future Improvements

1. Improved natural language understanding using more advanced LLM integration
2. More sophisticated automatic rigging with bone placement based on image analysis
3. Expanded library of animation templates
4. Real-time preview rendering
5. More export formats and options

## Documentation

- [Animation Creation Guide](ANIMATION_CREATION_GUIDE.md) - Complete guide for creating animations from scratch with just a PSD file
- [SPINE2D Integration Guide](SPINE2D_INTEGRATION.md) - Instructions for connecting MCP server outputs to your SPINE2D software