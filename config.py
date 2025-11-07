import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class for the AI Image Generation Agent."""

    # Google Gemini API Configuration
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

    # Image Generation Settings
    IMAGE_MODEL = os.getenv('IMAGE_MODEL', 'imagen-3.0-generate-001')  # Imagen model
    IMAGE_SIZE = os.getenv('IMAGE_SIZE', '1024x1024')  # 256x256, 512x512, 1024x1024, etc.
    NUM_IMAGES = int(os.getenv('NUM_IMAGES', '1'))  # Number of images to generate

    # Output Settings
    OUTPUT_DIR = os.getenv('OUTPUT_DIR', 'generated_images')

    @classmethod
    def validate(cls):
        """Validate required configuration."""
        if not cls.GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY is not set. Please set it in your .env file or environment variables."
            )

        return True
