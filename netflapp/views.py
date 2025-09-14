from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from netmiko import ConnectHandler
import getpass,tqdm,os,re,json,sys,random
from itertools import groupby
from operator import itemgetter
import time
from datetime import datetime

net_obj = {}
ipcol = {}

def getnetfl2(out2,tf):
    sumval=0
    xval=[]
    allip={}    
    sdata = sorted(out2,key = itemgetter('srcipaddress'))
    gbsrcip = {}
    for k,g in groupby(sdata,key=itemgetter('srcipaddress')):
        gbsrcip[k] = list(g)
    
    for arr in gbsrcip:
        allip[arr] = max([int(float(i['active']))*int(i['bytes']) for i in gbsrcip[arr]])
        
    xval.append(datetime.now().strftime('%H:%M:%S'))
    return allip, xval

 
def index(request):
    return HttpResponse('<H2>Use This Url Template:</H2><BR/><H3>[server_IP]/[router_IP]/[Number_of_X_Point]/[Sleep_Time_between_Point]</H3>')

def req(request,host,tm=20,per=6):
    conf={'device_type':'cisco_ios', 'host':host, 'username':settings.USER, 'password':settings.PASSWD}
    request.session['ipx']=str(host)
    global net_obj
    net_obj[request.session['ipx']]=ConnectHandler(**conf)
    out2={}
    out2=net_obj[request.session['ipx']].send_command("show ip cache verbose flow",use_textfsm=True,textfsm_template="netflowv2.textfsm")    

    allip, xval = getnetfl2(out2,True)
    
    ipcol[request.session['ipx']]={}
    for ip in allip:
        ipcol[request.session['ipx']][ip]={}
        ipcol[request.session['ipx']][ip]['data']=round(allip[ip]/1024)
        ipcol[request.session['ipx']][ip]['color']=f'#{random.randint(0,255):02x}{random.randint(0,255):02x}{random.randint(0,255):02x}'
    return render(request,'netflow.html',context={'xval' : xval,'tm' : tm, 'per' : per, 'ipcol' : ipcol })

def req2(request):
    out2={}
    global net_obj
    out2=net_obj[request.session['ipx']].send_command("show ip cache verbose flow",use_textfsm=True,textfsm_template="netflowv2.textfsm")    

    allip, xval = getnetfl2(out2,False)
    for ip in allip:
        if ip not in ipcol:
            ipcol[request.session['ipx']][ip]={}
            ipcol[request.session['ipx']][ip]['data']=round(allip[ip]/1024)
            ipcol[request.session['ipx']][ip]['color']=f'#{random.randint(0,255):02x}{random.randint(0,255):02x}{random.randint(0,255):02x}'
        else:
            ipcol[request.session['ipx']][ip]['data']=round(allip[ip]/1024)
    return JsonResponse({'xval' : xval, 'ipcol' : ipcol })


       
    
