import json


class Page:
    def __init__(self, page_id):
        self.id = page_id
        self.state = None
        self.info = None

    def identify_page(self, page):
        pass

    def crate_page(self, page_info):
        self.info = page_info

    def export_page(self):
        return json.dumps(self.info)

    def find_page(self, page_id):
        pass
