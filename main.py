# Libraries / Bibliotecas -----------------------------

from pytube import YouTube 
import customtkinter
from customtkinter import *
from customtkinter import filedialog
from tkinter import messagebox
from PIL import Image

# Window Layout Configuration / Configuração da Janela --------------------------------

customtkinter.set_default_color_theme("dark-blue")
app = customtkinter.CTk()

app.geometry("600x500") 
app.resizable(False, False) 
app.title("UwUTuber - Kawaidesu youtube UwUloader") 
app.config(background="#ffffff")

   
# Variables / Variáveis -------------------------------------------

video_Link = StringVar() 
download_Path = StringVar()
streamProgress = 0   

# Program / Programa ---------------------------------------------

def Window(): 
    photo = CTkImage(Image.open("Logo.png"), size=(314, 222))
    imagem = CTkButton(master=app, image=photo, state="disabled", text='', fg_color='#ffffff')
    imagem.place(x=1,y=40,width=614,height=232)
    imagem["justify"] = "center"

    link_label = CTkLabel(master=app, text="YouTube link", fg_color='#ffffff') 
    link_label.grid(row=1, column=0, pady=5, padx=5)
    link_label.place(x=140,y=300,width=312,height=30)
    link_label["justify"] = "center"

    linkText = CTkEntry(master=app, width=255, textvariable=video_Link) 
    linkText.grid(row=1, column=1, pady=5, padx=5, columnspan = 2)
    linkText['borderwidth'] = '1px'
    linkText["justify"] = "center"
    linkText.place(x=90,y=330,width=410,height=34)

    destination_label = CTkLabel(master=app, text="Destination", fg_color='#ffffff') 
    destination_label.grid(row=2, column=0, pady=5, padx=5)
    destination_label["justify"] = "left"
    destination_label.place(x=75,y=380,width=100,height=30)

    destinationText = CTkEntry(master=app, width=145, textvariable=download_Path) 
    destinationText.grid(row=2, column=1, pady=5, padx=5)
    destinationText["justify"] = "center"
    destinationText.place(x=165,y=380,width=245,height=30)

    browse_B = CTkButton(master=app, text="Browse", command=Browse, width=10) 
    browse_B.grid(row=2, column=2, pady=1, padx=1)
    browse_B.place(x=420,y=380,width=71,height=30)
   
    Download_B = CTkButton(master=app, text="Download", command=Download, width=20) 
    Download_B.grid(row=3, column=1, pady=3, padx=3)
    Download_B.place(x=230,y=420,width=131,height=30) 
  
  
def Browse(): 
    download_Directory = filedialog.askdirectory(initialdir="Directory Path") 
    download_Path.set(download_Directory) 

def Download(): 
    def downloadCompleted(x,y):
        messagebox.showinfo("Uwu!! That's was successful! ",f"Your video has finished downloading!! \(>__<)/\nI saved it in the following directory:\n{download_Folder}")
    Youtube_link = video_Link.get() 
    download_Folder = download_Path.get() 
    getVideo = YouTube(Youtube_link, on_complete_callback=downloadCompleted)
    getVideo.streams.get_highest_resolution().download(download_Folder)


Window()
app.mainloop()
