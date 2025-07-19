import subprocess


def download() -> None:
    print("============================== STARTING DOWNLOAD ==============================")

    # 1. Make directories
    subprocess.run("mkdir -p datasets/rice-leaf-disease", shell=True, check=True)

    # 2. Change directory & download
    command = (
        "cd datasets/rice-leaf-disease && "
        "curl -L 'https://universe.roboflow.com/ds/wMunxiKjaW?key=<your-key>' -o roboflow.zip && "
        "unzip roboflow.zip && rm roboflow.zip"
    )

    subprocess.run(command, shell=True, check=True)
    print("============================== DOWNLOAD COMPLETE ✅ ==============================")
