from crewai import Task
from textwrap import dedent


class LogoDesignTasks:
    def __tip_section(self):
        return "If you do your BEST WORK, I'll give you a $10,000 commission!"

    def brand_strategy_task(self, agent, company_name, company_description, logo_style, industry_keywords="", brand_tone="", preferred_color=""):
        return Task(
            description=dedent(
                f"""
            Analyze the company profile and develop comprehensive brand strategy insights for logo design:
            
            COMPANY PROFILE:
            - Company Name: "{company_name}"
            - Company Description: "{company_description}"
            - Selected Logo Style: "{logo_style}"
            - Industry Keywords: "{industry_keywords}"
            - Brand Tone: "{brand_tone}"
            - Preferred Color: "{preferred_color}"
            
            Generate 3 WORLD-CLASS strategic logo concepts using Fortune 500 brand psychology principles:
            
            CRITICAL: All concepts must optimize the "{logo_style}" style for maximum business impact.
            
            Each concept must include:
            🎯 STRATEGIC BRAND POSITIONING:
            - Market psychology analysis and competitive warfare strategy
            - Target audience neuroscience triggers and emotional hijacking
            - Cultural symbolism optimization for global market domination
            - Brand personality alignment with customer aspirations
            
            🧠 PSYCHOLOGICAL ENGINEERING:
            - Subconscious messaging through visual hierarchy and composition
            - Color psychology with cultural sensitivity and accessibility compliance
            - Typography psychology creating trust/innovation/luxury perceptions
            - Subliminal brand messaging through strategic design choices
            
            💎 {logo_style.upper()} OPTIMIZATION MASTERY:
            - Mathematical precision using golden ratio and fibonacci principles
            - Scalability engineering ensuring impact from favicon to billboard
            - Industry-specific symbolism creating instant market recognition
            - Technical excellence meeting Fortune 500 reproduction standards
            
            🏆 COMPETITIVE DIFFERENTIATION:
            - Visual supremacy analysis against top 3 industry competitors
            - Proprietary brand language development for market ownership
            - Trademark viability and legal uniqueness verification
            - Long-term brand equity potential and cultural icon status
            
            📈 BUSINESS IMPACT METRICS:
            - Brand recognition enhancement projections
            - Market positioning advancement strategy
            - Customer conversion psychology optimization
            - Global expansion readiness assessment
            
            Format your response as:
            
            **🏆 CONCEPT 1: [Strategic Theme - e.g., "Market Dominance Through Premium Authority"]**
            {logo_style} Optimization: [Mathematical precision and scalability engineering approach]
            Psychological Warfare: [Target audience neuroscience triggers and emotional hijacking]
            Color Psychology: [Pantone-level specifications with cultural sensitivity analysis]
            Competitive Supremacy: [Visual differentiation strategy against top 3 industry competitors]
            Business Impact: [Brand recognition enhancement and conversion optimization projections]
            Global Readiness: [Cross-cultural appeal and international market expansion potential]
            
            **🚀 CONCEPT 2: [Strategic Theme - e.g., "Innovation Leadership Through Visual Breakthrough"]**
            {logo_style} Mastery: [Golden ratio principles and technical excellence specifications]
            Brand Psychology: [Subliminal messaging and customer aspiration alignment]
            Cultural Symbolism: [Industry-specific iconography with universal comprehension]
            Market Positioning: [Premium brand equity development and long-term value creation]
            Differentiation Matrix: [Proprietary visual language and trademark viability]
            ROI Potential: [Brand value enhancement and market share expansion projections]
            
            **💎 CONCEPT 3: [Strategic Theme - e.g., "Cultural Icon Status Through Timeless Excellence"]**
            {logo_style} Excellence: [Fortune 500 reproduction standards and scalability mastery]
            Neuroscience Triggers: [Subconscious brand messaging and emotional connection optimization]
            Color Mastery: [Advanced color theory with accessibility compliance and global appeal]
            Competitive Analysis: [Visual supremacy strategy and market ownership potential]
            Legacy Building: [50-year brand longevity and cultural icon development pathway]
            Global Domination: [International market psychology and cross-cultural effectiveness]
            
            {self.__tip_section()}
            
            Ensure each concept is strategically unique and aligned with professional brand identity principles.
        """
            ),
            expected_output="3 strategic logo concept directions with brand psychology insights and style recommendations",
            agent=agent,
        )

    def logo_design_task(self, agent, selected_concept, company_name, company_description, logo_style, brand_context):
        return Task(
            description=dedent(
                f"""
            Based on the selected brand concept: "{selected_concept}"
            Company Information:
            - Company Name: "{company_name}"
            - Company Description: "{company_description}"
            - Selected Logo Style: "{logo_style}"
            - Brand Context: "{brand_context}"
            
            Create a world-class professional logo design that perfectly represents the company's brand identity.
            
            LOGO DESIGN REQUIREMENTS:
            
            STYLE-SPECIFIC OPTIMIZATION:
            
            FOR WORDMARK LOGOS:
            - Focus on sophisticated typography and custom lettering
            - Emphasize readability and brand personality through font choice
            - Create memorable typographic treatment that works across all applications
            - Consider letter spacing, weight, and overall typographic harmony
            
            FOR LETTERMARK LOGOS:
            - Design elegant monogram or initial-based mark
            - Focus on geometric balance and visual weight
            - Create distinctive letter combinations that are instantly recognizable
            - Ensure scalability from favicon to signage
            
            FOR PICTORIAL MARK LOGOS:
            - Develop iconic, instantly recognizable symbol
            - Create simple yet distinctive imagery relevant to the industry
            - Focus on memorability and symbolic meaning
            - Ensure the icon works independently of company name
            
            FOR ABSTRACT LOGOS:
            - Design unique geometric or organic abstract forms
            - Create symbolic meaning through shape psychology
            - Focus on differentiation and modern aesthetic appeal
            - Develop forms that convey brand personality and values
            
            FOR COMBINATION MARK LOGOS:
            - Integrate text and symbol in harmonious composition
            - Create flexible system that works with symbol alone or combined
            - Balance visual weight between text and icon elements
            - Ensure both elements work independently when needed
            
            FOR EMBLEM LOGOS:
            - Design classic badge or crest-style mark
            - Create authoritative and trustworthy visual identity
            - Focus on traditional craftsmanship and premium feel
            - Ensure readability at various sizes despite detailed nature
            
            TECHNICAL SPECIFICATIONS:
            - Generate both PNG (1024x1024px) and SVG vector formats
            - Ensure perfect scalability from business card to billboard
            - Create high contrast design for optimal visibility
            - Use professional color palette aligned with brand strategy
            - Prioritize timeless design principles over trendy elements
            
            BRAND INTEGRATION:
            - Reflect company personality and industry positioning
            - Appeal to target audience demographic and psychographics
            - Differentiate from competitors while honoring industry conventions
            - Support long-term brand building and recognition goals
            
            🚀 DUAL-AI PROFESSIONAL LOGO GENERATION PROTOCOL:
            
            PHASE 1 - STRATEGIC DESIGN ENGINEERING:
            1. Analyze company requirements for mathematical composition opportunities
            2. Engineer professional prompt using Fortune 500 design principles
            3. Integrate golden ratio, color psychology, and cultural symbolism
            4. Optimize for dual-AI rendering capabilities (Ideogram V2A + Qwen)
            5. Ensure transparent background and clean standalone design requirements
            
            PHASE 2 - DUAL-MODEL LOGO GENERATION:
            Execute BOTH logo generation tools to leverage dual-AI enhancement:
            
            PRIMARY MODEL - Execute generate_svg_logo tool with COMPREHENSIVE parameters:
               - prompt: "Professional {logo_style} logo design for {company_name} in English text only, real logo not illustration, mathematical precision, golden ratio composition, Fortune 500 quality standards, trademark-ready uniqueness, scalability engineering, competitive differentiation, transparent background, no grid lines, no background elements, clean standalone logo, company name in English only"
               - logo_style: "{logo_style}"
               - company_name: "{company_name}"
            
            SECONDARY MODEL - Execute generate_qwen_logo tool for alternative approach:
               - prompt: "Professional {logo_style} logo design for {company_name} in English text only, real logo not illustration, mathematical precision, golden ratio composition, Fortune 500 quality standards, trademark-ready uniqueness, scalability engineering, competitive differentiation, transparent background, no grid lines, no background elements, clean standalone logo, company name in English only"
               - logo_style: "{logo_style}"
               - company_name: "{company_name}"
            
            PHASE 3 - QUALITY VERIFICATION & SELECTION:
            1. Verify both logos meet professional standards with transparent backgrounds
            2. Ensure both contain only English company name text
            3. Select the superior logo based on quality, clarity, and professional appearance
            4. Return the best result from dual-AI generation
            
            PROFESSIONAL PROMPT STRUCTURE:
            Create logo prompts that include:
            - Professional logo design terminology
            - Specific style requirements for the chosen logo type
            - Company industry and positioning context
            - Color psychology and brand-appropriate palette
            - Scalability and application requirements
            - Premium quality specifications for business use
            
            🚨 CRITICAL LOGO REQUIREMENTS:
            • ONLY include the exact company name "{company_name}" in ENGLISH - NO other text
            • Perfect spelling verification - company name must be 100% accurate
            • Font selection based on company personality and industry psychology
            • NO descriptions, taglines, explanations, or marketing copy in any language
            • Typography that enhances brand recognition and memorability
            • Clean, professional presentation suitable for all applications
            • Company name text MUST be in English language only
            • Design must be an actual LOGO, not an illustration or artwork
            • TRANSPARENT BACKGROUND - no solid backgrounds, grids, or decorative elements
            • Remove all grid lines, background textures, and additional visual elements
            • Logo should be standalone and isolated without any background elements
            • Generate as single PNG or SVG file with transparent background only
            
            EXAMPLE DUAL-AI TOOL USAGE:
            
            PRIMARY MODEL:
            Action: generate_svg_logo
            Action Input: {{
              "prompt": "Professional emblem logo featuring the company name 'Marqait' in English text only, perfect typography, classic badge design with purple color scheme, Fortune 500 quality, mathematical precision composition, brand-appropriate font psychology, transparent background, no grid lines, no background elements, clean standalone logo, real logo not illustration",
              "logo_style": "Emblem", 
              "company_name": "Marqait"
            }}
            
            SECONDARY MODEL:
            Action: generate_qwen_logo
            Action Input: {{
              "prompt": "Professional emblem logo featuring the company name 'Marqait' in English text only, perfect typography, classic badge design with purple color scheme, Fortune 500 quality, mathematical precision composition, brand-appropriate font psychology, transparent background, no grid lines, no background elements, clean standalone logo, real logo not illustration",
              "logo_style": "Emblem", 
              "company_name": "Marqait"
            }}
            
            QUALITY STANDARDS:
            - Fortune 500 company logo quality standards
            - Suitable for all business applications (digital, print, merchandise, signage)
            - Immediately recognizable and memorable
            - Timeless design that won't require frequent updates
            - Professional, trustworthy, and market-appropriate
            
            {self.__tip_section()}
            
            Generate professional logo files and return complete design specifications.
        """
            ),
            expected_output="Professional logo design in both PNG and SVG formats with complete technical specifications",
            agent=agent,
        )

    def brand_analysis_task(self, agent, logo_data, company_info):
        return Task(
            description=dedent(
                f"""
            Analyze the completed logo design and provide comprehensive brand strategy insights:
            
            LOGO DESIGN DATA:
            {logo_data}
            
            COMPANY INFORMATION:
            {company_info}
            
            Provide a detailed analysis explaining why this specific logo design is strategically perfect for this company.
            
            COMPREHENSIVE ANALYSIS REQUIREMENTS:
            
            ## 1. BRAND PSYCHOLOGY & EMOTIONAL IMPACT
            - Analyze how the logo triggers the right emotional responses in target audience
            - Explain the psychological alignment between design elements and brand positioning
            - Detail how visual elements communicate brand personality and values
            - Assess the logo's ability to create emotional connection with customers
            
            ## 2. COMPETITIVE DIFFERENTIATION STRATEGY  
            - Compare positioning against industry competitors
            - Explain how the logo creates unique market positioning
            - Analyze memorable features that aid brand recognition
            - Assess differentiation strength in crowded marketplace
            
            ## 3. PROFESSIONAL EFFECTIVENESS & CREDIBILITY
            - Evaluate industry appropriateness and professional standards
            - Analyze credibility factors and trustworthiness signals
            - Assess corporate image impact and business presentation value
            - Review alignment with target market expectations
            
            ## 4. SCALABILITY & APPLICATION VERSATILITY
            - Analyze performance across all business applications
            - Evaluate digital and print reproduction quality
            - Assess readability and recognition at various sizes
            - Review adaptability for different marketing materials
            
            ## 5. COLOR & TYPOGRAPHY PSYCHOLOGY
            - Explain strategic color choices and cultural impact
            - Analyze typography psychology and readability factors
            - Detail visual hierarchy and brand communication effectiveness
            - Assess color versatility and reproduction considerations
            
            ## 6. MARKET SUCCESS POTENTIAL & ROI
            - Evaluate target audience appeal and demographic alignment
            - Assess cross-cultural effectiveness and global scalability
            - Analyze long-term brand equity development potential
            - Review business impact and marketing effectiveness
            
            ## 7. IMPLEMENTATION RECOMMENDATIONS
            - Provide specific usage guidelines for optimal impact
            - Recommend brand application strategies
            - Suggest marketing integration approaches
            - Outline brand protection and consistency measures
            
            ANALYSIS DEPTH REQUIREMENTS:
            - Provide specific, evidence-based insights (not generic statements)
            - Include actionable recommendations for brand implementation
            - Demonstrate deep understanding of logo design psychology
            - Show clear connection between design choices and business outcomes
            - Reference industry best practices and successful brand examples
            - Quantify expected impact where possible
            
            FORMAT:
            Create a professional brand analysis report that could be presented to C-level executives, demonstrating the strategic value and market effectiveness of this logo investment.
            
            {self.__tip_section()}
            
            Deliver insights that prove this logo will drive business success and brand recognition.
        """
            ),
            expected_output="Comprehensive brand analysis explaining why this logo design is strategically perfect for the company",
            agent=agent,
        )

    def logo_optimization_task(self, agent, initial_logo, feedback, company_context):
        return Task(
            description=dedent(
                f"""
            Optimize the logo design based on specific feedback and requirements:
            
            INITIAL LOGO DATA:
            {initial_logo}
            
            OPTIMIZATION FEEDBACK:
            {feedback}
            
            COMPANY CONTEXT:
            {company_context}
            
            Refine and optimize the logo design to address specific concerns while maintaining brand integrity.
            
            OPTIMIZATION FOCUS AREAS:
            - Color adjustments for better brand alignment
            - Typography refinements for improved readability
            - Symbol modifications for enhanced recognition
            - Scalability improvements for various applications
            - Style adjustments while maintaining core brand identity
            
            PROCESS:
            1. Analyze the feedback and identify specific improvement areas
            2. Maintain the core brand strategy while addressing concerns
            3. Generate optimized version using refined prompts
            4. Ensure improvements don't compromise overall design integrity
            
            {self.__tip_section()}
            
            Deliver an optimized logo that addresses feedback while enhancing brand effectiveness.
        """
            ),
            expected_output="Optimized logo design with improvements based on specific feedback",
            agent=agent,
        )