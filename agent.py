#!/usr/bin/env python3
"""
AI Image Generation Agent
Generates AI images based on public personality names using Google's Gemini API.
"""

import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Literal
import base64
import time

import google.generativeai as genai
from PIL import Image
import io
import requests

from config import Config


class PersonalityImageAgent:
    """Agent for generating AI images and videos of public personalities."""

    def __init__(self):
        """Initialize the agent with configuration."""
        Config.validate()
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.output_dir = Path(Config.OUTPUT_DIR)
        self.output_dir.mkdir(exist_ok=True)
        self.video_output_dir = Path(Config.VIDEO_OUTPUT_DIR)
        self.video_output_dir.mkdir(exist_ok=True)

        # Hugging Face API endpoint
        self.hf_api_url = f"https://api-inference.huggingface.co/models/{Config.VIDEO_MODEL}"
        self.hf_headers = {}
        if Config.HUGGINGFACE_API_KEY:
            self.hf_headers["Authorization"] = f"Bearer {Config.HUGGINGFACE_API_KEY}"

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

    def generate_video_prompt(self, personality_name: str, custom_context: Optional[str] = None) -> str:
        """
        Generate a detailed prompt for video generation.

        Args:
            personality_name: Name of the public personality
            custom_context: Optional custom context to add to the prompt

        Returns:
            A detailed prompt string for video generation
        """
        if custom_context:
            prompt = f"{personality_name} {custom_context}"
        else:
            prompt = f"{personality_name} portrait, cinematic, high quality, realistic"

        return prompt

    def generate_video(self, personality_name: str, custom_context: Optional[str] = None) -> dict:
        """
        Generate an AI video for the given personality using Hugging Face.

        Args:
            personality_name: Name of the public personality
            custom_context: Optional custom context for the video

        Returns:
            Dictionary with video information (path, prompt)
        """
        try:
            # Generate the prompt using Gemini for enhancement
            base_prompt = self.generate_video_prompt(personality_name, custom_context)

            print(f"\n🎬 Generating video for: {personality_name}")
            print(f"📝 Base Prompt: {base_prompt}")
            print(f"⚙️  Model: {Config.VIDEO_MODEL}")
            print(f"⏱️  Duration: {Config.VIDEO_DURATION}s @ {Config.VIDEO_FPS} FPS")
            print("\n⏳ Enhancing prompt with Gemini...")

            # Use Gemini to enhance the video prompt
            response = self.model.generate_content([
                f"Create a detailed video description prompt for: {base_prompt}. "
                "Focus on movement, actions, expressions, and cinematic elements. "
                "Keep it concise (1-2 sentences) but descriptive. "
                "Provide only the video prompt, no explanations."
            ])

            enhanced_prompt = response.text.strip()
            print(f"✨ Enhanced Prompt: {enhanced_prompt}")
            print("\n⏳ Generating video with Hugging Face (this may take 1-2 minutes)...")
            print("💡 Note: Using free Hugging Face inference - first request may be slower as model loads")

            # Prepare the request payload
            payload = {
                "inputs": enhanced_prompt,
                "parameters": {
                    "num_frames": Config.VIDEO_DURATION * Config.VIDEO_FPS,
                    "num_inference_steps": Config.VIDEO_NUM_INFERENCE_STEPS
                }
            }

            # Make request to Hugging Face Inference API
            max_retries = 3
            retry_delay = 20  # seconds

            for attempt in range(max_retries):
                response = requests.post(
                    self.hf_api_url,
                    headers=self.hf_headers,
                    json=payload,
                    timeout=180  # 3 minutes timeout
                )

                if response.status_code == 503:
                    # Model is loading
                    print(f"⏳ Model is loading... (Attempt {attempt + 1}/{max_retries})")
                    if attempt < max_retries - 1:
                        print(f"   Waiting {retry_delay} seconds before retry...")
                        time.sleep(retry_delay)
                        continue
                    else:
                        return {
                            'success': False,
                            'personality': personality_name,
                            'error': 'Model is still loading. Please try again in a few minutes.',
                            'note': 'Hugging Face free tier models need time to load. Try again shortly.'
                        }

                elif response.status_code == 200:
                    # Success - save the video
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    safe_name = personality_name.replace(" ", "_").replace("/", "_")
                    filename = f"{safe_name}_{timestamp}.mp4"
                    filepath = self.video_output_dir / filename

                    # Save video file
                    with open(filepath, 'wb') as f:
                        f.write(response.content)

                    result = {
                        'success': True,
                        'personality': personality_name,
                        'prompt': base_prompt,
                        'enhanced_prompt': enhanced_prompt,
                        'file_path': str(filepath),
                        'filename': filename,
                        'duration': Config.VIDEO_DURATION,
                        'fps': Config.VIDEO_FPS
                    }

                    print(f"\n✅ Video generated successfully!")
                    print(f"💾 Saved to: {filepath}")
                    print(f"📊 Duration: {Config.VIDEO_DURATION}s @ {Config.VIDEO_FPS} FPS")

                    return result

                else:
                    # Error
                    error_msg = response.text
                    try:
                        error_json = response.json()
                        error_msg = error_json.get('error', error_msg)
                    except:
                        pass

                    return {
                        'success': False,
                        'personality': personality_name,
                        'error': f"API Error ({response.status_code}): {error_msg}",
                        'note': 'Check your Hugging Face API key or try a different model.'
                    }

        except requests.exceptions.Timeout:
            return {
                'success': False,
                'personality': personality_name,
                'error': 'Request timed out. Video generation can take several minutes.',
                'note': 'Try again with a shorter duration or fewer inference steps.'
            }
        except Exception as e:
            error_result = {
                'success': False,
                'personality': personality_name,
                'error': str(e)
            }
            print(f"\n❌ Error generating video: {e}")
            return error_result

    def generate_multiple_videos(self, personalities: list, custom_context: Optional[str] = None) -> list:
        """
        Generate videos for multiple personalities.

        Args:
            personalities: List of personality names
            custom_context: Optional custom context for all videos

        Returns:
            List of result dictionaries
        """
        results = []
        for personality in personalities:
            result = self.generate_video(personality, custom_context)
            results.append(result)
            print("\n" + "=" * 60 + "\n")

        return results


def main():
    """Main function to run the agent from command line."""
    print("=" * 60)
    print("🤖 AI Media Generation Agent - Images & Videos")
    print("=" * 60)

    # Check if personality name was provided as argument
    if len(sys.argv) > 1:
        # CLI mode with arguments
        personality_name = " ".join(sys.argv[1:])
        custom_context = None
        generation_mode = 'image'  # Default to image in CLI mode
    else:
        # Interactive mode
        print("\nWhat would you like to generate?")
        print("1. Image (description)")
        print("2. Video (actual video - FREE via Hugging Face)")
        mode_choice = input("\nEnter 1 or 2 (default: 2): ").strip()

        if mode_choice == '1':
            generation_mode = 'image'
        else:
            generation_mode = 'video'

        print(f"\n{'🎨 Image' if generation_mode == 'image' else '🎬 Video'} Generation Mode")
        print("\nEnter the name of a public personality:")
        personality_name = input("> ").strip()

        if not personality_name:
            print("❌ No personality name provided. Exiting.")
            sys.exit(1)

        # Optional: Ask for custom context
        if generation_mode == 'image':
            print("\nOptional: Add custom context (e.g., 'wearing a suit', 'smiling', etc.)")
        else:
            print("\nOptional: Add custom context (e.g., 'walking in a park', 'waving', etc.)")
        print("Press Enter to skip:")
        custom_context = input("> ").strip()
        custom_context = custom_context if custom_context else None

    # Create agent and generate
    agent = PersonalityImageAgent()

    if generation_mode == 'image':
        result = agent.generate_image(personality_name, custom_context)
    else:
        result = agent.generate_video(personality_name, custom_context)

    # Display results
    if result['success']:
        print("\n" + "=" * 60)
        print("📊 Generation Summary")
        print("=" * 60)
        print(f"Personality: {result['personality']}")
        print(f"Prompt Used: {result.get('prompt', result.get('enhanced_prompt', 'N/A'))}")

        if generation_mode == 'image':
            print(f"Description File: {result['file_path']}")
            if 'note' in result:
                print(f"\nNote: {result['note']}")
        else:
            print(f"Video File: {result['file_path']}")
            print(f"Duration: {result['duration']}s @ {result['fps']} FPS")

        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ Generation Failed")
        print("=" * 60)
        print(f"Error: {result['error']}")
        if 'note' in result:
            print(f"Note: {result['note']}")
        print("=" * 60)
        sys.exit(1)


if __name__ == "__main__":
    main()
