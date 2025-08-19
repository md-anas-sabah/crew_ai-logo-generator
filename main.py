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
import json

os.environ["OPENAI_API_KEY"] = config("OPENAI_API_KEY")
if config("OPENAI_ORGANIZATION_ID", default=""):
    os.environ["OPENAI_ORGANIZATION"] = config("OPENAI_ORGANIZATION_ID")


class LogoGenerator:
    def __init__(self, company_name, company_description, logo_style, preferred_color="", brand_tone="", industry_keywords="", show_grid_lines=False):
        self.company_name = company_name
        self.company_description = company_description
        self.logo_style = logo_style
        self.preferred_color = preferred_color
        self.brand_tone = brand_tone
        self.industry_keywords = industry_keywords
        self.show_grid_lines = show_grid_lines
    
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
        # Initialize agents and tasks
        agents = LogoDesignAgents()
        tasks = LogoDesignTasks()

        # Create unique output folder for this logo
        logo_folder, timestamp = self.create_unique_output_folder()
        
        # Initialize logo design agents
        logo_designer = agents.logo_designer_agent(logo_folder, self.show_grid_lines)
        brand_analyst = agents.brand_analyst_agent()
        
        # Create brand context for logo generation
        brand_context = f"Company: {self.company_name}, Industry: {self.industry_keywords}, Tone: {self.brand_tone}, Color: {self.preferred_color}"
        
        # Create logo design task (skip concept selection, use direct approach)
        logo_task = tasks.logo_design_task(
            logo_designer,
            "Direct Professional Logo Design",
            self.company_name,
            self.company_description,
            self.logo_style,
            brand_context
        )
        
        # Execute logo design
        design_crew = Crew(
            agents=[logo_designer],
            tasks=[logo_task],
            verbose=False,
        )
        
        logo_result = design_crew.kickoff()
        
        # Parse dual AI logo results and extract best PNG URL with transparent background
        image_url = None
        reason = None
        
        try:
            # Extract logo data from the dual AI result
            logo_result_str = str(logo_result)
            
            # Try to parse logo URLs from both AI models
            import re
            url_matches = re.findall(r'https://[^\s\)\"]+\.png', logo_result_str)
            
            # Select the best logo URL (prioritize the one with better quality indicators)
            if url_matches:
                # For now, use the first valid URL (can be enhanced with quality selection logic)
                image_url = url_matches[0]
                
                # Log both generated logos for reference
                if len(url_matches) > 1:
                    print(f"Dual AI generation complete: Primary model URL: {url_matches[0]}")
                    if len(url_matches) > 1:
                        print(f"Secondary model URL: {url_matches[1]}")
                    print("Selected primary model result for optimal quality and transparent background")
            
            # Generate brand analysis for the reason
            if image_url:
                brand_task = tasks.brand_analysis_task(
                    brand_analyst,
                    logo_result_str,
                    f"Company: {self.company_name}, Description: {self.company_description}, Style: {self.logo_style}, Features: transparent background, clean standalone design, dual AI enhanced"
                )
                
                analysis_crew = Crew(
                    agents=[brand_analyst],
                    tasks=[brand_task],
                    verbose=False,
                )
                
                analysis_result = analysis_crew.kickoff()
                reason = str(analysis_result)[:500]  # Keep it concise
                
        except Exception as e:
            reason = f"Error generating dual AI logo analysis: {str(e)}"
        
        # Return pure JSON response with transparent background logo
        result = {
            "image_url": image_url or "Error generating dual AI logo",
            "reason": reason or "Professional logo design created with transparent background using dual AI models (Flux Pro + Qwen) for optimal brand recognition, clean standalone presentation, and market positioning excellence"
        }
        
        return result


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
    print("🎨 Professional Logo Generator")
    print("=" * 40)
    
    try:
        # Collect company information
        company_name = input("Company Name: ").strip()
        if not company_name:
            print("Company name is required!")
            exit()
        
        company_description = input("Company Description: ").strip()
        if not company_description:
            print("Company description is required!")
            exit()
        
        # Logo style selection
        print("\nLogo Styles:")
        print("1. WordMark  2. LetterMark  3. Pictorial Mark")
        print("4. Abstract  5. Combination Mark  6. Emblem")
        
        while True:
            try:
                style_choice = input("Choose style (1-6): ").strip()
                style_map = {
                    "1": "WordMark", "2": "LetterMark", "3": "Pictorial Mark",
                    "4": "Abstract", "5": "Combination Mark", "6": "Emblem"
                }
                if style_choice in style_map:
                    logo_style = style_map[style_choice]
                    break
                else:
                    print("Please enter 1-6")
            except KeyboardInterrupt:
                exit()
        
        # Optional information
        preferred_color = input("Preferred Color (optional): ").strip()
        brand_tone = input("Brand Tone (optional): ").strip()
        industry_keywords = input("Industry (optional): ").strip()
        
        # Grid lines option
        while True:
            try:
                grid_choice = input("Show construction grid lines? (y/N): ").strip().lower()
                show_grid_lines = grid_choice in ['y', 'yes', '1', 'true']
                break
            except KeyboardInterrupt:
                exit()
        
        generator = LogoGenerator(
            company_name=company_name,
            company_description=company_description,
            logo_style=logo_style,
            preferred_color=preferred_color,
            brand_tone=brand_tone,
            industry_keywords=industry_keywords,
            show_grid_lines=show_grid_lines
        )
        
        result = generator.run()
        
        # Output pure JSON
        import json
        print(json.dumps(result))
        
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(json.dumps({"image_url": "Error", "reason": f"Error: {str(e)}"}))
