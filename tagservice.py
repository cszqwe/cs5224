from pytrends.request import TrendReq

class TagService():
    def __init__(self):
        self.pytrends = TrendReq(hl='en-US', tz=360)

    def getTag(self, tag):
        tag = tag.lower()
        kw_list = [tag]
        self.pytrends.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='', gprop='')
        if 'topic_title' in self.pytrends.related_topics()[tag]['rising'] and len(self.pytrends.related_topics()[tag]['rising']['topic_title']) > 0:
            return self.pytrends.related_topics()[tag]['rising']['topic_title'][0]
        return tag
