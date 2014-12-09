# Create your views here.
import re
import base64

from django.shortcuts import render_to_response
from django.template import RequestContext
from vrtManager.cookieutil import DES

from vrtManager.instance import wvmInstance

from xiangcloud.settings import WS_PORT
from xiangcloud.settings import WS_DESKEY


def console(request):
    """
    VNC instance block
    """
    if request.method == 'GET':
        hostname =  request.GET.get("host")
        name = request.GET.get("instance")
        display = name
        password = None
        login = None
        htype = 1
        
    try:
        conn = wvmInstance(hostname,
                           login,
                           password,
                           htype,
                           name)
        vnc_websocket_port = conn.get_vnc_websocket_port()
        vnc_passwd = conn.get_vnc_passwd()
    except:
        vnc_websocket_port = None
        vnc_passwd = None

    ws_port = vnc_websocket_port if vnc_websocket_port else WS_PORT
    ws_host = request.get_host()

    if ':' in ws_host:
        ws_host = re.sub(':[0-9]+', '', ws_host)

    response = render_to_response('console.html', locals(), context_instance=RequestContext(request))
    token = hostname + "|"+name +"|"+display
    des = DES()  
    des.input_key(WS_DESKEY)  
    encryptval = des.encode(token)  
    response.set_cookie('token', encryptval)
    return response
