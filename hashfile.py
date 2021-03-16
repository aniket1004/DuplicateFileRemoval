import os;
import hashlib;

def hashfile (path,blocksize=1024):
	afile=open(path,'rb');
	hasher=hashlib.md5();
	buf=afile.read(blocksize);
	while len(buf)>0:
		hasher.update(buf);
		buf=afile.read(blocksize);
	afile.close();
	return hasher.hexdigest();