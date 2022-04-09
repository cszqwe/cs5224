from pytrends.request import TrendReq

class TagService():
    def __init__(self):
        self.pytrends = TrendReq(hl='en-US', tz=360)

    def getTag(self, tag):
        tag = tag.lower()
        kw_list = [tag]
        try:
            self.pytrends.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='', gprop='')
            related_topics = self.pytrends.related_topics()
            if 'topic_title' in related_topics[tag]['rising'] and len(related_topics[tag]['rising']['topic_title']) > 0:
                return related_topics[tag]['rising']['topic_title'][0]
            return tag
        except:
            return tag
