from service.crawler_images_service import CrawlerImagesService
from .pipe import Pipe
from decorator.log_decorator import log_decorator

class CrawlerImagesPipe(Pipe):

    def __init__(self):
        pass

    @log_decorator
    def pipeline(self):
        crawler_images_acne = CrawlerImagesService('rosto acne', 5)
        crawler_images_acne.list_images_url()

        # TODO        
