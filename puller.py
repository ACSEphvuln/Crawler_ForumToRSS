import PyRSS2Gen
from lib.forumParser import ForumParser
import datetime

def getForumNews():
    url = "https://breached.vc/Forum-Databases?sortby=started&order=desc&datecut=1&prefix=0"
    getter = ForumParser(url)
    
    base = "/html/body/div[1]/main/table[2]/tbody"
    start = 10
    
    filters = {
        "Title":{
            "xpath": "/td[2]/div/div[1]/span/a",
            "attrib": None # Default get Text
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

    posts = getter.getPosts(base,start,filters)

    return posts

def postNews(filename):
    # create an RSS feed object
    elements = getForumNews()

    if element == None:
        print("Could not get feed for breached.vc")
        print("Check for manual captcha")
        return

    # Check if already present
    try :
        with open("cache/feed_items.txt",'r') as g:
            prev_items = g.read().split('\n')
            prev_items.pop()
    except:
        prev_items = [] 

    eTitles = []
    for e in elements:
        eTitles.append(e['Title'])

    if set(prev_items) == set(eTitles):
        print("Nothing to publish")
        return None

    with open("cache/feed_items.txt",'w') as g:
        for i in eTitles:
            g.write(f"{i}\n")

    # add each element to the RSS feed
    feed_items = []
    for element in elements:
        title = f"breached.vc | \"{element['Title']}\""
        link = f"https://breached.vc/{element['Link']}"
        description = f"Leaked by {element['Description']}"
        date = element['Date']
        feed_item = PyRSS2Gen.RSSItem(title=title, link=link, description=description, pubDate=date)
        feed_items.append(feed_item)

    feed = PyRSS2Gen.RSS2(
        title="New leaks @breach.vc",
        link="http://localhost", # TODO CHANGE
        description="Breachvc has new forum posts!",
        lastBuildDate=datetime.datetime.now(),
        items=feed_items
    )

    # print the RSS feed in XML format
    with open(filename,'w') as g:
        g.write(feed.to_xml())
    
    return feed.to_xml()

if __name__ == "__main__":
    postNews("feed/rss.xml")