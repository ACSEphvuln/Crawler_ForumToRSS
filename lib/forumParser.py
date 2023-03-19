from .webCrawl import PageGetter
from .xpathParser import TableParser

class ForumParser:
    def __init__(self,url,approach="dynamic") -> None:
        if approach == "dynamic":
            self.pageGetter = PageGetter(url)
        else:
            raise ValueError(f"Approach type {approach} is not implemented!")
        
    def getPosts(self, base, startElem, filters):
        # LOCAL TEST ONLY
        #html_content = self.pageGetter.getPage()
        #with open("cache.html",'w') as g:
        #    g.write(html_content)

        with open("cache.html") as g:
            html_content = g.read()

        tableParser = TableParser(html_content, base)
        
        tableParser.setGrabFilters(filters)

        posts = []
        for i in range(startElem, tableParser.getNumElem()):
            posts.append(tableParser.getElem(i))

        return posts
