# File Organizer Pro

![Python](https://img.shields.io/badge/Python-3.6%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Windows%2C%20macOS%2C%20Linux-lightgrey)
![Version](https://img.shields.io/badge/Version-2.0.0-blue)

A powerful Python script for automatic file organization with multiple sorting criteria and intelligent duplicate detection.

## ✨ Features

- **Multi-criteria Organization**: Sort by extension, size, date, or remove duplicates
- **Smart Size Categorization**: Light (<10MB), Medium (10-100MB), Heavy (>100MB)
- **Dual Calendar Support**: Persian (Jalali) and Gregorian date organization
- **Military-Grade Duplicate Detection**: MD5 hash-based verification
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Comprehensive Logging**: Detailed operation logs with error handling

## 🚀 Installation

```bash
# Clone repository
git clone https://github.com/hossein-naseri-dev/file_organizer_py.git
cd file_organizer_py

# Optional: Install Persian calendar support
pip install khayyam
```



## 💻 Usage
### Basic Commands
```bash
# Organize by file type
python file_organizer.py --extension

# Organize by size
python file_organizer.py --size --path ~/Downloads

# Remove duplicates
python file_organizer.py --erase_duplicates

# Organize by date
python file_organizer.py --last_modify_date
```



## Advanced Examples
```bash
# Organize specific directory by extension
python file_organizer.py --extension --path /path/to/your/directory

# Remove duplicates from documents folder
python file_organizer.py --erase_duplicates --path ~/Documents

# Organize photos by modification date
python file_organizer.py --last_modify_date --path ~/Pictures
```


## 📋 Command Options
### Option	Description	Default:
#### -e, --extension	Organize by file extension	False
#### -s, --size	Organize by file size	False
#### -l, --last_modify_date	Organize by modification date	False
#### -d, --erase_duplicates	Remove duplicate files	False
#### -p, --path	Target directory path	Current directory



## 🛡️ Safety Features
#### Automatic backup recommendations
#### Never modifies system files or script itself
#### Comprehensive error recovery
#### Detailed operation logging in file_organizer.log
#### Pre-operation checks and validations


## 📝 License
#### This project is licensed under the MIT License - see the LICENSE file for details.


## ⚠️ Troubleshooting
### Common issues and solutions:
#### 1) Permission Errors: Ensure you have proper read/write permissions for the target directory
#### 2) Missing Dependencies: Install required packages with pip install khayyam if using Persian calendar features
#### 3) Unicode Errors: Check system locale settings for UTF-8 support
#### 4) File in Use: Close any applications that might be using files you're trying to organize
#### 5) For detailed error information, check the file_organizer.log file.


## 🙏 Acknowledgments
#### Thanks to the Python community for excellent libraries and tools
#### Special thanks to the khayyam library maintainers for Persian calendar support
#### Inspired by the need for better digital file management solutions

### Contact me: dev.h.naseri@gmail.com
### ⭐ If you find this project useful, please give it a star on GitHub!