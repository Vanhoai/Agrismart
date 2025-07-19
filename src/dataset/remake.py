import os

root_directory = os.getcwd()


def remake(**kwargs) -> None:
    original_directory = os.path.join(root_directory, "datasets", "rice-leaf-disease")
    print(f"Original directory: {original_directory}")
