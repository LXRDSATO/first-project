import os
from jinja2 import Environment, FileSystemLoader
from backend.config.settings import REVIEW_FOLDER
import logging

class LandingPageGenerator:
    def __init__(self, template_dir=None, output_dir=None):
        self.template_dir = template_dir or os.path.join(os.path.dirname(__file__), 'templates')
        self.output_dir = output_dir or os.path.join(REVIEW_FOLDER, 'landing_pages')
        os.makedirs(self.output_dir, exist_ok=True)
        self.env = Environment(loader=FileSystemLoader(self.template_dir))
        self.logger = logging.getLogger("microtours.landingpage")

    def generate(self, spot, script, video_path):
        try:
            template = self.env.get_template('landing_page.html')
            html_content = template.render(
                spot=spot,
                script=script,
                video_path=video_path
            )
            filename = f"{spot['name'].replace(' ', '_')}.html"
            output_path = os.path.join(self.output_dir, filename)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            return output_path
        except Exception as e:
            self.logger.exception("Landing page generation failed")
            return None
