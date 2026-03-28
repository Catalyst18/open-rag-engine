from .base import MediaProcessor

class VideoProcessor(MediaProcessor):
    pass

    def read_contents(self):
        pass

    def extract(self):
        pass

    def run(self):
        self.read_contents()
        self.extract()
