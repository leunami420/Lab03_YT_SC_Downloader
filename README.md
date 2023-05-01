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

Once you have all the dependencies installed, you can simply download the `main.py` file from this repository and run it with Python:

```bash
python main.py
```

## 💻 Usage

When you run the app, a simple GUI will appear that prompts you to enter a valid YouTube or SoundCloud URL. You can also select the desired format (video or audio) from a dropdown menu.

![Screenshot of the GUI](https://imgur.com/o3SGTVc.png)

After entering a valid URL and selecting the desired format, click the "Download" button to start the download process. The app will automatically download the highest possible quality format for the selected type.

Once the download is complete, a message will appear indicating that the content has been downloaded. The downloaded content will be saved to the `downloads` folder in the app's working directory.

If the app appears to freeze during the download process, it is likely that it is busy downloading a large file. Please be patient and wait for the download to complete.

## 🚀 Future Implementations

Here are a few ideas for future implementations of the app:

- Add support for downloading content from other popular websites like Vimeo, Dailymotion, and Facebook.
- Allow users to specify the output directory for downloaded content instead of using the default "downloads" directory in the app's working directory.
- Implement a feature to automatically convert downloaded video files to different formats (e.g. from MP4 to AVI or from MOV to WMV).
- Add a feature to extract audio from video files and save them as separate files (e.g. extract the audio from a music video and save it as an MP3 file).
- Implement a feature to search for and download entire playlists or channels from YouTube or Soundcloud.
- Add support for downloading subtitles or closed captions for downloaded videos.
- Implement a feature to download only a specific portion of a video (e.g. download only the first 30 seconds of a music video).

## ⚠️ Disclaimer

This application is intended for personal use only. Downloading copyrighted material without permission is illegal in most countries, and we do not condone or encourage such activity. Please use this app responsibly and follow all applicable laws and regulations.