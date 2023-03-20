import pdfplumber

class MasterObj():
    def __init__(self, page_num = None, address=True, cross_check_page=None, entity_type='ORG', preced_text=None, succed_text = None) -> None:
        self.entityType = entity_type
        self.precedingText = preced_text 
        self.succedingText = succed_text

class ResultObj():
    def __init__(self, source, value, value_bbox, page_bbox) -> None:
        self.pageNo = source
        self.value = value
        self.bbox = value_bbox
        self.pageBbox = page_bbox

class AssetMgmt():

    def __init__(self) -> None:
        pass


    def validate(self):
        # title page
        # doc name(?)

        pass