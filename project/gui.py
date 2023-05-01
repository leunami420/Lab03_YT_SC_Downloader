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
        self.title("YouTube and SoundCloud Downloader")



        self.label = customtkinter.CTkLabel(master=self, text="YouTube and SoundCloud Downloader")
        self.label.pack()

        self.url_entry = customtkinter.CTkEntry(master=self, placeholder_text="Enter a valid URL", width=500)
        self.url_entry.pack(padx=10, pady=10)


        def button_find_event():
            entry = self.url_entry.get()
            youtube = "youtube.com"
            soundcloud = "soundcloud.com"
            if soundcloud in entry:
                def my_hook(d):
                    if d['status'] == 'finished':
                        self.label.configure(self, text="Downloaded!")
                        open_folder_with_explorer()
                    if d['status'] == 'downloading':
                        self.label.configure(self, text="Downloading...")
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': './downloads/%(title)s.%(ext)s',
                    'noplaylist': True,
                    'progress_hooks': [my_hook],
                }
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([entry])
            if youtube in entry:
                def my_hook(d):
                    if d['status'] == 'finished':
                        self.label.configure(self, text="Downloaded!")
                        open_folder_with_explorer()

                    if d['status'] == 'downloading':
                        self.label.configure(self, text="Downloading...")
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
                    ydl.download([entry])


        def optionmenu_callback(choice):
            self.selectedFormat= choice

        self.label = customtkinter.CTkLabel(self, text="Enter a Soundcloud or Youtube URL")
        self.label.pack()

        self.optionmenu = customtkinter.CTkOptionMenu(self, values=["Audio", "Video"],
                                                 command=optionmenu_callback)
        self.optionmenu.set("Select format")
        self.optionmenu.pack(padx=10, pady=10)

        self.button_find = customtkinter.CTkButton(self, text="Download", command=button_find_event)
        self.button_find.pack(padx=10, pady=10)

