#!/usr/bin/env python3
"""
Video Downloader CLI Tool
Supports YouTube, Instagram, and Twitter/X video downloads using yt-dlp
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any


class VideoDownloader:
    """Main video downloader class handling platform-specific logic and downloads."""
    
    # Supported platforms mapping
    PLATFORMS = {
        'youtube': ['youtube.com', 'youtu.be'],
        'instagram': ['instagram.com'],
        'twitter': ['twitter.com', 'x.com'],
        'x': ['twitter.com', 'x.com']  # Alias for twitter
    }
    
    # Quality options
    QUALITY_OPTIONS = ['360', '480', '720', '1080', 'best']
    
    def __init__(self, platform: str, link: str, quality: Optional[str] = None,
                 output_dir: Optional[str] = None, audio_only: bool = False,
                 filename: Optional[str] = None, cookies: Optional[str] = None,
                 format: Optional[str] = None):
        """
        Initialize the video downloader.
        
        Args:
            platform: Platform name (youtube, instagram, twitter/x)
            link: Video URL
            quality: Video quality (360, 480, 720, 1080, best)
            output_dir: Output directory path
            audio_only: Whether to download audio only
            filename: Custom output filename
            cookies: Path to cookies file for authentication
            format: Output format (e.g., mp4, webm, mkv for video; mp3, m4a, opus for audio)
        """
        self.platform = self._normalize_platform(platform)
        self.link = link
        self.quality = quality or 'best'
        self.output_dir = Path(output_dir) if output_dir else Path.cwd()
        self.audio_only = audio_only
        self.filename = filename
        self.cookies = cookies
        self.format = format
        
        # Validate inputs
        self._validate_inputs()
        
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def _normalize_platform(self, platform: str) -> str:
        """Normalize platform name (e.g., 'x' -> 'twitter')."""
        platform_lower = platform.lower()
        if platform_lower == 'x':
            return 'twitter'
        return platform_lower
    
    def _validate_inputs(self) -> None:
        """Validate platform, URL, and other inputs."""
        # Validate platform
        if self.platform not in self.PLATFORMS:
            valid_platforms = ', '.join([p for p in self.PLATFORMS.keys() if p != 'x'])
            raise ValueError(f"Invalid platform '{self.platform}'. Supported platforms: {valid_platforms}")
        
        # Validate URL format
        if not self.link.startswith(('http://', 'https://')):
            raise ValueError(f"Invalid URL format: {self.link}")
        
        # Validate platform URL match
        url_lower = self.link.lower()
        platform_domains = self.PLATFORMS[self.platform]
        if not any(domain in url_lower for domain in platform_domains):
            print(f"Warning: URL '{self.link}' may not match platform '{self.platform}'")
        
        # Validate quality
        if self.quality not in self.QUALITY_OPTIONS:
            valid_qualities = ', '.join(self.QUALITY_OPTIONS)
            raise ValueError(f"Invalid quality '{self.quality}'. Supported qualities: {valid_qualities}")
        
        # Validate cookies file if provided
        if self.cookies and not os.path.isfile(self.cookies):
            raise FileNotFoundError(f"Cookies file not found: {self.cookies}")
    
    def _get_quality_format_selector(self) -> str:
        """
        Generate yt-dlp format selector based on quality preference.
        
        Returns:
            Format selector string for yt-dlp
        """
        if self.audio_only:
            return 'bestaudio/best'
        
        if self.quality == 'best':
            return 'bestvideo+bestaudio/best'
        
        # For numeric qualities, find closest available ≤ requested
        try:
            target_height = int(self.quality)
        except ValueError:
            return 'bestvideo+bestaudio/best'
        
        # Format selector: prefer video with height <= target, fallback to best
        # This selects the best quality video with height <= target_height
        return f'bestvideo[height<={target_height}]+bestaudio/best[height<={target_height}]/best'
    
    def _get_output_template(self) -> str:
        """
        Generate output filename template for yt-dlp.
        
        Returns:
            Output template string
        """
        if self.filename:
            # User provided custom filename
            # Remove any existing extension and let yt-dlp handle it
            base_name = os.path.splitext(self.filename)[0]
            # For audio-only, we'll post-process to mp3, so use a temp extension
            if self.audio_only:
                template = base_name + '.%(ext)s'
            else:
                template = base_name + '.%(ext)s'
            return str(self.output_dir / template)
        
        # Default template
        return str(self.output_dir / '%(title)s.%(ext)s')
    
    def _get_ydl_opts(self) -> Dict[str, Any]:
        """
        Generate yt-dlp options dictionary.
        
        Returns:
            Dictionary of yt-dlp options
        """
        # Use custom progress hook if set, otherwise use default
        progress_hook = getattr(self, '_custom_progress_hook', None) or self._progress_hook
        
        opts = {
            'format': self._get_quality_format_selector(),
            'outtmpl': self._get_output_template(),
            'quiet': False,
            'no_warnings': False,
            'progress_hooks': [progress_hook],
        }
        
        # Add cookies if provided
        if self.cookies:
            opts['cookiefile'] = self.cookies
        
        # Audio-only specific options
        if self.audio_only:
            # Use specified format or default to mp3
            audio_codec = self.format or 'mp3'
            opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': audio_codec,
                'preferredquality': '192',
            }]
            # Override output template for audio
            if not self.filename:
                opts['outtmpl'] = str(self.output_dir / '%(title)s.%(ext)s')
        else:
            # For video, use merge_output_format if format is specified
            if self.format:
                opts['merge_output_format'] = self.format
        
        return opts
    
    def _progress_hook(self, d: Dict[str, Any]) -> None:
        """Progress hook for yt-dlp to show download status."""
        if d['status'] == 'downloading':
            if 'total_bytes' in d:
                percent = (d['downloaded_bytes'] / d['total_bytes']) * 100
                print(f"\rDownloading: {percent:.1f}%", end='', flush=True)
            elif '_percent_str' in d:
                print(f"\r{d['_percent_str']}", end='', flush=True)
        elif d['status'] == 'finished':
            print(f"\rDownload complete!                    ")
    
    def download(self, suppress_output: bool = False) -> Optional[str]:
        """
        Download the video/audio.
        
        Args:
            suppress_output: If True, suppress print statements (useful for GUI)
        
        Returns:
            Path to downloaded file on success, None on failure
        """
        # Import yt-dlp here to allow --help to work without it installed
        try:
            import yt_dlp
            from yt_dlp import utils as yt_dlp_utils
        except ImportError:
            error_msg = "Error: yt-dlp is not installed. Please install it with: pip install yt-dlp"
            if not suppress_output:
                print(error_msg)
            sys.exit(1)
        
        if not suppress_output:
            print(f"Platform: {self.platform}")
            print(f"Quality: {self.quality}")
            if self.format:
                print(f"Format: {self.format}")
            print(f"Output directory: {self.output_dir.absolute()}")
            if self.audio_only:
                print("Mode: Audio only")
            print()
        
        ydl_opts = self._get_ydl_opts()
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Extract info first to get the final filename
                info = ydl.extract_info(self.link, download=False)
                
                # Download
                ydl.download([self.link])
                
                # Determine final file path
                # For custom filename, construct the path
                if self.filename:
                    base_name = os.path.splitext(self.filename)[0]
                    if self.audio_only:
                        # Use specified format or default to mp3
                        ext = self.format or 'mp3'
                    else:
                        # Use specified format or get from info
                        ext = self.format or info.get('ext', 'mp4')
                    final_filename = base_name + '.' + ext
                    final_path = (self.output_dir / final_filename).absolute()
                else:
                    # Use the prepared filename from yt-dlp
                    final_filename = ydl.prepare_filename(info)
                    if self.audio_only:
                        # Postprocessor converts to specified format or mp3
                        base = os.path.splitext(final_filename)[0]
                        ext = self.format or 'mp3'
                        final_path = Path(base + '.' + ext).absolute()
                    else:
                        # If format was specified, replace extension
                        if self.format:
                            base = os.path.splitext(final_filename)[0]
                            final_path = Path(base + '.' + self.format).absolute()
                        else:
                            final_path = Path(final_filename).absolute()
                
                if not suppress_output:
                    print(f"\n✓ Successfully downloaded to: {final_path}")
                return str(final_path)
                
        except yt_dlp_utils.DownloadError as e:
            error_msg = f"Download error: {str(e)}"
            if not suppress_output:
                print(f"\n✗ {error_msg}")
                sys.exit(1)
            raise Exception(error_msg)
        except yt_dlp_utils.ExtractorError as e:
            error_msg = f"Extraction error: {str(e)}"
            if not suppress_output:
                print(f"\n✗ {error_msg}")
                print("This might be due to an invalid URL or unsupported content.")
                sys.exit(1)
            raise Exception(error_msg)
        except Exception as e:
            if not suppress_output:
                print(f"\n✗ Unexpected error: {str(e)}")
                sys.exit(1)
            raise


def main():
    """Main entry point for the CLI tool."""
    parser = argparse.ArgumentParser(
        description='Download videos from YouTube, Instagram, and Twitter/X',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  download_vid --platform youtube --link "https://youtube.com/watch?v=..." --quality 720
  download_vid --platform instagram --link "https://instagram.com/p/..." --output ./downloads
  download_vid --platform twitter --link "https://twitter.com/.../status/..." --audio-only
  download_vid --platform x --link "https://x.com/.../status/..." --quality best --filename "my_video"
  download_vid --platform youtube --link "https://youtube.com/watch?v=..." --format webm
  download_vid --platform youtube --link "https://youtube.com/watch?v=..." --audio-only --format m4a
        """
    )
    
    parser.add_argument(
        '--platform',
        required=True,
        choices=['youtube', 'instagram', 'twitter', 'x'],
        help='Platform name (youtube, instagram, twitter, or x)'
    )
    
    parser.add_argument(
        '--link',
        required=True,
        help='Video URL to download'
    )
    
    parser.add_argument(
        '--quality',
        default='best',
        choices=['360', '480', '720', '1080', 'best'],
        help='Video quality (default: best)'
    )
    
    parser.add_argument(
        '--output',
        default=None,
        help='Output directory (default: current directory)'
    )
    
    parser.add_argument(
        '--audio-only',
        action='store_true',
        help='Download audio only (MP3)'
    )
    
    parser.add_argument(
        '--filename',
        default=None,
        help='Custom output filename (extension will be added automatically)'
    )
    
    parser.add_argument(
        '--cookies',
        default=None,
        help='Path to cookies file for authentication (useful for Instagram/Twitter)'
    )
    
    parser.add_argument(
        '--format',
        default=None,
        help='Output format (e.g., mp4, webm, mkv for video; mp3, m4a, opus for audio). Default: auto-detect'
    )
    
    args = parser.parse_args()
    
    try:
        downloader = VideoDownloader(
            platform=args.platform,
            link=args.link,
            quality=args.quality,
            output_dir=args.output,
            audio_only=args.audio_only,
            filename=args.filename,
            cookies=args.cookies,
            format=args.format
        )
        
        downloader.download()
        
    except ValueError as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nDownload cancelled by user.")
        sys.exit(1)


if __name__ == '__main__':
    main()

