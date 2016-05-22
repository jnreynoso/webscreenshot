#!/usr/bin/python

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from urlparse import urlparse, parse_qs
from os import curdir, sep
import threading
import time
import os

PORT = 8080

class Handler(BaseHTTPRequestHandler):

    ENABLE_THREAD = None

    def do_GET(self):

        self.ENABLE_THREAD = False
        url = self.path
        parameters = parse_qs(urlparse(url).query)

        #Static Files
        if url == "/":
            url = "/index.html"

        if 'geturl' in self.path:
            self.ENABLE_THREAD = True

        try:
            send_reply = False
            param_validate = False

            if url.endswith(".html"):
                mimetype = 'text/html'
                send_reply = True
            elif url.endswith(".png"):
                mimetype = 'image/png'
                send_reply = True
            elif url.endswith(".js"):
                mimetype = 'application/javascript'
                send_reply = True
            elif url.endswith(".css"):
                mimetype = 'text/css'
                send_reply = True
            else:
                check_param = self.check_parameters(parameters)
                if check_param:
                    send_reply = True
                    param_validate = True
                    mimetype = 'image/png'

            if send_reply == True:

                if param_validate == True:
                    now = time.strftime("%Y%m%d%H%M%S") + '.png'
                    self.webkit2png(parameters,now)
                    f = open(os.getcwd() + '/screenshots/' + now)
                else:
                    f = open(curdir + sep + url)

                self.send_response(200)
                self.send_header('Content-type',mimetype)
                self.end_headers()
                self.wfile.write(f.read())
                f.close()

            return
        except IOError:
            self.send_error(404,'File Not Found: %s' % url)

    def check_parameters(self,parameters):
        paraments_allowed = ['url', 'width','height', 'format','scale','wait','transparent','aspect']
        result = False

        for param in parameters.keys():
            if param in paraments_allowed:
                result = True

        return result

    def make_arguments(self,parameters={}):
        arguments_allowed = ['url', 'width','height','wait','transparent','aspect']
        arguments = parameters.keys()
        output = ' -f png '
        go = False

        for argument in arguments:
            if argument in arguments_allowed:
                go = True

        if go == True:

            if arguments_allowed[0] in arguments:
                output = output + parameters[arguments_allowed[0]][0] + ' '
            if arguments_allowed[1] in arguments and arguments_allowed[2] in argument:
                output = output + '-g ' + parameters[arguments_allowed[1]][0] + ' ' + parameters[arguments_allowed[2]][0] + ' '
            elif arguments_allowed[1] in arguments:
                output = output + '-g ' + parameters[arguments_allowed[1]][0] + ' 768 '
            if arguments_allowed[3] in arguments:
                output = output + '-w ' + parameters[arguments_allowed[3][0] + ' ' ]
            if arguments_allowed[4] in arguments:
                output = output + '-T '
            if arguments_allowed[5] in arguments:
                output = output + '--aspect-ratio=' + parameters[arguments_allowed[5]][0] + ' '

        return output + '-o ' # Output File

    def webkit2png(self,parameters={},now=''):

        arguments = self.make_arguments(parameters)
        directory_screenshots = os.getcwd() + "/screenshots/" + now

        if self.ENABLE_THREAD == True:
            t = threading.Thread(target=os.system, args=("webkit2png" + arguments + directory_screenshots,))
            t.start()
        else:
            os.system("webkit2png" + arguments + directory_screenshots)

def main():
    try:
        server = HTTPServer(('',PORT),Handler)
        print 'Started HTTPServer on port ',PORT
        server.serve_forever()
    except KeyboardInterrupt:
        print ' | Close received, shutting down the web server'
        server.socket.close()

if __name__ == '__main__':
    main()
