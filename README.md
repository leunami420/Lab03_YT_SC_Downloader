
# 🎥🎵 YouTube and SoundCloud Downloader 

YouTube and SoundCloud Downloader is a simple Python application that allows you to download videos and audio from YouTube and SoundCloud with just a few clicks. The app uses the `youtube_dl` module to download the content and a custom GUI built with `tkinter` and `customtkinter` for the user interface.

## 🚀 Installation

To use the app, you must have Python 3 and the `youtube_dl` module installed on your computer. To install `youtube_dl`, run the following command in your terminal:

```bash
pip install youtube_dl
```

You also need to have the `tkinter` and `customtkinter` modules installed. These modules come pre-installed with Python 3 on most operating systems, but if you encounter any issues, you can install them using pip:

```bash
pip install tkinter
pip install customtkinter
```

For the conversion process the app requires moviepy:

```bash
Copy code
pip install moviepy
```

To install PIL, run the following command in your terminal:

```bash
Copy code
pip install pillow
```

Once you have all the dependencies installed, you can simply download the `main.py` file from this repository and run it with Python:

```bash
python main.py
```



## 💻 Usage

When you run the app, a simple GUI will appear that prompts you to enter a valid YouTube or SoundCloud URL. You can also select the desired format (video or audio) from a dropdown menu.

![Screenshot of a downloaded YoutTube Video](https://imgur.com/EXob1RI.png)

After entering a valid URL and selecting the desired format, click the "Download" button to start the download process. The app will automatically download the highest possible quality format for the selected type.

Once the download is complete, a message will appear indicating that the content has been downloaded. The downloaded content will be saved to the `downloads` folder in the app's working directory.

If the app appears to freeze during the download process, it is likely that it is busy downloading a large file. Please be patient and wait for the download to complete.

![List of supported file formats](https://imgur.com/G7w2NYs.png)



## 🚀 Future Implementations

Here are a few ideas for future implementations of the app:

- Add support for downloading content from other popular websites like Vimeo, Dailymotion, and Facebook.
- Allow users to specify the output directory for downloaded content instead of using the default "downloads" directory in the app's working directory.
- Implement a feature to search for and download entire playlists or channels from YouTube or Soundcloud.
- Add support for downloading subtitles or closed captions for downloaded videos.
- Implement a feature to download only a specific portion of a video (e.g. download only the first 30 seconds of a music video).

## ⚠️ Disclaimer

This application is intended for personal use only. Downloading copyrighted material without permission is illegal in most countries, and we do not condone or encourage such activity. Please use this app responsibly and follow all applicable laws and regulations.

## 🐛 Known Bugs

If you encounter the error `"Unable to extract uploader id; please report this issue on https://github.com/yt-dlp/yt-dlp/issues?q=` try the following steps:

1. Confirm that you are on the latest version of yt-dlp by running `yt-dlp -U` in your command prompt or terminal.
2. If you are still encountering the error, uninstall youtube_dl by running `pip uninstall youtube_dl`.
3. Install youtube-dl via pip with the following command: `pip install --upgrade --force-reinstall "git+https://github.com/ytdl-org/youtube-dl.git"`

This should resolve the issue.

## Updates

### Version 1.2.0 (2023-05-02)
- Added a slider option to not open the output directory after downloading content
- Updated the GUI to provide more detailed information about the downloaded content
- Improved the code structure and readability
- Implemented a feature to automatically convert downloaded files to a desired format (mp3,wav,ogg,mp4,ogv,webm,avi).

### Version 1.1 (2023-05-01)
- Added support for downloading SoundCloud tracks and playlists
- Added a thumbnail image, title, author and file format preview for downloaded files

### Version 1.0 (2023-04-30)
- Initial release with support for downloading YouTube videos and playlists.
