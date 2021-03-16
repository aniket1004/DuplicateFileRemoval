import os;
import time;
from hashfile import *;
from MailSender import *;
from tkinter import *;


def DuplicateFileRemoval(path,mid,starttime):
	dire=os.path.abspath("MADS");
	if os.path.isdir(dire)==False:
		os.makedirs(dire);
	filename=os.path.join(dire,"Logfile%s.txt"%time.time());
	fobj=open(filename,'w');
	dup={};
	for folder,subfolder,files in os.walk(path):
		for fname in files:
			fname=os.path.join(folder,fname);
			checksum=hashfile(fname);
			if checksum in dup:
				dup[checksum].append(fname);
			else:
				dup[checksum]=[fname];
	result=list(filter(lambda x:len(x)>1,dup.values()));
	fcnt=0;
	icnt=0;
	dfile=0;
	if len(result)==0:
		fobj.write("No Duplicate files");
	else:
		fobj.write("Duplicate files are :"+"\n");
		for s in result:
			icnt=0;
			for f in s:
				fcnt+=1;	
				icnt+=1;
				if icnt>1:
					dfile+=1;
					fobj.write(f+"\n\n");
					os.remove(f);		
	fobj.close();
	body="""Hello ,Starting time of scanning: %s. Total number of files scanned: %s. Total number of duplicate files found: %s """%(starttime,fcnt,dfile);
					
	if is_connected():			
		MailSender(mid,filename,body,starttime);
			
	else:
		print ("Internet connection is off");
