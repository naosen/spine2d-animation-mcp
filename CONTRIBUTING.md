# Contributing to SPINE2D Animation MCP Server

Thank you for considering contributing to the SPINE2D Animation MCP Server! This document provides guidelines and instructions for contributing to this project.

## How to Contribute

1. **Report bugs and request features** by creating issues.
2. **Discuss the current state of the code** in issues or discussions.
3. **Submit fixes and features** via pull requests.

## Development Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/my-new-feature`)
5. Create a new Pull Request

## Pull Request Guidelines

1. Update the README.md with details of changes if applicable
2. Update the documentation if necessary
3. The PR should work on Python 3.6 or higher
4. Ensure any new code has appropriate test coverage
5. Maintain the coding style of the project

## Code Style

Please follow these guidelines for code style:

- Use 4 spaces for indentation
- Follow PEP 8 style guide for Python code
- Use descriptive variable names
- Add comments for complex operations

## Adding New Features

When adding new animation types or features:

1. **Animation Types**: Add new templates to the `animation_generator.py` file
2. **Emotion Modifiers**: Update the emotions dictionary in `animation_generator.py`
3. **SPINE2D Integration**: Modify the conversion methods in `spine2d_integration.py`
4. **MCP Tools**: Update the tool definitions in `server.py`

## Testing

1. Ensure your code works with various PSD file formats
2. Test with simple and complex character structures
3. Verify SPINE2D compatibility of exported files

## Documentation

When adding new features, please document them in:

1. Code comments for implementation details
2. `README.md` for user-facing features
3. `ANIMATION_CREATION_GUIDE.md` or `SPINE2D_INTEGRATION.md` as appropriate

## License

By contributing to the SPINE2D Animation MCP Server, you agree that your contributions will be licensed under the project's MIT License.