""" from https://www.geeksforgeeks.org/convert-text-and-text-file-to-pdf-using-python/"""
# Python program to create a pdf file
  
  
from fpdf import FPDF
import os
import re
import csv

prefix = r"\\...Staging\..." #enter folder name #honestly I could regenerate for the main server instead of copying... see last line
suffix = r"\2023\Videos"

dict1 = {}
with open("...titles.tsv", newline="") as csvfile:#enter filename
    readthing = csv.reader(csvfile, delimiter="\t")
    for index,row in enumerate(readthing):
        if index>0:
            print("...title: "+str(index)+"out of ??")#enter folder name and total if desired
            print(row[1]+" -> "+row[2])
            dict1[row[1]]=row[2]
dict2 = {}
with open("...titles.tsv", newline="") as csvfile:#enter filename
    readthing = csv.reader(csvfile, delimiter="\t")
    for index,row in enumerate(readthing):
        if index>0:
            print("...title: "+str(index)+"out of ??")#enter folder name and total if desired
            print(row[1]+" -> "+row[2])
            dict2[row[1]]=row[2]

dicts={r"\...": dict1, r"\...": dict2}#enter folder names

for course in [r"\...",r"\..."]:#enter folder names
    with os.scandir(prefix + course + suffix + r"\Transcripts") as it:
        for entry in it:
            if entry.name.endswith(".txt"):# and not(entry.name.endswith("links.txt")):#this is just to skip links
                txt_file_name = entry.path
                #pdf_name =  re.sub(r'.txt$', '_transcript.pdf', txt_file_name)
                pdf_name =  re.sub(r'.txt$', '.pdf', txt_file_name)
                cut_name = re.split("_",entry.name[:-4])[-1]
                print(cut_name)#debug
                try:
                    lesson_name=(dicts[course])[cut_name]
                except KeyError:
                    print("ERROR! "+course+": "+cut_name)
                    lesson_name=re.sub("([a-z])([A-Z])","\g<1> \g<2>",cut_name)#https://stackoverflow.com/a/5020947/
                #lesson_name=cut_name[0]+"-"+"-".join(cut_name[2:])
                print(lesson_name)#debug
                pdf = FPDF(format = "Letter")
                pdf.add_font('verdana', '', r"...\verdana.ttf", uni=True)#enter folder name
                pdf.add_font('verdanab', '', r"...\verdanab.ttf", uni=True)#enter folder name
                pdf.add_font('calibri', '', r"...\calibri.ttf", uni=True)#enter folder name
                pdf.add_page()
                pdf.set_font("verdana", size = 16)
                pdf.cell(200, 10, txt = "Transcript:", ln = 1, align = 'C')
                pdf.set_font("verdanab", size = 20)
                pdf.cell(200, 10, txt = lesson_name, ln = 2, align = 'C') 
                pdf.set_font("calibri", size = 12)
                #pdf.cell(200, 10, txt = "test", ln = 2)
                with open(txt_file_name, "r", encoding="utf-8") as f: #I manually modified [a file] to avoid weird 1/3 characters this encoding wasn't working for.
                    for x in f.read().splitlines():
                        #If the line is too long, like more than 120, split it at the middle space and hope it's not twice too long.
                        #That's a reasonable assumption because our professionally made captions rarely top 80 characters.
                        #[One particular file] gets really close, suggesting 120 is high, but I think this is good enough.
                        if len(x)<115:
                            pdf.cell(200, 10, txt = x, ln = 1)
                        else:
                            chunx=x.split(" ")
                            x1=" ".join(chunx[:len(chunx)//2])
                            x2=" ".join(chunx[len(chunx)//2:])
                            print(x1)#debug
                            pdf.cell(200, 10, txt = x1, ln = 1)
                            print(x2)#debug
                            pdf.cell(200, 10, txt = x2, ln = 1)
                pdf.output(pdf_name)
                pdf.output(re.sub(r'...Staging', '...', pdf_name))#enter folder names
