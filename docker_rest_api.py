# -*- coding: utf-8 -*-

import json
import urllib2
import logging
import os
import string
import subprocess
import base64
import string
import getpass
import optparse
import ConfigParser
import commands
import sys
import getopt
import re
import gobject
import time
import pango # set font style and size

DKCONTNM='day01_vdi01'
DKCONTIP=''
ERROR_CODE=''
DKHOST='127.0.0.1'
DKPORT='2375'

class DK_RESTAPI:
    def GET_url(self,URL):
        global ERROR_CODE
        request = urllib2.Request(URL)
        request.add_header("Content-Type", "application/json;charset=utf-8")
        request.add_header("Accept","application/json")
        try:
            jsondata = urllib2.urlopen(request).read()
        except urllib2.URLError, e:
            ERROR_CODE = str(e)
            return False
        list_dict = json.loads(jsondata)
        return list_dict
    def POST_url(self,URL, json_req):
        global ERROR_CODE
        request = urllib2.Request(URL)
        request.add_header("Content-Type", "application/json;charset=utf-8")
        request.add_header("Accept","application/json")
        request.get_method = lambda: 'POST'
        try:
            jsondata = urllib2.urlopen(request, json_req).read()
        except urllib2.URLError, e:
            ERROR_CODE = str(e)
            return False
        if jsondata.strip(): # judge jsondata is null
            list_dict = json.loads(jsondata)
            return list_dict

class DK_OPS:
    def __init__(self):
        self.dk_rest_api = DK_RESTAPI()
    def cont_info(self, cont_nm):
        cont_url = r'http://%s:%s/containers/json?all=1' % (DKHOST, DKPORT)
        cons_ls_dict = self.dk_rest_api.GET_url(cont_url)
        for con in cons_ls_dict:
            if con['Names'][0] == u'/' + u'%s' % DKCONTNM:
                return con['Id']
		return None

    def get_cont_stat(self, cont_id):
        global DKCONTIP
        cont_url = r'http://%s:%s/containers/%s/json' % (DKHOST, DKPORT, cont_id)
        cont_stat_dict = self.dk_rest_api.GET_url(cont_url)
        if cont_stat_dict['State']['Running']:
            DKCONTIP = cont_stat_dict['NetworkSettings']['IPAddress']
            return True
        else:
            return False

    def check_cont_stat(self, cont_id):
        global DKCONTIP
        cont_url = r'http://%s:%s/containers/%s/json' % (DKHOST, DKPORT, cont_id)
        time.sleep(2)
        i = 0;
        while i < 10:
            cont_stat_dict = self.dk_rest_api.GET_url(cont_url)
            print cont_stat_dict
            if cont_stat_dict['State']['Running']:
                break
            time.sleep(3)
            i += 1
        if i >= 10:
            return False
        else:
            DKCONTIP = cont_stat_dict['NetworkSettings']['IPAddress']
            return True

    def cont_act(self, cont_id, cont_act):
        cont_url = r'http://%s:%s/containers/%s/%s' % (DKHOST, DKPORT, cont_id, cont_act)
        self.dk_rest_api.POST_url(cont_url, '')

if __name__ == '__main__':
    dk_action = DK_OPS()
    dk_cont_id = dk_action.cont_info(DKCONTNM)
    if dk_cont_id is None:
       print "Can not find the container %s" % DKCONTNM
       sys.exit(1)
    if dk_action.get_cont_stat(dk_cont_id):
       os.system('vncviewer %s:1 -passwd passwd' % DKCONTIP)
    else:
       dk_action.cont_act(dk_cont_id, 'start')
       if dk_action.check_cont_stat(dk_cont_id):
           os.system('vncviewer %s:1 -passwd passwd' % DKCONTIP)











