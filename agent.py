#!/usr/bin/env python3
"""
AI Image Generation Agent
Generates AI images based on public personality names.
"""

import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import requests
from openai import OpenAI

from config import Config


class PersonalityImageAgent:
    """Agent for generating AI images of public personalities."""

    def __init__(self):
        """Initialize the agent with configuration."""
        Config.validate()
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.output_dir = Path(Config.OUTPUT_DIR)
        self.output_dir.mkdir(exist_ok=True)

    def generate_prompt(self, personality_name: str, custom_context: Optional[str] = None) -> str:
        """
        Generate a detailed prompt for the personality.

        Args:
            personality_name: Name of the public personality
            custom_context: Optional custom context to add to the prompt

        Returns:
            A detailed prompt string for image generation
        """
        base_prompt = f"A professional portrait of {personality_name}"

        if custom_context:
            prompt = f"{base_prompt}, {custom_context}"
        else:
            prompt = f"{base_prompt}, realistic style, high quality, detailed features"

        return prompt

    def generate_image(self, personality_name: str, custom_context: Optional[str] = None) -> dict:
        """
        Generate an AI image for the given personality.

        Args:
            personality_name: Name of the public personality
            custom_context: Optional custom context for the image

        Returns:
            Dictionary with image information (path, url, prompt)
        """
        try:
            # Generate the prompt
            prompt = self.generate_prompt(personality_name, custom_context)

            print(f"\n🎨 Generating image for: {personality_name}")
            print(f"📝 Prompt: {prompt}")
            print(f"⚙️  Model: {Config.IMAGE_MODEL}")
            print(f"📐 Size: {Config.IMAGE_SIZE}")
            print(f"✨ Quality: {Config.IMAGE_QUALITY}")
            print("\n⏳ Please wait, generating image...")

            # Call OpenAI API to generate image
            response = self.client.images.generate(
                model=Config.IMAGE_MODEL,
                prompt=prompt,
                size=Config.IMAGE_SIZE,
                quality=Config.IMAGE_QUALITY,
                style=Config.IMAGE_STYLE if Config.IMAGE_MODEL == 'dall-e-3' else None,
                n=1
            )

            # Get the image URL
            image_url = response.data[0].url

            # Download and save the image
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_name = personality_name.replace(" ", "_").replace("/", "_")
            filename = f"{safe_name}_{timestamp}.png"
            filepath = self.output_dir / filename

            # Download the image
            image_response = requests.get(image_url)
            image_response.raise_for_status()

            with open(filepath, 'wb') as f:
                f.write(image_response.content)

            result = {
                'success': True,
                'personality': personality_name,
                'prompt': prompt,
                'image_path': str(filepath),
                'image_url': image_url,
                'filename': filename
            }

            print(f"\n✅ Image generated successfully!")
            print(f"💾 Saved to: {filepath}")

            return result

        except Exception as e:
            error_result = {
                'success': False,
                'personality': personality_name,
                'error': str(e)
            }
            print(f"\n❌ Error generating image: {e}")
            return error_result

    def generate_multiple_images(self, personalities: list, custom_context: Optional[str] = None) -> list:
        """
        Generate images for multiple personalities.

        Args:
            personalities: List of personality names
            custom_context: Optional custom context for all images

        Returns:
            List of result dictionaries
        """
        results = []
        for personality in personalities:
            result = self.generate_image(personality, custom_context)
            results.append(result)
            print("\n" + "=" * 60 + "\n")

        return results


def main():
    """Main function to run the agent from command line."""
    print("=" * 60)
    print("🤖 AI Image Generation Agent - Personality Edition")
    print("=" * 60)

    # Check if personality name was provided as argument
    if len(sys.argv) > 1:
        personality_name = " ".join(sys.argv[1:])
    else:
        # Interactive mode
        print("\nEnter the name of a public personality to generate an image:")
        personality_name = input("> ").strip()

        if not personality_name:
            print("❌ No personality name provided. Exiting.")
            sys.exit(1)

    # Optional: Ask for custom context
    print("\nOptional: Add custom context (e.g., 'wearing a suit', 'smiling', etc.)")
    print("Press Enter to skip:")
    custom_context = input("> ").strip()
    custom_context = custom_context if custom_context else None

    # Create agent and generate image
    agent = PersonalityImageAgent()
    result = agent.generate_image(personality_name, custom_context)

    # Display results
    if result['success']:
        print("\n" + "=" * 60)
        print("📊 Generation Summary")
        print("=" * 60)
        print(f"Personality: {result['personality']}")
        print(f"Prompt Used: {result['prompt']}")
        print(f"Image Path: {result['image_path']}")
        print(f"Image URL: {result['image_url']}")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ Generation Failed")
        print("=" * 60)
        print(f"Error: {result['error']}")
        print("=" * 60)
        sys.exit(1)


if __name__ == "__main__":
    main()
