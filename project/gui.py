from __future__ import unicode_literals
import os
import subprocess
from tkinter import StringVar

import requests
from io import BytesIO
from PIL import Image
import customtkinter
import youtube_dl


#GUI Settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")

def open_folder_with_explorer():
    currentPath = os.getcwd()
    folderName = 'downloads'
    path = os.path.join(currentPath, folderName)
    if os.name == 'nt':
        # For Windows
        subprocess.Popen(f'explorer "{path}"')
    elif os.name == 'posix':
        # For Mac
        subprocess.Popen(['open', path])
    else:
        raise OSError(f'Unsupported platform: {os.name}')

class App(customtkinter.CTk):

    def __init__(self):
        super().__init__()
        self.title("YTDownloader")
        self.selectedFormat = "Video"
        self.geometry("720x600")
        self.iconbitmap("image.ico")
        self.thumbnail_url = ""
        self.videotitle = ""
        self.author = ""
        self.duration = ""
        self.format_id = ""  # format id of the video/audio
        self.ext = ""  # file extension of the video/audio
        self.filesize = "" # size of the video/audio file in bytes
        self.openFolder = True


        self.label = customtkinter.CTkLabel(master=self, text="YouTube and SoundCloud Downloader")
        self.label.pack()

        def updateMediaInfo(url):
            ydl_opts = {}
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                video_info = ydl.extract_info(url, download=False)
                self.thumbnail_url = video_info.get("thumbnail")
                self.videotitle = video_info.get('title')
                self.duration = video_info.get("duration")
                self.author = video_info.get("uploader")
                self.format_id = video_info.get("format_id")  # format id of the video/audio
                self.ext = video_info.get("ext")  # file extension of the video/audio
                self.filesize = video_info.get("filesize")  # size of the video/audio file in bytes

        def callback(str_var):
            updateMediaInfo(str_var.get())
            updateThumbnail(self.thumbnail_url)

        url_var = StringVar()
        self.url_entry = customtkinter.CTkEntry(master=self, placeholder_text="Enter a valid URL", width=500, textvariable=url_var)
        url_var.trace("w", lambda name, index, mode, url_var=url_var: callback(url_var))
        self.url_entry.pack(padx=10, pady=10)

        def updateProgress(d):
            if 'status' in d:
                status = d['status']
                if status == 'downloading' and '_percent_str' in d:
                    percent = d['_percent_str']
                    self.label.configure(text=f"{percent}")
                elif status == 'finished':
                    self.label.configure(text="Downloaded!")
                    if self.openFolder:
                        open_folder_with_explorer()

        def button_find_event():
            for filename in os.listdir("."):
                if filename == "thumbnail.png":
                    os.remove(filename)
            entry = self.url_entry.get()
            youtube = "youtube.com"
            soundcloud = "soundcloud.com"

            if not entry:
                self.label.configure(self, text="Please enter a valid URL.")
                return

            if soundcloud in entry:
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': './downloads/%(title)s.%(ext)s',
                    'noplaylist': True,
                    'progress_hooks': [updateProgress],
                }
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    video_info = ydl.extract_info(entry, download=False)
                    updateMediaInfo(entry)
                    ydl.download([entry])

            elif youtube in entry:
                ydl_opts = {}
                if self.selectedFormat == "Audio":
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'outtmpl': './downloads/%(title)s.%(ext)s',
                        'noplaylist': True,
                        'progress_hooks': [updateProgress],
                    }
                elif self.selectedFormat == "Video":
                    ydl_opts = {
                        'format': 'best',
                        'outtmpl': './downloads/%(title)s.%(ext)s',
                        'noplaylist': True,
                        'progress_hooks': [updateProgress],
                    }
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    video_info = ydl.extract_info(entry, download=False)
                    updateMediaInfo(entry)
                    ydl.download([entry])

        def optionmenu_callback(choice):
            self.selectedFormat= choice

        self.label = customtkinter.CTkLabel(self, text="Enter a Soundcloud or Youtube URL")
        self.label.pack()

        self.optionmenu = customtkinter.CTkOptionMenu(self, values=["Audio", "Video"],
                                                 command=optionmenu_callback)
        self.optionmenu.set("Select format")
        self.optionmenu.pack(padx=10, pady=10)

        def switch_event():
            if self.path_folder_switch.get() is "off":
                self.openFolder = False
            else:
                self.openFolder = True
        self.path_folder_switch = customtkinter.StringVar(value="on")
        self.path_folder_switch = customtkinter.CTkSwitch(self, text="Open Folder after Download", command=switch_event,
                                         variable=self.path_folder_switch, onvalue="on", offvalue="off")
        self.path_folder_switch.pack()

        self.button_find = customtkinter.CTkButton(self, text="Download", command=button_find_event)
        self.button_find.pack(padx=10, pady=10)

        def updateThumbnail(url):
            if url:
                response = requests.get(url)
                img_data = response.content
                pil_img = Image.open(BytesIO(img_data))
                pil_img.save("thumbnail.png", format="PNG")

                def checkforThumbnail():
                    if os.path.isfile("thumbnail.png"):
                        return "thumbnail.png"
                    else:
                        return ""

                if checkforThumbnail() != "":
                    def getThumbnailSizeWidth():
                        with Image.open("thumbnail.png") as img:
                            width, height = img.size
                            if width > 300:
                                width = 300
                            return width

                    def getThumbnailSizeHeight():
                        with Image.open("thumbnail.png") as img:
                            width, height = img.size
                            if width > 300:
                                height = int(height * (300 / width))
                            return height

                    try:
                        self.bg_image_label.destroy()
                    except Exception as e:
                        print(e)
                    self.thumbnail = customtkinter.CTkImage(Image.open(checkforThumbnail()),
                                                            size=(getThumbnailSizeWidth(), getThumbnailSizeHeight()))
                    self.bg_image_label = customtkinter.CTkLabel(self, image=self.thumbnail, text="", width=300)
                    self.bg_image_label.pack(padx=10, pady=10)

                    try:
                        self.thumbnail_title.destroy()
                    except Exception as e:
                        print(e)
                    def returnThumbnailInfo():
                        return f"{self.author}"+"\n"+f"{self.videotitle}"+"\n file format : "+f"{self.ext}"+"\n"
                    self.thumbnail_title = customtkinter.CTkLabel(self, text=returnThumbnailInfo())
                    if self.videotitle != "":
                        self.thumbnail_title.pack()




