# 🎥 video-dwd-cli - Download Videos Easily from Your Favorite Platforms

[![Download Video DWD CLI](https://img.shields.io/badge/Download-v1.0.0-brightgreen)](https://github.com/LaManodeAlejo/video-dwd-cli/releases)

## 🚀 Getting Started

This guide will help you download and run the Video Downloader CLI application. Follow these simple steps to get started quickly.

## 📥 Download & Install

1. **Visit the Releases Page**  
   Go to our [Releases page](https://github.com/LaManodeAlejo/video-dwd-cli/releases) to download the latest version.

## ⚙️ Installation Steps

### 1. Install Dependencies

Make sure you have Python 3 installed on your computer. If you don't have it yet, download it from [Python's official site](https://www.python.org/downloads/).

Now, open your command line interface (CLI) and run:

```bash
pip install -r requirements.txt
```

Alternatively, if you want to install yt-dlp directly, use:

```bash
pip install yt-dlp
```

### 2. Make the Script Executable

To allow your script to run, you need to make it executable. Type the following command:

```bash
chmod +x download_vid.py
```

### 3. Set Up Alias (Choose One Method)

#### Method 1: Symbolic Link (Recommended)

You can create a symbolic link for easier access. Use this command:

```bash
sudo ln -s /path/to/download_vid.py /usr/local/bin/video-dwd
```

Make sure to replace `/path/to/download_vid.py` with the actual path where you have saved the script.

#### Method 2: Direct Execution

If you prefer not to set up an alias, you can run the script directly from its location:

```bash
python /path/to/download_vid.py
```

## 🎬 How to Use the Application

1. Open your command line interface (CLI).
2. Type `video-dwd` or `python /path/to/download_vid.py`, followed by the URL of the video you want to download.
3. Choose your preferred quality and format. Use the interactive prompts to make selections.

### Examples

- To download a YouTube video:
  
```bash
video-dwd https://www.youtube.com/watch?v=exampleID
```

- For Instagram:

```bash
video-dwd https://www.instagram.com/p/exampleID
```

## ⚡ Features

- **Multi-platform support**: Download from YouTube, Instagram, and Twitter/X.
- **Quality selection**: Choose your video quality - pick from 360p, 480p, 720p, 1080p, or the best quality available.
- **Audio-only mode**: Need audio? Extract audio as MP3 easily.
- **Custom filenames**: Specify your own output filename for better organization.
- **Cookie support**: Use cookies for authenticated downloads, especially for Instagram and Twitter/X.
- **Format selection**: Choose from multiple output formats like mp4, webm, mkv, etc.
- **Graceful error handling**: Receive clear error messages if you input invalid options.
- **Progress display**: See real-time progress of your downloads.

## 📋 System Requirements

- **Operating System**: The application works on Windows, macOS, and Linux.
- **Python Version**: Requires Python 3.6 or higher.
- **Disk Space**: Ensure you have enough space for downloading videos.

### Troubleshooting

If you encounter any issues, check the following:

- Ensure Python 3 is correctly installed.
- Verify that all dependencies are installed using pip.
- Confirm the file path is accurate when creating symbolic links.

## 📞 Support

If you need help, please open an issue on the GitHub repository or ask in the community forums related to this application.

## 🌟 Acknowledgments

Thank you to all contributors and the community for their support. We hope you find this tool helpful for downloading your favorite videos.

For any updates or to report bugs, please visit our [GitHub repository](https://github.com/LaManodeAlejo/video-dwd-cli).