#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Titanium Compiler plugin 
# __PROJECT_ID__
#

import os, sys, subprocess, codecs, hashlib

try:
    import json
except:
    import simplejson as json

# The Titanium build scripts contain their own json library (Patrick Logan's),
# so we have to figure out which json functions to use.
json_read = None
json_write = None
build_config = {}
if hasattr(json, 'loads'):
    json_read = json.loads
else:
    json_read = json.read
if hasattr(json, 'dumps'):
    json_write = json.dumps
else:
    json_write = json.write

ignoreFiles = ['.gitignore', '.cvsignore', '.DS_Store', 'TiUIwrapper.js']
ignoreDirs = ['.git','.svn','_svn', 'CVS']

ERROR_LOG_PREFIX = '[ERROR]'
INFO_LOG_PREFIX = '[INFO]'
DEBUG_LOG_PREIX = '[DEBUG]'

def project_root():
    current_dir = os.getcwd()
    project_root = "/"
    found_path = False
    tries = 0
    
    while found_path == False:
        
        if os.path.exists("%s/Resources/" % current_dir):
            
            project_root = current_dir
            
            found_path = True
        
        else:
            if tries == 5:
                die("You are not in a Titanium project...")
            
            if this_dir == "/":
                die("You are not in a Titanium project...")
            
            this_dir = current_dir.split('/').pop()
            current_dir = current_dir.replace('/' + this_dir, '')
            ++tries
    
    return project_root

def log(prefix, msg, stream=None):
    if not stream is None:
        print >> stream, "%s %s" % (prefix, msg)
    else:
        print "%s %s" % (prefix, msg)

def err(msg, stream=None):
    # Matches the [ERROR]... messages of the Titanium builder.py, so the
    # message can be recognized as an error for console purposes
    log(ERROR_LOG_PREFIX, msg, stream)

def info(msg):
    # Matches the [INFO]... messages of the Titanium builder.py, so the
    # message can be recognized as an info msgs for console purposes
    log(INFO_LOG_PREFIX, msg)

def debug(msg):
    # Matches the [DEBUG]... messages of the Titanium builder.py, so the
    # message can be recognized as an debug msgs for console purposes
    log(DEBUG_LOG_PREIX, msg)

def wrapperNeedsReloading(wrapper_file):
    #if len(sys.argv) < 2:
    #   proj_dir = os.getcwd()
    #elif sys.argv[1] == 'run' or sys.argv[1] == 'deploy':
    #    proj_dir = project_root()
    #else:
    #    proj_dir = sys.argv[1]
    
    #wrapper_file = os.path.join(proj_dir, 'Resources/TiUIwrapper.js')
    
    #ti_sdk = build_config['tiapp'].properties['sdk-version']
    
    #plugin_version = build_config['plugin'].get('version')
    
    #with open(wrapper_file, 'r') as f:
    #while True:
    #line1 = f.readline()
    #line2 = f.readline()
    
    #if line1.find(ti_sdk) and line2.find(plugin_version):
    return True
#else:
#    return True

#if not line2: break

def read_json_api():
    if len(sys.argv) < 2:
        proj_dir = os.getcwd()
    elif sys.argv[1] == 'run' or sys.argv[1] == 'deploy':
        proj_dir = project_root()
    else:
        proj_dir = sys.argv[1]
    
    ti_root = build_config['template_dir'].replace('/iphone', '').replace('/android', '')
    
    json_file = os.path.join(ti_root, 'api.jsca')
    info(json_file)
    objects = {}
    finalObjects = {}
    if os.path.exists(json_file):
        f = open(json_file, 'r')
        text = f.read()
        f.close()
        if len(text):
            objects = json_read(text)
            for field in objects['types']:
                if field.get('name').startswith('Titanium.UI'):
                    finalObjects[field.get('name')] = field
    return finalObjects

def write_file_wrapper(path, text):
    hashes_file = os.path.join(path, 'TiUIwrapper.js')
    info(hashes_file)
    f = open(hashes_file, 'w+')
    f.write(text)
    f.close()

def build_wrapper():
    if len(sys.argv) < 2:
        proj_dir = os.getcwd()
    elif sys.argv[1] == 'run' or sys.argv[1] == 'deploy':
        proj_dir = project_root()
    else:
        proj_dir = sys.argv[1]
    
    info('Wrapper compiled')
    api = read_json_api()
    
    ti_sdk = build_config['tiapp'].properties['sdk-version']
    
    plugin_version = build_config['plugin'].get('version')
    
    string = '// ' + ti_sdk + "\n"
    string +='// ' + plugin_version + "\n"
    
    string += 'var w=exports;'
    string += 'w.iOS={};'
    string += 'w.iPhone={};'
    string += 'w.Android={};'
    
    used_elements = []
    all_elements = []
    
    for key in api['Titanium.UI'].get('functions'):
        if key['name'].startswith('create'):
            all_elements.append(key)
    
    #for key in all_elements:
    for root, dirs, files in os.walk(proj_dir):
        for dir in dirs:
            if dir in ignoreDirs:
                dirs.remove(dir)
        if len(files) > 0:
            prefix = root[len(proj_dir):]
            for f in files:
                fp = os.path.splitext(f)
                if fp[1] == '.js':
                    fullpath = os.path.join(root,f)
                    relative = prefix[1:]
                    #js_contents = make_function_from_file(fullpath, pack=False)
                    ext = os.path.splitext(fullpath)
                    path = os.path.expanduser(fullpath)
                    if ext[1][1:] == 'js':
                        out = codecs.open(path,'r',encoding='utf-8').read()
                        for line in out.split(';'):
                            for method in all_elements:
                                if line.find(method['name']) != -1:
                                    if not method['name'] in used_elements:
                                        used_elements.append(method['name'])
    
    for key in all_elements:
        if key['name'] in used_elements:
            string += 'w.' + key['name'] + '=function(_args){this.proxy=Ti.UI.' + key['name'] + '(_args);};'
            
            if key['name'].replace('create', '')[0].isdigit():
                object_name = key['name'].replace('create', '_')
            else:
                object_name = key['name'].replace('create', '')
            
            for method in api['Titanium.UI.' + object_name].get('functions'):
                parameters = ''
                parm_count = 0
                param_view = ''
                if 'parameters' in method:
                    for param in method['parameters']:
                        parm_count += 1
                        parameters += param.get('name')
                        
                        if param.get('type').startswith('Titanium.UI'):
                            param_view = param.get('name')
                        
                        if parm_count != len(method.get('parameters')):
                            parameters += ','
                    
                    if param_view != '':
                        string += 'w.' + key['name'] + '.prototype.'+method.get('name')+'=function('+parameters+') {var '+param_view+'='+param_view+'.proxy||'+param_view+'; this.proxy.'+method.get('name')+'('+parameters+');};'
                    else:
                        string += 'w.' + key['name'] + '.prototype.' + method.get('name') + '=function('+parameters+') {this.proxy.' + method.get('name') + '('+parameters+');};'
                
                else:
                    string += 'w.' + key['name'] + '.prototype.' + method.get('name') + '=function() {this.proxy.' + method.get('name') + '();};'
            
            string += 'w.' + key['name'] + '.prototype.onDestroy=function() {};'
            string += 'w.' + key['name'] + '.prototype.release=function() {this.proxy.backgroundImage=undefined;this.proxy=undefined;this.onDestroy();};'
    
    string += 'exports = w'
    return string

def find_wrapper(path, file_hash_folder):
    for root, dirs, files in os.walk(path):
        for name in files:
            if name == 'TiUIwrapper.js':
                if wrapperNeedsReloading(os.path.join(root, name)):
                    info("Compiling Wrapper")
                    
                    file_hashes = build_wrapper()
                    write_file_wrapper(file_hash_folder, file_hashes)


def real_compile(config, file_hash_folder):
    if file_hash_folder is None:
        file_hash_folder = os.path.abspath(os.path.join(config['build_dir'], '..'))
    info(file_hash_folder)
    find_wrapper(os.path.join(config['project_dir'], 'Resources'), file_hash_folder)

def compile(config):
    global build_config
    build_config = config
    if len(sys.argv) < 2:
        proj_dir = os.getcwd()
    elif sys.argv[1] == 'run' or sys.argv[1] == 'deploy':
        proj_dir = project_root()
    else:
        proj_dir = sys.argv[1]
    
    resource_dir = os.path.join(proj_dir, 'Resources')
    if not os.path.exists(resource_dir):
        err("%s does not look like a Titanium project folder.  Resources/ folder not found." % proj_dir, sys.stderr)
    config = {'project_dir': proj_dir}
    if os.path.exists(os.path.join(proj_dir, 'Resources')):
        real_compile(config, os.path.join(proj_dir, 'Resources'))
    else:
        real_compile(config, proj_dir)