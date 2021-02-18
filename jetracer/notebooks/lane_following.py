import cv2
import numpy as np
import matplotlib.pyplot as plt
from jetracer.nvidia_racecar import NvidiaRacecar
import os 
import keyboard

def make_points(image, line):
    slope, intercept = line
    y1 = int(image.shape[0])# bottom of the image
    y2 = int(y1*3/5)         # slightly lower than the middle
    x1 = int((y1 - intercept)/slope)
    x2 = int((y2 - intercept)/slope)
    return [[x1, y1, x2, y2]]
 
def average_slope_intercept(image, lines):
    left_fit    = []
    right_fit   = []
    if lines is None:
        return None
    for line in lines:
        for x1, y1, x2, y2 in line:
            fit = np.polyfit((x1,x2), (y1,y2), 1)
            slope = fit[0]
            intercept = fit[1]
            if slope < 0: # y is reversed in image
                left_fit.append((slope, intercept))
            else:
                right_fit.append((slope, intercept))
    # add more weight to longer lines
    if len(left_fit) and len(right_fit):
    ##over-simplified if statement (should give you an idea of why the error occurs)
        left_fit_average  = np.average(left_fit, axis=0)
        right_fit_average = np.average(right_fit, axis=0)
        left_line  = make_points(image, left_fit_average)
        right_line = make_points(image, right_fit_average)
        averaged_lines = [left_line, right_line]
        return averaged_lines
 
def canny(img):
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    kernel = 5
    blur = cv2.GaussianBlur(gray,(kernel, kernel),0)
    canny = cv2.Canny(gray, 50, 150)
    return canny
 
def display_lines(img,lines):
    line_image = np.zeros_like(img)
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(line_image,(x1,y1),(x2,y2),(255,0,0),10)
    return line_image
 
def region_of_interest(canny):
    height = canny.shape[0]
    width = canny.shape[1]
    print([height,width])
    mask = np.zeros_like(canny)
    
    triangle = np.array([[
    (0, height/2),
    (0, height),
    (width, height),(width, height/2)]], np.int32)
    cv2.fillPoly(mask, triangle, 255)
    masked_image = cv2.bitwise_and(canny, mask)
    return masked_image

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
# os.mkdir(path) 

print("Directory '% s' created" % file)
cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
print("successful")


car = NvidiaRacecar()
car.throttle = 0
car.steering = 0.5

i = 0
print("press keys")
while True:
    '''while True:
        ret_val,image = cap.read()
    #   cv2.imshow("CSI Camera", image)
        cv2.imwrite(path+'/'+str(i)+'.jpeg',image)
        i+=1'''
    
    if keyboard.is_pressed("w"):
        car.throttle = 1.0
    elif keyboard.is_pressed("s"):
        car.throttle = -1.0
    elif keyboard.is_pressed("d"):
        car.steering = 1.0
    elif keyboard.is_pressed("a"):
        car.steering = -1.0
    elif keyboard.is_pressed("z"):
        car.throttle = 0.0
    elif keyboard.is_pressed("q"):
        break
    else:
        pass
#     car.steering = float(input("Give steering:"))
#     car.throttle = float(input("Give throttle:"))

