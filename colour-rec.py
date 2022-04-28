from serial import Serial
import cv2 as cv
import numpy as np


arduino = Serial('/dev/cu.usbserial-1410', 9600, timeout=0.1) # initiate arduino connection 

# dicts containing colour lower and upper hsv values
red = {
    "lower" : [136, 87, 111],
    "upper" : [180, 255, 255],
    "name" : "red"
}

blue = {
    "lower" : [94, 80, 2],
    "upper" : [120, 255, 255], 
    "name" : "blue"
}

green = {
    "lower" : [25, 52, 72],
    "upper" : [102, 255, 255],
    "name" : "green"
}

# provide function with hsv_values to find the desired colours
def track_colour(hsv_values):

    # set the camera source
    camera = cv.VideoCapture(0)

    while True:
        # read video source saving frames as imgs - convert to hsv colour space
        _, image_frame = camera.read()
        hsv_convert =  cv.cvtColor(image_frame, cv.COLOR_BGR2HSV)

        # use hsv values provided to define colour contours
        colour_lower, colour_upper = np.array(hsv_values["lower"], np.uint8), np.array(hsv_values["upper"], np.uint8)
        colour_mask = cv.inRange(hsv_convert, colour_lower, colour_upper)

        kernal = np.ones((5, 5), "uint8")
        colour_mask = cv.dilate(colour_mask, kernal)
        res_colour = cv.bitwise_and(image_frame, image_frame, 
                              mask = colour_mask)

        contours, hierarchy = cv.findContours(colour_mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
      
        for pic, contour in enumerate(contours):
            area = cv.contourArea(contour)
            if(area > 5000 and area < 20000): # this conditional can be changed to adjust size of colour box found
                x, y, w, h = cv.boundingRect(contour)
                mid_x, mid_y = int((x + w) / 2), int((y + h) / 2)
                position = f"X{mid_x} Y{mid_y}"
                arduino.write(position.encode('utf-8'))
                image_frame = cv.rectangle(image_frame, (x, y), 
                                       (x + w, y + h), 
                                       (0, 0, 255), 2)
                
                cv.putText(image_frame, hsv_values["name"] , (x, y),
                        cv.FONT_HERSHEY_SIMPLEX, 1.0,
                        (0, 0, 255))    
    

        cv.imshow("Colour Detection", image_frame)
        if cv.waitKey(10) & 0xFF == ord('q'):
            cv.destroyAllWindows()
            break

if __name__ == "__main__":
    track_colour(green)

