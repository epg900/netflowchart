from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from netmiko import ConnectHandler
import getpass,tqdm,os,re,json,sys,random
from itertools import groupby
from operator import itemgetter
import time
from datetime import datetime

net_obj=None

ipcol = {}

def getnetfl2(out2,tf):
    sumval=0
    xval=[]
    allip={}   
    sdata = sorted(out2,key = itemgetter('srcip'))
    gbsrcip = {}
    for k,g in groupby(sdata,key=itemgetter('srcip')):
        gbsrcip[k] = list(g)
    
    for arr in gbsrcip:
        sumval=0
        for i in gbsrcip[arr]:
            if int(i['pkts']) > sumval:
                sumval=int(i['pkts'])
        allip[arr] = sumval
        
    xval.append(datetime.now().strftime('%H:%M:%S'))
    return allip, xval

 
def index(request):
    return HttpResponse('<H2>Use This Url Template:</H2><BR/><H3>[server_IP]/[router_IP]/[Number_of_X_Point]/[Sleep_Time_between_Point]</H3>')

def req(request,host,tm=20,per=6):
    conf={'device_type':'cisco_ios', 'host':host, 'username':settings.USER, 'password':settings.PASSWD}
    global net_obj
    net_obj=ConnectHandler(**conf)
    out2={}
    out2=net_obj.send_command("show ip cache flow",use_textfsm=True,textfsm_template="netflow.textfsm")
    allip, xval = getnetfl2(out2,True)
    for ip in allip:
        ipcol[ip]={}
        ipcol[ip]['data']=allip[ip]
        ipcol[ip]['color']=f'#{random.randint(0,255):02x}{random.randint(0,255):02x}{random.randint(0,255):02x}'
    return render(request,'netflow.html',context={'xval' : xval,'tm' : tm, 'per' : per, 'ipcol' : ipcol })

def req2(request):
    global net_obj
    out2={}
    out2=net_obj.send_command("show ip cache flow",use_textfsm=True,textfsm_template="netflow.textfsm")
    allip, xval = getnetfl2(out2,False)
    for ip in allip:
        if ip not in ipcol:
            ipcol[ip]={}
            ipcol[ip]['data']=allip[ip]
            ipcol[ip]['color']=f'#{random.randint(0,255):02x}{random.randint(0,255):02x}{random.randint(0,255):02x}'
        else:
            ipcol[ip]['data']=allip[ip]
    return JsonResponse({'xval' : xval, 'ipcol' : ipcol })


       
    
