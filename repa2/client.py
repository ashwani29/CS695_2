from __future__ import print_function
import sys
import libvirt
import time
import socket
import threading
import os


lst_of_IP = []
lst_of_SCKT = []
dictry = {}

def deleteVM():
    while(True):
            
        print("deleteVM assigned to thread: {}".format(threading.current_thread().name))
        domains = conn.listAllDomains(1)
        n = 11
        while(n):

            for domain in domains:
                time.sleep(4)
                var = domain.getCPUStats(True)
                var1 = var[0]['cpu_time']   
                print(var1) 
                time.sleep(4) 
                var = domain.getCPUStats(True)
                var2 = var[0]['cpu_time']   
                print(var2)
                var3 = ((var2-var1)/(4*1000000000))*100
                print("CPU decreasing  ",domain.name(), var3)    
                if(var3 > 20.0):
                    n = 11
                    break

                if(len(dictry) > 1):
                    if len(domains) !=0:
                        for domain in domains:
                            print(''+domain.name())
                            domainName = domain.name()
                            dom = conn.lookupByName(domainName)
                            ifaces = dom.interfaceAddresses(0)
                            vnet = list(ifaces.keys())
                            ip = ifaces[vnet[0]]['addrs'][0]['addr']
                            #print(ip)
                            # lst_of_IP.append(ip)
                            # print(lst_of_IP[0])                
                            # ip = lst_of_IP.pop(0)
                            dictry.pop(ip, None)
                            domain.destroy()
                            continue
            n = n-1              
        


        
def spawnVM():

    print("spawnVM assigned to thread: {}".format(threading.current_thread().name))
    domains = conn.listAllDomains(1)
    n = 10
    while(n):

        for domain in domains:
            time.sleep(4)
            var = domain.getCPUStats(True)
            var1 = var[0]['cpu_time']   
            print(var1) 
            time.sleep(4) 
            var = domain.getCPUStats(True)
            var2 = var[0]['cpu_time']   
            print(var2)
            var3 = ((var2-var1)/(4*1000000000))*100
            print("CPU increasing  ",domain.name(), var3)    
            if(var3 < 30.0):
                n = 11
                break
        n = n-1        


    domains = conn.listAllDomains(2)
    for domain in domains:
        domain.create()  
        time.sleep(20)
        domainName = domain.name()
        print(domainName,"$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        dom = conn.lookupByName(domainName)
        ifaces = dom.interfaceAddresses(0)
        vnet = list(ifaces.keys())
        ip = ifaces[vnet[0]]['addrs'][0]['addr']
        print(ip)
        lst_of_IP.append(ip)  

        s = socket.socket()          

        # Define the port on which you want to connect -----------
        port = 8081

        # connect to the server on local computer ---------
        s.connect((ip, port))
        lst_of_SCKT.append(s)
        time.sleep(3)
        dictry[ip] = s
        print(dictry[ip], "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        break
        


if __name__ == "__main__":

    conn = libvirt.open('qemu:///system')
    if conn == None:
        print('Failed to open connection to qemu:///system', file=sys.stderr)
        exit(1)
    else: 
        print('Hypervisor connected')
    

    domains = conn.listAllDomains(1)
    if len(domains) !=0:
        for domain in domains:
            # domain.destroy()
            # exit
            print(''+domain.name())
            domainName = domain.name()
            dom = conn.lookupByName(domainName)
            ifaces = dom.interfaceAddresses(0)
            vnet = list(ifaces.keys())
            ip = ifaces[vnet[0]]['addrs'][0]['addr']
            #print(ip)
            lst_of_IP.append(ip)
            # print(lst_of_IP[0])


    # domains = conn.listAllDomains(2) /////////////////////////////////////
    # for domain in domains:
    #     print(''+domain.name())
    t1 = threading.Thread(target=spawnVM, name='t1') 
    t1.start()           

    # time.sleep(10)
    # t2 = threading.Thread(target=deleteVM, name='t2') 
    # t2.start()  

    i=0

    for ip in lst_of_IP:
        print(ip)
        # Create a socket object -----------------
        s = socket.socket()          
  
        # Define the port on which you want to connect -----------
        port = 8081
  
        # connect to the server on local computer ---------
        s.connect((ip, port))
        lst_of_SCKT.append(s)
        dictry[ip] = s
        print(dictry[ip])
        print(i) 

    # n= 5
    
    while (True):
        # n=n-1
        dct_keys = list(dictry.keys())
        for key in dct_keys:
            # s = socket.socket()--------------
            s = dictry[key]
            # s.connect((key, 8081))-----------
            s.send('Ashwani'.encode())
            print(s.recv(1024))
            # time.sleep(0.002)


