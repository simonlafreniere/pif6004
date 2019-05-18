from imageai.Detection import ObjectDetection
import os

execution_path = os.getcwd()
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
        result.append(eachObject["box_points"])
    return result

def main():
    print('proximitySensor')

if __name__ == '__main__':
    main()