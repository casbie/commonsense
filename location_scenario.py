#-*- coding: utf-8 -*-
import json
import urllib2

def getPage(url):
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        return response.read()

if __name__ == '__main__':

        url = "http://conceptnet5.media.mit.edu/data/5.1/c/zh_TW/咖啡廳"
        content = getPage(url)
        cafe = json.loads(content)
        for item in cafe['edges']:
                print_line = item['startLemmas'].encode('utf-8')+item['rel'].encode('utf-8')+item['endLemmas'].encode('utf-8')
                print print_line
                temp = item['startLemmas']
                if temp == u'咖啡廳':
                        temp = item['endLemmas']
                sub_url = u"http://conceptnet5.media.mit.edu/data/5.1/c/zh_TW/"+temp
                sub_url = sub_url.encode('utf-8')
                content = getPage(sub_url)
                sub_cafe = json.loads(content)
                for sub_item in sub_cafe['edges']:
                        print_line = '\t'+sub_item['startLemmas'].encode('utf-8')+sub_item['rel'].encode('utf-8')+sub_item['endLemmas'].encode('utf-8')
                        print print_line
