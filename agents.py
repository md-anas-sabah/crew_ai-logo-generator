from crewai import Agent
from textwrap import dedent
from langchain_openai import OpenAI, ChatOpenAI
from langchain.tools import BaseTool
from typing import Any, Type
from pydantic import BaseModel, Field
import requests
import os
import re
from datetime import datetime
import json
import uuid
import fal_client as fal
from decouple import config
from claude_refinement import ClaudeRefinementService


class LogoGeneratorArgs(BaseModel):
    prompt: str = Field(description="The prompt for logo generation")
    logo_style: str = Field(default=None, description="Logo style: WordMark, LetterMark, Pictorial, Abstract, Combination, Emblem")
    company_name: str = Field(default=None, description="Company name for the logo")
    
class SVGLogoGeneratorArgs(BaseModel):
    prompt: str = Field(description="The prompt for SVG logo generation")
    logo_style: str = Field(default=None, description="Logo style: WordMark, LetterMark, Pictorial, Abstract, Combination, Emblem")
    company_name: str = Field(default=None, description="Company name for the logo")

class ImageGeneratorArgs(BaseModel):
    prompt: str = Field(description="The prompt for image generation")

class LogoGeneratorTool(BaseTool):
    name: str = "generate_logo"
    description: str = "Generate a professional logo using Ideogram V2A. Use with: prompt (description of the logo design), logo_style (WordMark/LetterMark/Pictorial/Abstract/Combination/Emblem), company_name (company name)."
    args_schema: Type[BaseModel] = LogoGeneratorArgs
    output_folder: str = None
    claude_service: ClaudeRefinementService = None

    def __init__(self, output_folder=None):
        super().__init__()
        self.output_folder = output_folder
        self.claude_service = ClaudeRefinementService()

    def _run(self, prompt: str, logo_style: str = None, company_name: str = None) -> str:
        try:
            # Handle case where CrewAI passes everything as a JSON string in prompt
            import json
            if logo_style is None or company_name is None:
                try:
                    # Try to parse prompt as JSON
                    data = json.loads(prompt)
                    if isinstance(data, dict):
                        prompt = data.get('prompt', prompt)
                        logo_style = data.get('logo_style', logo_style)
                        company_name = data.get('company_name', company_name)
                except (json.JSONDecodeError, TypeError):
                    # If not JSON, try to extract from prompt string
                    if 'Marqait' in prompt and logo_style is None:
                        company_name = 'Marqait'
                        logo_style = 'Emblem'  # Default based on user selection
            
            # Create logo-specific context for Claude refinement
            logo_context = f"Logo style: {logo_style}, Company: {company_name}, Professional brand identity"
            
            # Refine the prompt using Claude specifically for logo design
            print(f"Original logo prompt: {prompt}")
            refined_prompt = self.claude_service.refine_logo_prompt(prompt, logo_context, logo_style)
            print(f"Claude-refined logo prompt: {refined_prompt}")
            
            # Ensure FAL_KEY is set in environment
            os.environ['FAL_KEY'] = config('FAL_KEY')
            
            # Submit request to Ideogram V2A with logo-optimized settings
            result = fal.run(
                "fal-ai/ideogram/v2a",
                arguments={
                    "prompt": refined_prompt,
                    "aspect_ratio": "1:1",  # Square format optimal for logos
                    "style": "design",  # Design style for clean, professional logos
                    "resolution": "1024x1024"  # High resolution for professional use
                }
            )
            
            image_url = result['images'][0]['url']
            
            # Download and save the logo locally
            image_response = requests.get(image_url)
            if image_response.status_code == 200:
                # Create unique filename for the logo
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                unique_id = str(uuid.uuid4())[:8]
                safe_company_name = re.sub(r'[^\w\s-]', '', company_name.lower().replace(' ', '_'))[:20]
                filename = f"logo_{safe_company_name}_{logo_style.lower()}_{timestamp}_{unique_id}.png"
                
                # Use the specific output folder if provided
                if self.output_folder:
                    os.makedirs(self.output_folder, exist_ok=True)
                    local_path = os.path.join(self.output_folder, filename)
                else:
                    # Fallback to default logos folder
                    current_dir = os.getcwd()
                    logos_dir = os.path.join(current_dir, "generated_logos")
                    os.makedirs(logos_dir, exist_ok=True)
                    local_path = os.path.join(logos_dir, filename)
                
                with open(local_path, 'wb') as f:
                    f.write(image_response.content)
                
                return json.dumps({
                    "image_url": image_url,
                    "local_path": local_path,
                    "filename": filename,
                    "company_name": company_name,
                    "logo_style": logo_style,
                    "original_prompt": prompt,
                    "refined_prompt": refined_prompt,
                    "format": "PNG",
                    "resolution": "1024x1024",
                    "seed": result.get('seed'),
                    "logo_type": "professional_brand_logo"
                })
            else:
                return json.dumps({
                    "image_url": image_url,
                    "local_path": "Failed to download",
                    "filename": "Failed to download",
                    "company_name": company_name,
                    "logo_style": logo_style,
                    "prompt": prompt,
                    "error": f"Failed to download logo: {image_response.status_code}"
                })
                
        except Exception as e:
            return json.dumps({
                "image_url": "Error",
                "local_path": "Error",
                "filename": "Error",
                "company_name": company_name,
                "logo_style": logo_style,
                "prompt": prompt,
                "error": f"Error generating logo: {str(e)}"
            })

class SVGLogoGeneratorTool(BaseTool):
    name: str = "generate_svg_logo"
    description: str = "Generate a professional SVG vector logo using specialized logo generation with scalable vector output."
    args_schema: Type[BaseModel] = SVGLogoGeneratorArgs
    output_folder: str = None
    claude_service: ClaudeRefinementService = None

    def __init__(self, output_folder=None):
        super().__init__()
        self.output_folder = output_folder
        self.claude_service = ClaudeRefinementService()

    def _run(self, prompt: str, logo_style: str = None, company_name: str = None) -> str:
        try:
            # Handle case where CrewAI passes everything as a JSON string in prompt
            import json
            if logo_style is None or company_name is None:
                try:
                    # Try to parse prompt as JSON
                    data = json.loads(prompt)
                    if isinstance(data, dict):
                        prompt = data.get('prompt', prompt)
                        logo_style = data.get('logo_style', logo_style)
                        company_name = data.get('company_name', company_name)
                except (json.JSONDecodeError, TypeError):
                    # If not JSON, try to extract from prompt string
                    if 'Marqait' in prompt and logo_style is None:
                        company_name = 'Marqait'
                        logo_style = 'Emblem'  # Default based on user selection
            
            # Create SVG-specific context for Claude refinement
            logo_context = f"SVG vector logo, Logo style: {logo_style}, Company: {company_name}, Scalable vector graphics, Clean lines, Professional brand identity"
            
            # Refine the prompt using Claude specifically for SVG logo design
            print(f"Original SVG logo prompt: {prompt}")
            refined_prompt = self.claude_service.refine_logo_prompt(prompt, logo_context, logo_style, format="SVG")
            print(f"Claude-refined SVG logo prompt: {refined_prompt}")
            
            # Ensure FAL_KEY is set in environment
            os.environ['FAL_KEY'] = config('FAL_KEY')
            
            # Submit request to Ideogram V2A with SVG-optimized settings
            result = fal.run(
                "fal-ai/ideogram/v2a",
                arguments={
                    "prompt": refined_prompt,
                    "aspect_ratio": "1:1",
                    "style": "design",
                    "resolution": "1024x1024"
                }
            )
            
            image_url = result['images'][0]['url']
            
            # Download and save the SVG logo locally
            image_response = requests.get(image_url)
            if image_response.status_code == 200:
                # Create unique filenames for both PNG and SVG
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                unique_id = str(uuid.uuid4())[:8]
                safe_company_name = re.sub(r'[^\w\s-]', '', company_name.lower().replace(' ', '_'))[:20]
                png_filename = f"logo_{safe_company_name}_{logo_style.lower()}_{timestamp}_{unique_id}.png"
                svg_filename = f"logo_{safe_company_name}_{logo_style.lower()}_{timestamp}_{unique_id}.svg"
                
                # Use the specific output folder if provided
                if self.output_folder:
                    os.makedirs(self.output_folder, exist_ok=True)
                    png_local_path = os.path.join(self.output_folder, png_filename)
                    svg_local_path = os.path.join(self.output_folder, svg_filename)
                else:
                    # Fallback to default logos folder
                    current_dir = os.getcwd()
                    logos_dir = os.path.join(current_dir, "generated_logos")
                    os.makedirs(logos_dir, exist_ok=True)
                    png_local_path = os.path.join(logos_dir, png_filename)
                    svg_local_path = os.path.join(logos_dir, svg_filename)
                
                # Save PNG version
                with open(png_local_path, 'wb') as f:
                    f.write(image_response.content)
                
                # Create a basic SVG version (this would ideally be a proper SVG conversion)
                # For now, we'll create a placeholder SVG structure that embeds the PNG
                svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="1024" height="1024" viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg">
  <!-- Professional logo for {company_name} -->
  <!-- Style: {logo_style} -->
  <image href="data:image/png;base64,{self._encode_image_to_base64(image_response.content)}" width="1024" height="1024"/>
</svg>'''
                
                with open(svg_local_path, 'w', encoding='utf-8') as f:
                    f.write(svg_content)
                
                return json.dumps({
                    "image_url": image_url,
                    "png_local_path": png_local_path,
                    "svg_local_path": svg_local_path,
                    "png_filename": png_filename,
                    "svg_filename": svg_filename,
                    "company_name": company_name,
                    "logo_style": logo_style,
                    "original_prompt": prompt,
                    "refined_prompt": refined_prompt,
                    "formats": ["PNG", "SVG"],
                    "resolution": "1024x1024",
                    "seed": result.get('seed'),
                    "logo_type": "professional_vector_logo"
                })
            else:
                return json.dumps({
                    "image_url": image_url,
                    "png_local_path": "Failed to download",
                    "svg_local_path": "Failed to download",
                    "png_filename": "Failed to download",
                    "svg_filename": "Failed to download",
                    "company_name": company_name,
                    "logo_style": logo_style,
                    "prompt": prompt,
                    "error": f"Failed to download SVG logo: {image_response.status_code}"
                })
                
        except Exception as e:
            return json.dumps({
                "image_url": "Error",
                "png_local_path": "Error",
                "svg_local_path": "Error",
                "png_filename": "Error",
                "svg_filename": "Error",
                "company_name": company_name,
                "logo_style": logo_style,
                "prompt": prompt,
                "error": f"Error generating SVG logo: {str(e)}"
            })
    
    def _encode_image_to_base64(self, image_content: bytes) -> str:
        """Encode image content to base64 for SVG embedding"""
        import base64
        return base64.b64encode(image_content).decode('utf-8')

class ImageGeneratorTool(BaseTool):
    name: str = "generate_image"
    description: str = "Generate an image using Ideogram V2A based on the provided prompt."
    args_schema: Type[BaseModel] = ImageGeneratorArgs
    output_folder: str = None
    claude_service: ClaudeRefinementService = None

    def __init__(self, output_folder=None):
        super().__init__()
        self.output_folder = output_folder
        self.claude_service = ClaudeRefinementService()

    def _run(self, prompt: str) -> str:
        try:
            # Refine the prompt using Claude before sending to FAL.ai
            print(f"Original prompt: {prompt}")
            refined_prompt = self.claude_service.refine_image_prompt(prompt)
            print(f"Claude-refined prompt: {refined_prompt}")
            
            # Ensure FAL_KEY is set in environment
            os.environ['FAL_KEY'] = config('FAL_KEY')
            
            # Submit request to Ideogram V2A with refined prompt
            result = fal.run(
                "fal-ai/ideogram/v2a",
                arguments={
                    "prompt": refined_prompt,
                    "aspect_ratio": "1:1",
                    "style": "auto"
                }
            )
            
            image_url = result['images'][0]['url']
            
            # Download and save the image locally
            image_response = requests.get(image_url)
            if image_response.status_code == 200:
                # Create unique filename with timestamp
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                unique_id = str(uuid.uuid4())[:8]
                filename = f"generated_image_{timestamp}_{unique_id}.png"
                
                # Use the specific output folder if provided, otherwise use default
                if self.output_folder:
                    os.makedirs(self.output_folder, exist_ok=True)
                    local_path = os.path.join(self.output_folder, filename)
                else:
                    # Fallback to default generated_images folder
                    current_dir = os.getcwd()
                    images_dir = os.path.join(current_dir, "generated_images")
                    os.makedirs(images_dir, exist_ok=True)
                    local_path = os.path.join(images_dir, filename)
                
                with open(local_path, 'wb') as f:
                    f.write(image_response.content)
                
                return json.dumps({
                    "image_url": image_url,
                    "local_path": local_path,
                    "filename": filename,
                    "original_prompt": prompt,
                    "refined_prompt": refined_prompt,
                    "seed": result.get('seed')
                })
            else:
                return json.dumps({
                    "image_url": image_url,
                    "local_path": "Failed to download",
                    "filename": "Failed to download",
                    "prompt": prompt,
                    "error": f"Failed to download image: {image_response.status_code}"
                })
                
        except Exception as e:
            return json.dumps({
                "image_url": "Error",
                "local_path": "Error",
                "filename": "Error", 
                "prompt": prompt,
                "error": f"Error generating image: {str(e)}"
            })


class CarouselImageGeneratorArgs(BaseModel):
    prompts: list = Field(description="List of prompts for carousel image generation")
    
class CarouselImageGeneratorTool(BaseTool):
    name: str = "generate_carousel_images"
    description: str = "Generate multiple images for carousel posts using Ideogram V2A based on a list of prompts."
    args_schema: Type[BaseModel] = CarouselImageGeneratorArgs
    output_folder: str = None
    claude_service: ClaudeRefinementService = None

    def __init__(self, output_folder=None):
        super().__init__()
        self.output_folder = output_folder
        self.claude_service = ClaudeRefinementService()

    def _run(self, prompts: list) -> str:
        try:
            carousel_images = []
            
            for i, prompt in enumerate(prompts, 1):
                try:
                    # Refine each prompt using Claude
                    print(f"Carousel slide {i} - Original prompt: {prompt}")
                    refined_prompt = self.claude_service.refine_image_prompt(prompt, f"Carousel slide {i}")
                    print(f"Carousel slide {i} - Claude-refined prompt: {refined_prompt}")
                    
                    # Ensure FAL_KEY is set in environment
                    os.environ['FAL_KEY'] = config('FAL_KEY')
                    
                    result = fal.run(
                        "fal-ai/ideogram/v2a",
                        arguments={
                            "prompt": refined_prompt,
                            "aspect_ratio": "1:1",
                            "style": "auto"
                        }
                    )
                    
                    image_url = result['images'][0]['url']
                    
                    # Download and save the image locally
                    image_response = requests.get(image_url)
                    if image_response.status_code == 200:
                        # Create unique filename with carousel index
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        unique_id = str(uuid.uuid4())[:8]
                        filename = f"carousel_slide_{i}_{timestamp}_{unique_id}.png"
                        
                        # Use the specific output folder if provided, otherwise use default
                        if self.output_folder:
                            os.makedirs(self.output_folder, exist_ok=True)
                            local_path = os.path.join(self.output_folder, filename)
                        else:
                            # Fallback to default generated_images folder
                            current_dir = os.getcwd()
                            images_dir = os.path.join(current_dir, "generated_images")
                            os.makedirs(images_dir, exist_ok=True)
                            local_path = os.path.join(images_dir, filename)
                        
                        with open(local_path, 'wb') as f:
                            f.write(image_response.content)
                        
                        carousel_images.append({
                            "slide_number": i,
                            "image_url": image_url,
                            "local_path": local_path,
                            "filename": filename,
                            "original_prompt": prompt,
                            "refined_prompt": refined_prompt,
                            "seed": result.get('seed')
                        })
                    else:
                        carousel_images.append({
                            "slide_number": i,
                            "image_url": image_url,
                            "local_path": "Failed to download",
                            "filename": "Failed to download",
                            "prompt": prompt,
                            "error": f"Failed to download image: {image_response.status_code}"
                        })
                        
                except Exception as e:
                    carousel_images.append({
                        "slide_number": i,
                        "image_url": "Error",
                        "local_path": "Error",
                        "filename": "Error",
                        "prompt": prompt,
                        "error": f"Error generating image {i}: {str(e)}"
                    })
            
            return json.dumps({
                "carousel_images": carousel_images,
                "total_images": len(carousel_images),
                "successful_images": len([img for img in carousel_images if "error" not in img])
            })
                
        except Exception as e:
            return json.dumps({
                "carousel_images": [],
                "total_images": 0,
                "successful_images": 0,
                "error": f"Error generating carousel images: {str(e)}"
            })


class StoryImageGeneratorArgs(BaseModel):
    prompt: str = Field(description="The prompt for story image generation")

class StoryImageGeneratorTool(BaseTool):
    name: str = "generate_story_image"
    description: str = "Generate a single vertical story image (9:16 format) using Ideogram V2A based on the provided prompt."
    args_schema: Type[BaseModel] = StoryImageGeneratorArgs
    output_folder: str = None
    claude_service: ClaudeRefinementService = None

    def __init__(self, output_folder=None):
        super().__init__()
        self.output_folder = output_folder
        self.claude_service = ClaudeRefinementService()

    def _run(self, prompt: str) -> str:
        try:
            # Refine the prompt using Claude for story format
            print(f"Story - Original prompt: {prompt}")
            refined_prompt = self.claude_service.refine_image_prompt(prompt, "Story format - vertical 9:16")
            print(f"Story - Claude-refined prompt: {refined_prompt}")
            
            # Ensure FAL_KEY is set in environment
            os.environ['FAL_KEY'] = config('FAL_KEY')
            
            result = fal.run(
                "fal-ai/ideogram/v2a",
                arguments={
                    "prompt": refined_prompt,
                    "aspect_ratio": "9:16",
                    "style": "auto"
                }
            )
            
            image_url = result['images'][0]['url']
            
            # Download and save the image locally
            image_response = requests.get(image_url)
            if image_response.status_code == 200:
                # Create unique filename with timestamp
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                unique_id = str(uuid.uuid4())[:8]
                filename = f"story_image_{timestamp}_{unique_id}.png"
                
                # Use the specific output folder if provided, otherwise use default
                if self.output_folder:
                    local_path = os.path.join(self.output_folder, filename)
                else:
                    # Fallback to default generated_images folder
                    current_dir = os.getcwd()
                    images_dir = os.path.join(current_dir, "generated_images")
                    os.makedirs(images_dir, exist_ok=True)
                    local_path = os.path.join(images_dir, filename)
                
                with open(local_path, 'wb') as f:
                    f.write(image_response.content)
                
                return json.dumps({
                    "image_url": image_url,
                    "local_path": local_path,
                    "filename": filename,
                    "original_prompt": prompt,
                    "refined_prompt": refined_prompt,
                    "format": "story_single",
                    "dimensions": "9:16",
                    "seed": result.get('seed')
                })
            else:
                return json.dumps({
                    "image_url": image_url,
                    "local_path": "Failed to download",
                    "filename": "Failed to download",
                    "prompt": prompt,
                    "format": "story_single",
                    "error": f"Failed to download image: {image_response.status_code}"
                })
                
        except Exception as e:
            return json.dumps({
                "image_url": "Error",
                "local_path": "Error",
                "filename": "Error", 
                "prompt": prompt,
                "format": "story_single",
                "error": f"Error generating story image: {str(e)}"
            })


class StorySeriesGeneratorArgs(BaseModel):
    prompts: list = Field(description="List of prompts for story series generation")
    
class StorySeriesGeneratorTool(BaseTool):
    name: str = "generate_story_series"
    description: str = "Generate multiple vertical story images (9:16 format) for story series using Ideogram V2A based on a list of prompts."
    args_schema: Type[BaseModel] = StorySeriesGeneratorArgs
    output_folder: str = None
    claude_service: ClaudeRefinementService = None

    def __init__(self, output_folder=None):
        super().__init__()
        self.output_folder = output_folder
        self.claude_service = ClaudeRefinementService()

    def _run(self, prompts: list) -> str:
        try:
            story_images = []
            
            for i, prompt in enumerate(prompts, 1):
                try:
                    # Refine each story prompt using Claude
                    print(f"Story series {i} - Original prompt: {prompt}")
                    refined_prompt = self.claude_service.refine_image_prompt(prompt, f"Story series {i} - vertical 9:16")
                    print(f"Story series {i} - Claude-refined prompt: {refined_prompt}")
                    
                    # Ensure FAL_KEY is set in environment
                    os.environ['FAL_KEY'] = config('FAL_KEY')
                    
                    result = fal.run(
                        "fal-ai/ideogram/v2a",
                        arguments={
                            "prompt": refined_prompt,
                            "aspect_ratio": "9:16",
                            "style": "auto"
                        }
                    )
                    
                    image_url = result['images'][0]['url']
                    
                    # Download and save the image locally
                    image_response = requests.get(image_url)
                    if image_response.status_code == 200:
                        # Create unique filename with story index
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        unique_id = str(uuid.uuid4())[:8]
                        filename = f"story_{i}_{timestamp}_{unique_id}.png"
                        
                        # Use the specific output folder if provided, otherwise use default
                        if self.output_folder:
                            os.makedirs(self.output_folder, exist_ok=True)
                            local_path = os.path.join(self.output_folder, filename)
                        else:
                            # Fallback to default generated_images folder
                            current_dir = os.getcwd()
                            images_dir = os.path.join(current_dir, "generated_images")
                            os.makedirs(images_dir, exist_ok=True)
                            local_path = os.path.join(images_dir, filename)
                        
                        with open(local_path, 'wb') as f:
                            f.write(image_response.content)
                        
                        story_images.append({
                            "story_number": i,
                            "image_url": image_url,
                            "local_path": local_path,
                            "filename": filename,
                            "original_prompt": prompt,
                            "refined_prompt": refined_prompt,
                            "seed": result.get('seed')
                        })
                    else:
                        story_images.append({
                            "story_number": i,
                            "image_url": image_url,
                            "local_path": "Failed to download",
                            "filename": "Failed to download",
                            "prompt": prompt,
                            "error": f"Failed to download image: {image_response.status_code}"
                        })
                        
                except Exception as e:
                    story_images.append({
                        "story_number": i,
                        "image_url": "Error",
                        "local_path": "Error",
                        "filename": "Error",
                        "prompt": prompt,
                        "error": f"Error generating story image {i}: {str(e)}"
                    })
            
            return json.dumps({
                "story_images": story_images,
                "total_stories": len(story_images),
                "successful_stories": len([img for img in story_images if "error" not in img]),
                "format": "story_series",
                "dimensions": "9:16"
            })
                
        except Exception as e:
            return json.dumps({
                "story_images": [],
                "total_stories": 0,
                "successful_stories": 0,
                "format": "story_series",
                "error": f"Error generating story series: {str(e)}"
            })

class TimingArgs(BaseModel):
    platform: str = Field(default="instagram", description="Social media platform")

class TimingTool(BaseTool):
    name: str = "get_optimal_posting_time"
    description: str = "Get optimal posting times for different social media platforms."
    args_schema: Type[BaseModel] = TimingArgs

    def _run(self, platform: str = "instagram") -> str:
        times = {
            "instagram": "6:00 PM - 9:00 PM (weekdays), 10:00 AM - 1:00 PM (weekends)",
            "facebook": "1:00 PM - 4:00 PM (weekdays), 12:00 PM - 2:00 PM (weekends)", 
            "twitter": "8:00 AM - 10:00 AM and 7:00 PM - 9:00 PM",
            "linkedin": "8:00 AM - 10:00 AM and 5:00 PM - 6:00 PM (Tuesday-Thursday)"
        }
        return times.get(platform.lower(), "6:00 PM - 9:00 PM (general recommendation)")


class CaptionRefinementArgs(BaseModel):
    caption: str = Field(description="The caption to refine")
    context: str = Field(default="", description="Additional context for refinement")
    platform: str = Field(default="instagram", description="Target platform")

class CaptionRefinementTool(BaseTool):
    name: str = "refine_caption"
    description: str = "Refine social media captions using Claude for maximum engagement"
    args_schema: Type[BaseModel] = CaptionRefinementArgs
    claude_service: ClaudeRefinementService = None

    def __init__(self):
        super().__init__()
        self.claude_service = ClaudeRefinementService()

    def _run(self, caption: str, context: str = "", platform: str = "instagram") -> str:
        try:
            refined_caption = self.claude_service.refine_caption(caption, context, platform)
            return refined_caption
        except Exception as e:
            print(f"Error refining caption: {str(e)}")
            return caption


class HashtagRefinementArgs(BaseModel):
    hashtags: list = Field(description="List of hashtags to refine")
    context: str = Field(default="", description="Additional context for refinement")
    platform: str = Field(default="instagram", description="Target platform")

class HashtagRefinementTool(BaseTool):
    name: str = "refine_hashtags"
    description: str = "Refine hashtag strategy using Claude for maximum reach and engagement"
    args_schema: Type[BaseModel] = HashtagRefinementArgs
    claude_service: ClaudeRefinementService = None

    def __init__(self):
        super().__init__()
        self.claude_service = ClaudeRefinementService()

    def _run(self, hashtags: list, context: str = "", platform: str = "instagram") -> str:
        try:
            refined_hashtags = self.claude_service.refine_hashtags(hashtags, context, platform)
            return "\n".join(refined_hashtags)
        except Exception as e:
            print(f"Error refining hashtags: {str(e)}")
            return "\n".join(hashtags) if hashtags else ""


class LogoDesignAgents:
    def __init__(self):
        self.OpenAIGPT35 = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
        self.OpenAIGPT4 = ChatOpenAI(model_name="gpt-4", temperature=0.7)
        self.creative_llm = ChatOpenAI(model_name="gpt-4", temperature=0.9)
        self.brand_analyst_llm = ChatOpenAI(model_name="gpt-4", temperature=0.8)

    def brand_strategist_agent(self):
        return Agent(
            role="Brand Strategy & Psychology Expert",
            backstory=dedent("""You are a world-renowned brand strategist and design psychologist with 15+ years 
                            of experience creating iconic logos for Fortune 500 companies, startups, and everything 
                            in between. You understand brand psychology, color theory, typography psychology, 
                            cultural symbolism, and market positioning. You have deep knowledge of logo design 
                            principles, brand differentiation strategies, and consumer psychology. Your expertise 
                            includes understanding how different logo styles (WordMark, LetterMark, Pictorial, 
                            Abstract, Combination, Emblem) impact brand perception and market success."""),
            goal=dedent("""Analyze the company's identity, industry, target audience, and objectives to develop 
                       comprehensive brand strategy insights. Generate 3 distinct logo concept directions that 
                       align with brand psychology principles, market positioning goals, and industry best 
                       practices. Each concept should leverage different psychological triggers and visual 
                       approaches to maximize brand impact and memorability."""),
            allow_delegation=False,
            verbose=True,
            llm=self.OpenAIGPT4,
        )

    def logo_designer_agent(self, output_folder=None):
        return Agent(
            role="Master Logo Designer & Visual Identity Expert",
            backstory=dedent("""You are an elite logo designer with expertise in creating world-class visual 
                            identities. You have designed logos for major brands like Apple, Nike, Google, and 
                            thousands of successful companies. You understand the nuances of different logo styles, 
                            typography selection, color psychology, scalability requirements, and brand application 
                            needs. You specialize in creating logos that work perfectly across all mediums - from 
                            business cards to billboards, from mobile apps to merchandise. You always use the 
                            logo generation tools to create professional SVG and PNG outputs with Claude's 
                            refinement for world-class results."""),
            goal=dedent("""Transform brand strategy insights into stunning, professional logo designs that 
                       perfectly capture the company's essence and market positioning. Create logos that are 
                       memorable, scalable, timeless, and psychologically effective. Always generate both 
                       SVG and PNG formats for maximum usability. Use advanced logo generation tools with 
                       Claude refinement to ensure world-class quality and professional standards."""),
            tools=[LogoGeneratorTool(output_folder), SVGLogoGeneratorTool(output_folder)],
            allow_delegation=False,
            verbose=True,
            llm=self.creative_llm,
        )

    def brand_analyst_agent(self):
        return Agent(
            role="Brand Psychology & Strategy Analyst",
            backstory=dedent("""You are a renowned brand psychologist and strategic analyst who specializes 
                            in explaining the psychological and strategic rationale behind successful logo designs. 
                            You have deep expertise in consumer psychology, market research, competitive analysis, 
                            brand positioning theory, and design psychology. You understand why certain logos 
                            succeed in their markets, how visual elements trigger emotional responses, and how 
                            logo design choices impact brand perception, customer loyalty, and business success. 
                            You can analyze any logo design and provide comprehensive insights into its 
                            effectiveness, market positioning, and psychological impact."""),
            goal=dedent("""Analyze the final logo design and provide comprehensive strategic insights explaining 
                       why this specific logo design is perfect for the company. Cover brand psychology, 
                       competitive differentiation, target audience appeal, market positioning, scalability, 
                       memorability factors, and long-term brand building potential. Provide actionable 
                       insights that demonstrate the logo's strategic value and effectiveness."""),
            allow_delegation=False,
            verbose=True,
            llm=self.brand_analyst_llm,
        )

    def hashtag_agent(self):
        return Agent(
            role="Hashtag Research Specialist",
            backstory=dedent("""You are a social media growth expert who understands hashtag strategies, 
                            trending topics, and how to maximize reach and engagement through strategic 
                            hashtag usage. You always use the refine_hashtags tool to enhance your hashtag 
                            strategies with Claude's advanced optimization capabilities."""),
            goal=dedent("""Research and provide relevant, trending hashtags that will maximize the reach 
                       and engagement of social media posts while staying relevant to the content. Always 
                       refine your hashtags using the refine_hashtags tool to ensure optimal performance."""),
            tools=[HashtagRefinementTool()],
            allow_delegation=False,
            verbose=True,
            llm=self.OpenAIGPT35,
        )

    def timing_agent(self):
        return Agent(
            role="Social Media Timing Optimizer",
            backstory=dedent("""You are a data-driven social media analyst who understands audience 
                            behavior patterns, optimal posting times, and platform algorithms."""),
            goal=dedent("""Provide optimal posting times and platform-specific recommendations to 
                       maximize reach and engagement."""),
            tools=[TimingTool()],
            allow_delegation=False,
            verbose=True,
            llm=self.OpenAIGPT35,
        )

    def calendar_planner_agent(self):
        return Agent(
            role="Content Calendar Planning Specialist",
            backstory=dedent("""You are an expert content calendar strategist with extensive experience 
                            in social media planning, content organization, and strategic scheduling. 
                            You understand how to create comprehensive content calendars that ensure 
                            consistency, strategic alignment, and maximum engagement across multiple 
                            platforms and content types."""),
            goal=dedent("""Create detailed content calendar plans that organize and schedule social media 
                       content strategically. Generate comprehensive calendar structures that include 
                       dates, platforms, content types, themes, and scheduling recommendations to 
                       help maintain consistent and effective social media presence."""),
            allow_delegation=False,
            verbose=True,
            llm=self.OpenAIGPT4,
        )
