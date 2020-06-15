import os, sys
import shutil
import hashlib

# source directorypath of root opgeven, bijv c: or / - met r optie, ingelezen als raw string. (tbv van windows \ backslash)
dir_src = (r"C:\Users\xxxxx\temp_input_folder")
# destination directory opgeven.
dir_dest = (r"C:\Users\xxxxxx\temp_output_folder")
# extension opgeven, hoeft geen punt . te bevatten.
extension = (".txt", "jpg", "jpeg", "xls", "doc")
mydict = {}
doublefilesdict = {}

# genereer md5 hash waarde voor file in path, met gelimiteerd tot 64k buffer.
def hashfile(path, blocksize = 65536):
    afile = open(path, 'rb')
    hasher = hashlib.md5()
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()
    return hasher.hexdigest()

# controleer Destination folder op files, en plaats deze in mydict (dictionary)
def CheckDestinationFolder():
    mydict_double_destination = {}
    print( "Check Destination Folder : ", dir_dest )
    for dirName, subdirs, fileList in os.walk(dir_dest):
        print('Scanning %s...' % dirName)
        for filename in fileList:
            # alleen uitvoeren als files een bepaalde extensie hebben. .lower() voor incasesensitivity.
            if filename.endswith(extension):
                # Wat is het path, waar de file in staat, maak daar samen 1 string van.
                path = os.path.join(dirName, filename)
                # Bereken hash
                file_hash = hashfile(path)
                # voeg md5 hash waarde toe aan dictionary.
                if file_hash in mydict:
                    if file_hash in mydict_double_destination:
                        mydict_double_destination[file_hash].append(path)
                        print ( "extra!Dubbele MD5 hash gevonden, in mydict_double_destination geplaatst = ", file_hash + path )
                    else:
                        mydict_double_destination[file_hash] = [path]
                        print ( "Dubbele MD5 hash gevonden, in mydict_double_destination geplaatst = ", file_hash + path )
                else:
                    mydict[file_hash] = [path]
                    print ( "initieel laden van MD5+filename in dictionary mydict = ", file_hash + path )
    print( "================= Klaar met maken Destination Dictionary =====================" )

# controleer Source op files, en valideer deze tegen bestaande files in mydict (dictionary) en kopieer.
def CopySourceFiles():
    print( "Check Source Folder en onderliggende folders : ", dir_src )
    for dirName, subdirs, fileList in os.walk(dir_src):
        print('Scanning %s...' % dirName)
        for filename in fileList:
            # alleen uitvoeren als files een bepaalde extensie hebben.
            if filename.endswith(extension):
                # Wat is het path, waar de file in staat, maak daar samen 1 string van.
                path = os.path.join(dirName, filename)
                # Bereken hash
                file_hash = hashfile(path)
                # Als MD5 has waarde voorkomt in dictionary, plaats dan in dubbele dictionary. Anders kopieer bestand naar Destination en voeg md5 waarde toe aan dictionary.
                if file_hash in mydict:
                    if file_hash in doublefilesdict:
                        doublefilesdict[file_hash].append(path)
                        print ( "extra!Dubbele MD5 hash gevonden, in doublefilesdict geplaatst = ", file_hash + path )
                    else:
                        doublefilesdict[file_hash] = [path]
                        print ( "Dubbele MD5 hash gevonden, in doublefilesdict geplaatst = ", file_hash + path )
                else:
                    try:
                        # aanngezien shutil.copy alles overschrijft, omzichtetige loop om zelfde naam bestanden niet te overschrijven met andere content.
                        # Wat is het destination path, waar de file in gaat staan, maak daar samen 1 string van.
                        destpath = os.path.join(dir_dest, filename)  # /output/testfile
                        # lelijke opvraging, om extensie van filename te weten, en deze later te gebruiken.
                        filename, file_extension = os.path.splitext(destpath)
                        if os.path.isfile(destpath):
                            # /output/testfile  is dus aanwezig.
                            expand = 1
                            while True:
                                expand += 1
                                # Bestandsnaam, slitten en bestandnaam <expand> + .extensie toevoegen.
                                new_destpath = destpath.split(file_extension)[0] + str(expand) + file_extension
                                if os.path.isfile(new_destpath):
                                    # bestaat, bestandsnaam+1.ext ? dan opnieuw.
                                    continue
                                else:
                                    destpath = new_destpath
                                    # bestandsnaam+1.ext ? bestaat niet, of heeft zelfde MD5 waarde.
                                    break
                                
                        # os.open als extra check om geen symlinks, etc te kopieren.
                        fd = os.open(destpath, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                                # os.O_WRONLY − open for writing only
                                # os.O_CREAT − create file if it does not exist
                                # os.O_EXCL − error if create and file exists
                                # os.O_NOFOLLOW − do not follow symlinks ! eventueel aanzetten voor verder script.

                        shutil.copy( path, destpath)
                     
                    except IOError as e:
                        print("Unable to copy file. %s" % e)
                    except:
                        print("Unexpected error:", sys.exc_info())
                                            
                    print ( "Bestand gekopieerd = ", dir_dest + filename )
                    
                    # voeg MD5 waarde van gekopieerde bestand toe.
                    mydict[file_hash] = [path]
                    
                    print ( "MD5+filename ge update in dictionary mydict = ", file_hash + path )

    print( "================= Klaar met kopieren" )

print("Start Main")
if __name__ == '__main__':
    CheckDestinationFolder()
    CopySourceFiles()