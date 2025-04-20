#!/usr/bin/env python3
import os
import json
import uuid
from typing import Dict, List, Any, Optional, Tuple
import logging
from psd_tools import PSDImage
from psd_tools.constants import LayerFlags
from PIL import Image

logger = logging.getLogger("spine2d-mcp.psd_parser")

class PsdParser:
    """Parse PSD files and extract layers for SPINE2D animation"""
    
    def __init__(self, storage_dir: str = "./storage"):
        self.storage_dir = storage_dir
        self.characters_dir = os.path.join(storage_dir, "characters")
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Ensure storage directories exist"""
        os.makedirs(self.storage_dir, exist_ok=True)
        os.makedirs(self.characters_dir, exist_ok=True)
    
    def parse_psd(self, file_path: str) -> Dict[str, Any]:
        """Parse a PSD file and extract layers"""
        try:
            # Validate input
            if not os.path.isfile(file_path):
                raise FileNotFoundError(f"PSD file not found: {file_path}")
            
            if not file_path.lower().endswith(".psd"):
                raise ValueError(f"File is not a PSD: {file_path}")
            
            # Generate character ID
            base_name = os.path.basename(file_path)
            character_id = f"char_{str(uuid.uuid4())[:8]}_{base_name.replace('.psd', '')}"
            character_dir = os.path.join(self.characters_dir, character_id)
            os.makedirs(character_dir, exist_ok=True)
            
            # Load PSD file
            psd = PSDImage.open(file_path)
            
            # Extract basic information
            width, height = psd.width, psd.height
            
            # Process layers
            layers_info = self._process_layers(psd, character_dir)
            
            # Save metadata
            metadata = {
                "character_id": character_id,
                "original_file": os.path.basename(file_path),
                "dimensions": {"width": width, "height": height},
                "layers_count": len(layers_info),
                "layers": layers_info,
                "imported_at": self._get_timestamp()
            }
            
            self._save_metadata(character_dir, metadata)
            
            return {
                "character_id": character_id,
                "dimensions": {"width": width, "height": height},
                "layers_count": len(layers_info)
            }
            
        except Exception as e:
            logger.error(f"Error parsing PSD file {file_path}: {e}")
            raise
    
    def _process_layers(self, psd: PSDImage, output_dir: str, parent_path: str = "") -> List[Dict[str, Any]]:
        """Process layers in the PSD file"""
        layers_info = []
        
        # Process layers in reverse order (bottom to top)
        for i, layer in enumerate(reversed(psd)):
            # Skip hidden layers
            if layer.is_hidden():
                continue
            
            layer_name = layer.name
            layer_id = f"layer_{i}"
            
            # Build the layer path
            current_path = f"{parent_path}/{layer_name}" if parent_path else layer_name
            
            if layer.is_group():
                # Process group layers recursively
                sublayers = self._process_layers(layer, output_dir, current_path)
                
                layers_info.append({
                    "id": layer_id,
                    "name": layer_name,
                    "type": "group",
                    "path": current_path,
                    "visible": not layer.is_hidden(),
                    "children": sublayers
                })
            else:
                # Process pixel layer
                layer_image_path = self._save_layer_image(layer, output_dir, layer_id)
                
                # Get layer bounds
                if layer.has_pixels():
                    left, top, right, bottom = layer.bbox
                    width = right - left
                    height = bottom - top
                else:
                    left, top, width, height = 0, 0, 0, 0
                
                layers_info.append({
                    "id": layer_id,
                    "name": layer_name,
                    "type": "pixel",
                    "path": current_path,
                    "visible": not layer.is_hidden(),
                    "position": {"x": left, "y": top},
                    "dimensions": {"width": width, "height": height},
                    "opacity": layer.opacity / 255.0 if hasattr(layer, "opacity") else 1.0,
                    "blend_mode": str(layer.blend_mode) if hasattr(layer, "blend_mode") else "normal",
                    "image_path": os.path.basename(layer_image_path) if layer_image_path else None
                })
        
        return layers_info
    
    def _save_layer_image(self, layer, output_dir: str, layer_id: str) -> Optional[str]:
        """Save layer as PNG image"""
        try:
            if not layer.has_pixels():
                return None
            
            # Extract layer image
            layer_image = layer.composite()
            if layer_image is None:
                return None
            
            # Save image
            image_filename = f"{layer_id}.png"
            image_path = os.path.join(output_dir, image_filename)
            
            # Save with transparency
            layer_image.save(image_path, "PNG")
            
            return image_path
        except Exception as e:
            logger.warning(f"Failed to save layer image: {e}")
            return None
    
    def _save_metadata(self, character_dir: str, metadata: Dict[str, Any]):
        """Save character metadata to JSON file"""
        metadata_path = os.path.join(character_dir, "metadata.json")
        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=2)
    
    def get_character_metadata(self, character_id: str) -> Optional[Dict[str, Any]]:
        """Get character metadata by ID"""
        character_dir = os.path.join(self.characters_dir, character_id)
        metadata_path = os.path.join(character_dir, "metadata.json")
        
        if not os.path.isfile(metadata_path):
            return None
        
        with open(metadata_path, "r") as f:
            return json.load(f)
    
    def list_characters(self) -> List[Dict[str, Any]]:
        """List all available characters"""
        characters = []
        
        # Check if characters directory exists
        if not os.path.isdir(self.characters_dir):
            return characters
        
        # Iterate through character directories
        for char_dir in os.listdir(self.characters_dir):
            char_path = os.path.join(self.characters_dir, char_dir)
            
            if os.path.isdir(char_path):
                metadata_path = os.path.join(char_path, "metadata.json")
                
                if os.path.isfile(metadata_path):
                    try:
                        with open(metadata_path, "r") as f:
                            metadata = json.load(f)
                            
                            characters.append({
                                "id": metadata.get("character_id"),
                                "name": metadata.get("original_file", "Unknown").replace(".psd", ""),
                                "dimensions": metadata.get("dimensions", {}),
                                "layers_count": metadata.get("layers_count", 0),
                                "imported_at": metadata.get("imported_at")
                            })
                    except Exception as e:
                        logger.warning(f"Failed to read metadata for {char_dir}: {e}")
        
        return characters
    
    def _get_timestamp(self) -> str:
        """Get current timestamp in ISO format"""
        from datetime import datetime
        return datetime.utcnow().isoformat() + "Z"