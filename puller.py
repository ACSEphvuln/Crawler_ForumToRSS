import PyRSS2Gen
import datetime
from lib.rssMaker import RSSPuller

def getSite1():
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
                            "url":"https://example.com/db?sortby=started&order=desc&datecut=1&prefix=0",
                            "base":"/html/body/div[1]/main/table[2]/tbody",
                            "start":10,
                            "filters":filters,
                            },
                        cachefile="cache/cache1.txt",
                        pull_type="dynamic")
    
    return br_pull.getRSSItems()

def getSite2():
    filters = {
        "Title":{
            "xpath": "/td[2]/h4/a/span[1]",
            "attrib": None 
        },
        "Date":{
            "xpath": "/td[5]/ul/li[2]/a",
            "attrib": None
        },
        "Link":{
            "xpath": "/td[2]/h4/a",
            "attrib": "href"
        },
        "Description":{
            "xpath": "/td[2]/span",
            "attrib": None
        },
    }

    br_pull = RSSPuller(forumStruct={
                            "url":"https://sub.example.com/forum/dbs",
                            "base":"/html/body/div[4]/div[3]/div/div[3]/div[4]/div[3]/div[3]/div/table",
                            "start":5,
                            "filters":filters,
                            },
                        cachefile="cache/cache2.txt",
                        pull_type="static")

    return br_pull.getRSSItems()

def postNews(filename):
    #feed_items = []
    #feed_items.append(getSite1()) - SITE DOWN
    feed_items = getSite2()

    if feed_items == []:
        print("[INF] Nothing to publish")
        return

    feed = PyRSS2Gen.RSS2(
        title="New leaks",
        link="http://localhost", # TODO CHANGE
        description="Feeding new leaks..",
        lastBuildDate=datetime.datetime.now(),
        items=feed_items
    )

    # print the RSS feed in XML format
    f = feed.to_xml()
    with open(filename,'w') as g:
        g.write(f)
    
    return f

if __name__ == "__main__":
    postNews("feed/rss.xml")
