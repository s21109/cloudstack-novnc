import base64

if __name__ == '__main__': 
    base = "MTkyLjE2OC4zMC41OXxpLTItMTc2LVZNfHRlc3Q="
    reqstr = base64.decodestring(base)
    print reqstr