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
            
            Generate exactly 3 strategic logo concept directions that leverage different psychological approaches:
            
            IMPORTANT: All concepts must use the selected logo style "{logo_style}" - do not recommend different styles.
            
            Each concept should include:
            - Brand positioning strategy and market differentiation approach
            - Target audience psychological triggers and emotional appeal
            - How the {logo_style} style will be optimized for this concept
            - Color psychology reasoning and palette recommendations
            - Typography psychology and font personality alignment (for text elements)
            - Competitive differentiation strategy
            - Long-term brand building potential
            
            Format your response as:
            
            **Concept 1: [Strategic Theme]**
            Logo Style: {logo_style} - [How this style supports the strategic theme]
            Brand Psychology: [Psychological positioning and emotional triggers]
            Color Strategy: [Color psychology and palette recommendations]
            Target Impact: [Expected market impact and audience response]
            Differentiation: [How this approach stands out from competitors]
            
            **Concept 2: [Strategic Theme]**
            Logo Style: {logo_style} - [How this style supports the strategic theme]
            Brand Psychology: [Psychological positioning and emotional triggers]
            Color Strategy: [Color psychology and palette recommendations]
            Target Impact: [Expected market impact and audience response]
            Differentiation: [How this approach stands out from competitors]
            
            **Concept 3: [Strategic Theme]**
            Logo Style: {logo_style} - [How this style supports the strategic theme]
            Brand Psychology: [Psychological positioning and emotional triggers]
            Color Strategy: [Color psychology and palette recommendations]
            Target Impact: [Expected market impact and audience response]
            Differentiation: [How this approach stands out from competitors]
            
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
            
            LOGO GENERATION PROCESS:
            1. Use the generate_logo tool with these exact parameters:
               - prompt: "Professional [logo_style] logo for [company_name], [detailed design description]"
               - logo_style: "{logo_style}"
               - company_name: "{company_name}"
            2. Use the generate_svg_logo tool with the same parameter format for vector version
            3. Ensure both formats maintain design integrity and professional quality
            4. Create detailed, professional logo design descriptions
            
            PROFESSIONAL PROMPT STRUCTURE:
            Create logo prompts that include:
            - Professional logo design terminology
            - Specific style requirements for the chosen logo type
            - Company industry and positioning context
            - Color psychology and brand-appropriate palette
            - Scalability and application requirements
            - Premium quality specifications for business use
            
            EXAMPLE TOOL USAGE:
            Action: generate_logo
            Action Input: {{
              "prompt": "Professional emblem logo for Marqait, featuring classic badge design with purple color scheme, AI marketing automation company, modern professional aesthetic, Fortune 500 quality",
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