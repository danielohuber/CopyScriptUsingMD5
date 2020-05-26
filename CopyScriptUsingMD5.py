import os, sys
import shutil
import hashlib

dir_src = ("C:/Users/xxxxx/temp_input_folder/")
dir_dest = ("C:/Users/xxxxxx/temp_output_folder/")
extension = ("txt")
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
            # alleen uitvoeren als files een bepaalde extensie hebben.
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
                        shutil.copy( path, dir_dest)                        
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