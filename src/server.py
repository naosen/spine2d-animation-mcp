#!/usr/bin/env python3
import os
import sys
import json
import logging
from typing import Dict, List, Any, Optional
import traceback

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger("spine2d-mcp")

class McpError(Exception):
    """MCP protocol error"""
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(message)


class McpServer:
    """Model Context Protocol server implementation for SPINE2D animation"""
    
    def __init__(self, name: str, version: str):
        self.name = name
        self.version = version
        self.handlers = {}
        
        # Dependencies will be set by main.py
        self.psd_parser = None
        self.animation_generator = None
        self.spine2d_integration = None
        
        self.register_handlers()
    
    def register_handlers(self):
        """Register all request handlers"""
        self.handlers = {
            "listTools": self.handle_list_tools,
            "callTool": self.handle_call_tool,
            "listResources": self.handle_list_resources,
            "readResource": self.handle_read_resource,
        }
    
    def handle_list_tools(self, params: Dict) -> Dict:
        """Handle listTools request"""
        return {
            "tools": [
                {
                    "name": "import_psd",
                    "description": "Upload and process a PSD file",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "Path to PSD file"
                            }
                        },
                        "required": ["file_path"]
                    }
                },
                {
                    "name": "setup_character",
                    "description": "Automatically rig the character",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "character_id": {
                                "type": "string",
                                "description": "Character ID from import_psd"
                            }
                        },
                        "required": ["character_id"]
                    }
                },
                {
                    "name": "generate_animation",
                    "description": "Create animation from text description",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "character_id": {
                                "type": "string",
                                "description": "Character ID"
                            },
                            "description": {
                                "type": "string",
                                "description": "Animation description (e.g., 'wave happily')"
                            }
                        },
                        "required": ["character_id", "description"]
                    }
                },
                {
                    "name": "preview_animation",
                    "description": "Get a preview of the animation",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "character_id": {
                                "type": "string",
                                "description": "Character ID"
                            },
                            "animation_id": {
                                "type": "string",
                                "description": "Animation ID"
                            }
                        },
                        "required": ["character_id", "animation_id"]
                    }
                },
                {
                    "name": "export_animation",
                    "description": "Export the final animation",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "character_id": {
                                "type": "string",
                                "description": "Character ID"
                            },
                            "animation_id": {
                                "type": "string",
                                "description": "Animation ID"
                            },
                            "format": {
                                "type": "string",
                                "description": "Export format (json, png, gif)",
                                "enum": ["json", "png", "gif"]
                            }
                        },
                        "required": ["character_id", "animation_id", "format"]
                    }
                }
            ]
        }
    
    def handle_call_tool(self, params: Dict) -> Dict:
        """Handle callTool request"""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        if tool_name == "import_psd":
            return self._import_psd(arguments)
        elif tool_name == "setup_character":
            return self._setup_character(arguments)
        elif tool_name == "generate_animation":
            return self._generate_animation(arguments)
        elif tool_name == "preview_animation":
            return self._preview_animation(arguments)
        elif tool_name == "export_animation":
            return self._export_animation(arguments)
        else:
            raise McpError("MethodNotFound", f"Unknown tool: {tool_name}")
    
    def handle_list_resources(self, params: Dict) -> Dict:
        """Handle listResources request"""
        return {
            "resources": [
                {
                    "uri": "spine2d://characters",
                    "name": "Available Characters",
                    "mimeType": "application/json",
                    "description": "List of available characters that have been imported"
                }
            ]
        }
    
    def handle_read_resource(self, params: Dict) -> Dict:
        """Handle readResource request"""
        uri = params.get("uri")
        
        if uri == "spine2d://characters":
            # Example implementation - would actually read from storage
            characters = self._get_available_characters()
            return {
                "contents": [
                    {
                        "uri": uri,
                        "mimeType": "application/json",
                        "text": json.dumps(characters, indent=2)
                    }
                ]
            }
        else:
            raise McpError("InvalidRequest", f"Invalid URI: {uri}")
    
    def _import_psd(self, args: Dict) -> Dict:
        """Import a PSD file and extract layers"""
        file_path = args.get("file_path")
        if not file_path:
            return self._error_response("Missing file_path parameter")
        
        if not os.path.isfile(file_path):
            return self._error_response(f"File not found: {file_path}")
        
        try:
            # Use the PSD parser module
            if self.psd_parser is None:
                return self._error_response("PSD parser not initialized")
            
            result = self.psd_parser.parse_psd(file_path)
            
            return {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps({
                            "status": "success",
                            "message": f"PSD file '{file_path}' imported successfully",
                            "character_id": result["character_id"],
                            "layers_count": result["layers_count"],
                            "dimensions": result["dimensions"]
                        }, indent=2)
                    }
                ]
            }
        except Exception as e:
            logger.error(f"Error importing PSD: {e}")
            return self._error_response(f"Error importing PSD: {str(e)}")
    
    def _setup_character(self, args: Dict) -> Dict:
        """Automatically rig the character"""
        character_id = args.get("character_id")
        if not character_id:
            return self._error_response("Missing character_id parameter")
        
        try:
            # Use the SPINE2D integration module
            if self.spine2d_integration is None:
                return self._error_response("SPINE2D integration not initialized")
            
            # Check if character exists
            if self.psd_parser is None:
                return self._error_response("PSD parser not initialized")
            
            metadata = self.psd_parser.get_character_metadata(character_id)
            if metadata is None:
                return self._error_response(f"Character not found: {character_id}")
            
            # Create the rig
            result = self.spine2d_integration.rig_character(character_id)
            
            return {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps({
                            "status": "success",
                            "message": f"Character '{character_id}' rigged successfully",
                            "rig_id": result["rig_id"],
                            "bones_count": result["bone_count"],
                            "ik_constraints": result["ik_count"]
                        }, indent=2)
                    }
                ]
            }
        except Exception as e:
            logger.error(f"Error setting up character: {e}")
            return self._error_response(f"Error setting up character: {str(e)}")
    
    def _generate_animation(self, args: Dict) -> Dict:
        """Generate animation from text description"""
        character_id = args.get("character_id")
        description = args.get("description")
        
        if not character_id or not description:
            return self._error_response("Missing character_id or description parameter")
        
        try:
            # Use the animation generator module
            if self.animation_generator is None:
                return self._error_response("Animation generator not initialized")
            
            # Check if character exists
            if self.psd_parser is None:
                return self._error_response("PSD parser not initialized")
            
            metadata = self.psd_parser.get_character_metadata(character_id)
            if metadata is None:
                return self._error_response(f"Character not found: {character_id}")
            
            # Generate the animation
            result = self.animation_generator.generate_animation(character_id, description)
            
            return {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps({
                            "status": "success",
                            "message": f"Animation '{description}' generated successfully",
                            "animation_id": result["animation_id"],
                            "animation_type": result["animation_type"],
                            "emotion": result["emotion"],
                            "duration": result["duration"]
                        }, indent=2)
                    }
                ]
            }
        except Exception as e:
            logger.error(f"Error generating animation: {e}")
            return self._error_response(f"Error generating animation: {str(e)}")
    
    def _preview_animation(self, args: Dict) -> Dict:
        """Get a preview of the animation"""
        character_id = args.get("character_id")
        animation_id = args.get("animation_id")
        
        if not character_id or not animation_id:
            return self._error_response("Missing character_id or animation_id parameter")
        
        try:
            # Use the SPINE2D integration module
            if self.spine2d_integration is None:
                return self._error_response("SPINE2D integration not initialized")
            
            # Check if animation exists
            if self.animation_generator is None:
                return self._error_response("Animation generator not initialized")
            
            animation = self.animation_generator.get_animation_metadata(animation_id)
            if animation is None:
                return self._error_response(f"Animation not found: {animation_id}")
            
            # Generate a preview by exporting to GIF
            result = self.spine2d_integration.export_animation(character_id, animation_id, "gif")
            
            # Create a URL to the preview file
            preview_url = f"file://{result['file_path']}"
            
            return {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps({
                            "status": "success",
                            "message": f"Preview for animation '{animation_id}' generated",
                            "preview_url": preview_url,
                            "export_id": result["export_id"]
                        }, indent=2)
                    }
                ]
            }
        except Exception as e:
            logger.error(f"Error generating preview: {e}")
            return self._error_response(f"Error generating preview: {str(e)}")
    
    def _export_animation(self, args: Dict) -> Dict:
        """Export the final animation"""
        character_id = args.get("character_id")
        animation_id = args.get("animation_id")
        format = args.get("format", "json")
        
        if not character_id or not animation_id:
            return self._error_response("Missing character_id or animation_id parameter")
        
        try:
            # Use the SPINE2D integration module
            if self.spine2d_integration is None:
                return self._error_response("SPINE2D integration not initialized")
            
            # Check if animation exists
            if self.animation_generator is None:
                return self._error_response("Animation generator not initialized")
            
            animation = self.animation_generator.get_animation_metadata(animation_id)
            if animation is None:
                return self._error_response(f"Animation not found: {animation_id}")
            
            # Export the animation
            result = self.spine2d_integration.export_animation(character_id, animation_id, format)
            
            # Create a URL to the exported file
            export_url = f"file://{result['file_path']}"
            
            return {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps({
                            "status": "success",
                            "message": f"Animation '{animation_id}' exported as {format}",
                            "export_url": export_url,
                            "export_id": result["export_id"],
                            "animation_name": result["animation_name"]
                        }, indent=2)
                    }
                ]
            }
        except Exception as e:
            logger.error(f"Error exporting animation: {e}")
            return self._error_response(f"Error exporting animation: {str(e)}")
    
    def _get_available_characters(self) -> List[Dict]:
        """Get list of available characters"""
        try:
            if self.psd_parser is None:
                return []
            
            return self.psd_parser.list_characters()
        except Exception as e:
            logger.error(f"Error listing characters: {e}")
            return []
    
    def _error_response(self, message: str) -> Dict:
        """Create an error response"""
        logger.error(f"Error response: {message}")
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps({
                        "status": "error",
                        "message": message
                    }, indent=2)
                }
            ],
            "isError": True
        }
    
    def process_request(self, request: Dict) -> Dict:
        """Process an MCP request"""
        try:
            request_id = request.get("id")
            method = request.get("method")
            params = request.get("params", {})
            
            if method not in self.handlers:
                raise McpError("MethodNotFound", f"Unknown method: {method}")
            
            result = self.handlers[method](params)
            
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": result
            }
        except McpError as e:
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "error": {
                    "code": e.code,
                    "message": e.message
                }
            }
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            logger.error(traceback.format_exc())
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "error": {
                    "code": "InternalError",
                    "message": str(e)
                }
            }
    
    def run(self):
        """Run the MCP server over stdio"""
        logger.info(f"Starting {self.name} v{self.version}")
        
        try:
            while True:
                # Read request from stdin
                line = sys.stdin.readline()
                if not line:
                    break
                
                # Parse request
                try:
                    request = json.loads(line)
                except json.JSONDecodeError:
                    logger.error(f"Failed to parse request: {line}")
                    continue
                
                # Process request
                response = self.process_request(request)
                
                # Write response to stdout
                sys.stdout.write(json.dumps(response) + "\n")
                sys.stdout.flush()
        
        except KeyboardInterrupt:
            logger.info("Server shutdown requested")
        except Exception as e:
            logger.error(f"Fatal error: {e}")
            logger.error(traceback.format_exc())
            sys.exit(1)
        
        logger.info("Server shutdown complete")


if __name__ == "__main__":
    server = McpServer("spine2d-animation-server", "0.1.0")
    server.run()