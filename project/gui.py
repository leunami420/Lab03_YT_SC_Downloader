from __future__ import unicode_literals

import os
import subprocess
import tkinter
import customtkinter
import youtube_dl




#GUI Settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

def open_folder_with_explorer():
    print("testet")
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
        self.selectedFormat = "Video"
        self.geometry("720x480")
        self.title("YouTube and SoundCloud Converter")



        self.label = customtkinter.CTkLabel(master=self, text="YouTube and SoundCloud Converter")
        self.label.pack()

        self.url_entry = customtkinter.CTkEntry(master=self, placeholder_text="Enter a valid URL")
        self.url_entry.pack(padx=10, pady=10)


        def button_find_event():
            entry = self.url_entry.get()
            youtube = "youtube.com"
            soundcloud = "soundcloud.com"
            if soundcloud in entry:
                # if entered url contains youtube.com do the following:
                # retrieve video metadata
                def my_hook(d):
                    if d['status'] == 'finished':
                        self.label_invalidUrl.configure(self, text="Downloaded!")
                        open_folder_with_explorer()
                    if d['status'] == 'downloading':
                        self.label_invalidUrl.configure(self, text="Downloading...")


                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': './downloads/%(title)s.%(ext)s',
                    'noplaylist': True,
                    'progress_hooks': [my_hook],
                }
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(entry, download=False)
                    filename = ydl.prepare_filename(info_dict)
                    ydl.download([entry])
            if youtube in entry:
                #if entered url contains youtube.com do the following:
                #retrieve video metadata
                def my_hook(d):
                    if d['status'] == 'finished':
                        self.label_invalidUrl.configure(self, text="Downloaded!")
                        open_folder_with_explorer("./downloads/")

                    if d['status'] == 'downloading':
                        self.label_invalidUrl.configure(self, text="Downloading...")
                ydl_opts = {}
                if self.selectedFormat == "Audio":
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'outtmpl': './downloads/%(title)s.%(ext)s',
                        'noplaylist': True,
                        'progress_hooks': [my_hook],
                    }
                if self.selectedFormat == "Video":
                    ydl_opts = {
                        'format': 'best',
                        'outtmpl': './downloads/%(title)s.%(ext)s',
                        'noplaylist': True,
                        'progress_hooks': [my_hook],
                    }
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(entry, download=False)
                    filename = ydl.prepare_filename(info_dict)
                    ydl.download([entry])


        def optionmenu_callback(choice):
            self.selectedFormat= choice

        self.label_invalidUrl = customtkinter.CTkLabel(self, text="Enter a Soundcloud or Youtube URL")
        self.label_invalidUrl.pack()

        self.optionmenu = customtkinter.CTkOptionMenu(self, values=["Audio", "Video"],
                                                 command=optionmenu_callback)
        self.optionmenu.set("Select format")
        self.optionmenu.pack(padx=10, pady=10)

        self.button_find = customtkinter.CTkButton(self, text="find", command=button_find_event)
        self.button_find.pack(padx=10, pady=10)

