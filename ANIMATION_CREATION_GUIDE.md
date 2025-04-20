# Creating SPINE2D Animations From Scratch with MCP Server

This guide walks you through the complete process of creating SPINE2D animations from scratch, starting with just a PSD file of your character.

## Prerequisites

1. A PSD file with your character artwork
2. Properly installed SPINE2D Animation MCP server
3. SPINE2D software (only needed for the final steps)

## PSD File Preparation

For best results, organize your PSD file with these guidelines:

1. **Layer Structure**: Each body part should be on a separate layer
2. **Naming Convention**: Name layers clearly (e.g., "head", "arm_right", "leg_left")
3. **Transform Origin**: Set pivot points for parts that will rotate
4. **Group Related Layers**: Group parts that move together
5. **Clean Transparency**: Remove any unwanted transparent pixels

Example layer structure:
```
Character
├── Head
│   ├── Hair
│   ├── Face
│   └── Neck
├── Torso
├── Arms
│   ├── Arm_Right
│   ├── Hand_Right
│   ├── Arm_Left
│   └── Hand_Left
├── Legs
│   ├── Leg_Right
│   ├── Foot_Right
│   ├── Leg_Left
│   └── Foot_Left
```

## Step 1: Import the PSD File

First, import your character PSD file using the MCP server:

```
Import my character from /path/to/your/character.psd
```

The MCP server will:
- Extract all layers from the PSD
- Organize them into a character structure
- Create individual PNG files for each part
- Generate a character ID for future reference

Example response:
```
Character imported successfully! Character ID: char_a1b2c3d4_CharacterName
```

## Step 2: Automatically Rig the Character

Next, create a skeleton rig for your character:

```
Set up rigging for character char_a1b2c3d4_CharacterName
```

The MCP server will:
- Analyze the character's structure
- Create a bone hierarchy
- Set up IK constraints
- Attach the PSD layers to the appropriate bones
- Create a complete SPINE2D-compatible rig

Example response:
```
Character rigged successfully! 15 bones and 4 IK constraints created. Rig ID: rig_e5f6g7h8_CharacterName
```

## Step 3: Generate Animations with Natural Language

Now, you can create animations using simple natural language descriptions:

```
Generate a happy waving animation for character char_a1b2c3d4_CharacterName
```

The MCP server will:
- Parse your description to identify:
  - Base animation (wave)
  - Emotion (happy)
  - Intensity (normal)
- Apply animation templates to the character's skeleton
- Generate keyframes for all bones
- Add emotional expressions
- Apply physics (hair/clothing movement)
- Add particle effects if specified

Example response:
```
Animation generated successfully! Animation ID: anim_i9j0k1l2_wave
```

## Step 4: Preview the Animation

To see what your animation looks like:

```
Show me a preview of animation anim_i9j0k1l2_wave for character char_a1b2c3d4_CharacterName
```

The MCP server will:
- Render the animation to a GIF
- Provide a URL to view the animation

## Step 5: Refine the Animation with More Specifics

You can create multiple animations with different descriptions:

```
Create a running animation with scared expression for character char_a1b2c3d4_CharacterName
```

```
Generate a slow jumping animation with excitement and sparkle effects for character char_a1b2c3d4_CharacterName
```

Each description can include:
- Animation type (walk, run, jump, idle, etc.)
- Emotion (happy, sad, angry, excited, etc.)
- Intensity modifiers (slightly, very, extremely)
- Special effects (sparkles, fire, water)
- Timing modifiers (slow, fast, quick)

## Step 6: Export for SPINE2D

When you're satisfied with an animation, export it for SPINE2D:

```
Export animation anim_i9j0k1l2_wave for character char_a1b2c3d4_CharacterName as json
```

The MCP server will:
- Convert the animation to SPINE2D format
- Create a complete SPINE2D project file
- Include all necessary image assets
- Save everything to the exports directory

## Step 7: Import to SPINE2D for Final Touches

Open SPINE2D and import the exported JSON file:

1. Launch SPINE2D
2. Select "File" → "Import Data"
3. Navigate to the export directory and select the JSON file
4. Make any desired adjustments to the animation

## Example: Complete Workflow

Starting with a character PSD file `/Users/eli/Desktop/Assets/Characters/MS_Char_Morgana.psd`:

1. **Import:**
   ```
   Import my character from /Users/eli/Desktop/Assets/Characters/MS_Char_Morgana.psd
   ```
   Response: Character ID `char_a1b2c3d4_Morgana`

2. **Rig:**
   ```
   Set up rigging for character char_a1b2c3d4_Morgana
   ```
   Response: Rig created successfully

3. **Create first animation:**
   ```
   Generate a happy waving animation with sparkles for character char_a1b2c3d4_Morgana
   ```
   Response: Animation ID `anim_e5f6g7h8_wave`

4. **Preview:**
   ```
   Show me a preview of animation anim_e5f6g7h8_wave for character char_a1b2c3d4_Morgana
   ```
   Response: GIF preview URL

5. **Create additional animation:**
   ```
   Create an excited jumping animation for character char_a1b2c3d4_Morgana
   ```
   Response: Animation ID `anim_i9j0k1l2_jump`

6. **Export first animation:**
   ```
   Export animation anim_e5f6g7h8_wave for character char_a1b2c3d4_Morgana as json
   ```
   Response: Export path

7. **Export second animation:**
   ```
   Export animation anim_i9j0k1l2_jump for character char_a1b2c3d4_Morgana as json
   ```
   Response: Export path

8. Open SPINE2D and import each animation for final adjustments

## Tips for Better Animations

1. **Be Specific**: Include emotion, intensity, and speed in your descriptions
2. **Combine Animations**: Create sequences like "walk then wave" for more complex movements
3. **Use Physics Terms**: Mention "bounce", "weight", or "follow-through" for more natural movement
4. **Target Specific Body Parts**: Specify "with head tilt" or "using left arm" for detailed control
5. **Add Effects**: Mention "sparkles", "dust", "fire" or other effects to enhance animations

## Conclusion

This MCP server eliminates the need to manually rig and animate characters in SPINE2D. By using natural language, you can rapidly create animations from just a PSD file, then import them into SPINE2D for any final adjustments.