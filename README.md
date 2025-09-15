# 🎵 Music Extractor GUI

A modern Python GUI application for extracting and organizing music zip files from your Downloads folder into a proper music library structure.

![Python](https://img.shields.io/badge/python-3.6+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows%20%7C%20macOS-lightgrey.svg)

## ✨ Features

- 🎨 **Modern, elegant GUI** with white/black theme
- 🗂️ **Automatic organization** into Artist/Album folder structure
- 🔍 **Smart zip file detection** with multiple naming patterns
- ⚙️ **Customizable settings** with persistent preferences
- 📊 **Real-time progress tracking** and statistics
- 📋 **File preview** before extraction
- 🗑️ **Auto-delete option** for processed zip files
- ⌨️ **Keyboard shortcuts** for power users
- 📁 **Quick folder access** to extraction destination

## 🖼️ Screenshots

The application features a clean, modern interface with:
- Compact settings panel for Downloads and Music Library paths
- Format selection dropdown for different zip file naming patterns
- Real-time statistics showing found, processed, and failed files
- Expandable output section with file preview and activity log
- Progress bar and status notifications

## 🚀 Quick Start

### Prerequisites
- **Python 3.6 or higher**
- **tkinter** (usually included with Python)

### Installation

1. **Download the application:**
   ```bash
   # Option 1: Direct download
   wget https://raw.githubusercontent.com/yourusername/Music-Extractor-GUI/main/Music_Extractor.py
   
   # Option 2: Clone the repository
   git clone https://github.com/yourusername/Music-Extractor-GUI.git
   cd Music-Extractor-GUI
   ```

2. **Make it executable:**
   ```bash
   chmod +x Music_Extractor.py
   ```

3. **Run the application:**
   ```bash
   python3 Music_Extractor.py
   ```

### Alternative: Using the install script
```bash
# Download and run the install script
curl -O https://raw.githubusercontent.com/yourusername/Music-Extractor-GUI/main/install.sh
chmod +x install.sh
./install.sh
```

## 📖 How to Use

1. **Configure Settings:**
   - Set your Downloads folder path (where zip files are located)
   - Set your Music Library destination path
   - Choose the zip file naming format that matches your files

2. **Scan for Files:**
   - Click "🔍 Scan" to find music zip files
   - View found files in the preview table

3. **Extract Music:**
   - Click "📦 Extract" to organize files into your music library
   - Monitor progress with the progress bar and statistics

4. **Access Results:**
   - Click "📂 Open Extraction Folder" to view organized music
   - Check the activity log for detailed processing information

## 🎯 Supported Zip File Formats

The application supports multiple naming patterns:

- `Artist - Album.zip` (e.g., "The Beatles - Abbey Road.zip")
- `Artist_Album.zip` (e.g., "The_Beatles_Abbey_Road.zip")
- `Artist.Album.zip` (e.g., "The.Beatles.Abbey.Road.zip")
- `Album by Artist.zip` (e.g., "Abbey Road by The Beatles.zip")
- `Artist - Album - Year.zip` (e.g., "The Beatles - Abbey Road - 1969.zip")

## ⌨️ Keyboard Shortcuts

- `Ctrl+S` - Scan for music zip files
- `Ctrl+E` - Extract all found files
- `F5` - Refresh/scan again

## ⚙️ Configuration

The application automatically saves your settings to `~/.music_extractor_settings.json`:

- Downloads folder path
- Music library destination
- Selected naming format
- Auto-delete zip files preference

## 🏗️ Project Structure

```
Music-Extractor-GUI/
├── Music_Extractor.py      # Main application file
├── README.md               # This file
├── LICENSE                 # MIT License
├── requirements.txt        # Python dependencies
├── install.sh             # Installation script
├── .gitignore             # Git ignore rules
└── CONTRIBUTING.md        # Contribution guidelines
```

## 🔧 Troubleshooting

### Common Issues

**"tkinter not found" error:**
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# CentOS/RHEL/Fedora
sudo yum install tkinter
# or
sudo dnf install python3-tkinter

# Arch Linux
sudo pacman -S tk
```

**"Permission denied" error:**
```bash
chmod +x Music_Extractor.py
```

**Python not found:**
```bash
# Install Python 3
sudo apt-get install python3  # Ubuntu/Debian
sudo yum install python3      # CentOS/RHEL
```

### Getting Help

- Check the activity log for detailed error messages
- Ensure your paths are correct and accessible
- Verify zip files are not corrupted
- Make sure you have write permissions to the music library folder

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with Python's tkinter for cross-platform compatibility
- Uses only standard library modules for maximum portability
- Inspired by the need for organized music libraries

## 📧 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/Music-Extractor-GUI/issues) page
2. Create a new issue with detailed information
3. Include your operating system and Python version

---

**Made with ❤️ for music lovers who value organization**
