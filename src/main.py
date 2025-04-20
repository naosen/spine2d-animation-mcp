#!/usr/bin/env python3
import os
import sys
import logging
import argparse
from server import McpServer
from psd_parser import PsdParser
from animation_generator import AnimationGenerator
from spine2d_integration import Spine2DIntegration

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger("spine2d-mcp")

def parse_args():
    parser = argparse.ArgumentParser(description='SPINE2D Animation MCP Server')
    parser.add_argument(
        '--storage', 
        default='./storage', 
        help='Storage directory path'
    )
    return parser.parse_args()

def main():
    args = parse_args()
    
    # Create storage directory if it doesn't exist
    os.makedirs(args.storage, exist_ok=True)
    
    # Initialize dependencies
    parser = PsdParser(args.storage)
    generator = AnimationGenerator(args.storage)
    integration = Spine2DIntegration(args.storage)
    
    # Create MCP server
    server = McpServer(
        name="spine2d-animation-server",
        version="0.1.0"
    )
    
    # Set dependencies
    server.psd_parser = parser
    server.animation_generator = generator
    server.spine2d_integration = integration
    
    # Run server
    logger.info(f"Starting SPINE2D Animation MCP Server")
    server.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        import traceback
        logger.error(traceback.format_exc())
        sys.exit(1)