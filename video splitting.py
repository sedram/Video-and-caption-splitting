from moviepy.editor import VideoFileClip
def getsec(timestr):
    if timestr=="end":
        return None
    substrings=timestr.split(":")
    return int(substrings[0])*60+int(substrings[1])#this works whether or not :00 at end
def foldconv(str):
    return ("\\\\...Staging"+str.split("....edu")[1]).replace("/","\\")#fill in full paths
import csv
with open("....tsv", newline="") as csvfile:#fill in filename
    readthing = csv.reader(csvfile, delimiter="\t")
    for index,row in enumerate(readthing):
        if index>??: #fill in with number to start from
            print("LIN: "+str(index)+" out of ??")#fill in with total expected
            with VideoFileClip(row[1]) as clip:
                #print(row[1])
                with clip.subclip(getsec(row[4]),getsec(row[5])) as subclip:
                    #print(getsec(row[4]),getsec(row[5]))
                    #print(foldconv(row[6])+"\\"+row[9]+".mp4")
                    subclip.write_videofile(foldconv(row[6])+"\\"+row[9]+".mp4")
