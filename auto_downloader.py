#Currently only works with 2014-2015 open evidence website!
#Written By Delan Huang
#Written 7/30/2014
def downloadFiles(url, extension):
    import requests
    from bs4 import BeautifulSoup

    #url = str(raw_input("Enter the url here: "))
    #extension = str(raw_input("Enter the extension of the file type you wsh to download (.docx): "))

    camps = ['Baylor', 'Berkeley', 'CDL', 'DDI', 'DDIx', 'Emory', 'Georgetown', 'Georgia', 'GMU','Gonzaga', 'Harvard', 
            'HSS','JDI','Michigan7', 'MichiganClassic', 'SDI', 'MNDI', 'Samford', 'UTD', 'Wake'
            'MSDI', 'MoneyGram', 'NAUDL', 'UNT', 'Northwestern', 'UTNIF', 'WSDI']

    r = requests.get(url,stream=True)
    data = r.text
    soup = BeautifulSoup(data)
    for link in soup.find_all('a'):
        if link.get('href').endswith(extension):
            file_name = link.get('href').split('/')[-1]
            #print file_name
            
            file_name_split = file_name.split()
            for elem in file_name_split:
                if elem in camps:
                    file_camp = elem + '/'
                    #print file_camp

            dude = ['http://openev.debatecoaches.org/bin/download/2015/']
            dude.append(file_camp)
            dude.append(file_name.replace(' ', '%20'))
            #print dude
            file_address = ''.join(dude)
            #print file_address

            with open(file_name, 'wb') as f:
                response = requests.get(file_address, stream=True)
                for block in response.iter_content(1024):
                    if not block:
                        break
                    f.write(block)
                                             

def setupDirectory(dirname):
    """
    Creates and sets up a parent directory, then moves the cwd to the new parent directory.
    Removes corrupted files afterwards.
    """
    import os
    import shutil
    import sys
    
    #dirname = str(raw_input("Enter the folder name you wish to put these files in: ")

    try:
        os.chdir(dl_dir)
    except WindowsError:
        print 'Invalid directory: %s' % dl_dir
        sys.exit(0)
    
    try:
        os.mkdir(dirname) 
        os.chdir(dirname)
    except WindowsError:
        print "WARNING: There already is a folder named %s in %s" % (dirname, dl_dir)
        go_anyway = str(raw_input("Would you like to delete this folder?(Y/N): ")).upper()
        if go_anyway == 'Y':
            shutil.rmtree(dirname) 
            os.mkdir(dirname)
            os.chdir(dirname)
        else:
            os.chdir(dirname)

def removeCorruptFiles(dl_dir, dirname):
    import os

    os.chdir(os.path.join(dl_dir,dirname))
    for root, dirs, files in os.walk(os.path.join(dl_dir,dirname)):
        for corrupt_file in files:
            if os.path.getsize(corrupt_file) < 15813L:
               os.remove(corrupt_file)

dl_dir = str(raw_input("Enter the full path of where you wish to put the folder: "))    
dirname = "Open Evidence 2015-2016"
url = "http://openevidence.debatecoaches.org/bin/2015/WebHome"


setupDirectory(dirname)
downloadFiles(url, '.doc')
downloadFiles(url, '.docx')
removeCorruptFiles(dl_dir, dirname)

print "Job's done!"

#http://openev.debatecoaches.org/bin/download/2014/JDI/(de)Coloniality%20Affirmative%20-%20JDI%202014.doc
#http://old.debatecoaches.org/openev-archive/files/download/1_H0_Afghan_Nation_Building_Bad_Aff.doc
