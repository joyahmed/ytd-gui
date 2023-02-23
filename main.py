from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Progressbar
import pyperclip
from pytube import Playlist
from tqdm import tqdm

root = Tk()
root.geometry('400x250')
root.title('JYTD- Playlist Downloader')

link_label = Label(root, text='Enter Playlist URL:')
link_label.pack()

link_entry = Entry(root, width=50)
link_entry.pack()

# Automatically paste URL from clipboard
clipboard_text = pyperclip.paste()
if clipboard_text.startswith('https://www.youtube.com/playlist?list='):
    link_entry.insert(0, clipboard_text)

path_label = Label(root, text='Select save path:')
path_label.pack()

def choose_path():
    path = filedialog.askdirectory()
    path_entry.delete(0, END)
    path_entry.insert(0, path)

path_button = Button(root, text='Choose folder', command=choose_path)
path_button.pack()

path_entry = Entry(root, width=50)
path_entry.pack()

progress_bar = Progressbar(root, orient=HORIZONTAL, length=200, mode='determinate')
progress_bar.pack(pady=10)

def download():
    link = link_entry.get()
    path = path_entry.get()

    playlist = Playlist(link)

    for i, video in tqdm(enumerate(playlist.videos), total=len(playlist)):
        video_title = video.title
        filename = f'{i+1:02d}. {video_title}.mp4'
        video.streams.get_highest_resolution().download(path, filename_prefix='downloading: ', filename=filename)
        print('Video downloaded: ', filename)
        progress_bar['value'] = (i+1) * 100 // len(playlist)
        progress_bar.update()

    download_label.config(text='All videos are downloaded')

download_button = Button(root, text='Download', command=download)
download_button.pack()

download_label = Label(root, text='')
download_label.pack()

root.mainloop()