#!/usr/bin/env python
# coding: utf-8

# In[1]:


from opcua import Server, Client, ua, uamethod

from snap7.client import Client as SnapClient
from snap7.types import areas
from snap7.util import *
from plc_utils import read_data, write_data


from random import randint
import datetime
import time
import os
import cv2
#from face_server_security import OPC_SERVER_SECURITY


# In[2]:


server = Server()
opc_server = OPC_SERVER_SECURITY()
global plc
plc=SnapClient()


# In[3]:


url = "opc.tcp://127.0.0.1:4840"
server.set_endpoint(url)


# In[4]:



plc_ip="192.168.0.1"#usually same in all s7s but confirm kwa TIA
plc.connect(plc_ip, 0, 1)
plc.get_connected()


# In[5]:


name = "OPC_Server_Analytic_station"
addspace = server.register_namespace(name)#address space


# In[6]:


node = server.get_objects_node()
plc_node = node.add_object(addspace, "PLC_S71200")


# In[7]:

#(addspace,"variable_name",initial_value)
process_PH=plc_node.add_variable(addspace,"process_PH",0)   
setpoint = plc_node.add_variable(addspace, "setpoint",0.0 )
start = plc_node.add_variable(addspace, "start",False, ua.VariantType.Boolean )
stop = plc_node.add_variable(addspace, "stop",False, ua.VariantType.Boolean )


# In[8]:


process_PH.set_writable()
setpoint.set_writable()
start.set_writable()
stop.set_writable()


# In[9]:


server.start()
print("Server started at {}".format(url))

#opc_server.init_opc_server_security('192.168.43.104')
while True:
    #recognized= opc_server.client_authentication()
    #while recognized:
    process_PH.set_value(read_data(plc, 'IW98'))
    print(process_PH)
    setpoint.set_value(read_data(plc, 'DB3.DBD0'))
    start.set_value(read_data(plc, 'M0.2'))
    
    #stop.set_value(read_data(plc, 'M0.3'))
    #print(stop)#prints the node id used below
    stop = server.get_node('ns=2; i=5')
    stop = Stop.get_value()
    print(stop)#prints the value at the node in this case False


        

        


# In[ ]:




