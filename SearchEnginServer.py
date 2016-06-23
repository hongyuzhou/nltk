# -*- coding:utf-8 -*-

import tornado.ioloop
import tornado.web
import jnius_config
import jnius
import json

#jnius_config.set_classpath('.', '/home/hongyz/workspace/doc-lucene/target/doc-lucene-0.0.1-SNAPSHOT-jar-with-dependencies.jar')
ChatBotSearchEngin = jnius.autoclass('com.baina.dolphin.doc_lucene.ChatBotSearchEngin')
cbse = ChatBotSearchEngin("/home/hongyz/chatBoxIndex",20,10.0,0.0)
      
def index(arg1,arg2,arg3,arg4):
    cbse.createIndexOnTime(arg1,arg2,arg3,arg4)

def search(keywords):
    return cbse.searchIndex(keywords)

class IndexHandler(tornado.web.RequestHandler):
    def post(self):
        _id = long(self.get_argument('id', ''))
        url = self.get_argument('url', '').encode('utf-8')
        title = self.get_argument('title', '').encode('utf-8')
        content = self.get_argument('content', '').encode('utf-8')
        index(_id,url,title,content)

    def get(self):
        _id = long(self.get_argument('id', ''))
        url = self.get_argument('url', '').encode('utf-8')
        title = self.get_argument('title', '').encode('utf-8')
        content = self.get_argument('content', '').encode('utf-8')
        index(_id,url,title,content)

class SearchHandler(tornado.web.RequestHandler):
    def post(self):
        keywords = self.get_argument('keywords', '')
        print 'post Function===========>>' + keywords
        print 'Search Result Info: '
        result = search(keywords)
        print result
        # write into response
        self.write(result)

    def get(self):
        keywords = self.get_argument('keywords', '')
        print 'get Function ============>>' + keywords
        result = search(keywords)
        print result     
        self.write(result)

def make_app():
    return tornado.web.Application([
        (r"/index",IndexHandler),
        (r"/search",SearchHandler)
        ])

if __name__ == '__main__':
    app = make_app()
    app.listen(12000)
    tornado.ioloop.IOLoop.current().start()