import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class for the AI Image Generation Agent."""

    # Google Gemini API Configuration
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

    # Hugging Face API Configuration (Optional - for video generation)
    HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY', None)

    # Image Generation Settings
    IMAGE_MODEL = os.getenv('IMAGE_MODEL', 'imagen-3.0-generate-001')  # Imagen model
    IMAGE_SIZE = os.getenv('IMAGE_SIZE', '1024x1024')  # 256x256, 512x512, 1024x1024, etc.
    NUM_IMAGES = int(os.getenv('NUM_IMAGES', '1'))  # Number of images to generate

    # Video Generation Settings
    VIDEO_MODEL = os.getenv('VIDEO_MODEL', 'ali-vilab/text-to-video-ms-1.7b')  # HuggingFace model
    VIDEO_DURATION = int(os.getenv('VIDEO_DURATION', '4'))  # Duration in seconds
    VIDEO_FPS = int(os.getenv('VIDEO_FPS', '8'))  # Frames per second
    VIDEO_NUM_INFERENCE_STEPS = int(os.getenv('VIDEO_NUM_INFERENCE_STEPS', '25'))  # Quality vs speed

    # Output Settings
    OUTPUT_DIR = os.getenv('OUTPUT_DIR', 'generated_images')
    VIDEO_OUTPUT_DIR = os.getenv('VIDEO_OUTPUT_DIR', 'generated_videos')

    @classmethod
    def validate(cls):
        """Validate required configuration."""
        if not cls.GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY is not set. Please set it in your .env file or environment variables."
            )

        return True
