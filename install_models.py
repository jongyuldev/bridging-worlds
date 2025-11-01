"""
Script to download required models for the vision assistant.
"""

import os
import urllib.request
from pathlib import Path

def download_file(url, destination):
    """Download a file with progress indication."""
    print(f"Downloading {os.path.basename(destination)}...")
    
    def progress(block_num, block_size, total_size):
        downloaded = block_num * block_size
        if total_size > 0:
            percent = downloaded * 100 / total_size
            print(f"\rProgress: {percent:.1f}%", end='')
    
    urllib.request.urlretrieve(url, destination, progress)
    print("\nDownload complete!")

def main():
    # Create models directory
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    
    print("Downloading MobileNet SSD models...")
    
    # MobileNet SSD Caffe model
    prototxt_url = "https://raw.githubusercontent.com/chuanqi305/MobileNet-SSD/master/MobileNetSSD_deploy.prototxt"
    caffemodel_url = "https://github.com/chuanqi305/MobileNet-SSD/raw/master/MobileNetSSD_deploy.caffemodel"
    
    prototxt_path = models_dir / "MobileNetSSD_deploy.prototxt"
    caffemodel_path = models_dir / "MobileNetSSD_deploy.caffemodel"
    
    if not prototxt_path.exists():
        download_file(prototxt_url, prototxt_path)
    else:
        print(f"{prototxt_path.name} already exists, skipping...")
    
    if not caffemodel_path.exists():
        download_file(caffemodel_url, caffemodel_path)
    else:
        print(f"{caffemodel_path.name} already exists, skipping...")
    
    print("\nAll models downloaded successfully!")
    print("You can now run the vision assistant.")

if __name__ == "__main__":
    main()
