from .forumParser import ForumParser
import PyRSS2Gen
import html
from dateutil import parser
import pytz
from urllib.parse import urlsplit, quote, urlunsplit

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
        super().__init__(forumStruct["url"], pull_type)
        self.url = forumStruct["url"]
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

        if set(prev_items) == set(eTitles): # BUG: maybe keep a single cache file so a site dosen't take over if an other dosent publish
            print(f"[INF] Nothing to publish for {self.url}")
            return []

        with open(self.cachefile,'w') as g:
            for i in eTitles:
                g.write(f"{i}\n")

        # add each element to the RSS feed
        feed_items = []
        
        for element in elements:
            title = html.escape(f"{self.domain} | \"{element['Title']}\"", quote=True) 
            link = html.escape(iri_to_ascii_url(element['Link']))
            
            description = html.escape(f"Leaked by {element['Description']}")
            date = html.escape(parser.parse(element['Date'].replace('Today,','').replace("Yesterday,",'')).replace(tzinfo=pytz.timezone('GMT')).strftime("%a, %d %b %y %H:%M:%S %Z"))
            feed_item = PyRSS2Gen.RSSItem(title=title, link=link, description=description, pubDate=date)
            feed_items.append(feed_item)
        
        return feed_items
    
def iri_to_ascii_url(iri):
    # Parse the IRI into its components
    scheme, netloc, path, query, fragment = urlsplit(iri)

    # Encode the IRI components to URL-encoded format
    scheme = quote(scheme)
    netloc = quote(netloc)
    path = quote(path)
    query = quote(query)
    fragment = quote(fragment)

    # Construct the ASCII-only URL using urlunsplit()
    ascii_url = urlunsplit((scheme, netloc, path, query, fragment))

    return ascii_url