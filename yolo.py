'''


import os
import subprocess
from roboflow import Roboflow


def run_yolov5_pipeline():
    # Clone the YOLOv5 repository
    repository_url = "https://github.com/ultralytics/yolov5"
    directory_name = "yolov5"
    subprocess.run(f"git clone {repository_url} {directory_name}", shell=True)

    # Change directory to yolov5 and install requirements
    os.chdir("yolov5")
    subprocess.run("pip install -r requirements.txt", shell=True)

    # Create datasets directory if it doesn't exist and change directory
    os.makedirs("../datasets/", exist_ok=True)
    os.chdir("../datasets/")

    # Install Roboflow and download dataset
    subprocess.run("pip install roboflow", shell=True)
    rf = Roboflow(api_key="4hrmudsMFPu6NsoHy1is")
    project = rf.workspace("cybersecurityproject").project("network-components")
    dataset = project.version(12).download("folder")

    # Set environment variable for the dataset
    dataset_name = dataset.location.split(os.sep)[-1]
    os.environ["Network_Components_Image_Dataset"] = dataset_name

    # Change directory back to yolov5
    os.chdir("../yolov5")

    # Train the YOLOv5 model
    train_command = "python classify/train.py --model yolov5s-cls.pt --data Network-Components-12 --epochs 100 --img 451 --pretrained weights/yolov5s-cls.pt"
    subprocess.run(train_command, shell=True)

    # Validate the trained model
    val_command = "python classify/val.py --weights runs/train-cls/exp12/weights/best.pt --data ../datasets/Network-Components-12"
    subprocess.run(val_command, shell=True)

    # Get the path of an image from the test or validation set
    if os.path.exists(os.path.join(dataset.location, "test")):
        split_path = os.path.join(dataset.location, "test")
    else:
        split_path = os.path.join(dataset.location, "valid")
    
    example_class = os.listdir(split_path)[0]
    example_image_name = os.listdir(os.path.join(split_path, example_class))[0]
    example_image_path = os.path.join(split_path, example_class, example_image_name)
    os.environ["TEST_IMAGE_PATH"] = example_image_path

    print(f"Inferring on an example of the class '{example_class}'")

    # Infer using the trained model on a sample image
    infer_command = f"python classify/predict.py --weights runs/train-cls/exp11/weights/best.pt --source {example_image_path}"
    subprocess.run(infer_command, shell=True)


def main():
    # Esegui la pipeline YOLOv5
    run_yolov5_pipeline()

if __name__ == "__main__":
    main()

'''


import os
import subprocess
from roboflow import Roboflow
'''
def run_yolov5_pipeline():
    # Clone the YOLOv5 repository
    repository_url = "https://github.com/ultralytics/yolov5"
    directory_name = "yolov5"
    subprocess.run(f"git clone {repository_url} {directory_name}", shell=True)

    # Change directory to yolov5 and install requirements
    os.chdir("yolov5")
    subprocess.run("pip install -r requirements.txt", shell=True)

    # Create datasets directory if it doesn't exist and change directory
    os.makedirs("../datasets/", exist_ok=True)
    os.chdir("../datasets/")

    # Install Roboflow and download dataset
    subprocess.run("pip install roboflow", shell=True)
    rf = Roboflow(api_key="4hrmudsMFPu6NsoHy1is") # Replace with your Roboflow API key
    project = rf.workspace("cybersecurityproject").project("networkcomponents")  # Replace with your project details
    dataset = project.version(2).download("coco")

    # Set environment variable for the dataset
    dataset_name = dataset.location.split(os.sep)[-1]
    os.environ["YOLOv5_DATASET"] = dataset_name

    # Change directory back to yolov5
    os.chdir("../yolov5")

    # Train the YOLOv5 model

    train_command = f"python train.py --img 411 --batch 16 --epochs 100 --data 'C:/Users/Acer/Dropbox/PC/Desktop/cybersecurity/Progetto/datasets/networkcomponents-2/data.yaml' --cfg models/yolov5s.yaml --weights yolov5s.pt --name exp"
    subprocess.run(train_command, shell=True)

    # Validate the trained model
    val_command = f"python val.py --data '../datasets/{dataset_name}/data.yaml' --weights 'runs/train/exp/weights/best.pt'"
    subprocess.run(val_command, shell=True)

    # Get the path of an image from the test or validation set
    if os.path.exists(os.path.join(dataset.location, "test")):
        split_path = os.path.join(dataset.location, "test")
    else:
        split_path = os.path.join(dataset.location, "valid")
    
    example_image_path = os.path.join(split_path, os.listdir(split_path)[0])

    print(f"Inferring on an example image: {example_image_path}")

    # Infer using the trained model on a sample image
    infer_command = f"python detect.py --weights 'runs/train/exp/weights/best.pt' --img 640 --conf 0.4 --source {example_image_path}"
    subprocess.run(infer_command, shell=True)
'''
import os
import yaml

from roboflow import Roboflow

def train_custom_yolo(project_name, version_num, num_epochs=23, img_size=640, batch_size=16):
    # Initialize Roboflow
    '''
    rf = Roboflow(api_key="4hrmudsMFPu6NsoHy1is")
    project = rf.workspace("cybersecurityproject").project(project_name)
    dataset = project.version(version_num).download("yolov5")
    '''
    rf = Roboflow(api_key="4hrmudsMFPu6NsoHy1is")
    project = rf.workspace("cybersecurityproject").project(project_name)
    dataset = project.version(version_num).download("yolov5")

    # Read the number of classes from the YAML file
    with open(dataset.location + "/data.yaml", 'r') as stream:
        num_classes = str(yaml.safe_load(stream)['nc'])

    # Define the YOLOv5 model configuration
    custom_config = f'''
    nc: {num_classes}
    depth_multiple: 0.33
    width_multiple: 0.50
    anchors:
      - [10,13, 16,30, 33,23]
      - [30,61, 62,45, 59,119]
      - [116,90, 156,198, 373,326]
    transforms: 
    - mosaic: True  # Esempio di trasformazione di tipo mosaico
    - hsv_h: 0.015  # Esempio di regolazione dell'istogramma dei valori H, S e V
    - hsv_s: 0.7
    - hsv_v: 0.4
    - degrees: 0    # Esempio di rotazione
    - translate: 0.1 # Esempio di traslazione
    - scale: 0.5     # Esempio di scala
    - shear: 0.1 
    ... 
    '''

    # Write the custom YOLOv5 configuration to a file
    with open("custom_yolov5s.yaml", 'w') as config_file:
        config_file.write(custom_config)

    # Change directory to yolov5 folder
    os.chdir("C:/Users/Acer/Dropbox/PC/Desktop/yolov5")  # Replace with the actual path

    # Train YOLOv5 model
    train_command = f'''
    python train.py --img {img_size} --batch {batch_size} --epochs {num_epochs} --data {dataset.location}/data.yaml --cfg ./models/custom_yolov5s.yaml --weights '' --name yolov5s_results --cache 
    '''
    os.system(train_command)

# Call the function with your project and version details
#train_custom_yolo("networkcomponents", 2)

def main():
    # Execute the YOLOv5 pipeline
    train_custom_yolo("networkcomponents", 3)

    #run_yolov5_pipeline()

if __name__ == "__main__":
    main()

