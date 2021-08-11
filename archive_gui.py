# Extracts a zip archive while converting file names from Shift-JIS encoding to UTF-8.
#
# Will open three dialogs sequentially.
# First dialog to select the zip file.
# Second dialog for entering the password (optionally).
# Third dialog to select save location of extracted zip.

import zipfile
import sys
import os
import codecs

import tkinter as tk
import tkinter.filedialog as fd
import tkinter.simpledialog as sd

file_path_string = fd.askopenfilename(title='Select zip file.', filetypes=[
                                     ('ZIP file', '.zip'),
                                     ])

password_string = sd.askstring(title='Password',
                               prompt='Password (leave blank if not password protected):')

save_directory_string = fd.askdirectory(title='Save location.')

if any([len(file_path_string) < 1, file_path_string is None, len(save_directory_string) < 1, save_directory_string is None]):
    exit(1)

name = file_path_string

if len(password_string) > 0:
    password = password_string
else:
    password = None

directory = os.path.splitext(os.path.basename(name))[0]

print(directory)

if not os.path.exists(os.path.join(save_directory_string, directory)):
    os.makedirs(os.path.join(save_directory_string, directory))
    directory = os.path.join(save_directory_string, directory)

with zipfile.ZipFile(name, 'r') as z:
    if password:
        z.setpassword(password.encode('cp850','replace'))
    for f in z.infolist():
        bad_filename = f.filename
        if bytes != str:
            # Python 3 - decode filename into bytes
            # assume CP437 - these zip files were from Windows anyway
            bad_filename = bytes(bad_filename, 'cp437')
        try:
            uf = codecs.decode(bad_filename, 'sjis')
        except:
            uf = codecs.decode(bad_filename, 'shift_jisx0213')
        # need to print repr in Python 2 as we may encounter UnicodeEncodeError
        # when printing to a Windows console
        print(repr(uf))
        filename=os.path.join(directory, uf)
        # create directories if necessary
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        # don't try to write to directories
        if not filename.endswith('/'):
            with open(filename, 'wb') as dest:
                dest.write(z.read(f))
