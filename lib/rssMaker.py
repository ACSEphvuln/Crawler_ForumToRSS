from .forumParser import ForumParser
import PyRSS2Gen

"""
# FORUM STRUCTURE:
forumStruct = {
    "url":baseurl,
    "base":baseXPath,
    "filters":XPathFilters,
    "start":tableStart
}
"""

class RSSPuller(ForumParser):
    def __init__(self, forumStruct, cachefile, pull_type='static') -> None:
        super.__init__(self, forumStruct["url"], pull_type)
        self.base = forumStruct["base"]
        self.filters = forumStruct["filters"]
        self.start = forumStruct["start"]
        self.cachefile = cachefile
        self.domain = self.url[:self.url.find('/',8)]

    def getRSSItems(self):
        # create an RSS feed object
        elements = self.getPosts()

        if elements == None:
            print(f"[WRN] Could not get feed for {self.url}")
            print("[INF] Check for manual captcha")
            return []
        
        # Check if already present
        try :
            with open(self.cachefile,'r') as g:
                prev_items = g.read().split('\n')
                prev_items.pop()
        except:
            prev_items = [] 
        
        eTitles = [e['Title'] for e in elements]

        if set(prev_items) == set(eTitles):
            print(f"[INF] Nothing to publish for {self.url}")
            return []

        with open(self.cachefile,'w') as g:
            for i in eTitles:
                g.write(f"{i}\n")

        # add each element to the RSS feed
        feed_items = []
        for element in elements:
            title = f"{self.domain} | \"{element['Title']}\""
            link = f"{self.domain}/{element['Link']}"
            description = f"Leaked by {element['Description']}"
            date = element['Date']
            feed_item = PyRSS2Gen.RSSItem(title=title, link=link, description=description, pubDate=date)
            feed_items.append(feed_item)
        
        return feed_item