import urllib.request as urllib2;
import smtplib;
import os;
import psutil;
from sys import *;
import time; 
from email import encoders;
from email.mime.text import MIMEText;
from email.mime.base import MIMEBase;
from email.mime.multipart import MIMEMultipart;



def is_connected():
	try:
		urllib2.urlopen("http://216.58.192.142",timeout=1)
		return True;
	except urllib2.URLError as err:
		return False;
def MailSender(mid,filename,body,time):
	try:
		fromaddr="aniketdhole1004@gmail.com";
		toaddr=mid;

		msg=MIMEMultipart();
		
		msg['From']=fromaddr;
		msg['To']=toaddr;
		
		
		Subject="""Remove Duplicate file and  log of that work generated at :%s"""%(time);

		msg['Subject']=Subject;
		
		msg.attach(MIMEText(body,'plain'));
		
		attachment=open(filename,"rb");

		p=MIMEBase('application','octet-stream');

		p.set_payload((attachment).read());

		encoders.encode_base64(p);

		p.add_header('Content-Disposition',"attachment;filename=%s"%filename);
	
		msg.attach(p);
	
		s=smtplib.SMTP('smtp.gmail.com',587)

		s.starttls();
		
		s.login(fromaddr,"Maharaj7");
		
		text=msg.as_string();
			
		s.sendmail(fromaddr,toaddr,text);
	
		s.quit();
		print("Log file sucessfully sent through mail");
		
	except Exception as E:
		print ("Unable to send mail. ",E);		
