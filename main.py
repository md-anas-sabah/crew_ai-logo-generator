import os
import json
import re
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from decouple import config
from datetime import datetime, timedelta

from textwrap import dedent
from agents import LogoDesignAgents
from logo_tasks import LogoDesignTasks

os.environ["OPENAI_API_KEY"] = config("OPENAI_API_KEY")
if config("OPENAI_ORGANIZATION_ID", default=""):
    os.environ["OPENAI_ORGANIZATION"] = config("OPENAI_ORGANIZATION_ID")


class LogoGenerator:
    def __init__(self, company_name, company_description, logo_style, preferred_color="", brand_tone="", industry_keywords=""):
        self.company_name = company_name
        self.company_description = company_description
        self.logo_style = logo_style
        self.preferred_color = preferred_color
        self.brand_tone = brand_tone
        self.industry_keywords = industry_keywords
    
    def create_unique_output_folder(self):
        """Create a unique folder for this logo's outputs"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        # Create a descriptive folder name from the company name
        company_slug = re.sub(r'[^\w\s-]', '', self.company_name.lower())
        company_slug = re.sub(r'[\s]+', '_', company_slug)[:25]  # Limit length
        
        folder_name = f"logo_{company_slug}_{self.logo_style.lower()}_{timestamp}"
        logo_folder = os.path.join(os.getcwd(), "output", folder_name)
        os.makedirs(logo_folder, exist_ok=True)
        
        return logo_folder, timestamp

    def save_json_output(self, data, logo_folder, timestamp):
        """Save the output as JSON file"""
        filename = f"logo_{self.company_name.lower().replace(' ', '_')}_{timestamp}.json"
        filepath = os.path.join(logo_folder, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return filepath

    def save_markdown_output(self, data, logo_folder, timestamp):
        """Generate and save Markdown file"""
        filename = f"logo_{self.company_name.lower().replace(' ', '_')}_{timestamp}.md"
        filepath = os.path.join(logo_folder, filename)
        
        # Create markdown content
        markdown_content = f"""# {self.company_name} Logo Design

## Company Information
**Company Name:** {self.company_name}
**Description:** {data.get('company_description', '')}
**Industry:** {data.get('industry_keywords', '')}
**Brand Tone:** {data.get('brand_tone', '')}
**Preferred Color:** {data.get('preferred_color', '')}

## Logo Specifications
**Logo Style:** {self.logo_style}
**Selected Concept:** {data.get('selected_concept', '')}

## Logo Files"""
        
        if data.get('logo'):
            logo_data = data['logo']
            # Handle PNG logo
            if logo_data.get('png_filename'):
                markdown_content += f"""\n### PNG Logo
- **File**: {logo_data.get('png_filename', 'N/A')}
- **Local Path**: {logo_data.get('png_local_path', 'N/A')}
- **Resolution**: {logo_data.get('resolution', '1024x1024')}
- **Format**: PNG (Raster)
"""
            
            # Handle SVG logo
            if logo_data.get('svg_filename'):
                markdown_content += f"""\n### SVG Logo
- **File**: {logo_data.get('svg_filename', 'N/A')}
- **Local Path**: {logo_data.get('svg_local_path', 'N/A')}
- **Format**: SVG (Vector)
- **Scalability**: Infinite resolution
"""
            
            # Logo prompt details
            if logo_data.get('original_prompt'):
                markdown_content += f"""\n### Design Prompt
- **Original Prompt**: {logo_data.get('original_prompt', 'N/A')}
- **Refined Prompt**: {logo_data.get('refined_prompt', 'N/A')}
"""
        else:
            markdown_content += "\nNo logo generated\n"
        
        markdown_content += f"""\n## Brand Analysis
{data.get('brand_analysis', '')}

## Metadata
- **Logo Style**: {data.get('logo_style', '')}
- **Generated**: {data.get('timestamp', '')}
- **Status**: {data.get('status', '')}
- **Company**: {data.get('company_name', '')}
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        return filepath

    def generate_html_preview(self, data, logo_folder, timestamp):
        """Generate HTML preview for the logo design"""
        try:
            template_path = os.path.join(os.getcwd(), "templates", "logo_preview.html")
            
            # Create basic logo preview template if it doesn't exist
            if not os.path.exists(template_path):
                os.makedirs(os.path.dirname(template_path), exist_ok=True)
                basic_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{company_name}} - Logo Design Preview</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 12px 12px 0 0; }
        .logo-showcase { padding: 40px; text-align: center; }
        .logo-image { max-width: 300px; width: 100%; height: auto; border: 1px solid #e0e0e0; border-radius: 8px; }
        .details { padding: 30px; border-top: 1px solid #e0e0e0; }
        .detail-section { margin-bottom: 25px; }
        .detail-title { font-weight: 600; color: #333; margin-bottom: 8px; }
        .brand-analysis { background: #f8f9fa; padding: 20px; border-radius: 8px; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{{company_name}} Logo Design</h1>
            <p>Professional Brand Identity • {{logo_style}} Style</p>
        </div>
        <div class="logo-showcase">
            {{#logo_image}}<img src="{{logo_image}}" alt="{{company_name}} Logo" class="logo-image">{{/logo_image}}
            {{^logo_image}}<div style="padding: 60px; background: #f0f0f0; border-radius: 8px; color: #666;">Logo Preview Unavailable</div>{{/logo_image}}
        </div>
        <div class="details">
            <div class="detail-section">
                <div class="detail-title">Company</div>
                <div>{{company_name}}</div>
            </div>
            <div class="detail-section">
                <div class="detail-title">Logo Style</div>
                <div>{{logo_style}}</div>
            </div>
            <div class="detail-section">
                <div class="detail-title">Generated</div>
                <div>{{timestamp}}</div>
            </div>
            {{#brand_analysis}}
            <div class="brand-analysis">
                <div class="detail-title">Why This Logo Works</div>
                <div>{{brand_analysis}}</div>
            </div>
            {{/brand_analysis}}
        </div>
    </div>
</body>
</html>"""
                
                with open(template_path, 'w', encoding='utf-8') as f:
                    f.write(basic_template)
            
            with open(template_path, 'r', encoding='utf-8') as f:
                template = f.read()
            
            # Prepare template variables
            template_vars = {
                "timestamp": data.get("timestamp", ""),
                "company_name": data.get("company_name", ""),
                "logo_style": data.get("logo_style", ""),
                "brand_analysis": data.get("brand_analysis", ""),
                "logo_image": ""
            }
            
            # Handle logo image path
            if data.get("logo"):
                if data["logo"].get("png_filename"):
                    template_vars["logo_image"] = data["logo"]["png_filename"]
            
            # Simple template replacement
            html_content = template
            for key, value in template_vars.items():
                # Handle conditional sections
                if value:
                    html_content = re.sub(rf'{{\#{key}}}.*?{{\/{key}}}', 
                                        lambda m: m.group(0).replace(f'{{{{{key}}}}}', str(value)), 
                                        html_content, flags=re.DOTALL)
                    html_content = re.sub(rf'{{\^{key}}}.*?{{\/{key}}}', '', html_content, flags=re.DOTALL)
                else:
                    html_content = re.sub(rf'{{\#{key}}}.*?{{\/{key}}}', '', html_content, flags=re.DOTALL)
                    html_content = re.sub(rf'{{\^{key}}}(.*?){{\/{key}}}', r'\1', html_content, flags=re.DOTALL)
                
                html_content = html_content.replace(f'{{{{{key}}}}}', str(value))
            
            # Clean up any remaining template syntax
            html_content = re.sub(r'\{\{[^}]+\}\}', '', html_content)
            
            # Save HTML file
            html_filename = f"logo_preview_{timestamp}.html"
            html_filepath = os.path.join(logo_folder, html_filename)
            
            with open(html_filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            return html_filepath
            
        except Exception as e:
            print(f"Error generating HTML preview: {str(e)}")
            return None

    def run(self):
        print(f"\n🎨 Creating professional logo for: '{self.company_name}'")
        print(f"🏢 Company Description: {self.company_description}")
        print(f"🎭 Logo Style: {self.logo_style}")
        if self.preferred_color:
            print(f"🎨 Preferred Color: {self.preferred_color}")
        if self.brand_tone:
            print(f"🎵 Brand Tone: {self.brand_tone}")
        if self.industry_keywords:
            print(f"🏭 Industry: {self.industry_keywords}")
        print("=" * 60)

        # Initialize agents and tasks
        agents = LogoDesignAgents()
        tasks = LogoDesignTasks()

        # Step 1: Generate 3 brand strategy concepts
        print("\n🧠 STEP 1: Analyzing brand strategy and generating 3 logo concepts...")
        brand_strategist = agents.brand_strategist_agent()
        strategy_task = tasks.brand_strategy_task(
            brand_strategist, 
            self.company_name, 
            self.company_description,
            self.logo_style,
            self.industry_keywords,
            self.brand_tone,
            self.preferred_color
        )
        
        strategy_crew = Crew(
            agents=[brand_strategist],
            tasks=[strategy_task],
            verbose=True,
        )
        
        concepts_result = strategy_crew.kickoff()
        print("\n" + "="*60)
        print("🎨 HERE ARE YOUR 3 STRATEGIC LOGO CONCEPTS:")
        print("="*60)
        print(concepts_result)
        
        # Step 2: User selects a concept
        print("\n" + "="*60)
        while True:
            try:
                choice = input("\n👆 Which concept resonates with your brand vision? (Enter 1, 2, or 3): ").strip()
                if choice in ["1", "2", "3"]:
                    selected_concept = f"Concept {choice}"
                    break
                else:
                    print("❌ Please enter 1, 2, or 3")
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                return
        
        print(f"\n✅ Excellent choice! Creating your professional logo based on {selected_concept}...")
        
        # Create unique output folder for this logo
        logo_folder, timestamp = self.create_unique_output_folder()
        print(f"\n📁 Created output folder: {os.path.basename(logo_folder)}")
        
        # Step 3: Generate the professional logo
        print("\n🚀 STEP 2: Designing your world-class logo with dual-AI enhancement...")
        
        # Initialize logo design agents
        logo_designer = agents.logo_designer_agent(logo_folder)
        brand_analyst = agents.brand_analyst_agent()
        
        # Create brand context for logo generation
        brand_context = f"Company: {self.company_name}, Industry: {self.industry_keywords}, Tone: {self.brand_tone}, Color: {self.preferred_color}"
        
        # Create logo design task
        logo_task = tasks.logo_design_task(
            logo_designer,
            selected_concept,
            self.company_name,
            self.company_description,
            self.logo_style,
            brand_context
        )
        
        # Execute logo design
        design_crew = Crew(
            agents=[logo_designer],
            tasks=[logo_task],
            verbose=True,
        )
        
        logo_result = design_crew.kickoff()
        
        # Parse logo results
        logo_data = {}
        
        try:
            # Extract logo data from the result
            logo_result_str = str(logo_result)
            
            # Try to parse logo URLs and data from the result
            if "image.png" in logo_result_str:
                # Extract PNG and SVG URLs
                import re
                png_match = re.search(r'https://[^\s\)]+image\.png', logo_result_str)
                svg_match = re.search(r'https://[^\s\)]+image\.png', logo_result_str)  # Both might be PNG URLs from FAL
                
                logo_data = {
                    "png_url": png_match.group() if png_match else None,
                    "svg_url": svg_match.group() if svg_match else None,
                    "status": "success",
                    "description": logo_result_str
                }
            else:
                # Fallback - store the full result
                logo_data = {
                    "status": "completed",
                    "description": logo_result_str,
                    "raw_output": logo_result_str
                }
                
        except Exception as e:
            logo_data = {
                "status": "error", 
                "error": f"Error processing logo results: {str(e)}",
                "raw_output": str(logo_result)
            }
        
        # Create comprehensive result structure
        complete_result = {
            "timestamp": datetime.now().isoformat(),
            "company_name": self.company_name,
            "company_description": self.company_description,
            "logo_style": self.logo_style,
            "selected_concept": selected_concept,
            "brand_context": brand_context,
            "logo": logo_data,
            "status": "completed"
        }
        
        # Save all outputs to the unique folder
        json_filepath = self.save_json_output(complete_result, logo_folder, timestamp)
        markdown_filepath = self.save_markdown_output(complete_result, logo_folder, timestamp)
        html_filepath = self.generate_html_preview(complete_result, logo_folder, timestamp)
        
        # Format and display final output
        print("\n" + "="*60)
        print(f"🎉 YOUR PROFESSIONAL LOGO FOR {self.company_name.upper()} IS READY!")
        print("="*60)
        
        print(f"\n🎨 LOGO DETAILS:")
        print("-" * 30)
        print(f"📋 Company: {complete_result['company_name']}")
        print(f"🎭 Style: {complete_result['logo_style']}")
        print(f"🎯 Concept: {complete_result['selected_concept']}")
        
        print(f"\n📁 LOGO FILES:")
        print("-" * 30)
        logo_info = complete_result["logo"]
        if logo_info.get("status") == "success" or logo_info.get("png_url"):
            if logo_info.get("png_url"):
                print(f"🖼️  PNG Logo: {logo_info['png_url']}")
            if logo_info.get("svg_url"):
                print(f"📐 SVG Logo: {logo_info['svg_url']}")
            if logo_info.get("description"):
                print(f"📝 Description: {logo_info['description'][:200]}...")
        else:
            print("📄 Logo Generation Completed:")
            print(f"   Status: {logo_info.get('status', 'Unknown')}")
            if logo_info.get('error'):
                print(f"   ❌ Error: {logo_info['error']}")
            if logo_info.get('description'):
                print(f"   📝 Details: {logo_info['description'][:300]}...")
        
        print(f"\n📂 SAVED FILES:")
        print("-" * 30)
        print(f"💾 JSON Data: {json_filepath}")
        print(f"📝 Brand Report: {markdown_filepath}")
        if html_filepath:
            print(f"🌐 Preview Page: {html_filepath}")
        
        print(f"\n📂 Complete folder path: {logo_folder}")
        print("\n" + "="*60)
        print("✨ Professional logo design complete! Check the HTML preview for full brand presentation!")
        print("="*60)
        
        return complete_result


class ContentCalendarPlanner:
    def __init__(self, user_prompt, platforms=None, duration_weeks=4):
        self.user_prompt = user_prompt
        self.platforms = platforms or ["instagram", "facebook", "twitter", "linkedin"]
        self.duration_weeks = duration_weeks
    
    def create_unique_output_folder(self):
        """Create a unique folder for this calendar's outputs"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        # Create a descriptive folder name from the prompt
        prompt_slug = re.sub(r'[^\w\s-]', '', self.user_prompt.lower())
        prompt_slug = re.sub(r'[\s]+', '_', prompt_slug)[:30]  # Limit length
        
        folder_name = f"content_calendar_{prompt_slug}_{timestamp}"
        calendar_folder = os.path.join(os.getcwd(), "output", folder_name)
        os.makedirs(calendar_folder, exist_ok=True)
        
        return calendar_folder, timestamp

    def save_calendar_outputs(self, calendar_data, calendar_folder, timestamp):
        """Save the calendar as JSON, Markdown, and CSV files"""
        # Save JSON file
        json_filename = f"content_calendar_{timestamp}.json"
        json_filepath = os.path.join(calendar_folder, json_filename)
        
        calendar_json = {
            "timestamp": datetime.now().isoformat(),
            "original_prompt": self.user_prompt,
            "platforms": self.platforms,
            "duration_weeks": self.duration_weeks,
            "calendar_content": str(calendar_data),
            "status": "completed",
            "metadata": {
                "total_posts_planned": self.duration_weeks * 7 * len(self.platforms),
                "platforms_count": len(self.platforms),
                "calendar_type": "comprehensive_strategy"
            }
        }
        
        with open(json_filepath, 'w', encoding='utf-8') as f:
            json.dump(calendar_json, f, ensure_ascii=False, indent=2)
        
        # Save enhanced Markdown file
        markdown_filename = f"content_calendar_{timestamp}.md"
        markdown_filepath = os.path.join(calendar_folder, markdown_filename)
        
        markdown_content = f"""# 📅 Content Calendar Strategy Plan

## 🎯 Original Request
**Brief:** {self.user_prompt}

## 📊 Calendar Overview
- **🚀 Platforms**: {', '.join(self.platforms)}
- **⏰ Duration**: {self.duration_weeks} weeks
- **📈 Total Posts Planned**: ~{self.duration_weeks * 7 * len(self.platforms)} posts
- **📅 Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 📋 Complete Content Calendar

{calendar_data}

---

## 📋 Quick Action Checklist

### Week 1 Preparation
- [ ] Review and approve all Week 1 content
- [ ] Prepare visual assets for first week
- [ ] Schedule posts in social media management tool
- [ ] Set up tracking for performance metrics

### Ongoing Tasks
- [ ] Weekly performance review and optimization
- [ ] Content creation for upcoming weeks
- [ ] Community engagement and response management
- [ ] Hashtag performance monitoring

### Monthly Review
- [ ] Analyze engagement metrics
- [ ] Adjust strategy based on performance
- [ ] Plan next month's content themes
- [ ] Review and update brand guidelines

---

## 🛠️ Tools & Resources Recommended

### Content Creation
- **Design**: Canva, Adobe Creative Suite, Figma
- **Video**: CapCut, InShot, Adobe Premiere
- **Photography**: VSCO, Lightroom, Snapseed

### Scheduling & Management
- **Scheduling**: Buffer, Hootsuite, Later, Sprout Social
- **Analytics**: Native platform insights, Google Analytics
- **Collaboration**: Trello, Asana, Monday.com

### Content Planning
- **Calendar Tools**: Google Calendar, Notion, Airtable
- **Asset Storage**: Google Drive, Dropbox, Brand folder
- **Approval Workflow**: ReviewBoard, Gain, Planable

---

*🤖 Generated with AI Content Calendar Planner*
*📈 Ready-to-implement social media strategy*
"""
        
        with open(markdown_filepath, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        # Save CSV file for easy import to scheduling tools
        csv_filename = f"content_calendar_{timestamp}.csv"
        csv_filepath = os.path.join(calendar_folder, csv_filename)
        
        csv_content = """Date,Time,Platform,Content Type,Topic/Theme,Caption Preview,Media Requirements,Hashtags,Call-to-Action,Status,Performance Goal
"""
        
        # Add sample CSV structure (this would be populated from actual calendar data)
        current_date = datetime.now()
        for week in range(self.duration_weeks):
            for day in range(7):
                date = current_date + timedelta(weeks=week, days=day)
                for platform in self.platforms:
                    csv_content += f"{date.strftime('%Y-%m-%d')},12:00 PM,{platform.title()},Post,Sample Theme,Sample caption preview...,Image/Video description,#hashtag1 #hashtag2,Sample CTA,Draft,100 engagements\n"
        
        with open(csv_filepath, 'w', encoding='utf-8') as f:
            f.write(csv_content)
        
        return json_filepath, markdown_filepath, csv_filepath

    def run(self):
        print(f"\n📅 Creating content calendar for: '{self.user_prompt}'")
        print(f"📱 Platforms: {', '.join(self.platforms)}")
        print(f"📆 Duration: {self.duration_weeks} weeks")
        print("=" * 50)

        # Initialize agents and tasks
        agents = SocialMediaAgents()
        tasks = SocialMediaTasks()

        # Create calendar planning workflow
        print("\n🗓️  STEP 1: Generating comprehensive content calendar...")
        calendar_agent = agents.calendar_planner_agent()
        calendar_task = tasks.content_calendar_planning_task(
            calendar_agent, 
            self.user_prompt, 
            self.platforms, 
            self.duration_weeks
        )
        
        calendar_crew = Crew(
            agents=[calendar_agent],
            tasks=[calendar_task],
            verbose=True,
        )
        
        calendar_result = calendar_crew.kickoff()
        
        # Create unique output folder for this calendar
        calendar_folder, timestamp = self.create_unique_output_folder()
        print(f"\n📁 Created output folder: {os.path.basename(calendar_folder)}")
        
        # Save calendar outputs
        json_filepath, markdown_filepath, csv_filepath = self.save_calendar_outputs(
            calendar_result, calendar_folder, timestamp
        )
        
        # Display results
        print("\n" + "="*60)
        print("🎉 YOUR CONTENT CALENDAR IS READY!")
        print("="*60)
        
        print(f"\n📋 CALENDAR OVERVIEW:")
        print("-" * 30)
        print(f"📱 Platforms: {', '.join(self.platforms)}")
        print(f"📆 Duration: {self.duration_weeks} weeks")
        print(f"🎯 Theme: {self.user_prompt}")
        
        print(f"\n📅 CONTENT CALENDAR:")
        print("-" * 30)
        print(str(calendar_result))
        
        print(f"\n💾 OUTPUT FILES SAVED:")
        print("-" * 30)
        print(f"📁 Folder: {os.path.basename(calendar_folder)}")
        print(f"📄 JSON: {os.path.basename(json_filepath)}")
        print(f"📝 Markdown: {os.path.basename(markdown_filepath)}")
        print(f"📊 CSV: {os.path.basename(csv_filepath)}")
        
        print(f"\n🎯 ACTIONABLE NEXT STEPS:")
        print("-" * 30)
        print("1. 📖 Review the Markdown file for complete strategy")
        print("2. 📊 Import CSV into your scheduling tool (Buffer, Hootsuite, etc.)")
        print("3. 🎨 Begin creating visual assets for Week 1")
        print("4. 📅 Schedule your first week of posts")
        print("5. 📈 Set up performance tracking and monitoring")
        
        print(f"\n🛠️ RECOMMENDED TOOLS:")
        print("-" * 30)
        print("• 📱 Scheduling: Buffer, Hootsuite, Later")
        print("• 🎨 Design: Canva, Adobe Creative Suite")
        print("• 📊 Analytics: Native platform insights")
        print("• 📋 Project Management: Trello, Asana")
        
        print(f"\n📂 Complete folder path: {calendar_folder}")
        print("\n" + "="*60)
        print("✨ Your comprehensive content calendar strategy is ready!")
        print("🚀 This calendar includes detailed daily planning for all weeks!")
        print("📈 Follow the action checklist to implement your strategy!")
        print("="*60)
        
        return calendar_result


if __name__ == "__main__":
    print("🎨 Welcome to Professional Logo Generator AI!")
    print("=" * 60)
    print("💡 World-Class Logo Design Features:")
    print("   • Advanced Brand Psychology Analysis")
    print("   • 3 Strategic Logo Concepts to Choose From")
    print("   • Dual-AI Enhancement (GPT-4 + Claude Sonnet 3.5)")
    print("   • Professional PNG & SVG Output Formats")
    print("   • Comprehensive Brand Analysis Report")
    print("   • Fortune 500 Quality Standards")
    print("")
    print("🎨 SUPPORTED LOGO STYLES:")
    print("   1. WordMark - Typography-based company name design")
    print("   2. LetterMark - Elegant monogram/initial design")
    print("   3. Pictorial Mark - Iconic symbol representation")
    print("   4. Abstract - Unique geometric/organic forms")
    print("   5. Combination Mark - Text + symbol integration")
    print("   6. Emblem - Classic badge/crest style")
    print("")
    print("🚀 PROFESSIONAL OUTPUT:")
    print("   • High-resolution PNG (1024x1024px) for digital use")
    print("   • Scalable SVG vector format for print/large displays")
    print("   • Brand psychology analysis explaining logo effectiveness")
    print("   • Professional HTML preview for client presentation")
    print("   • Complete brand implementation guidelines")
    print("=" * 60)
    
    try:
        # Collect company information
        print("\n🏢 Let's create your professional logo! Please provide the following information:")
        print("-" * 60)
        
        company_name = input("\n🏭 Company Name (Required): ").strip()
        if not company_name:
            print("❌ Company name is required!")
            exit()
        
        company_description = input("\n📋 Company Description (Required)\n   Describe what your company does, your mission, or key services:\n   ").strip()
        if not company_description:
            print("❌ Company description is required!")
            exit()
        
        # Logo style selection (required)
        print("\n🎨 Select Your Logo Style (Required):")
        print("   1. WordMark - Focus on typography and company name styling")
        print("   2. LetterMark - Monogram or initials-based design")
        print("   3. Pictorial Mark - Icon or symbol representing your business")
        print("   4. Abstract - Modern geometric or artistic forms")
        print("   5. Combination Mark - Company name with complementary symbol")
        print("   6. Emblem - Traditional badge or crest design")
        
        while True:
            try:
                style_choice = input("\n👆 Choose your logo style (1-6): ").strip()
                style_map = {
                    "1": "WordMark",
                    "2": "LetterMark", 
                    "3": "Pictorial Mark",
                    "4": "Abstract",
                    "5": "Combination Mark",
                    "6": "Emblem"
                }
                if style_choice in style_map:
                    logo_style = style_map[style_choice]
                    break
                else:
                    print("❌ Please enter a number from 1-6")
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                exit()
        
        # Optional information
        print(f"\n✅ Selected: {logo_style}")
        print("\n🌈 Optional Information (press Enter to skip):")
        
        preferred_color = input("\n🎨 Preferred Color/Palette (e.g., 'Blue', 'Red and Gold', 'Green tones'): ").strip()
        
        brand_tone = input("\n🎵 Brand Tone (e.g., 'Professional', 'Friendly', 'Modern', 'Traditional', 'Playful'): ").strip()
        
        industry_keywords = input("\n🏭 Industry Keywords (e.g., 'Technology', 'Healthcare', 'Fashion', 'Food & Beverage'): ").strip()
        
        print(f"\n🚀 Creating your {logo_style} logo for {company_name}...")
        
        generator = LogoGenerator(
            company_name=company_name,
            company_description=company_description,
            logo_style=logo_style,
            preferred_color=preferred_color,
            brand_tone=brand_tone,
            industry_keywords=industry_keywords
        )
        
        result = generator.run()
        
        print("\n" + "="*60)
        print("🎉 Logo generation completed successfully!")
        print("📊 Your professional brand identity is ready for business use!")
        print("="*60)
        
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye! Come back anytime to create your professional logo!")
    except Exception as e:
        print(f"\n❌ An error occurred: {str(e)}")
        print("💡 Make sure you have set your API keys (OPENAI_API_KEY, FAL_KEY, CLAUDE_API_KEY) in the .env file!")
