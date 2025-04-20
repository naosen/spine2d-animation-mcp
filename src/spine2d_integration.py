#!/usr/bin/env python3
import os
import json
import uuid
from typing import Dict, List, Any, Optional, Tuple
import logging
from datetime import datetime

logger = logging.getLogger("spine2d-mcp.spine2d_integration")

class Spine2DIntegration:
    """Integration with SPINE2D for character rigging and animation export"""
    
    def __init__(self, storage_dir: str = "./storage"):
        self.storage_dir = storage_dir
        self.rigs_dir = os.path.join(storage_dir, "rigs")
        self.exports_dir = os.path.join(storage_dir, "exports")
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Ensure storage directories exist"""
        os.makedirs(self.storage_dir, exist_ok=True)
        os.makedirs(self.rigs_dir, exist_ok=True)
        os.makedirs(self.exports_dir, exist_ok=True)
    
    def rig_character(self, character_id: str) -> Dict[str, Any]:
        """Create a SPINE2D rig for a character"""
        try:
            from .psd_parser import PsdParser
            
            # Get character metadata
            parser = PsdParser(self.storage_dir)
            metadata = parser.get_character_metadata(character_id)
            
            if metadata is None:
                raise ValueError(f"Character not found: {character_id}")
            
            # Generate rig ID
            rig_id = f"rig_{str(uuid.uuid4())[:8]}_{character_id}"
            rig_dir = os.path.join(self.rigs_dir, rig_id)
            os.makedirs(rig_dir, exist_ok=True)
            
            # Analyze layers to determine character structure
            layers = metadata.get("layers", [])
            rig_data = self._analyze_character_structure(layers)
            
            # Create SPINE2D skeleton
            skeleton = self._create_skeleton(rig_data, metadata["dimensions"])
            
            # Create skin attachments
            skin = self._create_skin(rig_data, character_id, metadata)
            
            # Create IK constraints
            ik_constraints = self._create_ik_constraints(rig_data, skeleton)
            
            # Create SPINE2D project
            spine_project = {
                "skeleton": {
                    "hash": str(uuid.uuid4()),
                    "spine": "4.1.00",
                    "width": metadata["dimensions"]["width"],
                    "height": metadata["dimensions"]["height"],
                    "images": f"../characters/{character_id}/",
                    "audio": ""
                },
                "bones": skeleton["bones"],
                "slots": skeleton["slots"],
                "skins": {
                    "default": skin
                },
                "ik": ik_constraints,
                "animations": {}
            }
            
            # Save rig metadata
            rig_metadata = {
                "rig_id": rig_id,
                "character_id": character_id,
                "bone_count": len(skeleton["bones"]),
                "ik_count": len(ik_constraints),
                "created_at": self._get_timestamp()
            }
            
            self._save_rig_data(rig_dir, spine_project, rig_metadata)
            
            return {
                "rig_id": rig_id,
                "bone_count": len(skeleton["bones"]),
                "ik_count": len(ik_constraints)
            }
            
        except Exception as e:
            logger.error(f"Error rigging character {character_id}: {e}")
            raise
    
    def _analyze_character_structure(self, layers: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze character layers to determine structure"""
        # This is a simplified implementation
        # In a real implementation, we would use image analysis to detect parts
        
        rig_data = {
            "parts": {},
            "hierarchy": {}
        }
        
        # Define common body part names to look for
        body_parts = {
            "head": ["head", "face", "hair"],
            "body": ["body", "torso", "chest"],
            "arm_right": ["arm_right", "right_arm", "rightarm"],
            "arm_left": ["arm_left", "left_arm", "leftarm"],
            "hand_right": ["hand_right", "right_hand", "righthand"],
            "hand_left": ["hand_left", "left_hand", "lefthand"],
            "leg_right": ["leg_right", "right_leg", "rightleg"],
            "leg_left": ["leg_left", "left_leg", "leftleg"],
            "foot_right": ["foot_right", "right_foot", "rightfoot"],
            "foot_left": ["foot_left", "left_foot", "leftfoot"]
        }
        
        # Find layers matching body parts
        for layer in self._flatten_layers(layers):
            layer_name = layer["name"].lower()
            
            for part_key, part_names in body_parts.items():
                if any(part_name in layer_name for part_name in part_names):
                    rig_data["parts"][part_key] = layer
                    break
        
        # Define hierarchy relationships
        hierarchy = {
            "root": ["body"],
            "body": ["head", "arm_left", "arm_right", "leg_left", "leg_right"],
            "arm_left": ["hand_left"],
            "arm_right": ["hand_right"],
            "leg_left": ["foot_left"],
            "leg_right": ["foot_right"]
        }
        
        rig_data["hierarchy"] = hierarchy
        
        return rig_data
    
    def _flatten_layers(self, layers: List[Dict[str, Any]], parent_path: str = "") -> List[Dict[str, Any]]:
        """Flatten nested layers structure"""
        result = []
        
        for layer in layers:
            # Add current layer
            if layer["type"] != "group":
                result.append(layer)
            
            # Process children if it's a group
            if "children" in layer and isinstance(layer["children"], list):
                result.extend(self._flatten_layers(layer["children"], layer["path"]))
        
        return result
    
    def _create_skeleton(self, rig_data: Dict[str, Any], dimensions: Dict[str, int]) -> Dict[str, Any]:
        """Create SPINE2D skeleton from rig data"""
        bones = []
        slots = []
        
        # Create root bone
        bones.append({
            "name": "root",
            "x": dimensions["width"] / 2,
            "y": dimensions["height"] / 2,
            "length": 50
        })
        
        # Create bones for each part
        for part_name, layer in rig_data["parts"].items():
            if "position" in layer:
                x = layer["position"]["x"] + layer["dimensions"]["width"] / 2
                y = dimensions["height"] - layer["position"]["y"] - layer["dimensions"]["height"] / 2
            else:
                x = dimensions["width"] / 2
                y = dimensions["height"] / 2
            
            # Find parent
            parent = "root"
            for parent_name, children in rig_data["hierarchy"].items():
                if part_name in children:
                    parent = parent_name
                    break
            
            bones.append({
                "name": part_name,
                "parent": parent,
                "x": x - dimensions["width"] / 2,  # Relative to parent
                "y": y - dimensions["height"] / 2,  # Relative to parent
                "length": max(layer["dimensions"]["width"], layer["dimensions"]["height"]) / 2 if "dimensions" in layer else 50
            })
            
            # Create slot
            if "image_path" in layer and layer["image_path"]:
                slots.append({
                    "name": f"slot_{part_name}",
                    "bone": part_name,
                    "attachment": layer["image_path"].replace(".png", "")
                })
        
        return {
            "bones": bones,
            "slots": slots
        }
    
    def _create_skin(self, rig_data: Dict[str, Any], character_id: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Create skin attachments"""
        skin = {}
        
        # Create attachments for each part
        for part_name, layer in rig_data["parts"].items():
            if "image_path" in layer and layer["image_path"]:
                slot_name = f"slot_{part_name}"
                attachment_name = layer["image_path"].replace(".png", "")
                
                # Calculate attachment position
                if "dimensions" in layer:
                    width = layer["dimensions"]["width"]
                    height = layer["dimensions"]["height"]
                else:
                    width = height = 100  # Default
                
                skin[slot_name] = {
                    attachment_name: {
                        "x": 0,
                        "y": 0,
                        "width": width,
                        "height": height,
                        "path": layer["image_path"]
                    }
                }
        
        return skin
    
    def _create_ik_constraints(self, rig_data: Dict[str, Any], skeleton: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create IK constraints for the skeleton"""
        ik_constraints = []
        
        # Add arm IK
        if "arm_right" in rig_data["parts"] and "hand_right" in rig_data["parts"]:
            ik_constraints.append({
                "name": "arm_right_ik",
                "target": "hand_right",
                "bones": ["arm_right"],
                "mix": 1,
                "bendPositive": True
            })
        
        if "arm_left" in rig_data["parts"] and "hand_left" in rig_data["parts"]:
            ik_constraints.append({
                "name": "arm_left_ik",
                "target": "hand_left",
                "bones": ["arm_left"],
                "mix": 1,
                "bendPositive": False
            })
        
        # Add leg IK
        if "leg_right" in rig_data["parts"] and "foot_right" in rig_data["parts"]:
            ik_constraints.append({
                "name": "leg_right_ik",
                "target": "foot_right",
                "bones": ["leg_right"],
                "mix": 1,
                "bendPositive": False
            })
        
        if "leg_left" in rig_data["parts"] and "foot_left" in rig_data["parts"]:
            ik_constraints.append({
                "name": "leg_left_ik",
                "target": "foot_left",
                "bones": ["leg_left"],
                "mix": 1,
                "bendPositive": False
            })
        
        return ik_constraints
    
    def _save_rig_data(self, rig_dir: str, spine_project: Dict[str, Any], metadata: Dict[str, Any]):
        """Save rig data to JSON file"""
        # Save metadata
        metadata_path = os.path.join(rig_dir, "metadata.json")
        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=2)
        
        # Save SPINE2D project
        project_path = os.path.join(rig_dir, "spine_project.json")
        with open(project_path, "w") as f:
            json.dump(spine_project, f, indent=2)
    
    def export_animation(self, character_id: str, animation_id: str, format: str = "json") -> Dict[str, Any]:
        """Export animation to SPINE2D format"""
        try:
            from .animation_generator import AnimationGenerator
            
            # Get animation data
            generator = AnimationGenerator(self.storage_dir)
            animation_data = generator.get_animation_data(animation_id)
            animation_metadata = generator.get_animation_metadata(animation_id)
            
            if animation_data is None or animation_metadata is None:
                raise ValueError(f"Animation not found: {animation_id}")
            
            # Get character rig
            rig_id = self._find_rig_for_character(character_id)
            
            if rig_id is None:
                raise ValueError(f"No rig found for character: {character_id}")
            
            # Load rig data
            rig_dir = os.path.join(self.rigs_dir, rig_id)
            project_path = os.path.join(rig_dir, "spine_project.json")
            
            with open(project_path, "r") as f:
                spine_project = json.load(f)
            
            # Convert animation data to SPINE2D format
            animation_name = animation_metadata.get("animation_type", "animation")
            spine_animation = self._convert_to_spine_animation(animation_data)
            
            # Add animation to SPINE2D project
            spine_project["animations"][animation_name] = spine_animation
            
            # Generate export ID
            export_id = f"export_{str(uuid.uuid4())[:8]}_{animation_id}"
            export_dir = os.path.join(self.exports_dir, export_id)
            os.makedirs(export_dir, exist_ok=True)
            
            # Save export metadata
            export_metadata = {
                "export_id": export_id,
                "character_id": character_id,
                "animation_id": animation_id,
                "format": format,
                "created_at": self._get_timestamp()
            }
            
            metadata_path = os.path.join(export_dir, "metadata.json")
            with open(metadata_path, "w") as f:
                json.dump(export_metadata, f, indent=2)
            
            # Export in requested format
            export_path = ""
            
            if format == "json":
                export_path = os.path.join(export_dir, f"{animation_name}.json")
                with open(export_path, "w") as f:
                    json.dump(spine_project, f, indent=2)
            elif format == "png":
                # In a real implementation, we would render frames as PNG
                export_path = os.path.join(export_dir, f"{animation_name}.png")
                # Placeholder for rendering
                with open(export_path, "w") as f:
                    f.write("PNG output placeholder")
            elif format == "gif":
                # In a real implementation, we would render as GIF
                export_path = os.path.join(export_dir, f"{animation_name}.gif")
                # Placeholder for rendering
                with open(export_path, "w") as f:
                    f.write("GIF output placeholder")
            
            return {
                "export_id": export_id,
                "format": format,
                "file_path": export_path,
                "animation_name": animation_name
            }
            
        except Exception as e:
            logger.error(f"Error exporting animation {animation_id}: {e}")
            raise
    
    def _find_rig_for_character(self, character_id: str) -> Optional[str]:
        """Find a rig ID for a character"""
        if not os.path.isdir(self.rigs_dir):
            return None
        
        # Iterate through rig directories
        for rig_dir_name in os.listdir(self.rigs_dir):
            rig_path = os.path.join(self.rigs_dir, rig_dir_name)
            
            if os.path.isdir(rig_path):
                metadata_path = os.path.join(rig_path, "metadata.json")
                
                if os.path.isfile(metadata_path):
                    try:
                        with open(metadata_path, "r") as f:
                            metadata = json.load(f)
                            
                            if metadata.get("character_id") == character_id:
                                return rig_dir_name
                    except Exception as e:
                        logger.warning(f"Failed to read metadata for {rig_dir_name}: {e}")
        
        return None
    
    def _convert_to_spine_animation(self, animation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert our animation data to SPINE2D animation format"""
        spine_animation = {
            "bones": {},
            "slots": {},
            "deform": {},
            "drawOrder": [],
            "events": []
        }
        
        # Convert keyframes
        for bone_name, keyframes in animation_data.get("keyframes", {}).items():
            bone_animation = {}
            
            # Handle different properties
            for prop in ["rotate", "translate", "scale"]:
                bone_animation[prop] = []
            
            for keyframe in keyframes:
                time = keyframe.get("time", 0)
                
                # Handle rotation
                if "rotation" in keyframe:
                    bone_animation["rotate"].append({
                        "time": time,
                        "angle": keyframe["rotation"],
                        "curve": "stepped"
                    })
                
                # Handle translation
                if "x" in keyframe or "y" in keyframe:
                    bone_animation["translate"].append({
                        "time": time,
                        "x": keyframe.get("x", 0),
                        "y": keyframe.get("y", 0),
                        "curve": "stepped"
                    })
            
            # Only add bone if it has animations
            if bone_animation["rotate"] or bone_animation["translate"] or bone_animation["scale"]:
                spine_animation["bones"][bone_name] = bone_animation
        
        # Handle facial expressions as slot attachments
        if "face" in animation_data.get("keyframes", {}):
            slot_animation = {
                "attachment": []
            }
            
            for keyframe in animation_data["keyframes"]["face"]:
                if "expression" in keyframe:
                    slot_animation["attachment"].append({
                        "time": keyframe.get("time", 0),
                        "name": f"face_{keyframe['expression']}"
                    })
            
            spine_animation["slots"]["slot_face"] = slot_animation
        
        # Add particle effects if any
        if "particles" in animation_data:
            event_frames = []
            
            for particle in animation_data["particles"]:
                event_frames.append({
                    "time": 0,
                    "name": f"effect_{particle['type']}",
                    "string": particle.get("color", "#FFFFFF"),
                    "int": particle.get("count", 10),
                    "float": particle.get("duration", 1.0)
                })
            
            if event_frames:
                spine_animation["events"] = event_frames
        
        return spine_animation
    
    def get_rig_metadata(self, rig_id: str) -> Optional[Dict[str, Any]]:
        """Get rig metadata by ID"""
        rig_dir = os.path.join(self.rigs_dir, rig_id)
        metadata_path = os.path.join(rig_dir, "metadata.json")
        
        if not os.path.isfile(metadata_path):
            return None
        
        with open(metadata_path, "r") as f:
            return json.load(f)
    
    def get_export_metadata(self, export_id: str) -> Optional[Dict[str, Any]]:
        """Get export metadata by ID"""
        export_dir = os.path.join(self.exports_dir, export_id)
        metadata_path = os.path.join(export_dir, "metadata.json")
        
        if not os.path.isfile(metadata_path):
            return None
        
        with open(metadata_path, "r") as f:
            return json.load(f)
    
    def list_exports(self, character_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all exports, optionally filtered by character"""
        exports = []
        
        # Check if exports directory exists
        if not os.path.isdir(self.exports_dir):
            return exports
        
        # Iterate through export directories
        for export_dir_name in os.listdir(self.exports_dir):
            export_path = os.path.join(self.exports_dir, export_dir_name)
            
            if os.path.isdir(export_path):
                metadata_path = os.path.join(export_path, "metadata.json")
                
                if os.path.isfile(metadata_path):
                    try:
                        with open(metadata_path, "r") as f:
                            metadata = json.load(f)
                            
                            # Filter by character_id if provided
                            if character_id is None or metadata.get("character_id") == character_id:
                                exports.append({
                                    "id": metadata.get("export_id"),
                                    "character_id": metadata.get("character_id"),
                                    "animation_id": metadata.get("animation_id"),
                                    "format": metadata.get("format"),
                                    "created_at": metadata.get("created_at")
                                })
                    except Exception as e:
                        logger.warning(f"Failed to read metadata for {export_dir_name}: {e}")
        
        return exports
    
    def _get_timestamp(self) -> str:
        """Get current timestamp in ISO format"""
        return datetime.utcnow().isoformat() + "Z"