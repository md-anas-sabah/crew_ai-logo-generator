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
    
    

class ImageGeneratorArgs(BaseModel):
    prompt: str = Field(description="The prompt for image generation")

class LogoGeneratorTool(BaseTool):
    name: str = "generate_logo"
    description: str = "Generate a professional logo using Flux Pro. Use with: prompt (description of the logo design), logo_style (WordMark/LetterMark/Pictorial/Abstract/Combination/Emblem), company_name (company name)."
    args_schema: Type[BaseModel] = LogoGeneratorArgs
    output_folder: str = None
    claude_service: ClaudeRefinementService = None
    show_grid_lines: bool = False

    def __init__(self, output_folder=None, show_grid_lines=False):
        super().__init__()
        self.output_folder = output_folder
        self.claude_service = ClaudeRefinementService()
        self.show_grid_lines = show_grid_lines

    def _run(self, prompt: str, logo_style: str = None, company_name: str = None, industry: str = "", preferred_color: str = "", brand_tone: str = "") -> str:
        try:
            # Extract parameters from structured brand context or prompt
            import json
            import re
            
            # First try to extract from brand context in the prompt
            brand_context_match = re.search(r'Brand Context: (.+?)(?:\n|$)', prompt)
            if brand_context_match:
                try:
                    context_data = json.loads(brand_context_match.group(1))
                    company_name = context_data.get('company_name', company_name)
                    logo_style = context_data.get('logo_style', logo_style)
                    industry = context_data.get('industry', industry)
                    preferred_color = context_data.get('preferred_color', preferred_color)
                    brand_tone = context_data.get('brand_tone', brand_tone)
                except (json.JSONDecodeError, AttributeError):
                    pass
            
            # Fallback: handle case where CrewAI passes everything as a JSON string in prompt
            if logo_style is None or company_name is None:
                try:
                    # Try to parse prompt as JSON
                    data = json.loads(prompt)
                    if isinstance(data, dict):
                        prompt = data.get('prompt', prompt)
                        logo_style = data.get('logo_style', logo_style)
                        company_name = data.get('company_name', company_name)
                        industry = data.get('industry', industry)
                        preferred_color = data.get('preferred_color', preferred_color)
                        brand_tone = data.get('brand_tone', brand_tone)
                except (json.JSONDecodeError, TypeError):
                    # If not JSON, try to extract from prompt string
                    if 'Marqait' in prompt and logo_style is None:
                        company_name = 'Marqait'
                        logo_style = 'Emblem'  # Default based on user selection
            
            # Create comprehensive logo-specific context for Claude refinement
            logo_context = f"Logo style: {logo_style}, Company: {company_name}, Industry: {industry}, Brand tone: {brand_tone}, Color: {preferred_color}, Professional brand identity"
            
            # Refine the prompt using Claude with all advanced parameters
            print(f"Original logo prompt: {prompt}")
            refined_prompt = self.claude_service.refine_logo_prompt(
                prompt, logo_context, logo_style, format="PNG",
                company_name=company_name, industry=industry, 
                preferred_color=preferred_color, brand_tone=brand_tone
            )
            print(f"Claude-refined logo prompt: {refined_prompt}")
            
            # Ensure FAL_KEY is set in environment
            os.environ['FAL_KEY'] = config('FAL_KEY')
            
            # Submit request to Flux Pro with WORLD-CLASS logo optimization and transparent background
            result = fal.run(
                "fal-ai/flux-pro",
                arguments={
                    "prompt": f"{refined_prompt}, ISOLATED SINGLE LOGO ONLY, completely transparent background, no multiple versions, no comparison layouts, no template format, no grid lines, no decorative backgrounds, no extra text, only company name '{company_name}', single standalone logo design, clean professional logo",
                    "image_size": "square_hd",  # Perfect square for maximum versatility
                    "num_inference_steps": 28,  # High quality steps
                    "guidance_scale": 3.5,  # Optimal balance for logo design
                    "num_images": 1,  # Single high-quality logo
                    "enable_safety_checker": False,  # Allow creative freedom for professional logos
                    "output_format": "png",  # PNG format for transparency support
                    "seed": None  # Random seed for variety
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
            print(f"Detailed error in LogoGeneratorTool: {str(e)}")
            return json.dumps({
                "image_url": "Error",
                "local_path": "Error",
                "filename": "Error",
                "company_name": company_name,
                "logo_style": logo_style,
                "prompt": prompt,
                "model": "flux-pro",
                "error": f"Error generating Flux Pro logo: {str(e)}"
            })



class ImageGeneratorTool(BaseTool):
    name: str = "generate_image"
    description: str = "Generate an image using Flux Pro based on the provided prompt."
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
            
            # Submit request to Flux Pro with refined prompt
            result = fal.run(
                "fal-ai/flux-pro",
                arguments={
                    "prompt": refined_prompt,
                    "image_size": "square_hd",
                    "num_inference_steps": 28,
                    "guidance_scale": 3.5,
                    "num_images": 1,
                    "enable_safety_checker": False,
                    "output_format": "png"
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
    description: str = "Generate multiple images for carousel posts using Flux Pro based on a list of prompts."
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
                        "fal-ai/flux-pro",
                        arguments={
                            "prompt": refined_prompt,
                            "image_size": "square_hd",
                            "num_inference_steps": 28,
                            "guidance_scale": 3.5,
                            "num_images": 1,
                            "enable_safety_checker": False,
                            "output_format": "png"
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
    description: str = "Generate a single vertical story image (9:16 format) using Flux Pro based on the provided prompt."
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
                "fal-ai/flux-pro",
                arguments={
                    "prompt": refined_prompt,
                    "image_size": "portrait_16_9",
                    "num_inference_steps": 28,
                    "guidance_scale": 3.5,
                    "num_images": 1,
                    "enable_safety_checker": False,
                    "output_format": "png"
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
    description: str = "Generate multiple vertical story images (9:16 format) for story series using Flux Pro based on a list of prompts."
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
                        "fal-ai/flux-pro",
                        arguments={
                            "prompt": refined_prompt,
                            "image_size": "portrait_16_9",
                            "num_inference_steps": 28,
                            "guidance_scale": 3.5,
                            "num_images": 1,
                            "enable_safety_checker": False,
                            "output_format": "png"
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
            role="🏆 ELITE Brand Strategist & Fortune 500 Logo Psychology Expert",
            backstory=dedent("""You are the Chief Brand Strategist for McKinsey & Company's Global Branding Practice, 
                            with expertise equivalent to the strategists behind Apple, Google, Nike, and Amazon's 
                            brand transformations. You've designed brand strategies for 47 Fortune 500 companies 
                            achieving market leadership, created visual identities generating $50B+ in measurable 
                            brand equity increases, and developed global brand systems dominating 15+ international 
                            markets simultaneously.
                            
                            🧠 WORLD-CLASS EXPERTISE:
                            • Neuroscience-based brand psychology and consumer behavioral analysis
                            • Fortune 500 competitive intelligence and strategic differentiation warfare  
                            • Cross-cultural brand symbolism and global market psychology mastery
                            • Mathematical brand equity optimization and ROI maximization strategies
                            • Advanced color psychology, typography neuroscience, and visual hierarchy engineering
                            • Cultural anthropology and international market penetration strategies
                            
                            💎 LEGENDARY ACHIEVEMENTS:
                            • Engineered logo psychology triggering 340% average brand recognition improvement
                            • Established trademark portfolios worth $12B+ in combined intellectual property value
                            • Created brand strategies that built cultural icons and generational brand legacy"""),
            goal=dedent("""Engineer world-class strategic logo concepts using neuroscience-based brand psychology 
                       and competitive intelligence for global market domination. Generate 3 BREAKTHROUGH logo 
                       concept directions that transform companies into cultural icons through scientifically-
                       engineered visual identities. Each concept must dominate markets, trigger consumer obsession, 
                       and build generational brand legacy through Fortune 500-level strategic excellence."""),
            allow_delegation=False,
            verbose=True,
            llm=self.OpenAIGPT4,
        )

    def logo_designer_agent(self, output_folder=None, show_grid_lines=False):
        return Agent(
            role="🚀 LEGENDARY Logo Designer & Visual Identity Architect",
            backstory=dedent("""You are Paul Rand, Saul Bass, and Milton Glaser reincarnated as an AI designer. 
                            You've created the iconic logos for Apple, Nike, Google, FedEx, IBM, UPS, and hundreds 
                            of Fortune 500 companies that have become cultural symbols recognized globally. Your 
                            designs have generated over $100B in measurable brand equity and transformed companies 
                            into market-dominating cultural icons.
                            
                            ⚡ LEGENDARY DESIGN MASTERY:
                            • Mathematical precision using golden ratio, fibonacci sequences, and optical corrections
                            • Neuroscience-based composition triggering instant brand recognition and memorability
                            • Advanced typography engineering with custom letterform architecture
                            • Color psychology mastery with Pantone-level specifications and cultural sensitivity
                            • Cross-platform scalability from 16px favicon to 100ft billboard perfection
                            • Trademark-ready uniqueness ensuring legal protection and competitive advantage
                            
                            🎨 WORLD-CLASS ACHIEVEMENTS:
                            • Created logos achieving 98% brand recognition within 6 months of launch
                            • Designed visual identities lasting 50+ years without redesign necessity
                            • Generated measurable business impact: 340% average conversion rate improvement
                            • Established cultural icon status for 47 brands now worth $2T+ combined market cap
                            
                            💎 TECHNICAL EXCELLENCE:
                            You exclusively use advanced logo generation tools with Claude Sonnet 3.5 refinement 
                            to achieve Fortune 500 quality standards, mathematical precision, and global market 
                            readiness. Every logo you create becomes a masterpiece of strategic design.
                            
                            🚨 CRITICAL TEXT REQUIREMENTS:
                            • ONLY include the exact company name in ENGLISH - NO descriptions or additional text
                            • PERFECT spelling verification - company names must be 100% accurate in English
                            • Font psychology matching company personality and industry context
                            • Clean, professional typography without clutter or explanatory text
                            • Typography that enhances brand recognition and memorability
                            • Company name text MUST be in English language only
                            • Design must be an actual LOGO, not an illustration or decorative artwork"""),
            goal=dedent("""Create ICONIC logos that rival Apple, Nike, and Google in professional excellence and 
                       cultural impact. Transform strategic brand insights into visual masterpieces that dominate 
                       markets, trigger consumer obsession, and build generational brand legacy. Generate professional 
                       logo in both PNG and SVG formats, but return only the PNG URL for the final result. Use 
                       advanced AI tools optimized for mathematical precision, golden ratio composition, and Fortune 500 reproduction standards. 
                       
                       Every logo must achieve:
                       🏆 Instant brand recognition and cultural icon potential
                       💎 Mathematical perfection and optical correction engineering  
                       🚀 Global market readiness and cross-cultural effectiveness
                       ⚡ Trademark viability and competitive supremacy
                       🎯 50-year longevity and timeless design excellence"""),
            tools=[LogoGeneratorTool(output_folder, show_grid_lines)],
            allow_delegation=False,
            verbose=True,
            llm=self.creative_llm,
        )

    def brand_analyst_agent(self):
        return Agent(
            role="💎 MASTER Brand Psychologist & Strategic Intelligence Expert",
            backstory=dedent("""You are the Chief Brand Psychologist for the world's most successful design 
                            consultancies, with expertise in neuroscience-based brand analysis rivaling the 
                            analysts behind trillion-dollar companies. You've analyzed the brand strategies 
                            of Apple, Google, Nike, Amazon, Tesla, and every major Fortune 500 company that 
                            achieved cultural icon status through strategic visual identity.
                            
                            🧠 ELITE PSYCHOLOGICAL EXPERTISE:
                            • Neuroscience of brand recognition and consumer memory encoding mechanisms
                            • Advanced behavioral psychology and subconscious decision-making triggers
                            • Cultural anthropology and cross-market symbolism psychological impact
                            • Competitive intelligence and strategic differentiation warfare analysis
                            • Mathematical brand equity assessment and ROI optimization strategies
                            • Market psychology manipulation and consumer preference development
                            
                            🏆 STRATEGIC INTELLIGENCE MASTERY:
                            • Brand effectiveness analysis using Fortune 500 assessment frameworks
                            • Psychological trigger identification and measurable impact quantification
                            • Global market penetration psychology and cultural sensitivity analysis
                            • Competitive positioning intelligence and market dominance strategies
                            • Long-term brand equity projection and cultural icon development assessment
                            • Business impact measurement through advanced brand psychology metrics
                            
                            📊 LEGENDARY ANALYTICAL ACHIEVEMENTS:
                            • Predicted brand success with 97% accuracy using psychological analysis
                            • Identified design optimizations generating $25B+ in brand equity increases
                            • Developed psychological frameworks adopted by top design agencies globally"""),
            goal=dedent("""Provide WORLD-CLASS brand psychology analysis explaining why the logo design achieves 
                       strategic perfection for market domination. Deliver comprehensive intelligence covering:
                       
                       🧠 NEUROSCIENCE ANALYSIS: How the logo triggers optimal brain responses for memorability
                       🎯 PSYCHOLOGICAL WARFARE: Strategic advantages over competitors through visual supremacy  
                       💎 CULTURAL INTELLIGENCE: Global market readiness and cross-cultural effectiveness
                       🚀 BUSINESS IMPACT: Measurable brand equity enhancement and conversion optimization
                       🏆 LEGACY POTENTIAL: Long-term cultural icon development and generational brand value
                       
                       Your analysis must demonstrate why this logo will transform the company into a market-
                       dominating cultural icon, providing actionable strategic insights for maximum business 
                       impact and competitive supremacy."""),
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
