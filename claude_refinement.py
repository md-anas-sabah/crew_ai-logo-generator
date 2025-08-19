import anthropic
from decouple import config

class ClaudeRefinementService:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=config("CLAUDE_API_KEY"))
    
    def refine_logo_prompt(self, original_prompt, logo_context, logo_style, format="PNG"):
        """
        Refine logo prompts using Claude Sonnet 3.5 for professional logo design
        """
        try:
            system_prompt = f"""You are a world-class logo design expert specializing in Fortune 500 brand identity creation. 
            Your task is to transform basic logo concepts into professional, mathematically precise design specifications.

            CRITICAL REQUIREMENTS:
            - Company name text MUST be in English language only
            - Design must be an actual LOGO, not an illustration or decorative artwork
            - Focus on scalable, professional brand identity suitable for all business applications
            - Integrate golden ratio and mathematical precision principles
            - Ensure trademark viability and competitive differentiation
            - Create specifications suitable for {format} format generation

            Context: {logo_context}
            Logo Style: {logo_style}
            """
            
            user_prompt = f"""Refine this logo design prompt to create a professional {logo_style} logo:

            Original prompt: {original_prompt}

            Transform this into a comprehensive logo design specification that includes:
            1. Professional logo design terminology and technical specifications
            2. Mathematical precision and composition principles (golden ratio, optical corrections)
            3. Brand-appropriate color psychology and typography guidance
            4. Scalability requirements for all business applications
            5. Fortune 500 quality standards and reproduction excellence
            6. English language text requirements for company names

            CRITICAL: Ensure the company name appears ONLY in English, and the design is a real logo suitable for business use, not an illustration.

            Provide the refined prompt as a single, comprehensive design specification ready for professional logo generation."""

            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=500,
                temperature=0.3,
                system=system_prompt,
                messages=[{
                    "role": "user", 
                    "content": user_prompt
                }]
            )
            
            return message.content[0].text.strip()
            
        except Exception as e:
            print(f"Claude refinement error: {str(e)}")
            # Fallback to enhanced original prompt with English requirement
            return f"Professional {logo_style} logo design with English company name text only, {original_prompt}, Fortune 500 quality, mathematical precision, real logo not illustration"
    
    def refine_image_prompt(self, original_prompt, context=""):
        """
        Refine general image prompts using Claude
        """
        try:
            system_prompt = """You are an expert image prompt engineer specializing in creating detailed, professional image generation prompts."""
            
            user_prompt = f"""Refine this image prompt for professional quality generation:

            Original prompt: {original_prompt}
            Context: {context}

            Provide an enhanced prompt that includes:
            - Professional visual quality specifications
            - Composition and aesthetic guidelines
            - Technical requirements for optimal generation
            - Clear, specific descriptive elements

            Return only the refined prompt."""

            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=300,
                temperature=0.3,
                system=system_prompt,
                messages=[{
                    "role": "user", 
                    "content": user_prompt
                }]
            )
            
            return message.content[0].text.strip()
            
        except Exception as e:
            print(f"Claude image refinement error: {str(e)}")
            return original_prompt

    def refine_caption(self, caption, context="", platform="instagram"):
        """
        Refine social media captions for engagement
        """
        try:
            system_prompt = f"""You are a social media expert specializing in {platform} engagement optimization."""
            
            user_prompt = f"""Refine this caption for maximum {platform} engagement:

            Original caption: {caption}
            Context: {context}

            Optimize for:
            - Platform-specific engagement patterns
            - Audience connection and relatability
            - Call-to-action effectiveness
            - Hashtag integration readiness

            Return only the refined caption."""

            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=200,
                temperature=0.7,
                system=system_prompt,
                messages=[{
                    "role": "user", 
                    "content": user_prompt
                }]
            )
            
            return message.content[0].text.strip()
            
        except Exception as e:
            print(f"Claude caption refinement error: {str(e)}")
            return caption

    def refine_hashtags(self, hashtags, context="", platform="instagram"):
        """
        Refine hashtag strategies for maximum reach
        """
        try:
            system_prompt = f"""You are a {platform} hashtag optimization expert."""
            
            user_prompt = f"""Optimize these hashtags for {platform}:

            Original hashtags: {hashtags}
            Context: {context}

            Provide optimized hashtag strategy focusing on:
            - Mix of popular and niche hashtags
            - Platform-specific hashtag trends
            - Target audience alignment
            - Engagement potential

            Return as a list of optimized hashtags."""

            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=150,
                temperature=0.5,
                system=system_prompt,
                messages=[{
                    "role": "user", 
                    "content": user_prompt
                }]
            )
            
            result = message.content[0].text.strip()
            return result.split('\n') if '\n' in result else [result]
            
        except Exception as e:
            print(f"Claude hashtag refinement error: {str(e)}")
            return hashtags