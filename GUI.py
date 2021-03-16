from tkinter import *;
from tkinter import messagebox;
import os;
from sys import *;
import time;
import schedule;
from MailSender import *;
import schedule; 
from hashfile import *;
import re;


window=Tk();
window.title("AUTO FILE REMOVAL AND FILE SENDER");
window.geometry("1200x700+0+0");


#Accept Folder Name
Foldername=Label(window,text='Directory name  :');
Foldername.grid(row=0);
fname=Entry(window);
fname.grid(row=0,column=1);
x=Label(window,text='(Try to give absolute path)',fg='red');
x.grid(row=0,column=2);


#Accept Time Interval
tInterval=Label(window,text='Time interval(in min)  :');
tInterval.grid(row=1);
interval=Entry(window);
interval.grid(row=1,column=1);
y=Label(window,text='(Time in minutes)',fg='red');
y.grid(row=1,column=2);


#Accept Email-id
eid=Label(window,text='Email-id  :');
eid.grid(row=2);
emailId=Entry(window);
emailId.grid(row=2,column=1);
z=Label(window,text='(Enter valid email-id)',fg='red');
z.grid(row=2,column=2);


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
					fobj.write(f+"\n\n\n");
					os.remove(f);		
	fobj.close();
	body="""Hello ,Starting time of scanning: %s. Total number of files scanned: %s. Total number of duplicate files found: %s """%(starttime,fcnt,dfile);
					
	if is_connected():			
		MailSender(mid,filename,body,starttime);		
	else:
		print ("Internet connection is off");

def execute():
	
	regex='^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$';	
	if len(fname.get())==0 and len(interval.get())==0 and len(emailId.get())==0:
		messagebox.showinfo ('Warning','All fields are mandatory');
	elif len(fname.get())==0:
		messagebox.showinfo ('Warning','Please enter directory  name');	
	elif len(interval.get())==0:
		messagebox.showinfo ('Warning','Please enter time interval of script');
	elif len(emailId.get())==0:
		messagebox.showinfo ('Warning','Please enter email-id');	
	elif not(re.search(regex,emailId.get())):
		messagebox.showinfo ('Warning','Invalid email-id');
	else:
		path=fname.get();
		if os.path.isabs(path)==False:
			path=os.path.abspath(path);
		if os.path.isdir(path)==False:
			fobj.write("Directory does not exist");
		else:
			starttime=time.ctime();

			schedule.every(int(interval.get())).minutes.do(DuplicateFileRemoval,path=path,mid=emailId.get(),starttime=starttime);
			
			while True:
				schedule.run_pending();
				time.sleep(1);
				
#Submit the information
submit=Button(window,text='SUBMIT',command=execute);
submit.grid(row=3,column=1);

#
check=Label(window,text='Check output on your command prompt(WINDOWS) or terminal(LINUX)');
check.grid(row=4);

window.mainloop();
