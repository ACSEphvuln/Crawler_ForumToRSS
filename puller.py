import PyRSS2Gen
import datetime
from lib.rssMaker import RSSPuller

def getBreachedVC():
    filters = {
        "Title":{
            "xpath": "/td[2]/div/div[1]/span/a",
            "attrib": None 
        },
        "Date":{
            "xpath": "/td[5]/span/span",
            "attrib": "title"
        },
        "Link":{
            "xpath": "/td[2]/div/div[1]/span/a",
            "attrib": "href"
        },
        "Description":{
            "xpath": "/td[2]/div/div[2]/span[1]/a/span",
            "attrib": None
        },
    }

    br_pull = RSSPuller(forumStruct={
                            "url":"https://breached.vc/Forum-Databases?sortby=started&order=desc&datecut=1&prefix=0" ,
                            "base":"/html/body/div[1]/main/table[2]/tbody",
                            "start":10,
                            "filters":filters,
                            },
                        cachefile="cache/cache_breachedvc.txt",
                        pull_type="dynamic")
    return br_pull.getRSSItems()

def getNulledTO():
    raise NotImplementedError()

def postNews(filename):
    feed_items = []
    #feed_items.append(getBreachedVC()) - SITE DOWN
    feed_items.append(getNulledTO())

    feed = PyRSS2Gen.RSS2(
        title="New leaks",
        link="http://localhost", # TODO CHANGE
        description="Feeding new leaks..",
        lastBuildDate=datetime.datetime.now(),
        items=feed_items
    )

    # print the RSS feed in XML format
    with open(filename,'w') as g:
        g.write(feed.to_xml())
    
    return feed.to_xml()

if __name__ == "__main__":
    postNews("feed/rss.xml")