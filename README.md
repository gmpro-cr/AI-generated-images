# AI Media Generation Agent - Images & Videos

An intelligent agent that generates both AI images and videos of public personalities. Uses Google's Gemini API for prompt enhancement and Hugging Face's free inference API for actual video generation. Simply provide the name of any public figure, and the agent will create either a detailed image description or an actual AI-generated video!

## 🎬 NEW: Free AI Video Generation!

**This agent now supports FREE AI video generation** using Hugging Face's open-source models:
- ✅ **Completely FREE** - No API costs for video generation
- ✅ **Actual videos** - Get real MP4 video files, not just descriptions
- ✅ **Multiple models** - Choose from several open-source video models
- ✅ **Customizable** - Control duration, FPS, and quality
- ✅ **No credit card required** - Just a Gemini API key (free)

## Features

- 🎬 **Generate AI videos** using free Hugging Face models
- 🎨 Generate detailed image descriptions based on personality names
- 🤖 Uses Google's Gemini AI for prompt enhancement
- ⚡ Support for custom context and personalization
- 💾 Automatic storage with timestamps
- 🔄 Interactive and command-line modes
- 🆓 100% free to use (with free API keys)

## Prerequisites

- Python 3.8 or higher
- Google Gemini API key ([Get one here - FREE](https://aistudio.google.com/app/apikey))
- (Optional) Hugging Face API token for better rate limits ([Get one here - FREE](https://huggingface.co/settings/tokens))

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

4. Edit the `.env` file and add your API keys:
```
GEMINI_API_KEY=your_gemini_api_key_here
HUGGINGFACE_API_KEY=your_hf_token_here  # Optional - leave empty for free tier
```

## Getting Your FREE API Keys

### Gemini API Key (Required)
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and paste it in your `.env` file

### Hugging Face Token (Optional - Recommended for Video)
1. Go to [Hugging Face Settings](https://huggingface.co/settings/tokens)
2. Sign in or create a free account
3. Click "New token" and create a read token
4. Copy the token and paste it in your `.env` file
5. **Note**: You can use video generation without this, but with rate limits

## Usage

### Interactive Mode (Recommended)

Run the agent without arguments to enter interactive mode:

```bash
python agent.py
```

You'll be prompted to:
1. **Choose mode**: Image (description) or Video (actual video)
2. **Enter personality name**: Any public figure
3. **Optional context**: Add custom actions or settings

### Command-Line Mode

Provide the personality name as a command-line argument (defaults to image mode):

```bash
python agent.py "Albert Einstein"
```

### Example Sessions

#### Video Generation (NEW!)

```bash
$ python agent.py

============================================================
🤖 AI Media Generation Agent - Images & Videos
============================================================

What would you like to generate?
1. Image (description)
2. Video (actual video - FREE via Hugging Face)

Enter 1 or 2 (default: 2): 2

🎬 Video Generation Mode

Enter the name of a public personality:
> Marie Curie

Optional: Add custom context (e.g., 'walking in a park', 'waving', etc.)
Press Enter to skip:
> working in her laboratory

🎬 Generating video for: Marie Curie
📝 Base Prompt: Marie Curie working in her laboratory
⚙️  Model: ali-vilab/text-to-video-ms-1.7b
⏱️  Duration: 4s @ 8 FPS

⏳ Enhancing prompt with Gemini...
✨ Enhanced Prompt: Marie Curie in her laboratory, carefully examining test tubes with glowing radium samples, scientific equipment visible, early 1900s setting, cinematic lighting

⏳ Generating video with Hugging Face (this may take 1-2 minutes)...
💡 Note: Using free Hugging Face inference - first request may be slower as model loads

✅ Video generated successfully!
💾 Saved to: generated_videos/Marie_Curie_20240315_143022.mp4
📊 Duration: 4s @ 8 FPS

============================================================
📊 Generation Summary
============================================================
Personality: Marie Curie
Prompt Used: Marie Curie in her laboratory...
Video File: generated_videos/Marie_Curie_20240315_143022.mp4
Duration: 4s @ 8 FPS
============================================================
```

#### Image Description Generation

```bash
$ python agent.py

============================================================
🤖 AI Media Generation Agent - Images & Videos
============================================================

What would you like to generate?
1. Image (description)
2. Video (actual video - FREE via Hugging Face)

Enter 1 or 2 (default: 2): 1

🎨 Image Generation Mode

Enter the name of a public personality:
> Leonardo da Vinci

Optional: Add custom context (e.g., 'wearing a suit', 'smiling', etc.)
Press Enter to skip:
> painting the Mona Lisa

🎨 Generating image for: Leonardo da Vinci
📝 Prompt: A professional portrait of Leonardo da Vinci, painting the Mona Lisa
⚙️  Model: Gemini (Imagen)
📐 Size: 1024x1024

⏳ Please wait, generating image...

📋 Enhanced description: Leonardo da Vinci in his Renaissance workshop...

✅ Description generated successfully!
💾 Saved to: generated_images/Leonardo_da_Vinci_20240315_143022.txt
```

### Python API

Use the agent programmatically in your Python code:

```python
from agent import PersonalityImageAgent

# Create an agent instance
agent = PersonalityImageAgent()

# Generate a VIDEO (NEW!)
result = agent.generate_video("Marie Curie", custom_context="working in laboratory")

if result['success']:
    print(f"Video saved to: {result['file_path']}")
    print(f"Duration: {result['duration']}s @ {result['fps']} FPS")
else:
    print(f"Error: {result['error']}")

# Generate an image description
result = agent.generate_image("Leonardo da Vinci")

print(result['description'])
print(f"Saved to: {result['file_path']}")

# Generate with custom context
result = agent.generate_video(
    "Frida Kahlo",
    custom_context="painting a self-portrait with vibrant colors"
)

# Generate multiple videos
personalities = ["Isaac Newton", "Ada Lovelace", "Stephen Hawking"]
results = agent.generate_multiple_videos(personalities)

# Generate multiple image descriptions
results = agent.generate_multiple_images(personalities)
```

## Configuration

Configure the agent by editing your `.env` file:

### Required Settings

| Variable | Description | Default | Options |
|----------|-------------|---------|---------|
| `GEMINI_API_KEY` | Your Google Gemini API key | Required | Get from AI Studio |

### Optional Settings

| Variable | Description | Default | Options |
|----------|-------------|---------|---------|
| `HUGGINGFACE_API_KEY` | Hugging Face token (optional) | None | Get from HF Settings |

### Image Settings

| Variable | Description | Default | Options |
|----------|-------------|---------|---------|
| `IMAGE_MODEL` | Model identifier | `imagen-3.0-generate-001` | Any Gemini model |
| `IMAGE_SIZE` | Target image size | `1024x1024` | `256x256`, `512x512`, `1024x1024` |
| `NUM_IMAGES` | Number of variations | `1` | Any integer |
| `OUTPUT_DIR` | Output directory | `generated_images` | Any valid path |

### Video Settings (NEW!)

| Variable | Description | Default | Options |
|----------|-------------|---------|---------|
| `VIDEO_MODEL` | Hugging Face model | `ali-vilab/text-to-video-ms-1.7b` | See models below |
| `VIDEO_DURATION` | Duration in seconds | `4` | `2-8` recommended |
| `VIDEO_FPS` | Frames per second | `8` | `8-16` recommended |
| `VIDEO_NUM_INFERENCE_STEPS` | Quality vs speed | `25` | `15-50` |
| `VIDEO_OUTPUT_DIR` | Video output directory | `generated_videos` | Any valid path |

### Available Video Models (Free)

- `ali-vilab/text-to-video-ms-1.7b` - Recommended, good balance
- `damo-vilab/text-to-video-ms-1.7b` - Alternative, similar quality
- `cerspense/zeroscope_v2_576w` - Higher quality, slower

## Output

### Video Files (NEW!)

Generated videos are saved in the `generated_videos/` directory:

```
<personality_name>_<timestamp>.mp4
```

Example: `Marie_Curie_20240315_143022.mp4`

- Format: MP4 video file
- Duration: Configurable (default 4 seconds)
- FPS: Configurable (default 8 FPS)
- Ready to view with any video player

### Image Description Files

Generated descriptions are saved in the `generated_images/` directory:

```
<personality_name>_<timestamp>.txt
```

Example: `Albert_Einstein_20240315_143022.txt`

Each file contains:
- Personality name
- Original prompt
- Enhanced description generated by Gemini
- Notes about actual image generation options

## Code Structure

```
AI-generated-images/
├── agent.py              # Main agent implementation (images + videos)
├── config.py             # Configuration management
├── requirements.txt      # Python dependencies
├── .env.example          # Example environment variables
├── .gitignore           # Git ignore rules
├── README.md            # This file
├── generated_images/    # Generated descriptions (created automatically)
└── generated_videos/    # Generated videos (created automatically)
```

## API Response

### Video Generation Response

```python
{
    'success': True,
    'personality': 'Marie Curie',
    'prompt': 'Marie Curie working in laboratory',
    'enhanced_prompt': 'Marie Curie in her laboratory, carefully examining...',
    'file_path': 'generated_videos/Marie_Curie_20240315_143022.mp4',
    'filename': 'Marie_Curie_20240315_143022.mp4',
    'duration': 4,
    'fps': 8
}
```

### Image Generation Response

```python
{
    'success': True,
    'personality': 'Albert Einstein',
    'prompt': 'A professional portrait of Albert Einstein...',
    'description': 'Detailed visual description...',
    'file_path': 'generated_images/Albert_Einstein_20240315_143022.txt',
    'filename': 'Albert_Einstein_20240315_143022.txt',
    'note': 'Instructions for actual image generation'
}
```

## Converting Descriptions to Images

### Option 1: Google Cloud Vertex AI + Imagen (Recommended for Google)

```python
# Requires Google Cloud project and Vertex AI setup
from google.cloud import aiplatform
# ... use the description with Imagen API
```

### Option 2: OpenAI DALL-E

Use the generated descriptions with DALL-E:

```python
from openai import OpenAI
client = OpenAI(api_key="your-key")

# Read the description from the generated file
with open('generated_images/Marie_Curie_20240315_143022.txt') as f:
    description = f.read()

# Generate image
response = client.images.generate(
    model="dall-e-3",
    prompt=description,
    size="1024x1024"
)
```

### Option 3: Stability AI

```python
import stability_sdk
# Use the description with Stable Diffusion
```

## Costs

### 100% FREE Options 🎉

- **✅ Video Generation**: Completely FREE using Hugging Face inference API
  - No credit card required
  - Rate limits apply on free tier (can be lifted with free HF account)
  - Uses open-source models

- **✅ Prompt Enhancement**: FREE using Gemini API (generous free tier)
  - 1,500 requests per day on free tier
  - More than enough for personal projects

### Paid Options (for Image Generation)

If you want actual images instead of videos, costs depend on service:

- **Google Imagen (Vertex AI)**: Pay-per-use pricing (~$0.02-0.05 per image)
- **OpenAI DALL-E 3**: ~$0.04 per image
- **Stability AI**: Various pricing tiers

**Recommendation**: Use the FREE video generation feature! It's completely free and generates actual videos, not just descriptions.

## Limitations

### Video Generation
- First video generation may take 1-3 minutes (model loading time on free tier)
- Subsequent generations are faster (30 seconds - 2 minutes)
- Video quality is moderate (good for testing, demos, social media)
- Duration limited to 2-8 seconds for reasonable generation times
- Free tier has rate limits (upgradable with free HF account)

### Image Generation
- Gemini API generates descriptions only (not actual images)
- For actual images, need to integrate with paid services (Vertex AI, DALL-E, etc.)
- Or use the FREE video generation instead!

### General
- Requires a Gemini API key (free to get)
- Rate limits apply based on API tier (generous free tier)

## Troubleshooting

### Video Generation Issues

#### "Model is loading" error
- **Cause**: Hugging Face free tier models go to sleep when not used
- **Solution**: Wait 20-60 seconds and try again. The agent will retry automatically.
- **Tip**: First generation of the day is always slower

#### Video generation takes too long
- **Reduce** `VIDEO_DURATION` (try 2-3 seconds)
- **Reduce** `VIDEO_NUM_INFERENCE_STEPS` (try 15-20)
- **Reduce** `VIDEO_FPS` (try 6-8)

#### Rate limit errors
- **Get a free Hugging Face account** and add your token to `.env`
- **Wait a few minutes** between generations on free tier
- **Try a different model** (switch to `damo-vilab/text-to-video-ms-1.7b`)

#### Video quality is poor
- **Increase** `VIDEO_NUM_INFERENCE_STEPS` (try 35-50)
- **Try different model**: `cerspense/zeroscope_v2_576w` (higher quality, slower)
- **Be more descriptive** in custom context

### General Issues

#### "GEMINI_API_KEY is not set"
Make sure you've created a `.env` file from `.env.example` and added your API key.

#### "Invalid API key"
Verify your API key is correct at https://aistudio.google.com/app/apikey

#### Module not found errors
Install all dependencies:
```bash
pip install -r requirements.txt
```

### Want actual images?

You have several options:
1. **Use video generation instead** (FREE and generates actual media!)
2. Set up Google Cloud + Vertex AI for Imagen access
3. Use the OpenAI version of this agent (uses DALL-E)
4. Copy the generated descriptions and use them with any image generation service

## Why This Approach?

### The Power of Free Video Generation 🎬

This agent now generates **actual videos for FREE** instead of just image descriptions! Here's why this is better:

**Video Generation Advantages:**
- ✅ **Real output**: Get actual MP4 videos, not just descriptions
- ✅ **100% free**: No API costs thanks to Hugging Face's open-source models
- ✅ **More engaging**: Videos are more dynamic than static images
- ✅ **Easy to use**: No complex setup or paid accounts required

**Gemini Enhancement:**
- Uses Gemini's free API to create better video prompts
- Adds context, style, and cinematic elements automatically
- Improves video quality without extra cost

**Why Not Just Images?**
- Image generation (DALL-E, Imagen) costs $0.02-0.04 per image
- Or requires complex Vertex AI setup
- Videos are FREE and more impressive!

## Alternative Options

If you specifically need static images:

1. **Extract frames from videos** - Use the generated videos and extract the best frame
2. **Add Vertex AI integration** - For Google Imagen access (requires GCP setup)
3. **Switch to OpenAI DALL-E** - Costs ~$0.04 per image
4. **Use Stability AI** - Various pricing tiers

But honestly, **the free video generation is the best option**! Try it first.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Powered by [Google's Gemini API](https://ai.google.dev/)
- Built with Python and the Google Generative AI library

## Support

For issues, questions, or suggestions, please open an issue in the GitHub repository.
