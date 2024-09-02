# tree-recognition

This repository contains code and resources for training YOLOv8 models for object detection with a focus on evaluating the environmental impact of the training process. The project utilizes different configurations of datasets, including augmented and concatenated versions, to assess model performance and carbon emissions.

## Installation
To set up the environment, install the required Python packages listed in requirements.txt:
`pip install -r requirements.txt`

## Project Overview

The main objectives of this project are:
- **Data Augmentation:** Apply various data augmentation techniques to enhance the training dataset.
- **Train YOLOv8 Models:** Train object detection models using various dataset configurations.
- **Track Emissions:** Monitor and report the carbon emissions produced during training.
- **Analyze Results:** Evaluate model performance based on accuracy metrics and environmental impact.

## Data
The dataset is organized within the `Larch_Daset` folder. Two subsets are present: one with annotations (folder names ending with '7') and another without annotations (folder names ending with '9'). In both cases, bounding box annotations and tree types are included. Unfortunately, this dataset cannot be pushed on git because of its size 3.6 GB, so the following part is about this. However the dataset used for training is on the git in the `Data` so you should not need to do the following step anymore. If so go on the train tab.

To obtain the data:

1. Click on this [link](https://storage.googleapis.com/public-datasets-lila/larch-casebearer/Data_Set_Larch_Casebearer.zip) to download the Larch Dataset.
2. Extract the directory.
3. Open the extracted directory.
4. Copy all the folders (`Ctrl+A`, `Ctrl+C`).
5. Go back to your local repo, create a `Larch_Dataset/` folder.
6. Paste everything into your `Larch_Dataset/` folder.

You should have an architecture like this:
``` 
Larch_Dataset
├── Bebehojd_20190527
├── Bebehojd_20190819
├── Ekbacka_20190527
├── Ekbacka_20190819
├── Jallasvag_20190527
├── Jallasvag_20190819
├── Kampe_20190527
├── Kampe_20190819
├── Nordkap_20190527
└── Nordkap_20190819 
```

From this point on, you can preprocess the data by running the file `preprocessing.py`. This script will create a `Data/` folder and divide the data into three parts: **Train**, **Test**, and **Validation**. Simultaneously, the script transforms the label files from XML to text files using the YOLO format, and resize the images to the YOLO format as well which is (640,640). For more information about the YOLO format, refer to this [link](https://docs.ultralytics.com/yolov5/tutorials/train_custom_data/#21-create-datasetyaml).

Upon completing this step, you should still have your original `Larch_Dataset/` alongside the newly created `Data/`. If desired, you can remove the `Larch_Dataset/` directory to free up space. Your `Data/` directory should have the following structure:


```
Data
├── test
│   ├── images
│   └── labels
├── train
│   ├── images
│   └── labels
└── valid
    ├── images
    └── labels
```
### Annotations
For the annotated subset:
- **Bounding Box Annotations:** Present for all images.
- **Damage Annotations:**
  - **H:** Healthy
  - **LD:** Light Damage
  - **HD:** High Damage
  - **Other:** Unspecified

The tree type is also annotated:
- **Larch:** Pertaining to the trees of interest.
- **Other:** Denoting trees that are not relevant to the project.

## Data Augmentation
To enhance the training dataset, you need to run the datamodule.py script. This script performs data augmentation and concatenates datasets to improve model training. Execute the following command to run the data augmentation and concatenation process:
`python datamodule.py`

This script generates augmented datasets using various techniques, concatenates them with the original datasets, and saves the results to the appropriate directories.

## Train the model

Before to train you need to import the yolov8 repository. You need to be in your project repo and clone the yolov8 repo with this command:
**`git clone git@github.com:ultralytics/yolov8.git`**

From here you can try to train the model. I provide here an example of command to pass through the terminal but you can change every parameter you want following the ones in the `train.py` file of the yolov8 repo. Also you need to be in your repo in the yolov8 repo to execute the following command:
`python train.py --data ../data.yaml --weights yolov8n.pt --img 640 --epochs 10 --batch-size 16`

You can change the batch size to 8 if you are struggling running the training. You can also increase or decrease the amount of epochs.

Our training process tracks the carbon emissions using the `EmissionsTracker`. This feature monitors CO2 emissions produced during training and converts it to energy consumption (kWh) using the conversion factor `CO2_TO_KWH`.

## Demo

To test the models on your images, use Streamlit to run the demo:
`streamlit run front.py`

![demo](demo.gif)

## Visualizing Results

Run the `analysis.py` script to generate plots and rankings: 
`python analysis.py`
