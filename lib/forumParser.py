from .webCrawl import DynamicPageGetter, StaticPageGetter
from .xpathParser import TableParser

class ForumParser:
    def __init__(self,url,pull_type="static") -> None:
        if pull_type == "static":
            self.pageGetter = StaticPageGetter(url)
        elif pull_type == "dynamic":
            self.pageGetter = DynamicPageGetter(url)
        else:
            raise ValueError(f"Approach type {pull_type} is not implemented!")
    
    def setFilters(self,base,start,filters):
        self.base = base
        self.start = start
        self.filters = filters

    def getPosts(self):
        html_content = self.pageGetter.getPage()

        try:
            tableParser = TableParser(html_content, self.base)
        except:
            print("[Err] Could not get base element")
            return None

        tableParser.setGrabFilters(self.filters)

        posts = []
        for i in range(self.start, tableParser.getNumElem()):
            elem = tableParser.getElem(i)
            if elem != None:
                posts.append(elem)

        return posts
