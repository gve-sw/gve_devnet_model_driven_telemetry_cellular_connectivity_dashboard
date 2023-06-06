## READ ME:
# In case this script is used: 
# - Adjust the adjust._env file according to your requirements and IOS XE device configuration
# - Make sure the dependencies (under '# load modules' below) are installed and working
# - Execute the whole script at once, then start the subscription enablement process by running the start_subscriptions() function
## ----

# load modules
from ncclient import manager
import os
import time
from dotenv import load_dotenv

def start_subscriptions():
   # load environmental variables (from local .env file) # ---
   load_dotenv()

   # define specifications of IOS XE device
   ios_xe_device1 = {
       
        # IP info of IOS XE device (e.g. ISR router)
        'ip': os.getenv("TEL_IP_ADDRESS"),
        'port': os.getenv("TEL_PORT"),
        
        # login credentials for IOS XE device
        'username': os.getenv("TEL_USERNAME"),
        'password': os.getenv("TEL_PASSWORD")
    }
   
   # subscriptions
   subscription_list = os.getenv("TEL_SUBSCRIPTION_LIST").split(', ')
   period_list = os.getenv("TEL_PERIOD_LIST").split(', ')
   x_path_list = os.getenv("TEL_X_PATH_LIST").split(', ')
   ip_add_list = os.getenv("TEL_IP_ADD_LIST").split(', ')
   port_list = os.getenv("TEL_PORT_LIST").split(', ')

   # ---
   
   # open external xml document defining subscription
   netconf_template = open('telemetry/framework.xml').read()

   # establish connection to device (load specifications mentioned above)
   print("Establishing connection to your IOS XE device")
   m = manager.connect(host=ios_xe_device1['ip'], port=ios_xe_device1['port'], username=ios_xe_device1['username'],
                       password=ios_xe_device1['password'], device_params={'name':'iosxe'}, hostkey_verify=False)
   
   # loop through subscriptions
   for i in range(0, len(subscription_list)):
        print("Working on subscription ", subscription_list[i])
        
        netconf_payload = netconf_template.format(
          
          # subscription is sub id, period is in milliseconds (min. 100)
          subscription = subscription_list[i],
          
          # interval (in milliseconds)
          period = period_list[i],
          
          # xpath definition (use Cisco YANG Suite to configure)
          xpath = x_path_list[i],
          
          # IP address of receiver
          ip_address = ip_add_list[i],
          
          # port of receiver
          port = port_list[i])
        
        # update configuration
        response = m.edit_config(netconf_payload, target="running")
        
        if response.ok:
            print("Added subscription ",  subscription_list[i], " successfully")
            time.sleep(1)