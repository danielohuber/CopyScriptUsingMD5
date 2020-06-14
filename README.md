# CopyScriptUsingMD5
Python CopyScriptUsingMD5

link to xkmd picture says it all : https://xkcd.com/1360/

![old_files](https://user-images.githubusercontent.com/65910113/83727659-b5b95e00-a645-11ea-8d16-3f27bb6531bb.png)

script to copy all files from (root) folder, with all subfolders, with extension to a single destination directory. 
Using MD5 hash checksum, to verify content not already there. (duplicate.)

created to have all my old backups, finally merged together.

extension with case sensitvity & multiple extensions searchable.

pre-check filename on destination forlder, before copying. (race issue though still possible.)
Note to self : CombinefilenamewithMD5

output needs to be re-written for race conditions. 

Checked The weekend log - lot of issues still :(
