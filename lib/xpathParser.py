from lxml import html

"""
filter example:
filters = {
    "Title":{
        "xpath": "/td[2]/div/div[1]/span/a",
        "attrib": None # Default get Text
    },
    "Link":{
        "xpath": "/td[2]/div/div[1]/span/a",
        "attrib": "href"
    },
}
"""


class TableParser:
    def __init__(self, html_content : str, xpathBase : str) -> None:
        tree = html.fromstring(html_content)
        self.table = tree.xpath(xpathBase)[0]

    def getNumElem(self) -> int:
        return len(self.table.getchildren())
    
    def setGrabFilters(self, xfilters : dict) -> None:
        self.filters = xfilters
    
    def getElem(self, index : int) -> dict:
        grab = {x:None for x in self.filters.keys()}

        for k,e in self.filters.items():
            search_elem = f"tr[{index}]{e['xpath']}"

            xelem = self.table.xpath(search_elem)[0]
        
            val =  xelem.text if e["attrib"] == None else \
                   xelem.attrib[e["attrib"]]
            
            grab[k] = val
        
        return grab
