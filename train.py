from util.imports import *
from util.objects import *
from util.locations import *
from util.helpers import *
from util.parameters import *

def train_yolov8(yolo_size, augmented=False, concatenated=False):
    # création du data.yaml
    if augmented:
        train_images_path = DATASET_AUGMENTED_PATH+'/images'
        save_dir = MODELS_AUGMENTED
        prefix = "augmented"
    elif concatenated:
        train_images_path = DATASET_CONCATENATED_PATH+'/images'
        save_dir = MODELS_CONCATENATED
        prefix = "concatenated"
    else:
        train_images_path = DATASET_TRAIN_PATH+'/images'
        save_dir = MODELS_TRAIN
        prefix = "train"
    
    valid_images_path = DATASET_VALID_PATH+'/images'
    print(valid_images_path)
    create_data_yaml(train_images_path, valid_images_path)

    # train
    yolo = YOLO(f'yolov8{yolo_size}.pt')
    # run = wandb.init(project="YOLOv8", entity="rally2023", name=f"run_{prefix}_{yolo_size}_{EPOCHS}_{BATCH_SIZE}")
    tracker = EmissionsTracker()
    tracker.start()
    yolo.train(data='data.yaml', epochs=EPOCHS, batch=BATCH_SIZE,
                save_period=10, patience=50, name=f"{prefix}_{yolo_size}_{EPOCHS}_{BATCH_SIZE}")
    co2: float = tracker.stop()
    emission_kwh = co2 * CO2_TO_KWH
    print(f'Emission: {emission_kwh}')

if __name__ == "__main__":
    train_yolov8('n')
    train_yolov8('n', augmented=True)
    train_yolov8('n', concatenated=True)

