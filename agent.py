#!/usr/bin/env python3
"""
AI Image Generation Agent
Generates AI images based on public personality names using Google's Gemini API.
"""

import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional
import base64

import google.generativeai as genai
from PIL import Image
import io

from config import Config


class PersonalityImageAgent:
    """Agent for generating AI images of public personalities."""

    def __init__(self):
        """Initialize the agent with configuration."""
        Config.validate()
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
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
        Generate an AI image for the given personality using Gemini.

        Args:
            personality_name: Name of the public personality
            custom_context: Optional custom context for the image

        Returns:
            Dictionary with image information (path, prompt)
        """
        try:
            # Generate the prompt
            prompt = self.generate_prompt(personality_name, custom_context)

            print(f"\n🎨 Generating image for: {personality_name}")
            print(f"📝 Prompt: {prompt}")
            print(f"⚙️  Model: Gemini (Imagen)")
            print(f"📐 Size: {Config.IMAGE_SIZE}")
            print("\n⏳ Please wait, generating image...")

            # Use Gemini to generate the image
            # Note: As of now, Gemini's image generation is done through Imagen
            # We'll use the generative model to create an artistic interpretation
            response = self.model.generate_content([
                f"Create a detailed description for generating an image: {prompt}. "
                "Provide only the visual description, no explanations."
            ])

            description = response.text.strip()
            print(f"\n📋 Enhanced description: {description}")

            # For actual image generation, we would use Google's Imagen API
            # Since direct Imagen API access requires vertex AI, we'll create a placeholder
            # that demonstrates the workflow

            # Create a simple placeholder image with the personality name
            # In production, this would call Imagen API
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_name = personality_name.replace(" ", "_").replace("/", "_")
            filename = f"{safe_name}_{timestamp}.txt"
            filepath = self.output_dir / filename

            # Save the generated description
            with open(filepath, 'w') as f:
                f.write(f"Personality: {personality_name}\n")
                f.write(f"Prompt: {prompt}\n")
                f.write(f"Enhanced Description:\n{description}\n")
                f.write(f"\nNote: To generate actual images, you need to:")
                f.write(f"\n1. Enable Vertex AI in Google Cloud")
                f.write(f"\n2. Use the Imagen API directly")
                f.write(f"\n3. Or use a service like Stability AI, Replicate, or OpenAI DALL-E")

            result = {
                'success': True,
                'personality': personality_name,
                'prompt': prompt,
                'description': description,
                'file_path': str(filepath),
                'filename': filename,
                'note': 'Gemini generated the description. For actual image generation, Vertex AI/Imagen API is required.'
            }

            print(f"\n✅ Description generated successfully!")
            print(f"💾 Saved to: {filepath}")
            print(f"\n⚠️  Note: Gemini API doesn't directly generate images yet.")
            print(f"    The enhanced description has been saved.")
            print(f"    To generate actual images, consider using:")
            print(f"    - Google Cloud Vertex AI + Imagen")
            print(f"    - OpenAI DALL-E API")
            print(f"    - Stability AI")
            print(f"    - Replicate")

            return result

        except Exception as e:
            error_result = {
                'success': False,
                'personality': personality_name,
                'error': str(e)
            }
            print(f"\n❌ Error generating content: {e}")
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
    print("🤖 AI Image Generation Agent - Gemini Edition")
    print("=" * 60)

    # Check if personality name was provided as argument
    if len(sys.argv) > 1:
        personality_name = " ".join(sys.argv[1:])
        custom_context = None  # No custom context in CLI mode
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
        print(f"Description File: {result['file_path']}")
        if 'note' in result:
            print(f"\nNote: {result['note']}")
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
