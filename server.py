#!/usr/bin/python
from flask import Flask, render_template, send_file, redirect, request
import threading
import time
import os

app = Flask(__name__, static_url_path='/static')

#Static Files
@app.route('/<path:path>')
def static_proxy(path):
    return app.send_static_file(path)

#Home
@app.route('/')
def home():
    return app.send_static_file('index.html')

#Get URL Image
@app.route("/address", methods=['GET'])
def get_url():
    parameters = request.args
    ENABLE_THREAD = True
    webkit2png_arguments = make_arguments(parameters)
    screenshot_name = time.strftime("%Y%m%d%H%M%S") + '.png'
    webkit2png(parameters, screenshot_name, ENABLE_THREAD)

    return render_template('url.html', address=request.url_root + 'static/screenshots/' + screenshot_name)

#Get Image
@app.route("/image", methods=['GET'])
def get_image():
    parameters = request.args
    ENABLE_THREAD = False
    webkit2png_arguments = make_arguments(parameters)
    screenshot_name = time.strftime("%Y%m%d%H%M%S") + '.png'
    webkit2png(parameters, screenshot_name, ENABLE_THREAD)

    return send_file(os.getcwd() + '/static/screenshots/'+ screenshot_name, mimetype='image/png')

def make_arguments(parameters):
    arguments_allowed = {'url':None, 'width':None,'height':None,'wait':None,'transparent':None,'aspect':None}
    output = ' -f png '
    go = False

    for argument in arguments_allowed.keys():
        if parameters.get(argument, None) != None:
            arguments_allowed[argument] = 'filled'

    if arguments_allowed['url'] == 'filled':
        output = output + parameters.get('url',None) + ' '

    if arguments_allowed['width'] == 'filled' and arguments_allowed['height'] == None:
        output = output + '-g ' + parameters.get('width') + ' 768 '
    elif arguments_allowed['height'] == 'filled' and arguments_allowed['width'] == None:
        output = output + '-g ' + '900 ' + parameters.get('height')
    elif arguments_allowed['width'] and arguments_allowed['height'] == 'filled':
        output = output + '-g ' + parameters.get('width') + ' ' + parameters.get('height') + ' '

    if arguments_allowed['wait'] == 'filled':
        output = output + '-w ' + parameters.get('wait') + ' '
    if arguments_allowed['transparent'] == 'filled':
        output = output + '-T '
    if arguments_allowed['aspect'] == 'filled':
        output = output + '--aspect-ratio=' + parameters.get('aspect') + ' '

    return output + '-o ' # Output File

def webkit2png(parameters, now, ENABLE_THREAD):
    arguments = make_arguments(parameters)
    directory_screenshots = os.getcwd() + "/static/screenshots/" + now
    if ENABLE_THREAD == True:
        t = threading.Thread(target=os.system, args=("webkit2png" + arguments + directory_screenshots,))
        t.start()
    else:
        os.system("webkit2png" + arguments + directory_screenshots)

def main():
    try:
        app.run()
    except Exception:
        print '** Error ** | shutting down the web server'

if __name__ == "__main__":
    main()
