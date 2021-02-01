#!/usr/bin/python3 -W ignore::DeprecationWarning

import json
import requests
import time
import ipaddress
import apifunctions
import cgi,cgitb

#remove the InsecureRequestWarning messages
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

"""
greg / celticcow make my life easier for cam tunnel lockdown
"""

"""
take 2 lists, send you the difference between the 2
"""
def ListDiff(li1, li2):
    return(list(list(set(li1)-set(li2)) + list(set(li2)-set(li1))))

def get_group_contents(mds_ip, group, sid):
    debug = 1
    end = "<br>"
    print("get_group_contents", end=end)

    group_contents = list()

    if(apifunctions.group_exist(mds_ip, group, sid)):
        if(debug == 1):
            print("group exist", end=end)

        grp_json = {
            "name" : group
        }

        get_grp_contents_json = apifunctions.api_call(mds_ip, "show-group", grp_json, sid)

        if(debug == 1):
            print(json.dumps(get_grp_contents_json), end=end)
            print("*****************", end=end)
            print(get_grp_contents_json['members'], end=end)
        
        for mem in get_grp_contents_json['members']:
            if(mem['type'] == "host"):
                if(debug == 1):
                    print(mem['ipv4-address'], end=end)
                group_contents.append(mem['ipv4-address'])
    
    return(group_contents)
#end of get_group_contents

def main():
    debug = 1
    end = "<br>"

    ## cgi get
    form = cgi.FieldStorage()

    #static's
    mds_ip = "146.18.96.16"  #"204.135.121.150"
    cma_ip = "146.18.96.25"  #"204.135.121.164"
    userid = "gdunlap"    #form.getvalue('user')
    passwd = "2"     #form.getvalue('password')

    ## html header and config data dump
    print ("Content-type:text/html\r\n\r\n")
    print ("<html>")
    print ("<head>")
    print ("<title>Cam Tunnel Lockdown</title>")
    print ("</head>")
    print ("<body>")

    print("Begin work", end=end)

    ##static for now ... will get from form
    site_code  = form.getvalue('site_name')  #"NPIT"
    site_num   = form.getvalue('site_code')  #"150"

    ## get the form data for SSPC
    autodim_raw = form.getvalue('autodim')
    sick_raw = form.getvalue('sick')
    controller_raw = form.getvalue('controllers')

    autodim_stage1 = str(autodim_raw)
    sick_stage1 = str(sick_raw)
    controller_stage1 = str(controller_raw)

    autodim_stage2 = autodim_stage1.split(' ')
    sick_stage2 = sick_stage1.split(' ')
    controller_stage2 = controller_stage1.split(' ')

    autodim = autodim_stage2[0].split()
    sick    = sick_stage2[0].split()
    controllers = controller_stage2[0].split()
    
    #for debug purpose bypassing cgi
    #autodim = ['10.81.229.91', '10.81.229.81']
    #sick = ['10.81.229.26', '10.81.229.27']
    #controllers = ['10.81.232.197', '10.81.232.231', '10.81.232.196', '10.81.233.196', '10.81.233.197', '10.81.232.226']

    if(debug == 1):
        print(autodim, end=end)
        print("----------------------------", end=end)
        print(sick, end=end)
        print("----------------------------", end=end)

    site_autodim = "SSPC-Autodim-" + site_code + "-" + site_num
    site_sick    = "SSPC-SICK-" + site_code + "-" + site_num

    #login to cma
    sid = apifunctions.login(userid, passwd, mds_ip, cma_ip)

    if(debug == 1):
        print("session id : " + sid, end=end)
    
    ####
    cma_autodim = get_group_contents(mds_ip, site_autodim, sid)
    cma_sick    = get_group_contents(mds_ip, site_sick, sid)

    ##need to compare the 
    # sick vs cma_sick
    # autodim vs cma_autodim

    if(debug == 1):
        print("#################################", end=end)
        print(cma_sick, end=end)
        print(sick, end=end)
        print(cma_autodim, end=end)
        print(autodim, end=end)

    if(ListDiff(sick, cma_sick) and ListDiff(autodim, cma_autodim)):
        print("Lists are different", end=end)
    else:
        #lists are good to go
        print("SSPC are equiv", end=end)
        tmp_name = "CamTunController-" + site_num
        if(apifunctions.group_exist(mds_ip, tmp_name, sid) == False):
            apifunctions.add_a_group(mds_ip, tmp_name, sid)

        ##add controllers to group
        for ip in controllers:
            apifunctions.add_a_host_with_group(mds_ip, "g-"+ip, ip, tmp_name,sid)
        
        apifunctions.add_group_to_group(mds_ip, tmp_name, "Camera-Tunnel-Controller", sid)
        
    #### rule build area
    ### change layer to "7VRF_FXG-Hub Security"
    # need to add
    # "install-on" : "fw-fxg-hubs"
    add_inbound = {
        "layer" : "TestONLY Network",
        "position" : {
            "bottom" : "CamTunnel-Lockdown"
        },
        "name" : "camtun-" + site_code + "1",
        "destination" : ["CamTunController-"+site_num, "SSPC-Autodim-" + site_code + "-" + site_num, "SSPC-SICK-" + site_code + "-" + site_num],
        "action" : "Accept",
        "track" : "Log"
    }
    add_outbound = {
        "layer" : "TestONLY Network",
        "position" : {
            "bottom" : "CamTunnel-Lockdown"
        },
        "name" : "camtun-" + site_code + "2",
        "source" : ["CamTunController-"+site_num, "SSPC-Autodim-" + site_code + "-" + site_num, "SSPC-SICK-" + site_code + "-" + site_num],
        "action" : "Accept",
        "track" : "Log"
    }

    rule1_result = apifunctions.api_call(mds_ip, "add-access-rule", add_inbound, sid)
    rule2_result = apifunctions.api_call(mds_ip, "add-access-rule", add_outbound, sid)

    print(rule1_result, end=end)
    print(rule2_result, end=end)


    print("start of publish", end=end)
    time.sleep(5)
    publish_result = apifunctions.api_call(mds_ip, "publish", {}, sid)
    print("publish results : " + json.dumps(publish_result))

    time.sleep(20)

    ## logout
    logout_result = apifunctions.api_call(mds_ip, "logout", {}, sid)
    if(debug == 1):
        print(logout_result)
    
    print("------- end -------", end=end)
    print("</body>")
    print("</html>")
#end of main

if __name__ == "__main__":
    main()
#end of program