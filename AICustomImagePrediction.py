from imageai.Prediction.Custom import CustomImagePrediction
import os
execution_path = os.getcwd()


prediction = CustomImagePrediction()
prediction.setModelTypeAsResNet()
prediction.setModelPath(os.path.join(execution_path, "./models/model_ex-007_acc-0.587639.h5"))
prediction.setJsonPath(os.path.join(execution_path, "model_class.json"))
prediction.loadModel(num_objects=4)


predictions, probabilities = prediction.predictImage(os.path.join(execution_path, "8p.jpeg"), result_count=4)


for eachPrediction, eachProbability in zip(predictions, probabilities):
	print(eachPrediction + " : " + eachProbability)