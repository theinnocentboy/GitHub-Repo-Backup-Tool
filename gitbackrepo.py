import json
import urllib.request
from io import BytesIO
from datetime import datetime
import zipfile


class RepoBackupError(Exception):
    pass


class MetadataFetchError(RepoBackupError):
    pass


class DownloadError(RepoBackupError):
    pass


class ExtractionError(RepoBackupError):
    pass


def fetch_repo_metadata(owner, repo):
    """Fetch metadata from GitHub API and return dict (not saved locally)."""

    url = f"https://api.github.com/repos/{owner}/{repo}"

    try:
        with urllib.request.urlopen(url) as response:
            if response.status != 200:
                raise MetadataFetchError("GitHub API did not return 200 OK.")

            metadata = json.loads(response.read().decode())

    except urllib.error.HTTPError as e:
        raise MetadataFetchError(f"HTTP Error: {e.code} - {e.reason}")
    except urllib.error.URLError:
        raise MetadataFetchError("Network error: Could not reach GitHub API.")
    except json.JSONDecodeError:
        raise MetadataFetchError("Invalid JSON received from GitHub API.")

    return metadata


def download_repo_zip(owner, repo):
    """Download the repo ZIP into memory (BytesIO) without saving locally."""

    url = f"https://github.com/{owner}/{repo}/archive/refs/heads/main.zip"

    try:
        with urllib.request.urlopen(url) as response:
            if response.status != 200:
                raise DownloadError("Failed to download ZIP.")
            zip_bytes = response.read()

    except Exception as e:
        raise DownloadError(f"ZIP download failed: {str(e)}")

    return BytesIO(zip_bytes)  # return in-memory ZIP


def extract_zip_in_memory(zip_file: BytesIO):
    """Extract ZIP contents in memory (optional use)."""

    try:
        with zipfile.ZipFile(zip_file) as zf:
            file_dict = {name: zf.read(name) for name in zf.namelist()}

    except Exception:
        raise ExtractionError("ZIP extraction failed in memory.")

    return file_dict  # dict of {filename: filebytes}


def create_backup(owner, repo, extract=False):
    """Main backup: fetch metadata + ZIP (and extract if needed)."""

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        metadata = fetch_repo_metadata(owner, repo)
        zip_file = download_repo_zip(owner, repo)

        if extract:
            extracted_files = extract_zip_in_memory(zip_file)
        else:
            extracted_files = None

    except RepoBackupError as e:
        return {
            "success": False,
            "error": str(e),
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}",
        }

    else:
        return {
            "success": True,
            "timestamp": timestamp,
            "metadata": metadata,
            "zip_bytes": zip_file.getvalue(),
            "extracted_files": extracted_files,
        }
