# CopyScriptUsingMD5
Python CopyScriptUsingMD5

link to xkmd picture says it all : https://xkcd.com/1360/

![old_files](https://user-images.githubusercontent.com/65910113/83727659-b5b95e00-a645-11ea-8d16-3f27bb6531bb.png)

script to copy all files from (root) folder, with all subfolders, with extension to a single destination directory. 
Using MD5 hash checksum, to verify content not already there. (duplicate.)

created to have all my old backups, finally merged together.

extension with case sensitvity & multiple extensions searchable.

pre-check filename on destination. 
If file name there, create new file. example : filename(+1).txt

in comnination with raspberry pi4 , using dafvs2 mount to cloud as output.. the performance is terrible.. 
For next run, see to do a pre-check on size minimum. (thinking of files smaller then 1kb)
Still analyzing

Most likely issue is davfs2 protocol for cloud setup.. Will need to do some performance runs on python and setting up dictionaries. 

using new usb stick, first test looks much better.
Succes! Tomorrow will show results
