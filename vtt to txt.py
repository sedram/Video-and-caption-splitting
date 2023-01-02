"""
This comes from https://gist.github.com/glasslion/b2fcad16bc8a9630dbd7a945ab5ebf5e
Convert YouTube subtitles(vtt) to human readable text.
Download only subtitles from YouTube with youtube-dl:
youtube-dl  --skip-download --convert-subs vtt <video_url>
Note that default subtitle format provided by YouTube is ass, which is hard
to process with simple regex. Luckily youtube-dl can convert ass to vtt, which
is easier to process.
To conver all vtt files inside a directory:
find . -name "*.vtt" -exec python vtt2text.py {} \;
"""
#This has been modified from the original glasslion code for needed adjustments

import sys
import re
import os


def remove_tags(text):
    """
    Remove vtt markup tags
    """
    tags = [
        r'</c>',
        r'<c(\.color\w+)?>',
        r'<\d{2}:\d{2}:\d{2}\,\d{3}>',

    ]

    for pat in tags:
        text = re.sub(pat, '', text)

    # extract timestamp, only keep MM:SS
    text = re.sub(
        r'(\d{2}:\d{2})\,\d{3} --> .*', #align:start position:0%',
        r'\g<1>',
        text
    )

    text = re.sub(r'^\s+$', '', text, flags=re.MULTILINE)
    return text

def remove_header(lines):
    """
    Remove vtt file header
    """
    pos = -1
    for i in [0,1,2]:
        for mark in ('##', 'Language: en', "WEBVTT", "X-TIMESTAMP"):
            if mark in lines[i]:
                pos = i
    lines = lines[pos+1:]
    result = []
    # [particular file].vtt has extra numbers
    for line in lines:
        if not(re.match('\d+', line)):# and lines[i+1]=="\n"):
            result.append(line)
    return result


def merge_duplicates(lines):
    """
    Remove duplicated subtitles. Duplacates are always adjacent.
    """
    last_timestamp = ''
    last_cap = ''
    for line in lines:
        if line == "":
            continue
        if re.match('^\d{2}:\d{2}$', line):
            if line != last_timestamp:
                yield line
                last_timestamp = line
        else:
            if line != last_cap:
                yield line
                last_cap = line


def merge_short_lines(lines):
    buffer = ''
    for line in lines:
        if line == "" or re.match('^\d{2}:\d{2}$', line) or re.match('^\d{2}:\d{2}:\d{2}$', line):
            yield '\n' + line
            continue

        if len(line+buffer) < 80:
            buffer += ' ' + line
        else:
            yield buffer.strip()
            buffer = line
    yield buffer

def strip_empty_lines(lines):
    result = []
    for line in lines:
        #print(line[1])
        #print(re.match('\n0', line))
        if not(re.match('\n\d{2}:\d{2}.*', line)):# and lines[i+1]=="\n"):
            result.append(line)
    return result

course=r"\..."#fill in folder name
prefix = r"\\...Staging\..."#fill in folder name
suffix = r"\2023\Videos"

def main():
    counter = 0
    for entry in os.scandir(prefix + course + suffix + r"\..."):#fill in folder name
        if entry.name.endswith(".vtt"):
            counter += 1
            print(entry.name)
            ##print(entry.name, entry.path, "\n")
            vtt_file_name = entry.path#sys.argv[1]
            #txt_name =  re.sub("Captions", "Transcripts", re.sub(r'.vtt$', '.txt', vtt_file_name))
            txt_name =  re.sub(r'.vtt$', '.txt', vtt_file_name)
            #[particular file].vtt is encoded in something other than UTF-8 and breaks, so try latin
            #But then [particular file]...eng.txt breaks in it's apostrophes
            #if english:=entry.name.endswith("eng.vtt"):
            with open(vtt_file_name, encoding="utf8") as f:
                text = f.read()
            #else:
            #    with open(vtt_file_name, encoding="latin-1") as f:
            #        text = f.read()
            text = remove_tags(text)

            lines = text.splitlines()
            lines = lines[1:]# to strip the initial "1"
            lines = remove_header(lines)
            lines = merge_duplicates(lines)
            lines = list(lines)
            lines = merge_short_lines(lines)
            lines = strip_empty_lines(lines)
            #lines = list(lines)
            #if english:
            with open(txt_name, 'w', encoding="utf8") as f:
                for line in lines:
                    f.write(line)
                    f.write("\n")
            #else:
            #    with open(txt_name, 'w', encoding="latin-1") as f:
            #        for line in lines:
            #            f.write(line)
            #            f.write("\n")
    print(counter)#debug
    
if __name__ == "__main__":
    main()
