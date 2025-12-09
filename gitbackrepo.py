import os
import json
import shutil
import urllib.request
from datetime import datetime


def fetch_repo_metadata(owner, repo, backup_dir):
    url = f"https://api.github.com/repos/{owner}/{repo}"
    metadata_path = os.path.join(backup_dir, "repo_metadata.json")

    print(f"Fetching metadata from {url} ...")
    with urllib.request.urlopen(url) as response:
        metadata = json.loads(response.read().decode())

    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=4)

    print(f"Metadata saved at: {metadata_path}")
    return metadata_path


def download_repo_archive(owner, repo, backup_dir):
    url = f"https://github.com/{owner}/{repo}/archive/refs/heads/main.zip"
    zip_path = os.path.join(backup_dir, f"{repo}.zip")

    print(f"Downloading repository archive from {url} ...")
    urllib.request.urlretrieve(url, zip_path)
    print(f"Archive saved at: {zip_path}")
    return zip_path

def extract_archive(zip_path, extract_to):
    print(f"Extracting {zip_path} ...")
    shutil.unpack_archive(zip_path, extract_to)
    print(f"Files extracted to: {extract_to}")


def create_backup(owner, repo):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"{repo}_backup_{timestamp}"

    print(f"Creating backup folder: {backup_dir}")
    os.makedirs(backup_dir, exist_ok=True)

    # Step 1: Fetch metadata to JSON
    fetch_repo_metadata(owner, repo, backup_dir)

    # Step 2: Download repo as ZIP
    zip_path = download_repo_archive(owner, repo, backup_dir)
    

    # Step 3: Extract the ZIP archive
    extract_dir = os.path.join(backup_dir, "repo_files")
    os.makedirs(extract_dir, exist_ok=True)
    extract_archive(zip_path, extract_dir)


    print("\n✅ Backup complete!")
    print(f"Backup directory: {backup_dir}")


if __name__ == "__main__":
    owner = input("Enter username:")
    repo = input("Enter Repository Name:")

    create_backup(owner, repo)
