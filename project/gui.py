from __future__ import unicode_literals
import os
import shutil
import subprocess
from tkinter import StringVar, filedialog
import MediaConverter
import requests
from io import BytesIO
from PIL import Image
import customtkinter
import youtube_dl


#GUI Settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")

downloadPath = os.path.join(os.getcwd(), 'downloads')



class App(customtkinter.CTk):

    def __init__(self):
        super().__init__()
        #----------------
        # GUI Window Settings
        #----------------
        self.title("YTDownloader")
        self.geometry("720x700")
        self.iconbitmap("image.ico")
        # ----------------
        # Media Info
        # ----------------
        self.thumbnail_url = ""
        self.videotitle = ""
        self.author = ""
        self.duration = ""
        self.format_id = ""  # format id of the video/audio
        self.ext = ""  # file extension of the video/audio
        self.downloadedFileExt = ""
        self.filesize = ""  # size of the video/audio file in bytes
        # ----------------
        # Standard Settings
        # ----------------
        self.selectedFormat = "Video - Original"
        self.openFolder = True
        self.desiredExt = ""
        global downloadPath
        # ----------------
        # Update Media Information
        # input = MediaUrl
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


        # ----------------
        # Update Info&Thumbnail upon Entry
        def callback(str_var):
            updateMediaInfo(str_var.get())
            updateThumbnail()

        # ----------------
        # Callback Function on switch use
        # ----------------
        def switch_event():
            updateThumbnail()
            if self.path_folder_switch.get() == "off":
                self.openFolder = False
            else:
                self.openFolder = True

        # ----------------
        # Callback Function to Set The Download OptionMenu
        # inserts = "Audio" or "Video"
        # ----------------

        def optionmenu_callback(choice):
            self.selectedFormat = choice
            if "Original" not in choice:
                self.desiredExt = choice[8:]
            else:
                self.desiredExt = ""

        # ----------------
        # Place Title Label in GUI
        # ----------------
        self.label = customtkinter.CTkLabel(master=self, text="YouTube and SoundCloud Downloader")
        self.label.pack()

        # ----------------
        # ButtonEventMethod when Download is pressed
        # ----------------
        def button_find_event():
            for filename in os.listdir("tempfile"):
                os.remove("tempfile/" + filename)
            for filename in os.listdir("."):
                if filename == "thumbnail.png":
                    os.remove(filename)
            entry = self.url_entry.get()
            youtube = "youtube.com"
            soundcloud = "soundcloud.com"

            # ----------------
            # NO URL
            if not entry:
                self.label.configure(self, text="Please enter a valid URL.")
                return
            # ----------------
            # SOUNDCLOUD URL
            if soundcloud in entry:
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': './tempfile/%(title)s.%(ext)s',
                    'noplaylist': True,
                    'progress_hooks': [updateProgress],
                }
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    updateMediaInfo(entry)
                    ydl.download([entry])
            # ----------------
            # YOUTUBE URL
            elif youtube in entry:
                ydl_opts = {}
                if "Audio" in self.selectedFormat:
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'outtmpl': './tempfile/%(title)s.%(ext)s',
                        'noplaylist': True,
                        'progress_hooks': [updateProgress],
                    }
                if "Video" in self.selectedFormat:
                    ydl_opts = {
                        'format': 'best',
                        'outtmpl': './tempfile/%(title)s.%(ext)s',
                        'noplaylist': True,
                        'progress_hooks': [updateProgress],
                    }
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    updateMediaInfo(entry)
                    ydl.download([entry])

        # ----------------
        # URL Entry in GUI and callback
        # ----------------
        url_var = StringVar()
        self.url_entry = customtkinter.CTkEntry(master=self, placeholder_text="Enter a valid URL", width=500, textvariable=url_var)
        url_var.trace("w", lambda name, index, mode, url_var=url_var: callback(url_var))
        self.url_entry.pack(padx=10, pady=10)

        # ----------------
        # Hook Method that reads the Download Status
        # ----------------
        def updateProgress(d):
            if 'status' in d:
                status = d['status']
                if status == 'downloading' and '_percent_str' in d:
                    percent = d['_percent_str']
                    self.label.configure(text=f"{percent}")
                if status == 'finished':
                    #self.downloadedFileExt =
                    directory = "tempfile"
                    for file in os.listdir(directory):
                        self.downloadedFileExt= os.path.splitext(file)[-1]
                    self.downloadedFileExt = self.downloadedFileExt[1:]
                    # if the format is already the right one
                    if self.desiredExt == self.downloadedFileExt:
                        MediaConverter.movetoDownloads()
                        self.label.configure(text="Downloaded!")
                    # if desired ext specified convert the file
                    if self.desiredExt != "":
                        if "Audio" in self.selectedFormat:
                            MediaConverter.convert_audio_format(self.videotitle, self.downloadedFileExt, self.desiredExt)
                        if "Video" in self.selectedFormat:
                            MediaConverter.convert_video_format(self.videotitle, self.downloadedFileExt, self.desiredExt)
                    if self.desiredExt == "":
                        MediaConverter.movetoDownloads()
                        self.label.configure(text="Downloaded!")
                    self.WriteToDownload_dir_andOpen()

        # ----------------
        # Place Status Label in GUI
        # ----------------
        self.label = customtkinter.CTkLabel(self, text="Enter a Soundcloud or Youtube URL")
        self.label.pack()

        # ----------------
        # Tab in Gui [Download][Settings]
        # ----------------
        class MyTabView(customtkinter.CTkTabview):
            def __init__(self, master, **kwargs):
                super().__init__(master, **kwargs)
                global downloadPath

                # create tabs
                self.add("Download")
                self.add("Settings")

                # ----------------
                # Place OptionMenu in GUI [Download]
                # ----------------
                self.optionmenu = customtkinter.CTkOptionMenu(master=self.tab("Download"), values=["Audio - Original",
                                                                            "Audio - mp3",
                                                                            "Audio - wav",
                                                                            "Audio - ogg",
                                                                            "Video - Original",
                                                                            "Video - mp4",
                                                                            "Video - ogv",
                                                                            "Video - webm",
                                                                            "Video - avi", ],
                                                              command=optionmenu_callback)
                self.optionmenu.set("Select format")
                self.optionmenu.pack(padx=10, pady=10)
                # ----------------
                # Place the Download Button in GUI [Download]
                # ----------------
                self.button_find = customtkinter.CTkButton(master=self.tab("Download"), text="Download", command=button_find_event)
                self.button_find.pack(padx=10, pady=10)

                # ----------------
                # Place Switch to OpenDLPath in GUI [Settings]
                # ----------------
                self.path_folder_switch = customtkinter.StringVar(value="on")
                self.path_folder_switch = customtkinter.CTkSwitch(master=self.tab("Settings"),
                                                                  text="Open Folder after Download",
                                                                  command=switch_event,
                                                                  variable=self.path_folder_switch, onvalue="on",
                                                                  offvalue="off")
                self.path_folder_switch.pack(padx=10, pady=10)

                # ----------------
                # Label [Settings]
                # ----------------
                self.path_label = customtkinter.CTkLabel(master=self.tab("Settings"), text="Files will downloaded to :")
                self.path_label.pack(padx=20, pady=10)
                # ----------------
                # Current DownloadFolder [Settings]
                # ----------------
                self.path_label = customtkinter.CTkLabel(master=self.tab("Settings"), text=f"{downloadPath}")
                self.path_label.pack(padx=10, pady=10)
                # ----------------
                # Choose new Downloadfolder [Setting] callback()
                # ----------------
                def switchDownloadFolder():
                    global downloadPath
                    downloadPath = filedialog.askdirectory()
                    self.path_label.configure(text=downloadPath)
                # ----------------
                # Change Download Folder [Settings]
                # ----------------
                self.button_folder = customtkinter.CTkButton(master=self.tab("Settings"), text="Change",
                                                           command=switchDownloadFolder)
                self.button_folder.pack(padx=10, pady=10)



        self.tab_view = MyTabView(master=self, height=100)
        self.tab_view.pack()

        # ----------------
        # Metadata Preview Section
        # ----------------
        def updateThumbnail():
            IMGurl = self.thumbnail_url
            if IMGurl:
                response = requests.get(IMGurl)
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
                    self.bg_image_label.pack(padx=10, pady=30)

                    try:
                        self.thumbnail_title.destroy()
                    except Exception as e:
                        print(e)
                    def returnThumbnailInfo():
                        return f"{self.author}"+"\n"+f"{self.videotitle}"+"\n file format : "+f"{self.ext}"+"\n"
                    self.thumbnail_title = customtkinter.CTkLabel(self, text=returnThumbnailInfo())
                    self.thumbnail_title.pack()



    def WriteToDownload_dir_andOpen(self):
        global downloadPath
        downloads = os.path.join(os.getcwd(), 'downloads')
        path = downloadPath
        print(downloadPath)
        if downloads != path:
            files = os.listdir(downloads)
            for filename in files:
                src_file = os.path.join(downloads, filename)
                dest_file = os.path.join(path, filename)
                # Use shutil.move() to move the file
                shutil.move(src_file, dest_file)
        if self.openFolder:
            if os.name == 'nt':
                # For Windows
                os.startfile(path)
            elif os.name == 'posix':
                # For Mac
                subprocess.Popen(['open', path])
            else:
                raise OSError(f'Unsupported platform: {os.name}')