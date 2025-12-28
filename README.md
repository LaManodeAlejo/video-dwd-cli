# Video Downloader CLI

A production-ready command-line tool for downloading videos from YouTube, Instagram, and Twitter/X. Built with Python 3 and `yt-dlp`.

## Features

- **Multi-platform support**: YouTube, Instagram, Twitter/X
- **Quality selection**: Choose from 360p, 480p, 720p, 1080p, or best available
- **Audio-only mode**: Extract audio as MP3
- **Custom filenames**: Specify your own output filename
- **Cookie support**: Use cookies for authenticated downloads (Instagram/Twitter)
- **Format selection**: Choose output format (mp4, webm, mkv, etc.)
- **Graceful error handling**: Clear error messages for invalid inputs
- **Progress display**: Real-time download progress

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Or install directly:

```bash
pip install yt-dlp
```

### 2. Make Script Executable

```bash
chmod +x download_vid.py
```

### 3. Set Up Alias (Choose One Method)

#### Method 1: Symbolic Link (Recommended)

Create a symbolic link in `/usr/local/bin`:

```bash
sudo ln -s $(pwd)/download_vid.py /usr/local/bin/download_vid
```

Now you can use `download_vid` from anywhere.

#### Method 2: Shell Alias

Add to your shell configuration file (`~/.bashrc`, `~/.zshrc`, or `~/.config/fish/config.fish`):

```bash
alias download_vid="python /full/path/to/download_vid.py"
```

Replace `/full/path/to/` with the actual path to `download_vid.py`.

For Fish shell:
```fish
alias download_vid="python /full/path/to/download_vid.py"
```

Then reload your shell:
```bash
source ~/.bashrc  # or ~/.zshrc, or restart terminal
```

#### Method 3: Add to PATH

Add the script's directory to your PATH:

```bash
export PATH="$PATH:/full/path/to/video-dwd-cli"
```

Then you can use `./download_vid.py` or create a symlink.

## Usage

### Basic Syntax

```bash
download_vid \
  --platform <platform> \
  --link "<url>" \
  [--quality <quality>] \
  [--output <directory>] \
  [--audio-only] \
  [--filename <name>] \
  [--cookies <path>] \
  [--format <format>]
```

### Arguments

- `--platform` (required): Platform name (`youtube`, `instagram`, `twitter`, or `x`)
- `--link` (required): Video URL to download
- `--quality` (optional): Video quality (`360`, `480`, `720`, `1080`, `best`). Default: `best`
- `--output` (optional): Output directory. Default: current directory
- `--audio-only` (optional flag): Download audio only as MP3
- `--filename` (optional): Custom output filename (extension added automatically)
- `--cookies` (optional): Path to cookies file for authentication
- `--format` (optional): Output format (e.g., `mp4`, `webm`, `mkv` for video; `mp3`, `m4a`, `opus` for audio). Default: auto-detect

### Examples

#### Download YouTube Video (720p)

```bash
download_vid \
  --platform youtube \
  --link "https://www.youtube.com/watch?v=dQw4w9WgXcQ" \
  --quality 720 \
  --output ./downloads
```

#### Download Instagram Video (Best Quality)

```bash
download_vid \
  --platform instagram \
  --link "https://www.instagram.com/p/ABC123/" \
  --output ./downloads
```

#### Download Twitter/X Video with Audio Only

```bash
download_vid \
  --platform twitter \
  --link "https://twitter.com/user/status/1234567890" \
  --audio-only \
  --output ./downloads
```

#### Download with Custom Filename

```bash
download_vid \
  --platform youtube \
  --link "https://www.youtube.com/watch?v=dQw4w9WgXcQ" \
  --filename "my_video" \
  --quality 1080
```

#### Download with Cookies (for Private/Protected Content)

```bash
download_vid \
  --platform instagram \
  --link "https://www.instagram.com/p/ABC123/" \
  --cookies ~/cookies.txt \
  --output ./downloads
```

#### Download with Specific Format (Video)

```bash
download_vid \
  --platform youtube \
  --link "https://www.youtube.com/watch?v=dQw4w9WgXcQ" \
  --format webm \
  --quality 720
```

#### Download Audio with Specific Format

```bash
download_vid \
  --platform youtube \
  --link "https://www.youtube.com/watch?v=dQw4w9WgXcQ" \
  --audio-only \
  --format m4a
```

#### Using Python Directly

The script also works when called directly with Python:

```bash
python download_vid.py \
  --platform youtube \
  --link "https://www.youtube.com/watch?v=dQw4w9WgXcQ" \
  --quality 720
```

## Quality Selection

The tool uses intelligent quality selection:

- **Numeric qualities** (360, 480, 720, 1080): Selects the best available quality ≤ requested resolution
- **`best`**: Downloads the best available quality
- **Not specified**: Defaults to `best`

For example, if you request 720p but only 1080p and 480p are available, it will download 480p (the closest ≤ 720p).

## Format Selection

The `--format` option allows you to specify the output container format:

- **Video formats**: `mp4`, `webm`, `mkv`, `avi`, `mov`, `flv`
- **Audio formats**: `mp3`, `m4a`, `opus`, `ogg`, `wav`, `aac`
- **Not specified**: Auto-detects the best format available

When `--format` is specified:
- For video downloads: The video will be converted/merged to the specified format
- For audio-only downloads: The audio will be extracted in the specified format (defaults to `mp3` if not specified)

**Note**: Format conversion requires FFmpeg to be installed. If FFmpeg is not available, the tool will attempt to download in the requested format, but may fall back to the original format if conversion is not possible.

## Output

The tool provides clear feedback:

- Platform detected
- Selected quality
- Format (if specified)
- Output directory
- Real-time download progress
- Final file path on success
- Clear error messages on failure

Example output:

```
Platform: youtube
Quality: 720
Format: webm
Output directory: /home/user/downloads

Downloading: 45.2%
Download complete!                    
✓ Successfully downloaded to: /home/user/downloads/Video Title.webm
```

## Error Handling

The tool handles various error scenarios gracefully:

- **Invalid platform**: Shows supported platforms
- **Invalid URL**: Validates URL format
- **Unsupported quality**: Lists available quality options
- **Download failures**: Shows clear error messages
- **Missing cookies file**: Reports file not found

## Platform-Specific Notes

### YouTube
- Works with standard YouTube URLs
- Supports all quality options
- No authentication required for public videos

### Instagram
- May require cookies for private accounts
- Supports posts and reels
- Best quality is recommended for Instagram

### Twitter/X
- May require cookies for protected tweets
- Supports both `twitter.com` and `x.com` URLs
- Use `--platform twitter` or `--platform x` (both work)

## Cookies File

For Instagram and Twitter/X, you may need to provide a cookies file for authentication. Export cookies from your browser using extensions like:

- [Get cookies.txt LOCALLY](https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc) (Chrome)
- [cookies.txt](https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/) (Firefox)

Save the cookies to a file and provide the path with `--cookies`.

## Troubleshooting

### "yt-dlp is not installed"
Install the dependency:
```bash
pip install yt-dlp
```

### "Permission denied" when using alias
Make sure the script is executable:
```bash
chmod +x download_vid.py
```

### Download fails for Instagram/Twitter
Try providing a cookies file:
```bash
download_vid --platform instagram --link "..." --cookies ~/cookies.txt
```

### Alias not working
- Check that the path in your alias is correct
- Reload your shell configuration
- For symbolic links, ensure `/usr/local/bin` is in your PATH

## License

This tool uses `yt-dlp`, which is licensed under the Unlicense. Please respect the terms of service of the platforms you download from.

## Contributing

To extend support for new platforms, modify the `PLATFORMS` dictionary in the `VideoDownloader` class and add platform-specific logic if needed.

