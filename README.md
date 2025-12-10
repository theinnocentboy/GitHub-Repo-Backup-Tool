# ⬛ GitHub Repository Backup Tool (In-Memory)

A lightweight Python application that allows you to backup any public GitHub repository directly into memory without creating local files. Built with Streamlit for an intuitive web interface.

## 🌟 Features

- **In-Memory Processing**: Downloads and processes repository data without creating local files
- **Metadata Extraction**: Fetches comprehensive repository metadata via GitHub API
- **ZIP Archive Download**: Downloads the complete repository as a ZIP file
- **User-Friendly Interface**: Clean Streamlit web interface for easy interaction
- **Error Handling**: Robust error handling with custom exception classes
- **Download Options**: Download both metadata (JSON) and repository archive (ZIP)

## 📋 Prerequisites

- Python 3.8 or higher
- Internet connection (to access GitHub API and repositories)
- pip (Python package manager)

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/theinnocentboy/GitHub-Repo-Backup-Tool.git
cd GitHub-Repo-Backup-Tool
```

### 2. Create a Virtual Environment (Recommended)

**Windows:**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Required Dependencies

```bash
pip install -r requirements.txt
```

The `requirements.txt` includes:
- `streamlit>=1.39.0` - Web application framework
- `requests>=2.31.0` - HTTP library for API calls

## 📁 Project Structure

```
GitHub-Repo-Backup-Tool/
│
├── app.py              # Main Streamlit application
├── gitbackrepo.py      # Core backup functionality and utilities
├── requirements.txt    # Python dependencies
└── README.md          # Project documentation
```

## 🎯 Usage

### Running the Application

1. Ensure your virtual environment is activated (if you created one)

2. Start the Streamlit application:

```bash
streamlit run app.py
```

3. Your default web browser will automatically open to `http://localhost:8501`

### Using the Backup Tool

1. **Enter Repository Details**:
   - **GitHub Owner/Username**: Enter the username or organization name (e.g., `octocat`)
   - **Repository Name**: Enter the repository name (e.g., `Hello-World`)

2. **Start Backup**:
   - Click the "Start Backup" button
   - The application will fetch metadata and download the repository

3. **Download Results**:
   - **Download Metadata JSON**: Get repository metadata including stars, forks, description, etc.
   - **Download Repository ZIP**: Get the complete repository source code as a ZIP archive

## 🔧 Core Functionality

### `gitbackrepo.py` Module

#### Functions:

- **`fetch_repo_metadata(owner, repo)`**
  - Fetches repository metadata from GitHub API
  - Returns: Dictionary containing repository information

- **`download_repo_zip(owner, repo)`**
  - Downloads repository as ZIP file into memory
  - Returns: BytesIO object containing ZIP data

- **`extract_zip_in_memory(zip_file)`**
  - Extracts ZIP contents in memory (optional)
  - Returns: Dictionary of filenames and their bytes

- **`create_backup(owner, repo, extract=False)`**
  - Main backup function that orchestrates the entire process
  - Returns: Dictionary with backup results and data

#### Exception Classes:

- `RepoBackupError` - Base exception class
- `MetadataFetchError` - Raised when metadata fetch fails
- `DownloadError` - Raised when ZIP download fails
- `ExtractionError` - Raised when ZIP extraction fails

## 🌐 API Information

This tool uses the GitHub REST API v3:
- **Metadata Endpoint**: `https://api.github.com/repos/{owner}/{repo}`
- **ZIP Download**: `https://github.com/{owner}/{repo}/archive/refs/heads/main.zip`

**Note**: The tool assumes the default branch is `main`. For repositories with different default branches (e.g., `master`), you may need to modify the URL in `gitbackrepo.py`.

## ⚠️ Limitations

- Only works with **public repositories**
- Downloads from the **main** branch by default
- No authentication implemented (subject to GitHub API rate limits for unauthenticated requests: 60 requests/hour)
- Large repositories may take time to download

## 🛠️ Troubleshooting

### Common Issues:

1. **"Network error: Could not reach GitHub API"**
   - Check your internet connection
   - Verify the GitHub API is accessible

2. **"HTTP Error: 404"**
   - Verify the owner and repository names are correct
   - Ensure the repository is public

3. **"Failed to download ZIP"**
   - Check if the repository has a `main` branch
   - Large repositories may timeout; try again

4. **Rate Limit Exceeded**
   - GitHub limits unauthenticated requests to 60/hour
   - Wait for the rate limit to reset or implement authentication

## 🔒 Security Notes

- This tool does not store any credentials
- All processing happens in memory
- Downloaded files are only saved when you explicitly click download buttons
- No data is persisted on the server

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

## 👨‍💻 Author

**theinnocentboy**
- GitHub: [@theinnocentboy](https://github.com/theinnocentboy)

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Uses [GitHub REST API](https://docs.github.com/en/rest)

---

**Made with ❤️ for the GitHub community**
