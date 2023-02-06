# Libraries / Bibliotecas -----------------------------

from customtkinter import *
from customtkinter import filedialog
import customtkinter

from tkinter import messagebox, Listbox, Scrollbar
from PIL import Image
from pytube import YouTube
import tkinter

import subprocess
import threading
import time
from moviepy.video.io.VideoFileClip import VideoFileClip

import sys
import codecs
import os

from colored import fg, bg, attr

# Variables / Variáveis -------------------------------------------

app = customtkinter.CTk() # Cria o objeto app do qual tem a tela do programa e todas as funcionalidades.
video_Link = StringVar() 
download_Path = StringVar()
streamProgress = 0
lock = threading.Lock()
shared_index = 0
downloadNames = []

# Window Layout Configuration / Configuração da Janela --------------------------------

customtkinter.set_default_color_theme("dark-blue") 
app.wm_iconbitmap('logo.ico')
app.geometry("1000x500") 
app.resizable(False, False) 
app.title("UwUTuber - Kawaidesu youtube UwUloader") 
app.config(background="#ffffff")

# Window Layout Configuration / Configuração da Janela --------------------------------

photo = CTkImage(Image.open("logo.png"), size=(314, 222))
imagem = CTkButton(master=app, image=photo, state="disabled", text='', fg_color='#ffffff')
imagem.place(x=-30,y=40,width=614,height=232)
imagem["justify"] = "center"

link_label = CTkLabel(master=app, text="YouTube link", fg_color='#ffffff') 
link_label.grid(row=1, column=0, pady=5, padx=5)
link_label.place(x=110,y=300,width=312,height=30)
link_label["justify"] = "center"

linkText = CTkEntry(master=app, width=255, textvariable=video_Link) 
linkText.grid(row=1, column=1, pady=5, padx=5, columnspan = 2)
linkText['borderwidth'] = '1px'
linkText["justify"] = "center"
linkText.place(x=60,y=330,width=410,height=34)

destination_label = CTkLabel(master=app, text="Destination", fg_color='#ffffff') 
destination_label.grid(row=2, column=0, pady=5, padx=5)
destination_label["justify"] = "left"
destination_label.place(x=45,y=380,width=100,height=30)

destinationText = CTkEntry(master=app, width=145, textvariable=download_Path) 
destinationText.grid(row=2, column=1, pady=5, padx=5)
destinationText["justify"] = "center"
destinationText.place(x=135,y=380,width=245,height=30)

scrollbar = Scrollbar(app) # 
scrollbar.grid(row=3, column=4, pady=422, padx=422)
scrollbar.place(x=970,y=4,width=20, height=480)

listbox = Listbox(app, height=45, width=45, yscrollcommand=scrollbar.set)
listbox.grid(row=3, column=4, pady=422, padx=422)
listbox.place( x=520,y=5,width=450, height=480)
# listbox.pack(side="left", fill="both", expand=True)
# listbox.config(yscrollcommand=scrollbar.set)

scrollbar.config(command=listbox.yview)

def Browse(): 
    download_Directory = filedialog.askdirectory(initialdir="Directory Path") 
    download_Path.set(download_Directory) 

def update_progress(stream, chunk, bytes_remaining):
    global streamProgress
    streamProgress = (100 - ((100 * bytes_remaining) / stream.filesize))
    # listbox.itemconfig(shared_index, text="{:.2f} percent downloaded".format(streamProgress))
    listbox.delete(shared_index)
    listbox.insert(shared_index, "{}   ------ {:.2f}%".format(downloadNames[shared_index], streamProgress))

def update_progress_conversion(filename, progress, pkg_size):
    listbox.delete(shared_index)
    listbox.insert(shared_index, "{}   ------ {:.2f}%".format(filename, progress))

def ToggleDownload(state):
    if state == 'disabled':
        Download_B.configure(state='disabled')
        linkText.configure(state='disabled')
        destinationText.configure(state='disabled')
        browse_B.configure(state='disabled')
    else:
        Download_B.configure(state='normal')
        linkText.configure(state='normal')
        destinationText.configure(state='normal')
        browse_B.configure(state='normal')

def ThreadDownload():
    ToggleDownload('disabled')
    global shared_index
    if len(video_Link.get()) == 0:
        messagebox.showerror("Error", "Enter a YouTube link")
        return
    if len(download_Path.get()) == 0:
        messagebox.showerror("Error", "Enter a Destination")
        return
    with lock:
        shared_index = listbox.size()
        listbox.insert("end", "Downloading...")
    thread = threading.Thread(target=download_video, args=(shared_index, video_Link.get(), download_Path.get()))
    print(shared_index)
    downloadNames.append(YouTube(video_Link.get()).title)
    thread.daemon = True
    thread.start()

def download_video(index, url, path):
    global shared_index
    shared_index = index
    yt = YouTube(url, on_progress_callback=update_progress, on_complete_callback=CheckboxVerification)
    stream = yt.streams.get_highest_resolution()
    stream.download(output_path=path)

def CheckboxVerification(stream, file_path):
    print("on_complete_callback")
    if var_mp3.get() == "on":
        mp3Conversion(file_path)
    else:
        ToggleDownload('enabled')

def DeleteOldMp4(path):
    os.remove(path)
    listbox.delete(shared_index)
    listbox.insert(shared_index, "Conversão Realizada || {} ".format(downloadNames[shared_index]))
    ToggleDownload('enabled')


def mp3Conversion(path):
    clip = VideoFileClip(path)
    audio = clip.audio
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    listbox.delete(shared_index)
    listbox.insert(shared_index, "Convertendo: {} para o formato MP3.".format(downloadNames[shared_index]))
    audio.write_audiofile(path.replace(".mp4", ".mp3"), codec='libmp3lame') #, progress_callback=update_progress_conversion
    clip.close()
    DeleteOldMp4(path)

browse_B = CTkButton(master=app, text="Browse", command=Browse, width=10) 
browse_B.grid(row=2, column=2, pady=1, padx=1)
browse_B.place(x=390,y=380,width=71,height=30)

var_mp3 = tkinter.StringVar()
var_mp4 = tkinter.StringVar()
var_mp4.set("on")

def on_click_mp4():
    if var_mp4.get() == "on":
        var_mp3.set("off")

def on_click_mp3():
    if var_mp3.get() == "on":
        var_mp4.set("off")

mp3_checkbox = CTkCheckBox(master=app, text="MP4", command=on_click_mp4, variable=var_mp4, onvalue="on", offvalue="off")
mp3_checkbox.grid(row=3, column=1, pady=3, padx=3)
mp3_checkbox.place(x=60,y=420,width=65,height=25)

mp4_checkbox = CTkCheckBox(master=app, text="MP3", command=on_click_mp3, variable=var_mp3, onvalue="on", offvalue="off")
mp4_checkbox.grid(row=3, column=1, pady=3, padx=3)
mp4_checkbox.place(x=128,y=420,width=65,height=25)

Download_B = CTkButton(master=app, text="Download", command=ThreadDownload, width=20) 
Download_B.grid(row=3, column=1, pady=3, padx=3)
Download_B.place(x=200,y=420,width=131,height=30)

app.mainloop()
