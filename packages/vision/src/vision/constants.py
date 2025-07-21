import os


class VisionConstants:
    DATASET_DIRECTORY = "datasets"
    ORIGINAL_DATASET = "original-rice-leaf-diseases"
    REMAKE_DATASET = "remake-rice-leaf-diseases"

    ORIGINAL_DIRECTORY = os.path.join(os.getcwd(), DATASET_DIRECTORY, ORIGINAL_DATASET)
    REMAKE_DIRECTORY = os.path.join(os.getcwd(), DATASET_DIRECTORY, REMAKE_DATASET)
