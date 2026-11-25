#!/usr/bin/env python3
# setup_environment.py - Install required libraries for mobile honeypot project

import subprocess
import sys
import os

def install_requirements():
    """Install all required packages for the honeypot project."""
    
    print("Setting up environment for Mobile Honeypot project...")
    
    # Define required packages
    requirements = [
        "flask",           # For HTTP honeypot server
        "requests",        # For HTTP requests and testing
        "cryptography",    # For secure logging
        "matplotlib",      # For visualization dashboard
        "numpy",           # For data analysis
        "pandas",          # For log data manipulation
        "python-dateutil", # For timestamp handling
        "pyngrok",         # Optional: For exposing local server to internet (testing)
        "colorama"         # For colored terminal output
    ]
    
    # Check if virtual environment exists, create if not
    if not os.path.exists("venv"):
        print("Creating virtual environment...")
        try:
            subprocess.check_call([sys.executable, "-m", "venv", "venv"])
            print("Virtual environment created successfully.")
        except subprocess.CalledProcessError:
            print("Failed to create virtual environment. Please install venv manually.")
            return False
    
    # Determine pip path based on platform
    if sys.platform == "win32":
        pip_path = os.path.join("venv", "Scripts", "pip")
    else:
        pip_path = os.path.join("venv", "bin", "pip")
    
    # Upgrade pip
    print("Upgrading pip...")
    try:
        subprocess.check_call([pip_path, "install", "--upgrade", "pip"])
    except subprocess.CalledProcessError:
        print("Failed to upgrade pip. Continuing with installation...")
    
    # Install each package
    print("\nInstalling required packages:")
    for package in requirements:
        print(f"Installing {package}...")
        try:
            subprocess.check_call([pip_path, "install", package])
            print(f"✅ {package} installed successfully")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package}")
            return False
    
    print("\nAll required packages installed successfully!")
    print("\nTo activate the virtual environment:")
    if sys.platform == "win32":
        print("    venv\\Scripts\\activate")
    else:
        print("    source venv/bin/activate")
    
    return True

def check_android_requirements():
    """Check if Android development requirements are met."""
    print("\nChecking Android development requirements:")
    
    # Check if Android Studio is installed
    print("Note: For the Android portion of this project, you'll need:")
    print("  - Android Studio (https://developer.android.com/studio)")
    print("  - Chaquopy plugin for Android Studio")
    print("    (Install via Settings > Plugins > Marketplace > Search 'Chaquopy')")
    
    print("\nOnce Android Studio is set up, add this to your app's build.gradle:")
    print("""
    android {
        defaultConfig {
            ndk {
                abiFilters "armeabi-v7a", "arm64-v8a", "x86", "x86_64"
            }
            python {
                pip {
                    install "flask"
                    install "requests"
                    install "cryptography"
                }
            }
        }
    }
    
    dependencies {
        implementation 'com.chaquo.python:python:10.0.1'
    }
    """)

if __name__ == "__main__":
    if install_requirements():
        check_android_requirements()
        print("\nSetup complete! You can now start developing your mobile honeypot.")
