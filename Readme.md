# Motivation

At work I regularly need to share files with others over time through email. This happens a lot with pdfs and zipped files that are generated outputs of design documents. To help the recipients distinguish between a version of a file I sent last week vs today I often modify prepend the file name with the date. For example, the document `schematic.pdf` becomes `210521 schematic.pdf`. And if I'm sending a second update for the day it'll be `210521b schematic.pdf`. Oh man, what a pain that is to manually do.

# Description of program

This program automates this process. 

## Example inputs and resulting outputs

Assuming today is May 21st, 2021

* `schematic.pdf` -> `210521 schematic.pdf`
* `210521 schematic.pdf` -> `210521b schematic.pdf`
* `210521b schematic.pdf` -> `210521c schematic.pdf`
* `200521 schematic.pdf` -> prompt to confirm you want to reversion. If yes the result is `210521 schematic.pdf`. If no the file is unchanged
* `200521q schematic.pdf` -> prompt to confirm you want to reversion. If yes the result is `210521 schematic.pdf`. If no the file is unchanged

The last two items with prompts are cases that I don't see myself encountering, I don't revision already visioned files but I included them for the sake of completeness. They definitely break cross-platform compatibility.

## Note

It's probably important to note at this point that this program is written for a windows machine. I think at least os.rename works regardless of os and of course the commented out win32api stuff doesn't but otherwise idk.

# Installation

1. Pull git repo or download file to a directory.
1. Open regedit
1. Under HKEY_CLASSES_ROOT/*/shell add a key and name it something descriptive such as VersionFile. 
1. Enter the text you'd like to see in the right click context menu in the (Default) key value
1. Create a key under the key you just created and name it command
1. Change the (Default) key value to `PATH_TO_PYTHON\python.exe "PATH_TO_PROGRAM\version-file.py" "%1"`

This adds the option to the context menu for files. If you'd like to have the same option for directories follow the same process for HKEY_CLASSES_ROOT/Directory/shell.

# Known corner cases/bugs

If there are two files: `210521 schematic.pdf` and `200521 schematic.pdf` and you attempt to version the 200521 file it will prompt you to confirm you want to rename the file to `210521 schematic.pdf`. If you say yes nothing will happen and you won't be informed. I'm ok with this.

Should 26 versions of a file be generated in a single day and you get all the way up to `210521z schematic.pdf`, the next version will be `210521{ schematic.pdf`. The version after that will be `210521 210521{ schematic.pdf` because of the way the regular expressions work.

If your file happens to have six digits and a space at the beginning of the filename for whatever reason, the program has no way of knowing it's not an already versioned file. The most likely outcome is the prompt the the file is versioned at a different date and asking if you want to change it to the current date.