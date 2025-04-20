# Connecting MCP Server Outputs to SPINE2D Software

This guide explains how to use the animation files created by the SPINE2D Animation MCP server with your existing SPINE2D software.

## Export Formats

The MCP server can export animations in three formats:

1. **JSON** - SPINE2D project files that can be directly imported
2. **PNG** - Image sequences of the animation frames
3. **GIF** - Animated preview (not directly importable to SPINE2D)

## Workflow: MCP Server to SPINE2D

### Step 1: Export Animation as JSON

First, export your animation as a JSON file using the MCP server:

```
Export animation [animation_id] for character [character_id] as json
```

This will create a JSON file in the `/storage/exports/[export_id]/` directory. The exact path will be provided in the response.

### Step 2: Locate Exported Files

The export command creates several files:
- `[animation_name].json` - The main SPINE2D project file
- Associated image files for the character parts

All exported files are stored in the storage directory configured during installation, typically:
```
/Users/eli/Desktop/spine2d-animation-mcp/storage/exports/[export_id]/
```

### Step 3: Import into SPINE2D

1. Open SPINE2D software
2. Select "File" → "Import Data"
3. Navigate to the export directory and select the `.json` file
4. In the import dialog:
   - Set "Import scale" to 1.0
   - Check "Import images" option
   - Set the "Images folder" to the same export directory

### Step 4: Adjust the Imported Animation

After importing, you may need to:
- Fine-tune bone positions
- Adjust animation timing
- Modify attachments
- Add additional keyframes

## Important Notes on Compatibility

1. **SPINE2D Version**: The MCP server generates files compatible with SPINE2D version 4.1. If you're using a different version, you may need to adjust the import settings.

2. **Project Structure**: The server creates a complete SPINE2D project with:
   - Skeleton data
   - Bones hierarchy
   - Slots and attachments
   - Animations with keyframes
   - IK constraints

3. **Image Paths**: Make sure SPINE2D can access the image files. If you move the JSON file without the images, you'll need to update the paths.

4. **Character Structure**: The automatic rigging assumes a standard character structure. You may need to adjust the rig for characters with unique proportions or structures.

## Export Configuration

You can customize how animations are exported by modifying:

```python
# spine2d-animation-mcp/src/spine2d_integration.py
# Look for the _convert_to_spine_animation method
```

Key configurable settings include:
- Skeleton version
- Frame rate
- Interpolation methods
- Image output resolution

## Troubleshooting

If you encounter issues importing files:

1. **Missing Images**: Make sure all image files are in the correct location
2. **Version Mismatch**: Check that the SPINE2D version in the JSON file matches your software
3. **Path Issues**: Ensure paths in the JSON file match the actual file locations
4. **Image Format**: Verify SPINE2D can read the image format (PNG is recommended)

For more complex animations, you may want to export from the MCP server and then enhance them manually in SPINE2D.