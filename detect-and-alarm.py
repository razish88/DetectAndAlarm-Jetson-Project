#!/usr/bin/python3

import jetson.inference
import jetson.utils
import argparse
import sys
import time
from twilio.rest import Client

# parse the command line
parser = argparse.ArgumentParser(description="Locate objects in a live camera stream using an object detection DNN.", 
                                 formatter_class=argparse.RawTextHelpFormatter, epilog=jetson.inference.detectNet.Usage() +
                                 jetson.utils.videoSource.Usage() + jetson.utils.videoOutput.Usage() + jetson.utils.logUsage())

parser.add_argument("--object_to_detect",'--list', nargs='+', help="Objects you want to detect and send alarm", required=True)
parser.add_argument("--interval", type=int, default=60, help="interval in secs between sending alarm messages")

try:
    opt = parser.parse_known_args()[0]
except:
    print("")
    print("Please enter at least one object to detect\n")
    sys.exit(0)

# client credentials are read from TWILIO_ACCOUNT_SID and AUTH_TOKEN
client = Client()

# this is the Twilio sandbox testing number
from_whatsapp_number='whatsapp:+14155238886'

# replace this number with your own WhatsApp Messaging number
to_whatsapp_number='whatsapp:+972540000000'

# load the object detection network
net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.5)

# Map the indexes to names 
ssd_coco_lables_list = open("ssd_coco_labels.txt").readlines()
ssd_coco_lables_list = list(map(lambda s: s.strip(), ssd_coco_lables_list))
detections_list = []
# 1 sec = 15 loops
interval_in_sec = 15 * opt.interval
counter = 0
alert_message = "Alert: Suspicious movments!"

# create video sources & outputs
camera = jetson.utils.videoSource("/dev/video0")     
display = jetson.utils.videoOutput("display://0") 
   
# process frames until the user exits
while display.IsStreaming():
    # capture the next image
    img = camera.Capture()
    
     # detect objects in the image (with overlay)
    detections = net.Detect(img)
    
    # Add the detection to the list 
    for detection in detections:
        detections_list.append(ssd_coco_lables_list[detection.ClassID])
        
    # render the image
    display.Render(img)

    # update the title bar
    display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))
    result = all(elem in detections_list for elem in opt.object_to_detect)
    if result:
        if(counter % interval_in_sec == 0):
           client.messages.create(body=alert_message, from_=from_whatsapp_number, to=to_whatsapp_number)           
           time.sleep(10)
        counter += 1
 
    detections_list = []

