import webvtt
import os

root=r"\\...\2023\Videos"#enter folder name
for entry in os.scandir(root):
    if entry.name.endswith(".srt"):
        print(entry.name)#debug
        webvtt.from_srt(root+"\\"+entry.name).save()
