from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from netmiko import ConnectHandler
import getpass,tqdm,os,re,json,sys,random
from itertools import groupby
from operator import itemgetter
import time
from datetime import datetime

def getnetfl(user='', passwd='', host='', loop = 5, sleep = 1):
    conf={'device_type':'cisco_ios', 'host':host, 'username':user, 'password':passwd}
    net_obj=ConnectHandler(**conf)

    sumval=0
    allip={}
    xval=[]
    colorlst=[]

    for n in range(loop):
        out2={}
        out2=net_obj.send_command("show ip cache flow",use_textfsm=True,textfsm_template="netflow.textfsm")
        #net_obj.disconnect()
        sdata = sorted(out2,key = itemgetter('srcip'))
        gbsrcip = {}
        for k,g in groupby(sdata,key=itemgetter('srcip')):
            gbsrcip[k] = list(g)
        
        for arr in gbsrcip:
            sumval=0
            if arr not in allip:
                allip[arr]=[]
            for i in gbsrcip[arr]:
                sumval+=int(i['pkts'])
            allip[arr].append(sumval)
            colorlst.append(f'#{random.randint(0,255):02x}{random.randint(0,255):02x}{random.randint(0,255):02x}')
        time.sleep(sleep)        
        xval.append(datetime.now().strftime('%H:%M:%S'))
    
    return allip, xval, colorlst


def index(request):
    allip, xval, colorlst = getnetfl(settings.USER,settings.PASSWD,settings.HOST)       
    return render(request,'netflow.html',context={'allip' : allip, 'xval' : xval, 'colorlst' : colorlst })

def req(request,host,loop=5,sleep=1):
    allip, xval, colorlst = getnetfl(settings.USER,settings.PASSWD,host,loop,sleep)       
    return render(request,'netflow.html',context={'allip' : allip, 'xval' : xval, 'colorlst' : colorlst })

def req2(request,host,loop=5,sleep=1):
    allip, xval, colorlst = getnetfl(settings.USER,settings.PASSWD,host,loop,sleep)
    return JsonResponse({'allip' : allip, 'xval' : xval, 'colorlst' : colorlst })


       
    
