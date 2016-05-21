from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import os
import json
import pickle
from testloadjson import treeFromJSON
import try_text_json

def loadPkl(name):
    path = os.path.dirname(os.path.abspath(__file__)) + name;
    pkl_file  = open(path, 'rb')
    obj = pickle.load(pkl_file)
    pkl_file.close()
    return obj

suff_tree = treeFromJSON('suff_tree_long')
pref_tree = treeFromJSON('pref_tree_long')
all_words = loadPkl('/all_words_suff_wiki_7_10.pkl')

path_comp = os.path.dirname(os.path.abspath(__file__)) + '/comps1.txt';
lines_comp  = open(path_comp, 'r').readlines()
comp_list = []
for line in lines_comp:
    line1 = line.decode('utf-8').strip()
    comp_list.append(line1.lower())

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def _getPostBody(self):
        length = int(self.headers.getheader('content-length'))
        body = self.rfile.read(length).decode('utf-8')
        return body

    def do_POST(self):
        reload(try_text_json)
        from try_text_json import process

        text = self._getPostBody()
        res = process(text, pref_tree, suff_tree, comp_list, all_words)

        self._set_headers()
        self.wfile.write(json.dumps(res, separators=(',', ':')))

def run(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'ready!'
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
