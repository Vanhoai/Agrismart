### Rice Leaf Diseases Dataset

This dataset contains images of rice leaves affected by various diseases, including Bacterial Leaf Blight, Brown Spot,
Healthy, Leaf Blast, Leaf Blight, Leaf Scald, Leaf Smut, and Narrow Brown Spot. The dataset is structured into three
modes: TRAIN, VAL (validation), and TEST.

#### Dataset Information

Dataset URL: https://universe.roboflow.com/utopialab/rice-leaf-wfax3

Provided by a Roboflow user
License: CC BY 4.0

#### Download and Extract

1. Visit the [Rice Leaf Diseases dataset page](https://universe.roboflow.com/utopialab/rice-leaf-wfax3).
2. Click on the tab "Dataset" to view all versions of the dataset.
3. Select the version you want to download.
4. Click on the "Download" button to download the dataset:
    - Choose format YOLO for download.
    - After that you can get zip file or use script to download the dataset.

if you want to download the dataset using a script, you can use the following command look like in website:

```bash
# 1. in root project directory
mkdir datasets && cd datasets && mkdir rice-leaf-disease && cd rice-leaf-disease

# 2. download dataset
curl -L "https://universe.roboflow.com/ds/wMunxiKjaW?key=<your-key>" > roboflow.zip; unzip roboflow.zip; rm roboflow.zip
```

#### Root Dataset Statistics

| Mode  | Total Images | Total Labels | Empty Labels |
|-------|--------------|--------------|--------------|
| TRAIN | 3,894        | 3,894        | 44           |
| VAL   | 932          | 932          | 5            |
| TEST  | 362          | 362          | 4            |

##### 🔹Train

| Class                 | BBoxes | Polygons |
|-----------------------|--------|----------|
| Bacterial Leaf Blight | 509    | 36       |
| Brown Spot            | 3,735  | 625      |
| Healthy               | 76     | 554      |
| Leaf Blast            | 1,741  | 307      |
| Leaf Blight           | 336    | 244      |
| Leaf Scald            | 131    | 353      |
| Leaf Smut             | 1      | 145      |
| Narrow Brown Spot     | 1,285  | 828      |

##### 🔹Validation

| Class                 | BBoxes | Polygons |
|-----------------------|--------|----------|
| Bacterial Leaf Blight | 128    | 17       |
| Brown Spot            | 801    | 142      |
| Healthy               | 38     | 128      |
| Leaf Blast            | 487    | 80       |
| Leaf Blight           | 100    | 53       |
| Leaf Scald            | 29     | 98       |
| Leaf Smut             | 1      | 57       |
| Narrow Brown Spot     | 326    | 215      |

##### 🔹Test

| Class                 | BBoxes | Polygons |
|-----------------------|--------|----------|
| Bacterial Leaf Blight | 50     | 5        |
| Brown Spot            | 383    | 46       |
| Healthy               | 0      | 39       |
| Leaf Blast            | 160    | 25       |
| Leaf Blight           | 47     | 17       |
| Leaf Scald            | 8      | 37       |
| Leaf Smut             | 0      | 9        |
| Narrow Brown Spot     | 123    | 77       |
