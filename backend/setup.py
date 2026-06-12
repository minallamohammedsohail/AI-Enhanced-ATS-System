"""
Setup script for ATS Backend
This script helps set up the environment and download required models
"""
import subprocess
import sys
import os

def install_requirements():
    """Install Python requirements"""
    print("Upgrading pip and setuptools for Python 3.12+ compatibility...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip", "setuptools>=69.0.0"])
    print("Installing Python requirements...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("✓ Requirements installed")

def download_spacy_model():
    """Download spaCy English model"""
    print("Downloading spaCy English model...")
    try:
        subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
        print("✓ spaCy model downloaded")
    except subprocess.CalledProcessError:
        print("⚠ Warning: Could not download spaCy model. Please run manually:")
        print("  python -m spacy download en_core_web_sm")

def create_uploads_dir():
    """Create uploads directory"""
    uploads_dir = "uploads"
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)
        print(f"✓ Created {uploads_dir} directory")
    else:
        print(f"✓ {uploads_dir} directory already exists")

if __name__ == "__main__":
    print("Setting up ATS Backend...\n")
    install_requirements()
    print()
    download_spacy_model()
    print()
    create_uploads_dir()
    print("\n✓ Setup complete!")
    print("\nTo start the server, run: python app.py")

