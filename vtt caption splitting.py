import webvtt
import csv

def getsecforcap(timestr):
    if timestr=="end":
        return 60*60*3
    substrings=timestr.split(":")
    return int(substrings[0])*60+int(substrings[1])#this works whether or not :00 at end
def foldconv(str):
    return ("\\\\...Staging"+str.split("...test.edu")[1]).replace("/","\\")#fix paths


def tosec(stampstring):
    nums=stampstring.split(":")
    return int(nums[0])*60*60+int(nums[1])*60+float(nums[2])
def fromsec(flot):
    temp=int(flot)
    return str(int(temp/60/60)%60).zfill(2)+":"+str(int(temp/60)%60).zfill(2)+":"+str(temp%60).zfill(2)+"."+str(round(1000*(flot%60))%1000).zfill(3)


def vttmake(startstr,endstr,readname,writename):
    starttime=getsecforcap(startstr)#old test:    starttime=15*60+23
    endtime=getsecforcap(endstr)#old test:    endtime=22*60+int("02", base=10)
    myvtt=webvtt.read(readname)#(example.vtt')
    badindices=[]
    for index,caption in enumerate(myvtt):
        starts=tosec(caption.start)
        if starts<starttime or starts>endtime:
#            print("delete",index)
            badindices.append(index)
#        else:
#            print("keep",index)
    badindices.reverse()
    for ind in badindices:
        del myvtt.captions[ind]
    for index,caption in enumerate(myvtt):
        caption.start = fromsec(tosec(caption.start)-starttime)
        caption.end = fromsec(tosec(caption.end)-starttime)
#        print(index,caption)
    myvtt.save(writename)#("newchange.vtt")
#    print(index,caption.start,fromseconds(toseconds(caption.start)),caption.start==fromseconds(toseconds(caption.start)))



with open("....tsv", newline="") as csvfile:#input filename
    readthing = csv.reader(csvfile, delimiter="\t")
    for index,row in enumerate(readthing):
        if index>??:#input start
            print("file: "+str(index)+" out of ??")#input end
            vttmake(row[4],row[5],foldconv(row[2]),foldconv(row[7])+"\\"+row[9]+".vtt")
