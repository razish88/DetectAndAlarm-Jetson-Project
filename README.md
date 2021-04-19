# DetectAndAlarm-Jetson-Project

![image](https://user-images.githubusercontent.com/29065671/115146813-d3769280-a060-11eb-93cc-d58a9c55bf07.png)

Today we can find security cameras everywhere, but most of them record and save in hard disk/cloud, then if you suspicious and think something got wrong you can check the records.
This project makes things easier and in real-time, will add a customizable object detection feature, that’s mean you can tell the camera: “Please when you detect this object/s, send me an alarm.” That’s also mean you won’t be bothered by unnecessary surveillance alerts.
The object/s can be a person, a person with cell-phone, animals, cars, etc. (it depend on the model you are using to detect - I used = ssd-mobilenet-v2)
Customizable object detection feature can distinguish between suspicious movements in/around your home and normal, everyday activity, you define the objects of detecting. So, you’ll only be alerted with real-time security video when there’s an actual issue, rather than just usual stray object!

You can see the full list of objects you can define at ssd_coco_labels.txt

## Needed HW
1) C270 HD WEBCAM
2) Jetson Nano

## Setup
### Twilio
Open an account at https://www.twilio.com/login
Then Follow the this tutorial to send whatsapp message to your phone when alarm been detected:
https://www.twilio.com/blog/send-whatsapp-message-30-seconds-python

### Docker Contanier
Will use Hello AI World project as infrastructure, first thing we need to install the suitable image:
https://github.com/dusty-nv/jetson-inference/blob/master/docs/jetpack-setup-2.md

Then download the container:
https://github.com/dusty-nv/jetson-inference/blob/master/docs/aux-docker.md

## Run the code
1) Create new folder named "DetectAndAlarm" at "~/"
2) Copy detect-and-alarm.py & ssd_coco_labels.txt to it
3) Change the "to_whatsapp_number=" to your own number in detect-and-alarm.py
4) Enter the jetson folder --> cd jetson-inference
5) Mount the container with the folder you created --> docker/run.sh --volume ~/DetectAndAlarm:/DetectAndAlarm
6) Enter the folder --> cd /DetectAndAlarm
7) Export the needed vars for Twilio --> export TWILIO_ACCOUNT_SID='AC896b6c6793f7e0e9e40d6b8eaabddddd', export TWILIO_AUTH_TOKEN='64477a2e19f109fd1fb407ddddd'
8) Create a new virtual environment with the following Python 3 command --> python3 -m venv pywhatsapp
9) Activate the virtual-environmnet --> source pywhatsapp/bin/activate
10) Install twilio in it --> pip install twilio
11) Run the code --> ./detect-and-alarm.py --object_to_detect [object/objects to detect seperated by space] --interval [interval in secs between sending alarm messages] 

Example: ./detect-and-alarm.py --object_to_detect person "cell phone" --interval 300 

Thats mean if you detect person and cell phone in the same picture (both of them must be in the picture, if person or cell phone apear alone don't send alarm) send alarm and check again in loop every 5 min .
