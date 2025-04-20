#!/usr/bin/env python3
import os
import json
import uuid
import re
from typing import Dict, List, Any, Optional, Tuple
import logging
import random
from datetime import datetime

# In a real implementation, we would use OpenAI or another LLM API here
# import openai

logger = logging.getLogger("spine2d-mcp.animation_generator")

class AnimationGenerator:
    """Generate animations from natural language descriptions"""
    
    def __init__(self, storage_dir: str = "./storage"):
        self.storage_dir = storage_dir
        self.animations_dir = os.path.join(storage_dir, "animations")
        self._ensure_directories()
        
        # Initialize animation templates
        self.templates = self._initialize_templates()
        
        # Initialize emotion modifiers
        self.emotions = self._initialize_emotions()
    
    def _ensure_directories(self):
        """Ensure storage directories exist"""
        os.makedirs(self.storage_dir, exist_ok=True)
        os.makedirs(self.animations_dir, exist_ok=True)
    
    def _initialize_templates(self) -> Dict[str, Dict[str, Any]]:
        """Initialize animation templates"""
        return {
            "wave": {
                "name": "Wave",
                "duration": 2.0,
                "keyframes": {
                    "arm_right": [
                        {"time": 0.0, "rotation": 0, "x": 0, "y": 0},
                        {"time": 0.5, "rotation": 45, "x": 10, "y": -20},
                        {"time": 1.0, "rotation": -15, "x": 15, "y": -15},
                        {"time": 1.5, "rotation": 45, "x": 10, "y": -20},
                        {"time": 2.0, "rotation": 0, "x": 0, "y": 0}
                    ],
                    "hand_right": [
                        {"time": 0.0, "rotation": 0},
                        {"time": 0.5, "rotation": 15},
                        {"time": 1.0, "rotation": -10},
                        {"time": 1.5, "rotation": 15},
                        {"time": 2.0, "rotation": 0}
                    ],
                    "face": [
                        {"time": 0.0, "expression": "neutral"},
                        {"time": 2.0, "expression": "neutral"}
                    ]
                }
            },
            "jump": {
                "name": "Jump",
                "duration": 1.5,
                "keyframes": {
                    "root": [
                        {"time": 0.0, "y": 0},
                        {"time": 0.7, "y": 100},
                        {"time": 1.5, "y": 0}
                    ],
                    "leg_left": [
                        {"time": 0.0, "rotation": 0},
                        {"time": 0.3, "rotation": -15},
                        {"time": 0.7, "rotation": 10},
                        {"time": 1.2, "rotation": -20},
                        {"time": 1.5, "rotation": 0}
                    ],
                    "leg_right": [
                        {"time": 0.0, "rotation": 0},
                        {"time": 0.3, "rotation": -15},
                        {"time": 0.7, "rotation": 10},
                        {"time": 1.2, "rotation": -20},
                        {"time": 1.5, "rotation": 0}
                    ],
                    "face": [
                        {"time": 0.0, "expression": "neutral"},
                        {"time": 0.7, "expression": "excited"},
                        {"time": 1.5, "expression": "neutral"}
                    ]
                }
            },
            "walk": {
                "name": "Walk",
                "duration": 1.2,
                "keyframes": {
                    "root": [
                        {"time": 0.0, "x": 0},
                        {"time": 1.2, "x": 50}
                    ],
                    "leg_left": [
                        {"time": 0.0, "rotation": 0},
                        {"time": 0.3, "rotation": 20},
                        {"time": 0.6, "rotation": 0},
                        {"time": 0.9, "rotation": -20},
                        {"time": 1.2, "rotation": 0}
                    ],
                    "leg_right": [
                        {"time": 0.0, "rotation": -20},
                        {"time": 0.3, "rotation": 0},
                        {"time": 0.6, "rotation": 20},
                        {"time": 0.9, "rotation": 0},
                        {"time": 1.2, "rotation": -20}
                    ],
                    "arm_left": [
                        {"time": 0.0, "rotation": -10},
                        {"time": 0.6, "rotation": 10},
                        {"time": 1.2, "rotation": -10}
                    ],
                    "arm_right": [
                        {"time": 0.0, "rotation": 10},
                        {"time": 0.6, "rotation": -10},
                        {"time": 1.2, "rotation": 10}
                    ],
                    "face": [
                        {"time": 0.0, "expression": "neutral"},
                        {"time": 1.2, "expression": "neutral"}
                    ]
                }
            },
            "run": {
                "name": "Run",
                "duration": 0.8,
                "keyframes": {
                    "root": [
                        {"time": 0.0, "x": 0, "y": 0},
                        {"time": 0.2, "x": 15, "y": 10},
                        {"time": 0.4, "x": 30, "y": 0},
                        {"time": 0.6, "x": 45, "y": 10},
                        {"time": 0.8, "x": 60, "y": 0}
                    ],
                    "leg_left": [
                        {"time": 0.0, "rotation": -30},
                        {"time": 0.2, "rotation": 0},
                        {"time": 0.4, "rotation": 30},
                        {"time": 0.6, "rotation": 0},
                        {"time": 0.8, "rotation": -30}
                    ],
                    "leg_right": [
                        {"time": 0.0, "rotation": 30},
                        {"time": 0.2, "rotation": 0},
                        {"time": 0.4, "rotation": -30},
                        {"time": 0.6, "rotation": 0},
                        {"time": 0.8, "rotation": 30}
                    ],
                    "arm_left": [
                        {"time": 0.0, "rotation": 30},
                        {"time": 0.4, "rotation": -30},
                        {"time": 0.8, "rotation": 30}
                    ],
                    "arm_right": [
                        {"time": 0.0, "rotation": -30},
                        {"time": 0.4, "rotation": 30},
                        {"time": 0.8, "rotation": -30}
                    ],
                    "face": [
                        {"time": 0.0, "expression": "determined"},
                        {"time": 0.8, "expression": "determined"}
                    ]
                }
            },
            "idle": {
                "name": "Idle",
                "duration": 4.0,
                "keyframes": {
                    "root": [
                        {"time": 0.0, "y": 0},
                        {"time": 2.0, "y": -3},
                        {"time": 4.0, "y": 0}
                    ],
                    "body": [
                        {"time": 0.0, "rotation": 0},
                        {"time": 2.0, "rotation": 2},
                        {"time": 4.0, "rotation": 0}
                    ],
                    "head": [
                        {"time": 0.0, "rotation": 0},
                        {"time": 1.0, "rotation": -1},
                        {"time": 3.0, "rotation": 1},
                        {"time": 4.0, "rotation": 0}
                    ],
                    "face": [
                        {"time": 0.0, "expression": "neutral"},
                        {"time": 1.5, "expression": "blink"},
                        {"time": 1.7, "expression": "neutral"},
                        {"time": 4.0, "expression": "neutral"}
                    ]
                }
            }
        }
    
    def _initialize_emotions(self) -> Dict[str, Dict[str, Any]]:
        """Initialize emotion modifiers"""
        return {
            "happy": {
                "face": {
                    "base_expression": "happy",
                    "blink_rate": 0.3
                },
                "movement": {
                    "speed": 1.2,
                    "bounce": 1.3,
                    "energy": 1.3
                }
            },
            "sad": {
                "face": {
                    "base_expression": "sad",
                    "blink_rate": 0.1
                },
                "movement": {
                    "speed": 0.7,
                    "bounce": 0.5,
                    "energy": 0.6
                }
            },
            "angry": {
                "face": {
                    "base_expression": "angry",
                    "blink_rate": 0.1
                },
                "movement": {
                    "speed": 1.3,
                    "bounce": 0.8,
                    "energy": 1.5
                }
            },
            "scared": {
                "face": {
                    "base_expression": "scared",
                    "blink_rate": 0.4
                },
                "movement": {
                    "speed": 1.4,
                    "bounce": 0.7,
                    "energy": 1.1
                }
            },
            "excited": {
                "face": {
                    "base_expression": "excited",
                    "blink_rate": 0.2
                },
                "movement": {
                    "speed": 1.5,
                    "bounce": 1.5,
                    "energy": 1.8
                }
            }
        }
    
    def generate_animation(self, character_id: str, description: str) -> Dict[str, Any]:
        """Generate animation from text description"""
        try:
            # Parse the description
            animation_type, emotion, intensity = self._parse_description(description)
            
            # Generate animation ID
            animation_id = f"anim_{str(uuid.uuid4())[:8]}_{animation_type}"
            
            # Create animation directory
            animation_dir = os.path.join(self.animations_dir, animation_id)
            os.makedirs(animation_dir, exist_ok=True)
            
            # Get base template
            template = self._get_template(animation_type)
            
            # Apply emotion modifiers
            animation_data = self._apply_emotion(template, emotion, intensity)
            
            # Add character-specific adjustments
            animation_data = self._adjust_for_character(animation_data, character_id)
            
            # Add physics and effects
            animation_data = self._add_physics_and_effects(animation_data, description)
            
            # Save metadata
            metadata = {
                "animation_id": animation_id,
                "character_id": character_id,
                "description": description,
                "animation_type": animation_type,
                "emotion": emotion,
                "intensity": intensity,
                "duration": animation_data["duration"],
                "created_at": self._get_timestamp()
            }
            
            # Save animation data
            self._save_animation_data(animation_dir, animation_data, metadata)
            
            return {
                "animation_id": animation_id,
                "animation_type": animation_type,
                "emotion": emotion,
                "duration": animation_data["duration"]
            }
            
        except Exception as e:
            logger.error(f"Error generating animation: {e}")
            raise
    
    def _parse_description(self, description: str) -> Tuple[str, str, float]:
        """
        Parse animation description to extract type, emotion, and intensity
        
        In a real implementation, we would use an LLM here
        """
        description = description.lower()
        
        # Determine animation type
        animation_type = "idle"  # Default
        for template_name in self.templates.keys():
            if template_name in description:
                animation_type = template_name
                break
        
        # Determine emotion
        emotion = "neutral"  # Default
        for emotion_name in self.emotions.keys():
            if emotion_name in description:
                emotion = emotion_name
                break
        
        # Determine intensity
        intensity = 1.0  # Default
        
        intensity_words = {
            "very": 1.5,
            "extremely": 2.0,
            "slightly": 0.7,
            "barely": 0.5,
            "incredibly": 2.0,
            "super": 1.8,
            "little": 0.6
        }
        
        for word, modifier in intensity_words.items():
            if word in description:
                intensity = modifier
                break
        
        return animation_type, emotion, intensity
    
    def _get_template(self, animation_type: str) -> Dict[str, Any]:
        """Get animation template by type"""
        if animation_type not in self.templates:
            logger.warning(f"Unknown animation type: {animation_type}, using idle")
            animation_type = "idle"
        
        # Create a deep copy of the template
        import copy
        return copy.deepcopy(self.templates[animation_type])
    
    def _apply_emotion(self, template: Dict[str, Any], emotion: str, intensity: float) -> Dict[str, Any]:
        """Apply emotion modifiers to animation template"""
        if emotion not in self.emotions:
            return template
        
        emotion_data = self.emotions[emotion]
        result = template.copy()
        
        # Adjust animation speed based on emotion
        speed_modifier = emotion_data["movement"]["speed"]
        energy_modifier = emotion_data["movement"]["energy"]
        
        # Apply intensity
        speed_modifier = 1.0 + (speed_modifier - 1.0) * intensity
        energy_modifier = 1.0 + (energy_modifier - 1.0) * intensity
        
        # Adjust duration
        if speed_modifier != 1.0:
            result["duration"] = result["duration"] / speed_modifier
        
        # Adjust keyframes
        for bone_name, keyframes in result["keyframes"].items():
            if bone_name == "face":
                # Apply facial expression
                for keyframe in keyframes:
                    if keyframe["expression"] == "neutral":
                        keyframe["expression"] = emotion_data["face"]["base_expression"]
            else:
                # Adjust movement energy
                for keyframe in keyframes:
                    for prop in ["rotation", "x", "y"]:
                        if prop in keyframe and keyframe[prop] != 0:
                            keyframe[prop] = keyframe[prop] * energy_modifier
        
        return result
    
    def _adjust_for_character(self, animation_data: Dict[str, Any], character_id: str) -> Dict[str, Any]:
        """Adjust animation for specific character"""
        # In a real implementation, we would load character data and adjust the animation
        return animation_data
    
    def _add_physics_and_effects(self, animation_data: Dict[str, Any], description: str) -> Dict[str, Any]:
        """Add physics and effects based on description"""
        # Add hair physics
        if "hair" in animation_data["keyframes"]:
            return animation_data
        
        # Simple hair physics based on root movement
        if "root" in animation_data["keyframes"] and "hair" not in animation_data["keyframes"]:
            root_keyframes = animation_data["keyframes"]["root"]
            hair_keyframes = []
            
            # Delayed follow with some exaggeration
            delay = 0.1
            for i, kf in enumerate(root_keyframes):
                if i > 0:
                    time = min(kf["time"] + delay, animation_data["duration"])
                    hair_kf = {"time": time}
                    
                    # Copy relevant properties with delay and exaggeration
                    for prop in ["x", "y", "rotation"]:
                        if prop in kf:
                            hair_kf[prop] = kf[prop] * 1.2  # Exaggerate
                    
                    hair_keyframes.append(hair_kf)
            
            if hair_keyframes:
                animation_data["keyframes"]["hair"] = hair_keyframes
        
        # Add particle effects based on description
        particles = []
        
        if "sparkle" in description or "magic" in description:
            particles.append({
                "type": "sparkle",
                "count": 10,
                "duration": animation_data["duration"],
                "color": "#FFFF99"
            })
        
        if "fire" in description:
            particles.append({
                "type": "fire",
                "count": 20,
                "duration": animation_data["duration"],
                "color": "#FF5500"
            })
        
        if "water" in description or "splash" in description:
            particles.append({
                "type": "water",
                "count": 15,
                "duration": animation_data["duration"],
                "color": "#66CCFF"
            })
        
        if particles:
            animation_data["particles"] = particles
        
        return animation_data
    
    def _save_animation_data(self, animation_dir: str, animation_data: Dict[str, Any], metadata: Dict[str, Any]):
        """Save animation data to JSON file"""
        # Save metadata
        metadata_path = os.path.join(animation_dir, "metadata.json")
        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=2)
        
        # Save animation data
        animation_path = os.path.join(animation_dir, "animation.json")
        with open(animation_path, "w") as f:
            json.dump(animation_data, f, indent=2)
    
    def get_animation_metadata(self, animation_id: str) -> Optional[Dict[str, Any]]:
        """Get animation metadata by ID"""
        animation_dir = os.path.join(self.animations_dir, animation_id)
        metadata_path = os.path.join(animation_dir, "metadata.json")
        
        if not os.path.isfile(metadata_path):
            return None
        
        with open(metadata_path, "r") as f:
            return json.load(f)
    
    def get_animation_data(self, animation_id: str) -> Optional[Dict[str, Any]]:
        """Get animation data by ID"""
        animation_dir = os.path.join(self.animations_dir, animation_id)
        animation_path = os.path.join(animation_dir, "animation.json")
        
        if not os.path.isfile(animation_path):
            return None
        
        with open(animation_path, "r") as f:
            return json.load(f)
    
    def list_animations(self, character_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all available animations, optionally filtered by character"""
        animations = []
        
        # Check if animations directory exists
        if not os.path.isdir(self.animations_dir):
            return animations
        
        # Iterate through animation directories
        for anim_dir in os.listdir(self.animations_dir):
            anim_path = os.path.join(self.animations_dir, anim_dir)
            
            if os.path.isdir(anim_path):
                metadata_path = os.path.join(anim_path, "metadata.json")
                
                if os.path.isfile(metadata_path):
                    try:
                        with open(metadata_path, "r") as f:
                            metadata = json.load(f)
                            
                            # Filter by character_id if provided
                            if character_id is None or metadata.get("character_id") == character_id:
                                animations.append({
                                    "id": metadata.get("animation_id"),
                                    "character_id": metadata.get("character_id"),
                                    "description": metadata.get("description"),
                                    "animation_type": metadata.get("animation_type"),
                                    "emotion": metadata.get("emotion"),
                                    "duration": metadata.get("duration"),
                                    "created_at": metadata.get("created_at")
                                })
                    except Exception as e:
                        logger.warning(f"Failed to read metadata for {anim_dir}: {e}")
        
        return animations
    
    def _get_timestamp(self) -> str:
        """Get current timestamp in ISO format"""
        return datetime.utcnow().isoformat() + "Z"