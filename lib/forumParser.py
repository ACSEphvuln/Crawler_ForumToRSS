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
        # html_content = self.pageGetter.getPage()
        # with open("test/cache.html",'w') as g:
        #    g.write(html_content)

        with open("test/cache.html") as g:
            html_content = g.read()
        
        try:
            tableParser = TableParser(html_content, base)
        except:
            print("[Err] Could not get base element")
            return None

        tableParser.setGrabFilters(filters)

        posts = []
        for i in range(startElem, tableParser.getNumElem()):
            elem = tableParser.getElem(i)
            if elem != None:
                posts.append(elem)

        return posts
