from imageai.Detection import ObjectDetection
import os
import re

execution_path = os.getcwd()
boxPosition = []
result = []

def crop(image):
    return image[170:,:]

def getTraffic(img):
    image = crop(img)
    detector = ObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath( os.path.join(execution_path , "yolo.h5"))
    detector.loadModel(detection_speed="fastest")
    detections = detector.detectObjectsFromImage(input_image=image, input_type="array", minimum_percentage_probability=30)
    for eachObject in detections:
        boxPosition.append(eachObject["box_points"])
    for eachObject in boxPosition:
        eachObject = re.sub('[()]', '', str(eachObject))
        x1,y1,x2,y2 = eachObject.split(',')
        x =(int(x1)+int(x2))/2
        y =(int(y1)+int(y2))/2
        result.append("(" + str(int(x)) + ", " + str(int(y)) + ")")
    return result

def main():
    print('proximitySensor')

if __name__ == '__main__':
    main()