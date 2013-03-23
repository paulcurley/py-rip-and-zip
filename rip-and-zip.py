import os, glob, urllib, sys, shutil, zipfile

url = "http://urlgoeshere/" #local url
search_ext = "*.php*" #search extension
from_ext = ".php" 
to_ext = ".html" #save files with what extension
localpath = "/working_path/" #where you run the file from
destination = "/path_to_destination_output/" #where to save
IGNORE_PATTERNS = ('*.php', '*.py','includes','build','.svn')

def save(path):
	if not os.path.exists(destination):
	    os.makedirs(destination)
	file_list = glob.glob(search_ext)
	print file_list
	for fi in file_list:
		if fi != '*.py':
			page = urllib.urlopen(url + str(fi))
			data = page.read()
			newfilename = fi.replace(from_ext, to_ext)
			n = open(str(path+newfilename), "w")
			n.write(data.replace('\r', '').replace(from_ext, to_ext))
			page.close()
			n.close()
			
			
			
		
def copyTree(localpath, destination):
	if os.path.exists(destination):
	    shutil.rmtree(destination)
	shutil.copytree(localpath, destination, ignore=shutil.ignore_patterns('*.php', '*.py','includes','build','.svn', '*.zip'))

	
	
def ZipDir(inputDir, outputZip):
    '''Zip up a directory and preserve symlinks and empty directories'''
    zipOut = zipfile.ZipFile(outputZip, 'w', compression=zipfile.ZIP_DEFLATED)

    rootLen = len(os.path.dirname(inputDir))
    def _ArchiveDirectory(parentDirectory):
        contents = os.listdir(parentDirectory)
        #store empty directories
        if not contents:
            archiveRoot = parentDirectory[rootLen:].replace('\\', '/').lstrip('/')
            zipInfo = zipfile.ZipInfo(archiveRoot+'/')
            zipOut.writestr(zipInfo, '')
        for item in contents:
            fullPath = os.path.join(parentDirectory, item)
            if os.path.isdir(fullPath) and not os.path.islink(fullPath):
                _ArchiveDirectory(fullPath)
            else:
                archiveRoot = fullPath[rootLen:].replace('\\', '/').lstrip('/')
                if os.path.islink(fullPath):
                    zipInfo = zipfile.ZipInfo(archiveRoot)
                    zipInfo.create_system = 3
                    zipInfo.external_attr = 2716663808L
                    zipOut.writestr(zipInfo, os.readlink(fullPath))
                else:
                    zipOut.write(fullPath, archiveRoot, zipfile.ZIP_DEFLATED)
    _ArchiveDirectory(inputDir)
    shutil.rmtree(destination)
    zipOut.close()


copyTree(localpath, destination);
save(destination);
ZipDir(destination, localpath+'build.zip')


