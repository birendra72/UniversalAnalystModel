import streamlit as st
import os
import tempfile
import zipfile
import io
import shutil
from typing import List, Optional, Union
import base64
from pathlib import Path

class TempStorage:
    """Utility class for handling temporary file storage and downloads in Streamlit"""
    
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp(prefix="uam_temp_")
        st.session_state.setdefault('temp_files', [])
    
    def create_download_button(self, data: Union[bytes, str], 
                             file_name: str, 
                             mime_type: str, 
                             button_text: str = "📥 Download",
                             key: Optional[str] = None) -> None:
        """
        Create a download button for any type of data
        
        Args:
            data: The data to download (bytes or string)
            file_name: Name of the file to download
            mime_type: MIME type of the file
            button_text: Text to display on the button
            key: Optional unique key for the button
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        b64 = base64.b64encode(data).decode()
        href = f'<a href="data:{mime_type};base64,{b64}" download="{file_name}" ' \
               f'style="text-decoration: none;">{button_text}</a>'
        
        st.markdown(href, unsafe_allow_html=True)
    
    def download_file(self, file_path: str, 
                     download_name: Optional[str] = None,
                     button_text: str = "📥 Download File") -> None:
        """
        Create a download button for an existing file
        
        Args:
            file_path: Path to the file to download
            download_name: Optional custom name for the downloaded file
            button_text: Text to display on the button
        """
        if not os.path.exists(file_path):
            st.warning(f"File not found: {file_path}")
            return
        
        file_name = download_name or os.path.basename(file_path)
        
        with open(file_path, "rb") as f:
            data = f.read()
        
        # Determine MIME type based on file extension
        ext = os.path.splitext(file_path)[1].lower()
        mime_types = {
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.pdf': 'application/pdf',
            '.html': 'text/html',
            '.md': 'text/markdown',
            '.csv': 'text/csv',
            '.txt': 'text/plain',
            '.zip': 'application/zip'
        }
        mime_type = mime_types.get(ext, 'application/octet-stream')
        
        self.create_download_button(data, file_name, mime_type, button_text)
    
    def create_zip_download(self, files: List[str], 
                           zip_name: str = "download.zip",
                           button_text: str = "📦 Download All") -> None:
        """
        Create a zip file download from multiple files
        
        Args:
            files: List of file paths to include in the zip
            zip_name: Name of the zip file
            button_text: Text to display on the button
        """
        # Filter out non-existent files
        existing_files = [f for f in files if os.path.exists(f)]
        
        if not existing_files:
            st.warning("No files found to download")
            return
        
        # Create zip in memory
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in existing_files:
                arcname = os.path.basename(file_path)
                zipf.write(file_path, arcname)
        
        zip_data = zip_buffer.getvalue()
        self.create_download_button(zip_data, zip_name, 'application/zip', button_text)
    
    def download_directory_as_zip(self, directory_path: str, 
                                 zip_name: Optional[str] = None,
                                 button_text: str = "📦 Download Directory") -> None:
        """
        Create a zip download of an entire directory
        
        Args:
            directory_path: Path to the directory to zip
            zip_name: Name of the zip file (default: directory_name.zip)
            button_text: Text to display on the button
        """
        if not os.path.exists(directory_path) or not os.path.isdir(directory_path):
            st.warning(f"Directory not found: {directory_path}")
            return
        
        if zip_name is None:
            dir_name = os.path.basename(directory_path.rstrip('/\\'))
            zip_name = f"{dir_name}.zip"
        
        # Create zip in memory
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(directory_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, directory_path)
                    zipf.write(file_path, arcname)
        
        zip_data = zip_buffer.getvalue()
        self.create_download_button(zip_data, zip_name, 'application/zip', button_text)
    
    def save_temp_file(self, data: Union[bytes, str], file_name: str) -> str:
        """
        Save data to a temporary file and track it
        
        Args:
            data: Data to save (bytes or string)
            file_name: Name of the file
            
        Returns:
            Path to the saved temporary file
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        temp_path = os.path.join(self.temp_dir, file_name)
        os.makedirs(os.path.dirname(temp_path), exist_ok=True)
        
        with open(temp_path, 'wb') as f:
            f.write(data)
        
        # Track the file
        if 'temp_files' not in st.session_state:
            st.session_state.temp_files = []
        st.session_state.temp_files.append(temp_path)
        
        return temp_path
    
    def cleanup(self):
        """Clean up all temporary files"""
        if hasattr(self, 'temp_dir') and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
        
        # Clear tracked files
        if 'temp_files' in st.session_state:
            st.session_state.temp_files = []

# Global instance for easy access
temp_storage = TempStorage()

# Utility functions for common use cases
def download_image(image_path: str, caption: str = "Download Image"):
    """Helper function to download an image file"""
    temp_storage.download_file(image_path, button_text=f"📷 {caption}")

def download_report(report_path: str, report_type: str = "Report"):
    """Helper function to download a report file"""
    temp_storage.download_file(report_path, button_text=f"📄 Download {report_type}")

def download_visualizations(visualization_dir: str, dataset_name: str):
    """Helper function to download all visualizations from a directory"""
    if os.path.exists(visualization_dir) and os.path.isdir(visualization_dir):
        temp_storage.download_directory_as_zip(
            visualization_dir, 
            f"{dataset_name}_visualizations.zip",
            "📦 Download All Visualizations"
        )
