#!/usr/bin/env python3
"""
Simple demo script for the SPINE2D Animation MCP Server.
This script demonstrates how to use the server components directly.
"""

import os
import sys
import logging

# Add the parent directory to the Python path to import the src modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.psd_parser import PsdParser
from src.animation_generator import AnimationGenerator
from src.spine2d_integration import Spine2DIntegration

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("spine2d-demo")

def main():
    """Run a simple demonstration of SPINE2D Animation MCP functionality"""
    
    # Create storage directory
    storage_dir = os.path.join(os.path.dirname(__file__), 'demo_storage')
    os.makedirs(storage_dir, exist_ok=True)
    
    logger.info("Starting SPINE2D Animation Demo")
    
    # Initialize components
    psd_parser = PsdParser(storage_dir)
    animation_generator = AnimationGenerator(storage_dir)
    spine2d_integration = Spine2DIntegration(storage_dir)
    
    # Get PSD file path
    if len(sys.argv) > 1:
        psd_path = sys.argv[1]
    else:
        logger.info("No PSD file specified. Using a placeholder flow.")
        logger.info("To use a real PSD file, run: python simple_demo.py path/to/character.psd")
        psd_path = None
    
    # Demonstration flow
    if psd_path and os.path.isfile(psd_path):
        # 1. Import PSD file
        logger.info(f"Importing PSD file: {psd_path}")
        try:
            character_result = psd_parser.parse_psd(psd_path)
            character_id = character_result["character_id"]
            logger.info(f"Character imported with ID: {character_id}")
            
            # 2. Rig character
            logger.info(f"Setting up rigging for character: {character_id}")
            rig_result = spine2d_integration.rig_character(character_id)
            logger.info(f"Character rigged successfully. Bones: {rig_result['bone_count']}, IK: {rig_result['ik_count']}")
            
            # 3. Generate animation
            description = "happy waving with sparkles"
            logger.info(f"Generating animation: {description}")
            animation_result = animation_generator.generate_animation(character_id, description)
            animation_id = animation_result["animation_id"]
            logger.info(f"Animation generated with ID: {animation_id}")
            
            # 4. Export animation
            logger.info(f"Exporting animation: {animation_id}")
            export_result = spine2d_integration.export_animation(character_id, animation_id, "json")
            logger.info(f"Animation exported to: {export_result['file_path']}")
            
            logger.info("Demo completed successfully!")
            logger.info(f"All files are in: {storage_dir}")
        
        except Exception as e:
            logger.error(f"Error during demo: {e}")
    else:
        # Placeholder simulation
        logger.info("Running placeholder simulation...")
        
        character_id = "char_example"
        animation_id = "anim_example"
        
        logger.info(f"Character would be imported with ID: {character_id}")
        logger.info("Character would be rigged with approximately 15 bones and 4 IK constraints")
        logger.info(f"Animation 'happy waving with sparkles' would be generated with ID: {animation_id}")
        logger.info(f"Animation would be exported to: {os.path.join(storage_dir, 'exports', 'export_example', 'animation.json')}")
        
        logger.info("Demo simulation completed!")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())