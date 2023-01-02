import webvtt

myvtt = webvtt.read("....vtt")#input filename
newvtt = webvtt.WebVTT()
for index,caption in enumerate(myvtt):
    if index%2==0:
        starts=caption.start
        ends=caption.end
        c1=caption.text
    else:
        newvtt.captions.append(webvtt.Caption(starts,ends,c1+"\n"+caption.text))
newvtt.save("....vtt")#input filename
