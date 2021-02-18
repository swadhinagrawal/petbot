import os 
import cv2

def gstreamer_pipeline(
    capture_width=1280,
    capture_height=720,
    display_width=1280,
    display_height=720,
    framerate=60,
    flip_method=0,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )


# file 
file = "data"
  
# Parent Directory path 
parent_dir = "/home/petbot/jetracer/notebooks/"


# Path 
path = os.path.join(parent_dir, file) 
# print(path)
# os.mkdir(path) 
# Create the directory 
# 'GeeksForGeeks' in 
# '/home / User / Documents' 

print("Directory '% s' created" % file)
# cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
print("successful")
# while cv2.getWindowProperty("CSI Camera", 0) >= 0:
for i in range(20):
    print(i)
    cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
    ret_val, img = cap.read()
    cv2.imshow("CSI Camera", img)
#     cv2.imwrite(path+'/'+str(i)+'.jpg',img)