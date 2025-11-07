import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class for the AI Image Generation Agent."""

    # OpenAI API Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

    # Image Generation Settings
    IMAGE_MODEL = os.getenv('IMAGE_MODEL', 'dall-e-3')  # dall-e-2 or dall-e-3
    IMAGE_SIZE = os.getenv('IMAGE_SIZE', '1024x1024')  # dall-e-3: 1024x1024, 1792x1024, 1024x1792
    IMAGE_QUALITY = os.getenv('IMAGE_QUALITY', 'standard')  # standard or hd (dall-e-3 only)
    IMAGE_STYLE = os.getenv('IMAGE_STYLE', 'vivid')  # vivid or natural (dall-e-3 only)

    # Output Settings
    OUTPUT_DIR = os.getenv('OUTPUT_DIR', 'generated_images')

    @classmethod
    def validate(cls):
        """Validate required configuration."""
        if not cls.OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY is not set. Please set it in your .env file or environment variables."
            )

        return True
