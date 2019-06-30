from imageai.Prediction.Custom import ModelTraining
model_trainer = ModelTraining()
model_trainer.setModelTypeAsResNet()
model_trainer.setDataDirectory("MODERN_CAR_RACING")
model_trainer.trainModel(num_objects=4, num_experiments=30, 
						enhance_data=False, batch_size=16, 
						show_network_summary=True)