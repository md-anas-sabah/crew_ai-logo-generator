import anthropic
from decouple import config

class ClaudeRefinementService:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=config("CLAUDE_API_KEY"))
    
    def refine_logo_prompt(self, original_prompt, logo_context, logo_style, format="PNG", company_name="", industry="", preferred_color="", brand_tone=""):
        """
        Advanced logo prompt refinement using Claude Sonnet 3.5 with dynamic style adaptation and industry-specific constraints
        """
        try:
            # Dynamic style-specific instructions
            style_specific_instructions = self._get_style_specific_instructions(logo_style)
            
            # Industry-specific constraints
            industry_constraints = self._get_industry_constraints(industry)
            
            # Color palette specifications
            color_specifications = self._get_color_specifications(preferred_color, industry, brand_tone)
            
            # Font recommendations for text-based logos
            font_recommendations = self._get_font_recommendations(logo_style, brand_tone, industry)
            
            system_prompt = f"""You are a world-class logo design expert specializing in Fortune 500 brand identity creation. 
            Your task is to transform basic logo concepts into mathematically precise, industry-optimized design specifications.

            🎯 LOGO STYLE FOCUS: {logo_style}
            {style_specific_instructions}

            🏢 INDUSTRY OPTIMIZATION: {industry}
            {industry_constraints}

            🎨 COLOR PSYCHOLOGY REQUIREMENTS:
            {color_specifications}

            📝 TYPOGRAPHY SPECIFICATIONS:
            {font_recommendations}

            ⚠️ CRITICAL TEXT REQUIREMENTS - ZERO TOLERANCE POLICY:
            - ONLY the exact text "{company_name}" is allowed - NO OTHER TEXT WHATSOEVER
            - FORBIDDEN: APIC, API, acronyms, abbreviations, initials, codes, placeholders
            - FORBIDDEN: descriptions, slogans, taglines, explanatory text, sample text
            - FORBIDDEN: Lorem ipsum, placeholder text, generic text, template text
            - FORBIDDEN: foreign languages, symbols as text, decorative text elements
            - MANDATORY: Perfect spelling "{company_name}" - verify 100% accuracy
            - MANDATORY: English language only for the company name
            - MANDATORY: Real LOGO design, not illustration or artwork
            - NO TEXT ADDITIONS: Do not add any text beyond "{company_name}"

            🎨 VISUAL REQUIREMENTS:
            - 100% TRANSPARENT BACKGROUND - completely isolated logo mark
            - Mathematical precision using golden ratio and fibonacci principles
            - Trademark-ready uniqueness and competitive differentiation
            - Scalable from 16px favicon to 100ft billboard perfection
            - Fortune 500 reproduction standards

            Context: {logo_context}
            Format: {format}
            """
            
            user_prompt = f"""Transform this into a world-class {logo_style} logo specification:

            Original: {original_prompt}
            Company: "{company_name}"
            Industry: {industry}
            Brand Tone: {brand_tone}
            Color Preference: {preferred_color}

            CREATE COMPREHENSIVE SPECIFICATION INCLUDING:

            🎯 POSITIVE REQUIREMENTS:
            1. {style_specific_instructions}
            2. {color_specifications}
            3. {font_recommendations}
            4. {industry_constraints}
            5. Mathematical golden ratio composition
            6. Professional Fortune 500 quality standards
            7. Company name "{company_name}" in English only
            8. Transparent background isolation
            9. Trademark-ready uniqueness

            ⛔ NEGATIVE PROMPT (EXPLICITLY FORBIDDEN):
            - Any text except "{company_name}" - NO EXCEPTIONS
            - APIC, API, acronyms, abbreviations, initials, codes
            - Placeholder text: Lorem ipsum, sample text, generic text
            - Template text: Company Name, Your Text Here, Example Text
            - Slogans, taglines, descriptions, explanations, marketing copy
            - Background elements, environments, scenes, contexts
            - Construction grids, guides, rulers, alignment helpers, design templates
            - Decorative backgrounds, textures, gradients, patterns
            - Foreign language text, symbols as text, decorative typography
            - Illustrations or artwork (must be actual logo)
            - Shadows, lighting effects, 3D elements, special effects
            - Multiple logo variations in single image
            - Watermarks, copyright notices, credits, attribution text
            - ANY TEXT OTHER THAN "{company_name}" IS STRICTLY FORBIDDEN

            FINAL CRITICAL INSTRUCTION: The logo must contain ONLY the text "{company_name}" and NOTHING else. Do not add APIC, API, acronyms, or any other text. This is a ZERO TOLERANCE requirement.
            
            Provide the refined prompt as a single, comprehensive design specification ready for professional {logo_style} logo generation."""

            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=700,
                temperature=0.1,
                system=system_prompt,
                messages=[{
                    "role": "user", 
                    "content": user_prompt
                }]
            )
            
            return message.content[0].text.strip()
            
        except Exception as e:
            print(f"Claude refinement error: {str(e)}")
            # Fallback to enhanced original prompt with strict text requirements
            return f"Professional {logo_style} logo design with ONLY the text '{company_name}' in English - NO APIC, NO API, NO acronyms, NO abbreviations, NO other text whatsoever, {original_prompt}, Fortune 500 quality, mathematical precision, real logo not illustration, 100% TRANSPARENT BACKGROUND, NO GRIDS, NO DECORATIVE BACKGROUNDS, NO ENVIRONMENTS, NO SCENES, completely isolated logo mark only, clean standalone logo like Apple or Nike logos, company name '{company_name}' only"
    
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

    def _get_style_specific_instructions(self, logo_style):
        """Dynamic style-specific instructions for optimal logo generation"""
        instructions = {
            "WordMark": """
            - Focus on exceptional typography and custom lettering mastery
            - Emphasize kerning perfection, letter-spacing optimization, and optical corrections
            - Create memorable typographic treatment with mathematical precision
            - Consider x-height, ascender/descender ratios, and readability at all sizes
            - Integrate subtle ligatures or custom letterforms for distinctiveness
            - Ensure perfect legibility from business card to billboard scale
            """,
            
            "LetterMark": """
            - Design elegant monogram with geometric precision and visual balance
            - Focus on mathematical relationships between letter forms
            - Create distinctive initial combinations with perfect optical weight
            - Ensure circular, square, or golden ratio proportional containers
            - Integrate negative space utilization for enhanced recognition
            - Optimize for exceptional scalability in square formats
            """,
            
            "Pictorial": """
            - Develop iconic, instantly recognizable symbolic representation
            - Create simple yet distinctive imagery with cultural universality
            - Focus on symbolic meaning and metaphorical brand connection
            - Ensure the icon communicates core business values intuitively
            - Design for maximum memorability and instant brand association
            - Optimize symbol to work independently without text support
            """,
            
            "Abstract": """
            - Design unique geometric or organic abstract forms with deeper meaning
            - Create symbolic representation through advanced shape psychology
            - Focus on mathematical precision and artistic differentiation
            - Develop forms that convey brand personality through visual language
            - Ensure cultural sensitivity and universal aesthetic appeal
            - Create proprietary visual elements for complete market uniqueness
            """,
            
            "Combination": """
            - Integrate text and symbol in perfect mathematical harmony
            - Create flexible modular system working independently or combined
            - Balance visual weight distribution between textual and iconic elements
            - Ensure both components maintain strength when separated
            - Design responsive logo system for various application contexts
            - Optimize for seamless scalability across all business touchpoints
            """,
            
            "Emblem": """
            - Design classic badge, crest, or seal with traditional craftsmanship excellence
            - Create authoritative and trustworthy visual identity with heritage appeal
            - Focus on intricate detail balance with essential simplicity for scalability
            - Ensure premium feel with sophisticated border and internal organization
            - Integrate heraldic principles with contemporary brand sophistication
            - Maintain readability despite detailed emblem complexity at small sizes
            """
        }
        return instructions.get(logo_style, "Professional logo design with style-specific optimization")

    def _get_industry_constraints(self, industry):
        """Industry-specific design constraints and psychological requirements"""
        if not industry:
            return "Professional cross-industry adaptability with universal appeal"
            
        constraints = {
            "finance": "Evoke trust, stability, and security. Avoid playful or whimsical elements. Use solid, geometric forms suggesting reliability and conservative strength.",
            "technology": "Convey innovation, cutting-edge advancement, and digital sophistication. Incorporate clean, minimalist aesthetics with futuristic undertones.",
            "healthcare": "Communicate care, healing, and medical expertise. Use calming colors and forms suggesting life, wellness, and professional competence.",
            "education": "Express knowledge, growth, and academic excellence. Balance tradition with innovation, suggesting learning progression and intellectual development.",
            "legal": "Project authority, justice, and professional expertise. Use classical elements suggesting law, order, and institutional trustworthiness.",
            "retail": "Appeal to consumer desire and shopping experience. Create approachable, friendly design encouraging purchase behavior and brand loyalty.",
            "food": "Stimulate appetite and convey freshness, quality, and taste. Use organic forms and colors associated with nutrition and culinary excellence.",
            "energy": "Suggest power, sustainability, and forward momentum. Balance environmental responsibility with industrial strength and reliability.",
            "consulting": "Convey expertise, strategy, and professional guidance. Create sophisticated design suggesting analytical thinking and business acumen.",
            "real estate": "Express solidity, investment value, and lifestyle aspiration. Use architectural elements suggesting security, growth, and premium value."
        }
        
        industry_lower = industry.lower()
        for key, constraint in constraints.items():
            if key in industry_lower:
                return constraint
                
        return f"Industry-optimized design for {industry} sector with professional market positioning"

    def _get_color_specifications(self, preferred_color, industry, brand_tone):
        """Enhanced color palette specifications with hex codes and psychological justification"""
        if not preferred_color:
            # Industry-based color recommendations
            industry_colors = {
                "finance": "Deep blue (#003366) for trust, gray (#4A4A4A) for stability, gold (#FFD700) for premium value",
                "technology": "Electric blue (#0066FF) for innovation, silver (#C0C0C0) for tech sophistication, white (#FFFFFF) for clean minimalism",
                "healthcare": "Medical blue (#0080FF) for care, green (#00AA55) for health, white (#FFFFFF) for cleanliness and purity",
                "legal": "Navy blue (#000080) for authority, burgundy (#800020) for tradition, gold (#B8860B) for prestige",
                "energy": "Forest green (#228B22) for sustainability, orange (#FF8C00) for energy, blue (#4169E1) for reliability"
            }
            
            industry_lower = industry.lower() if industry else ""
            for key, colors in industry_colors.items():
                if key in industry_lower:
                    return f"Primary palette: {colors}. Secondary: Complementary neutrals for versatility and professional reproduction."
            
            return "Strategic color palette optimized for brand psychology, industry positioning, and global cultural sensitivity"
        else:
            return f"Primary color: {preferred_color} with professional secondary palette. Include specific hex codes and psychological justification for color choices."

    def _get_font_recommendations(self, logo_style, brand_tone, industry):
        """Specific font recommendations for text-based logos with psychological rationale"""
        if logo_style in ["WordMark", "LetterMark", "Combination", "Emblem"]:
            
            tone_fonts = {
                "modern": "Contemporary sans-serif like 'Montserrat', 'Lato', or 'Open Sans' for clean innovation and approachability",
                "professional": "Classic serif like 'Times New Roman', 'Georgia', or 'Playfair Display' for authority and trustworthiness",
                "elegant": "Sophisticated serif like 'Didot', 'Bodoni', or 'Trajan Pro' for luxury and premium positioning",
                "friendly": "Rounded sans-serif like 'Comfortaa', 'Nunito', or 'Poppins' for accessibility and warmth",
                "technical": "Geometric sans-serif like 'Futura', 'Avenir', or 'Proxima Nova' for precision and systematic thinking",
                "creative": "Unique display font with custom modifications for artistic expression and brand differentiation"
            }
            
            # Match brand tone to font recommendation
            tone_lower = brand_tone.lower() if brand_tone else "professional"
            for key, fonts in tone_fonts.items():
                if key in tone_lower:
                    return f"Typography: {fonts}. Rationale: Aligns with {brand_tone} brand positioning and {industry} industry expectations."
            
            return "Professional typography selection with custom letterform modifications for unique brand recognition and optimal readability"
        else:
            return "Typography considerations: If text elements are included, ensure perfect integration with symbolic elements"