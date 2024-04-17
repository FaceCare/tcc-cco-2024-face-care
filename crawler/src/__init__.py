import sys, os
import logging
# Fix path to imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Configure logs
logging.basicConfig(level=logging.INFO)

# -------

from pipe.crawler_images_pipe import CrawlerImagesPipe
pipe_images = CrawlerImagesPipe()
pipe_images.pipeline()
