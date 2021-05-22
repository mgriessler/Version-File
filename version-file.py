import sys
import os
import win32api
from datetime import date
import re

fn = sys.argv[1]                                # Get filename from argument
d = date.today().strftime("%d%m%y")             # Determine current date, if the pattern here is changed the regular expression must be changed too
head_tail = os.path.split(fn)                   # Separate file name and path

head = head_tail[0]
tail = head_tail[1]

p_ver_sub = re.compile("\d{6}[a-z]{0,1}\s")
p_sub = re.compile("\d{6}[a-z]{1}")

m_ver_sub = p_ver_sub.match(tail)
m_sub = p_sub.match(tail)

rename = 1
if m_ver_sub is not None:       # check to see if filename is versioned and/or subversioned
    if m_sub is not None:       # check to see if filename is versioned and subversioned
        sub_head = m_sub.group()[0:-1]
        if sub_head != d:
            result = win32api.MessageBox(None, "File is already versioned at a different date, are you sure you want to change the version?", "title", 1)
            if result == 1:
                tail = p_sub.sub(d, tail, count=1)
            else:
                rename = 0
        else:
            sub = m_sub.group()[-1]
            tail = p_sub.sub(d + chr(ord(sub)+1), tail, count = 1)
    else:                       # filename is versioned but not subversioned
        if m_ver_sub.group() == d + " ":   # check to see if subversion is necessary
            tail = p_ver_sub.sub(d + "b ", tail, count=1)
        else:                       # file is already versioned but at a presumably earlier date
            result = win32api.MessageBox(None, "File is already versioned at a different date, are you sure you want to change the version?", "title", 1)
            if result == 1:
                tail = p_ver_sub.sub(d + " ", tail, count=1)
            else:
                rename = 0
else:                               # filename is not versioned at all
    tail = d + " " + tail
tail = "\\" + tail

fn_new = head + tail

if rename == 1:
    os.rename(fn, fn_new)
