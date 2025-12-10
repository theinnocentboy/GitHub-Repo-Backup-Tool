import streamlit as st
import json
from datetime import datetime

from gitbackrepo import (
    create_backup,
    RepoBackupError,
    MetadataFetchError,
    DownloadError,
    ExtractionError,
)

# ----------------------------------------------
# Streamlit Page Configuration
# ----------------------------------------------
st.set_page_config(
    page_title="GitHub Repo Backup (In-Memory)",
    page_icon="⬛",
    layout="wide"
)

st.markdown("# ⬛ GitHub Repository Backup (In-Memory)")
st.markdown("Backup a GitHub repo directly into memory — no local files created.")
st.markdown("---")

# ----------------------------------------------
# Inputs
# ----------------------------------------------
col1, col2 = st.columns(2)

with col1:
    owner = st.text_input("GitHub Owner / Username", placeholder="octocat")

with col2:
    repo = st.text_input("Repository Name", placeholder="Hello-World")


start_btn = st.button("Start Backup", type="primary")

# ----------------------------------------------
# Backup Process
# ----------------------------------------------
if start_btn:
    if not owner or not repo:
        st.error("❌ Please provide both Owner and Repository name.")
        st.stop()

    st.info(f"📁 Starting backup for `{owner}/{repo}` at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    try:
        result = create_backup(owner, repo, extract=False)

        if not result["success"]:
            st.error(f"❌ Backup Failed: {result['error']}")
            st.stop()

        st.success("🎉 Backup Completed Successfully!")

        metadata = result["metadata"]
        zip_bytes = result["zip_bytes"]

        metadata_json = json.dumps(metadata, indent=2)

        # -------------------------------
        # DOWNLOAD SECTION
        # -------------------------------
        st.markdown("## 📥 Download Files")

        colA, colB = st.columns(2)

        # Download JSON metadata
        with colA:
            st.download_button(
                label="📄 Download Metadata JSON",
                data=metadata_json,
                file_name=f"{repo}_metadata.json",
                mime="application/json",
                use_container_width=True
            )

        # Download ZIP archive
        with colB:
            st.download_button(
                label="📦 Download Repository ZIP",
                data=zip_bytes,
                file_name=f"{repo}.zip",
                mime="application/zip",
                use_container_width=True
            )

        st.info("✔ Files generated in memory — no local storage used.")

    except MetadataFetchError as e:
        st.error(f"Metadata Error: {e}")
    except DownloadError as e:
        st.error(f"Download Error: {e}")
    except ExtractionError as e:
        st.error(f"Extraction Error: {e}")
    except RepoBackupError as e:
        st.error(f"Backup Error: {e}")
    except Exception as e:
        st.error(f"Unexpected Error: {e}")

    finally:
        st.markdown("### 🔚 Backup operation finished.")
