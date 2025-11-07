# AI Image Generation Agent - Personality Edition

An intelligent agent that generates AI images of public personalities using OpenAI's DALL-E API. Simply provide the name of any public figure, and the agent will create a high-quality AI-generated image.

## Features

- Generate AI images based on personality names
- Support for DALL-E 2 and DALL-E 3 models
- Customizable image parameters (size, quality, style)
- Automatic image download and storage
- Interactive and command-line modes
- Custom context support for personalized images

## Prerequisites

- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd AI-generated-images
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables:
```bash
cp .env.example .env
```

4. Edit the `.env` file and add your OpenAI API key:
```
OPENAI_API_KEY=your_actual_api_key_here
```

## Usage

### Interactive Mode

Run the agent without arguments to enter interactive mode:

```bash
python agent.py
```

You'll be prompted to:
1. Enter the name of a public personality
2. Optionally add custom context (e.g., "wearing a suit", "smiling")

### Command-Line Mode

Provide the personality name as a command-line argument:

```bash
python agent.py "Albert Einstein"
```

### Python API

Use the agent programmatically in your Python code:

```python
from agent import PersonalityImageAgent

# Create an agent instance
agent = PersonalityImageAgent()

# Generate a single image
result = agent.generate_image("Leonardo da Vinci")

# Generate with custom context
result = agent.generate_image(
    "Marie Curie",
    custom_context="in a laboratory, wearing a white coat"
)

# Generate multiple images
personalities = ["Isaac Newton", "Ada Lovelace", "Stephen Hawking"]
results = agent.generate_multiple_images(personalities)
```

## Configuration

Configure the agent by editing your `.env` file:

| Variable | Description | Default | Options |
|----------|-------------|---------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | Required | - |
| `IMAGE_MODEL` | DALL-E model to use | `dall-e-3` | `dall-e-2`, `dall-e-3` |
| `IMAGE_SIZE` | Size of generated images | `1024x1024` | See below |
| `IMAGE_QUALITY` | Image quality (DALL-E 3) | `standard` | `standard`, `hd` |
| `IMAGE_STYLE` | Image style (DALL-E 3) | `vivid` | `vivid`, `natural` |
| `OUTPUT_DIR` | Output directory | `generated_images` | Any valid path |

### Image Size Options

**DALL-E 3:**
- `1024x1024` (square)
- `1792x1024` (landscape)
- `1024x1792` (portrait)

**DALL-E 2:**
- `256x256`
- `512x512`
- `1024x1024`

## Examples

### Basic Usage

```bash
# Generate an image of a historical figure
python agent.py "Vincent van Gogh"

# Generate an image of a scientist
python agent.py "Neil deGrasse Tyson"

# Generate an image of a leader
python agent.py "Nelson Mandela"
```

### With Custom Context

When prompted for custom context, you can add specific details:

```
Enter the name of a public personality to generate an image:
> Frida Kahlo

Optional: Add custom context (e.g., 'wearing a suit', 'smiling', etc.)
Press Enter to skip:
> with flowers in hair, colorful background
```

## Output

Generated images are saved in the `generated_images/` directory (or your configured `OUTPUT_DIR`) with the following naming convention:

```
<personality_name>_<timestamp>.png
```

Example: `Albert_Einstein_20240315_143022.png`

## Code Structure

```
AI-generated-images/
├── agent.py              # Main agent implementation
├── config.py             # Configuration management
├── requirements.txt      # Python dependencies
├── .env.example          # Example environment variables
├── .gitignore           # Git ignore rules
├── README.md            # This file
└── generated_images/    # Generated images (created automatically)
```

## API Response

The agent returns a dictionary with the following structure:

```python
{
    'success': True,
    'personality': 'Albert Einstein',
    'prompt': 'A professional portrait of Albert Einstein, realistic style...',
    'image_path': 'generated_images/Albert_Einstein_20240315_143022.png',
    'image_url': 'https://...',  # Original DALL-E URL
    'filename': 'Albert_Einstein_20240315_143022.png'
}
```

## Error Handling

If an error occurs, the response will include:

```python
{
    'success': False,
    'personality': 'Name',
    'error': 'Error message'
}
```

## Costs

Image generation uses OpenAI's DALL-E API, which incurs costs:

- **DALL-E 3**: ~$0.04 per image (standard), ~$0.08 per image (HD)
- **DALL-E 2**: ~$0.02 per image (1024x1024)

Check [OpenAI's pricing page](https://openai.com/pricing) for current rates.

## Limitations

- Requires an active OpenAI API key with sufficient credits
- Generated images are AI interpretations, not actual photos
- Some personalities may be protected by OpenAI's content policy
- Rate limits apply based on your OpenAI account tier

## Troubleshooting

### "OPENAI_API_KEY is not set"

Make sure you've created a `.env` file from `.env.example` and added your API key.

### "Invalid API key"

Verify your API key is correct at https://platform.openai.com/api-keys

### "Rate limit exceeded"

You've hit OpenAI's rate limit. Wait a moment and try again, or upgrade your API plan.

### Module not found errors

Install all dependencies:
```bash
pip install -r requirements.txt
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Powered by [OpenAI's DALL-E API](https://platform.openai.com/docs/guides/images)
- Built with Python and the OpenAI Python library

## Support

For issues, questions, or suggestions, please open an issue in the GitHub repository.
