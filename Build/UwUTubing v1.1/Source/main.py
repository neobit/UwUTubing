# Libraries / Bibliotecas -----------------------------

from tkinter import messagebox, Listbox, Scrollbar
from tkinter import filedialog
from tkinter import *
import tkinter

from moviepy.video.io.VideoFileClip import VideoFileClip, AudioFileClip
from pytube import YouTube
from PIL import Image, ImageTk
import threading

import re
import codecs
import sys
import os
import unicodedata

# Variables / Variáveis -------------------------------------------

app = tkinter.Tk() # Cria o objeto app do qual tem a tela do programa e todas as funcionalidades.
video_Link = StringVar() 
download_Path = StringVar()
streamProgress = 0
lock = threading.Lock()
shared_index = 0
downloadNames = []

# Window Layout Configuration / Configuração da Janela --------------------------------

app.wm_iconbitmap('logo.ico')
app.geometry("1000x500") 
app.resizable(False, False) 
app.title("UwUTuber - Kawaidesu youtube UwUloader") 
app.config(background="#ffffff")

# Window Layout Configuration / Configuração da Janela --------------------------------

photo = Image.open("logo.png")
test = ImageTk.PhotoImage(photo)
label1 = tkinter.Label(image=test, bg='#ffffff')
label1.place(x=80,y=34,width=377,height=266)

link_label = Label(master=app, text="YouTube link", bg='#ffffff') 
link_label.grid(row=1, column=0, pady=5, padx=5)
link_label.place(x=110,y=300,width=312,height=30)
link_label["justify"] = "center"

linkText = Entry(master=app, width=255, textvariable=video_Link) 
linkText.grid(row=1, column=1, pady=5, padx=5, columnspan = 2)
linkText['borderwidth'] = '1px'
linkText["justify"] = "center"
linkText.place(x=60,y=330,width=410,height=34)

destination_label = Label(master=app, text="Destination", bg='#ffffff') 
destination_label.grid(row=2, column=0, pady=5, padx=5)
destination_label["justify"] = "left"
destination_label.place(x=45,y=380,width=100,height=30)

destinationText = Entry(master=app, width=145, textvariable=download_Path) 
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
    # ToggleDownload('disabled')
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
    NoNormalizedName = YouTube(video_Link.get()).title
    NormalizedName = re.sub(r'[^\w\s]', '' ,unicodedata.normalize('NFKD', NoNormalizedName).encode('ASCII', 'ignore').decode('ASCII'))
    downloadNames.append(NormalizedName)    
    thread.daemon = True
    thread.start()

def download_video(index, url, path):
    global shared_index
    shared_index = index
    yt = YouTube(url, on_progress_callback=update_progress, on_complete_callback=CheckboxVerification)
    stream = yt.streams.get_highest_resolution()
    stream.download(output_path=path, filename="{}.mp4".format(downloadNames[shared_index]))

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
    audio = AudioFileClip(path)
    mp3_path = path.replace(".mp4", ".mp3")
    audio.write_audiofile(mp3_path, codec='libmp3lame')
    DeleteOldMp4(path)

browse_B = Button(master=app, text="Browse", command=Browse, width=10) 
browse_B.grid(row=2, column=2, pady=1, padx=1)
browse_B.place(x=390,y=380,width=71,height=30)

var_mp3 = tkinter.StringVar()
var_mp4 = tkinter.StringVar()
var_mp4.set("on")
var_mp3.set("off")

def on_click_mp4():
    if var_mp4.get() == "on":
        var_mp3.set("off")

def on_click_mp3():
    if var_mp3.get() == "on":
        var_mp4.set("off")

mp3_checkbox = Checkbutton(master=app, text="MP4", command=on_click_mp4, variable=var_mp4, onvalue="on", offvalue="off", bg='#ffffff')
mp3_checkbox.grid(row=3, column=1, pady=3, padx=3)
mp3_checkbox.place(x=60,y=420,width=65,height=25)

mp4_checkbox = Checkbutton(master=app, text="MP3", command=on_click_mp3, variable=var_mp3, onvalue="on", offvalue="off", bg='#ffffff')
mp4_checkbox.grid(row=3, column=1, pady=3, padx=3)
mp4_checkbox.place(x=128,y=420,width=65,height=25)

Download_B = Button(master=app, text="Download", command=ThreadDownload, width=20) 
Download_B.grid(row=3, column=1, pady=3, padx=3)
Download_B.place(x=200,y=420,width=131,height=30)

app.mainloop()
