from ultralytics import YOLO

# Load a model
model = YOLO('PT/Humain.pt')  # load a custom trained model

# Export the model
model.export(format='engine', device=0, half=True)