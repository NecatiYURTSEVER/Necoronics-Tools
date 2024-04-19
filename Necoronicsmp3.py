import tkinter as tk
from tkinter import filedialog
from pytube import YouTube
from moviepy.editor import *
import os

# Değişkenler
kaydetme_yolu = None
def mp3_indir():
    global kaydetme_yolu  
    if not kaydetme_yolu:  
        konum_sec()  
    try:
        video_url = url_girdisi.get()
        yt = YouTube(video_url)
        video = yt.streams.get_highest_resolution()

        video_path = video.download(output_path=kaydetme_yolu)  
        video_title = yt.title 
        mp3_dosya = os.path.join(kaydetme_yolu, f"{video_title}.mp3") 

        if os.path.exists(mp3_dosya):
            dosya_adi, dosya_uzantisi = os.path.splitext(mp3_dosya)
            sira_numarasi = 1
            while os.path.exists(f"{dosya_adi} ({sira_numarasi}){dosya_uzantisi}"):
                sira_numarasi += 1
            mp3_dosya = f"{dosya_adi} ({sira_numarasi}){dosya_uzantisi}"

        video = VideoFileClip(video_path)
        video.audio.write_audiofile(mp3_dosya)
        video.close()
        os.remove(video_path)
        sonuc_etiketi.config(text=f"MP3 dosyası '{os.path.basename(mp3_dosya)}' başarıyla oluşturuldu!")
    except Exception as e:
        sonuc_etiketi.config(text=f"Hata: {str(e)}")

def konum_sec():
    global kaydetme_yolu
    kaydetme_yolu = filedialog.askdirectory()
    if not kaydetme_yolu:
        return
    konum_etiketi.config(text=f"Kaydedilecek konum: {kaydetme_yolu}")

def video_indir():
    global kaydetme_yolu
    if not kaydetme_yolu:
        konum_sec()
    try:
        video_url = url_girdisi.get()
        yt = YouTube(video_url)
        quality = kalite_secim.get() 
        video = yt.streams.filter(progressive=True, file_extension='mp4', res=quality).first()

        if video:
            video_path = os.path.join(kaydetme_yolu, video.default_filename)
            if os.path.exists(video_path): 
                dosya_adi, dosya_uzantisi = os.path.splitext(video_path)
                sira_numarasi = 1
                while os.path.exists(f"{dosya_adi} ({sira_numarasi}){dosya_uzantisi}"):
                    sira_numarasi += 1
                video_path = f"{dosya_adi} ({sira_numarasi}){dosya_uzantisi}"
            video.download(output_path=kaydetme_yolu)
            sonuc_etiketi.config(text=f"Video dosyası '{os.path.basename(video_path)}' başarıyla indirildi!")
        else:
            sonuc_etiketi.config(text="Video bulunamadı.")
    except Exception as e:
        sonuc_etiketi.config(text=f"Hata: {str(e)}")

pencere = tk.Tk()
pencere.title("Necoronics MP3-MP4")
pencere.iconbitmap("neco.ico")

url_etiketi = tk.Label(pencere, text="YouTube Video URL'si:")
url_etiketi.grid(row=0, column=0, sticky="w")

url_girdisi = tk.Entry(pencere, width=50)
url_girdisi.grid(row=0, column=1)

kalite_etiketi = tk.Label(pencere, text="Video Kalitesi:")
kalite_etiketi.grid(row=1, column=0, sticky="w")

kalite_secim = tk.StringVar(pencere)
kalite_secim.set("720p") 
kalite_secim_menu = tk.OptionMenu(pencere, kalite_secim, "360p", "480p", "720p", "1080p")
kalite_secim_menu.grid(row=1, column=1, sticky="w")

mp3_indir_dugmesi = tk.Button(pencere, text="MP3 Olarak İndir", command=mp3_indir)
mp3_indir_dugmesi.grid(row=2, column=0, columnspan=2, pady=5)

video_indir_dugmesi = tk.Button(pencere, text="Video Olarak İndir", command=video_indir)
video_indir_dugmesi.grid(row=3, column=0, columnspan=2, pady=5)

konum_sec_dugmesi = tk.Button(pencere, text="Kaydetme Konumu Seç", command=konum_sec)
konum_sec_dugmesi.grid(row=4, column=0, columnspan=2, pady=5)

konum_etiketi = tk.Label(pencere, text="")
konum_etiketi.grid(row=5, column=0, columnspan=2)

sonuc_etiketi = tk.Label(pencere, text="")
sonuc_etiketi.grid(row=6, column=0, columnspan=2)

pencere.mainloop()
