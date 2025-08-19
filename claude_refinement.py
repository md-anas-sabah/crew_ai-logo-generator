from anthropic import Anthropic
from decouple import config
import json
from typing import Dict, Any, List


class ClaudeRefinementService:
    def __init__(self):
        self.client = Anthropic(api_key=config('CLAUDE_API_KEY'))
    
    def refine_image_prompt(self, original_prompt: str, content_context: str = "", platform: str = "instagram") -> str:
        """
        Refine image generation prompts using Claude to create world-class prompts for FAL.ai
        """
        system_prompt = """You are an elite Ideogram V2A prompt engineer specializing in creating viral social media visuals. Your expertise lies in crafting prompts that produce stunning, share-worthy images that social media users absolutely love.

CRITICAL REQUIREMENT: You must preserve the EXACT spelling and text from the original prompt. Never change, alter, or "improve" the text content - only enhance the visual description around it.

IDEOGRAM V2A MASTERY RULES:
1. Ideogram V2A excels at high-quality imagery with perfect text rendering
2. Use specific visual descriptors that trigger maximum quality outputs
3. Focus on composition, lighting, and aesthetic trends that go viral
4. Specify clear text placement for perfect typography rendering
5. Match the requested art style while maximizing quality
6. Create Instagram/TikTok-worthy visual appeal

STYLE DETECTION & OPTIMIZATION:
- ANIME/MANGA: "High-quality anime style, studio-grade animation quality, detailed character design, vibrant colors, sharp lineart, professional anime illustration"
- PHOTOREALISTIC: "Photorealistic, natural features, perfect anatomy, professional photography quality"
- CARTOON/STYLIZED: "High-quality cartoon style, professional illustration, clean vector art, vibrant colors"
- LOGO/BRAND: "Professional logo design, crisp graphics, brand-quality imagery"

PERFECT TEXT RENDERING FORMULA (CRITICAL):
- ALWAYS use "bold, crystal-clear text" and "perfect typography"
- ALWAYS specify "perfect spelling, no text errors, crisp lettering"
- Specify exact placement: "centered overlay", "bottom third", "top banner"
- ALWAYS include "high contrast for readability"
- Use "professional font rendering, no blurred text"

VIRAL SOCIAL MEDIA AESTHETICS:
- Dramatic cinematic lighting or studio-quality illumination
- Trending color palettes that pop on social feeds
- Eye-catching compositions using rule of thirds
- High contrast and saturation for mobile viewing
- Clean backgrounds that make text and subjects stand out
- Instagram/TikTok trending visual styles

MAXIMUM QUALITY SPECIFICATIONS:
- ALWAYS include "8K resolution, ultra-detailed, crisp and sharp"
- "Professional grade quality, no artifacts, no distortions"
- "Trending on social media, viral aesthetic appeal"
- "High contrast, vibrant colors, perfect clarity"
- "Studio-quality rendering, masterpiece-level detail"

IDEOGRAM V2A OPTIMIZATION TEMPLATES:

FOR ANIME/STYLIZED:
"High-quality anime style illustration, [detailed scene], studio-grade animation quality, vibrant colors, sharp detailed lineart, featuring bold crystal-clear text '[EXACT TEXT]' with perfect spelling and typography, [text placement], cinematic lighting, 8K resolution, ultra-detailed, trending anime aesthetic, no artifacts, masterpiece quality"

FOR PHOTOREALISTIC:
"Photorealistic [image type], [detailed scene], professional photography, studio lighting, featuring bold crystal-clear text '[EXACT TEXT]' with perfect spelling, [text placement], shot with professional camera, 8K resolution, ultra-detailed, viral social media aesthetic, no artifacts, perfect clarity"

CRITICAL RULES:
- NEVER change spelling of any text in the image
- ALWAYS specify "perfect spelling, no text errors" for text
- Match the requested art style while maximizing quality
- ALWAYS include 8K resolution and ultra-detailed specifications
- Focus on viral, trending visual aesthetics
- Ensure maximum text clarity and contrast"""

        user_prompt = f"""Create a viral-worthy Ideogram V2A prompt that will generate stunning, high-quality social media content:

Original prompt: {original_prompt}
Content context: {content_context}
Platform: {platform}

CRITICAL REQUIREMENTS:
1. Preserve EXACT spelling of any text that appears in the image
2. Detect the art style (anime, photorealistic, cartoon, etc.) and optimize accordingly
3. ALWAYS specify "8K resolution, ultra-detailed, crisp and sharp, no artifacts"
4. ALWAYS include "bold crystal-clear text, perfect spelling, no text errors"
5. ALWAYS specify "high contrast for text readability, professional typography"
6. Include viral social media aesthetics for maximum engagement
7. Use appropriate quality keywords for the detected style

STYLE-SPECIFIC OPTIMIZATION:
- If ANIME/MANGA requested: Use "studio-grade animation quality, detailed character design, sharp lineart, professional anime illustration"
- If PHOTOREALISTIC requested: Use "photorealistic, natural features, professional photography quality"
- If CARTOON/STYLIZED requested: Use "high-quality cartoon style, professional illustration, clean vector art"

Transform this into an Ideogram V2A masterpiece prompt that will generate world-class images with perfect text rendering and maximum viral appeal. Focus on achieving the highest possible quality within the requested style."""

        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1000,
                temperature=0.7,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )
            
            refined_prompt = response.content[0].text.strip()
            return refined_prompt
            
        except Exception as e:
            print(f"Error refining image prompt with Claude: {str(e)}")
            return original_prompt
    
    def refine_caption(self, original_caption: str, content_context: str = "", platform: str = "instagram") -> str:
        """
        Refine social media captions using Claude for maximum engagement
        """
        system_prompt = """You are an expert social media copywriter with a proven track record of creating viral, engaging content. Your captions consistently drive high engagement, conversions, and brand awareness.

Your refined captions should be:
1. Hook-driven (start with attention-grabbing first line)
2. Emotionally engaging and relatable
3. Platform-optimized for maximum reach
4. Include strategic call-to-actions
5. Use storytelling techniques
6. Be conversational and authentic
7. Include strategic line breaks for readability
8. Consider trending topics and current events

Platform-specific optimization:
- Instagram: Visual storytelling, emojis, engaging questions
- Facebook: Community-focused, shareable content
- LinkedIn: Professional insights, thought leadership
- Twitter: Concise, witty, trending topics

Always maintain the brand voice while maximizing engagement potential."""

        user_prompt = f"""Please refine this social media caption to be world-class and highly engaging:

Original caption: {original_caption}
Content context: {content_context}
Platform: {platform}

Transform this into a caption that will maximize engagement, shares, and conversions. Make it compelling, authentic, and optimized for the platform."""

        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1000,
                temperature=0.8,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )
            
            refined_caption = response.content[0].text.strip()
            return refined_caption
            
        except Exception as e:
            print(f"Error refining caption with Claude: {str(e)}")
            return original_caption
    
    def refine_hashtags(self, original_hashtags: List[str], content_context: str = "", platform: str = "instagram") -> List[str]:
        """
        Refine hashtag strategy using Claude for maximum reach and engagement
        """
        system_prompt = """You are a social media growth expert specializing in hashtag strategy and viral content optimization. You understand algorithm behaviors, trending topics, and hashtag performance across platforms.

Your hashtag strategy should include:
1. Mix of trending and niche hashtags
2. Platform-specific optimization
3. Audience-targeted hashtags
4. Brand-relevant hashtags
5. Strategic hashtag volume (optimal for each platform)
6. Community hashtags for engagement
7. Location-based hashtags when relevant

Platform guidelines:
- Instagram: 8-15 hashtags, mix of broad and niche
- LinkedIn: 3-5 professional hashtags
- Twitter: 1-3 relevant hashtags
- Facebook: 1-3 hashtags maximum

Focus on hashtags that will:
- Increase discoverability
- Attract target audience
- Drive engagement
- Build community
- Support brand positioning"""

        hashtags_str = ", ".join(original_hashtags) if original_hashtags else "No hashtags provided"
        
        user_prompt = f"""Please refine this hashtag strategy to maximize reach and engagement:

Original hashtags: {hashtags_str}
Content context: {content_context}
Platform: {platform}

Provide an optimized list of hashtags that will maximize visibility and attract the right audience. Return only the hashtags, one per line, with the # symbol."""

        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=500,
                temperature=0.6,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )
            
            refined_hashtags_text = response.content[0].text.strip()
            # Extract hashtags from the response
            refined_hashtags = [tag.strip() for tag in refined_hashtags_text.split('\n') if tag.strip().startswith('#')]
            
            return refined_hashtags if refined_hashtags else original_hashtags
            
        except Exception as e:
            print(f"Error refining hashtags with Claude: {str(e)}")
            return original_hashtags
    
    def refine_logo_prompt(self, original_prompt: str, brand_context: str = "", logo_style: str = "Combination", format: str = "PNG") -> str:
        """
        Refine logo generation prompts using Claude for world-class professional logo design
        """
        system_prompt = """You are the world's leading logo design expert and Ideogram V2A prompt engineer specializing in creating iconic, professional brand identities. You have designed logos for Fortune 500 companies, successful startups, and prestigious brands worldwide.

LOGO DESIGN MASTERY:
1. Deep understanding of logo psychology, brand positioning, and visual identity theory
2. Expertise in all logo styles: WordMark, LetterMark, Pictorial, Abstract, Combination, Emblem
3. Master of typography psychology, color theory, and scalable design principles
4. Understanding of cross-cultural symbolism and global market appeal
5. Knowledge of logo applications across all mediums and platforms

IDEOGRAM V2A LOGO OPTIMIZATION:
- Ideogram V2A excels at creating professional, scalable logo designs
- Perfect for text rendering, clean typography, and brand-quality imagery
- Responds well to specific design terminology and professional specifications
- Produces logos suitable for print, digital, merchandise, and all applications

LOGO STYLE EXPERTISE:

WORDMARK LOGOS:
"Professional wordmark logo design, elegant typography, custom lettering for [COMPANY], sophisticated font treatment, perfect letter spacing, scalable text design, brand-quality typography, modern/classic letterforms, premium font styling, corporate identity standard"

LETTERMARK LOGOS:
"Minimalist lettermark logo, stylized initials [INITIALS], geometric letter design, sophisticated monogram, clean typography, balanced letterforms, professional initial design, scalable letter symbol, brand monogram identity"

PICTORIAL MARK LOGOS:
"Iconic pictorial logo symbol, recognizable [INDUSTRY] icon, simple yet distinctive imagery, clean vector-style illustration, memorable visual symbol, scalable pictorial mark, professional icon design, brand symbol identity"

ABSTRACT LOGOS:
"Abstract geometric logo design, unique symbolic representation, modern abstract shapes, sophisticated geometry, distinctive visual pattern, scalable abstract mark, conceptual design elements, innovative brand symbol"

COMBINATION MARK LOGOS:
"Professional combination mark logo, [COMPANY] wordmark with symbolic element, integrated text and icon design, balanced typography and imagery, cohesive brand identity system, versatile logo application"

EMBLEM LOGOS:
"Classic emblem logo design, badge-style brand mark, traditional crest elements, enclosed design format, institutional logo style, premium badge identity, authoritative brand emblem"

CRITICAL LOGO SPECIFICATIONS:
- ALWAYS specify "professional logo design, brand-quality imagery"
- ALWAYS include "scalable vector appearance, clean lines, crisp details"
- ALWAYS mention "suitable for business cards to billboards"
- ALWAYS specify "no gradients, solid colors, high contrast"
- Include "timeless design principles, memorable and distinctive"
- Specify "corporate identity standard, premium brand quality"

COLOR & TECHNICAL REQUIREMENTS:
- Specify color psychology aligned with brand positioning
- Always mention "works in full color and single color versions"
- Include "high contrast for visibility, readable at all sizes"
- Specify "professional color palette, brand-appropriate tones"

IDEOGRAM V2A LOGO FORMULA:
"Professional [STYLE] logo design for [COMPANY], [specific design elements], brand-quality imagery, scalable vector appearance, clean geometric lines, perfect typography, [color specifications], suitable for all applications from business cards to billboards, timeless and memorable design, corporate identity standard, high contrast visibility, premium brand identity"

CRITICAL RULES:
- Match the requested logo style exactly
- Ensure scalability and versatility for all applications
- Focus on timeless design principles over trends
- Prioritize memorability and brand recognition
- Consider global market appeal and cultural sensitivity"""

        user_prompt = f"""Create a world-class Ideogram V2A prompt for generating a professional, iconic logo:

Original prompt: {original_prompt}
Brand context: {brand_context}
Logo style: {logo_style}
Output format: {format}

LOGO REQUIREMENTS:
1. Professional brand identity suitable for Fortune 500 standards
2. Perfect alignment with the specified logo style ({logo_style})
3. Scalable design that works from favicon to billboard size
4. Timeless design principles for long-term brand building
5. High contrast and visibility across all applications
6. Brand-appropriate color psychology and typography
7. Memorable and distinctive visual identity
8. Cross-cultural appeal and market versatility

TRANSFORM REQUIREMENTS:
- Use professional logo design terminology
- Specify exact logo style optimization for {logo_style}
- Include technical specifications for scalability
- Add brand psychology elements for market positioning
- Ensure Ideogram V2A produces premium-quality results
- Focus on creating an iconic, recognizable brand mark

Create an Ideogram V2A masterpiece prompt that will generate a world-class, professional logo that elevates the brand and drives business success."""

        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1200,
                temperature=0.7,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )
            
            refined_prompt = response.content[0].text.strip()
            return refined_prompt
            
        except Exception as e:
            print(f"Error refining logo prompt with Claude: {str(e)}")
            return original_prompt
    
    def analyze_logo_effectiveness(self, logo_data: Dict[str, Any], company_info: Dict[str, Any]) -> str:
        """
        Analyze why a specific logo design is perfect for the company using brand psychology
        """
        system_prompt = """You are the world's leading brand strategist and logo psychology expert. You have analyzed thousands of successful brand identities and understand exactly why certain logos achieve market success while others fail.

Your expertise includes:
1. Brand psychology and consumer perception theory
2. Logo design psychology and visual communication principles
3. Market positioning and competitive differentiation strategies
4. Cross-cultural symbolism and global brand appeal
5. Typography psychology and color theory in branding
6. Logo scalability and application effectiveness
7. Long-term brand building and equity development
8. Industry-specific logo performance factors

Your analysis should cover:
- Brand psychology impact and emotional triggers
- Target audience appeal and demographic alignment
- Competitive differentiation and market positioning
- Visual memorability and recognition factors
- Scalability and application versatility
- Industry appropriateness and professional standards
- Long-term brand building potential
- Cross-platform effectiveness (digital, print, merchandise)
- Color psychology and cultural considerations
- Typography psychology and readability factors

Provide strategic insights that demonstrate deep understanding of why this specific logo will drive business success and brand recognition."""
        
        # Extract key information
        company_name = company_info.get('company_name', 'the company')
        company_description = company_info.get('company_description', '')
        industry = company_info.get('industry_keywords', '')
        brand_tone = company_info.get('brand_tone', '')
        preferred_color = company_info.get('preferred_color', '')
        logo_style = logo_data.get('logo_style', 'Unknown')
        
        user_prompt = f"""Analyze why this logo design is strategically perfect for this company:

COMPANY PROFILE:
- Company Name: {company_name}
- Description: {company_description}
- Industry: {industry}
- Brand Tone: {brand_tone}
- Color Preference: {preferred_color}

LOGO DESIGN:
- Style: {logo_style}
- Design Elements: Based on the refined prompt and generated imagery
- Professional quality with brand-appropriate styling

PROVIDE COMPREHENSIVE ANALYSIS:

1. BRAND PSYCHOLOGY IMPACT
   - How this logo triggers the right emotional responses
   - Psychological alignment with target audience
   - Brand personality expression and market positioning

2. COMPETITIVE DIFFERENTIATION
   - How this logo stands out in the industry
   - Unique positioning against competitors
   - Market memorability and recognition factors

3. PROFESSIONAL EFFECTIVENESS
   - Why this logo style works for this business type
   - Industry appropriateness and credibility factors
   - Professional standards and corporate image impact

4. SCALABILITY & APPLICATION
   - Versatility across all business applications
   - Digital and print performance optimization
   - Long-term brand building potential

5. COLOR & TYPOGRAPHY PSYCHOLOGY
   - Strategic color choices and cultural impact
   - Typography psychology and readability factors
   - Visual hierarchy and brand communication

6. MARKET SUCCESS POTENTIAL
   - Target audience appeal and demographic alignment
   - Cross-cultural effectiveness and global scalability
   - Long-term brand equity development

Provide specific, actionable insights that demonstrate why this logo will drive business success, customer recognition, and brand loyalty. Focus on strategic value and market effectiveness."""

        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
                temperature=0.8,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )
            
            logo_analysis = response.content[0].text.strip()
            return logo_analysis
            
        except Exception as e:
            print(f"Error analyzing logo effectiveness with Claude: {str(e)}")
            return f"This {logo_style} logo design effectively represents {company_name} through professional brand identity principles, combining visual appeal with strategic market positioning for optimal business impact."
    
    def refine_all_content(self, content_data: Dict[str, Any], platform: str = "instagram") -> Dict[str, Any]:
        """
        Refine all content elements (prompt, caption, hashtags) in one go
        """
        refined_content = content_data.copy()
        
        # Extract context for better refinement
        context = f"Platform: {platform}, Content type: {content_data.get('content_type', 'social media post')}"
        
        # Refine image prompt if present
        if 'image_prompt' in content_data:
            refined_content['image_prompt'] = self.refine_image_prompt(
                content_data['image_prompt'], 
                context, 
                platform
            )
            refined_content['original_image_prompt'] = content_data['image_prompt']
        
        # Refine caption if present
        if 'caption' in content_data:
            refined_content['caption'] = self.refine_caption(
                content_data['caption'], 
                context, 
                platform
            )
            refined_content['original_caption'] = content_data['caption']
        
        # Refine hashtags if present
        if 'hashtags' in content_data:
            refined_content['hashtags'] = self.refine_hashtags(
                content_data['hashtags'], 
                context, 
                platform
            )
            refined_content['original_hashtags'] = content_data['hashtags']
        
        refined_content['claude_refined'] = True
        refined_content['refinement_timestamp'] = str(json.dumps({"timestamp": "now"}))
        
        return refined_content