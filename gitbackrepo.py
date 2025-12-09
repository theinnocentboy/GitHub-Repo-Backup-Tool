import os
import json
import shutil
import urllib.request
from datetime import datetime


class RepoBackupError(Exception):
    """Base class for backup-related errors."""
    pass


class MetadataFetchError(RepoBackupError):
    """Raised when metadata fetching fails."""
    pass


class DownloadError(RepoBackupError):
    """Raised when repo download fails."""
    pass


class ExtractionError(RepoBackupError):
    """Raised when archive extraction fails."""
    pass



def fetch_repo_metadata(owner, repo, backup_dir):
    url = f"https://api.github.com/repos/{owner}/{repo}"
    metadata_path = os.path.join(backup_dir, "repo_metadata.json")

    print(f"Fetching metadata from {url} ...")

    try:
        with urllib.request.urlopen(url) as response:
            if response.status != 200:
                raise MetadataFetchError("GitHub API did not return 200 OK.")

            metadata = json.loads(response.read().decode())

    except urllib.error.HTTPError as e:
        raise MetadataFetchError(f"HTTP Error: {e.code} - {e.reason}")
    except urllib.error.URLError:
        raise MetadataFetchError("Network error: Unable to reach GitHub API.")
    except json.JSONDecodeError:
        raise MetadataFetchError("Failed to parse JSON from GitHub API.")

    else:
        try:
            with open(metadata_path, "w") as f:
                json.dump(metadata, f, indent=4)
        except OSError:
            raise MetadataFetchError("Failed to save metadata to file.")

        print(f"Metadata saved at: {metadata_path}")
        return metadata_path

    finally:
        print("Metadata fetch attempt completed.")


def download_repo_archive(owner, repo, backup_dir):
    url = f"https://github.com/{owner}/{repo}/archive/refs/heads/main.zip"
    zip_path = os.path.join(backup_dir, f"{repo}.zip")

    print(f"Downloading repository archive from {url} ...")

    try:
        urllib.request.urlretrieve(url, zip_path)
    except Exception:
        raise DownloadError("Failed to download repository ZIP file.")

    else:
        print(f"Archive saved at: {zip_path}")
        return zip_path

    finally:
        print("Download attempt completed.")


def extract_archive(zip_path, extract_to):
    print(f"Extracting {zip_path} ...")

    try:
        shutil.unpack_archive(zip_path, extract_to)
    except (shutil.ReadError, FileNotFoundError):
        raise ExtractionError("Invalid ZIP file or extraction failed.")
    except Exception:
        raise ExtractionError("Unexpected extraction error occurred.")

    else:
        print(f"Files extracted to: {extract_to}")

    finally:
        print("Extraction attempt finished.")


def create_backup(owner, repo):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"{repo}_backup_{timestamp}"

    print(f"Creating backup folder: {backup_dir}")

    try:
        os.makedirs(backup_dir, exist_ok=True)

        # Step 1: Fetch metadata
        fetch_repo_metadata(owner, repo, backup_dir)

        # Step 2: Download ZIP
        zip_path = download_repo_archive(owner, repo, backup_dir)

        # Step 3: Extract ZIP
        extract_dir = os.path.join(backup_dir, "repo_files")
        os.makedirs(extract_dir, exist_ok=True)

        extract_archive(zip_path, extract_dir)

    except RepoBackupError as e:
        print(f"\n❌ Backup failed: {e}")

    except Exception as e:
        print(f"\n⚠️ Unexpected error: {str(e)}")

    else:
        print("\n✅ Backup complete!")
        print(f"Backup directory: {backup_dir}")

    finally:
        print("Backup operation finished.\n")


if __name__ == "__main__":
    owner = input("Enter GitHub Username: ")
    repo = input("Enter Repository Name: ")

    create_backup(owner, repo)
