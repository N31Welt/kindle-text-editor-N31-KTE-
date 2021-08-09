#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys, os
from subprocess import call as subprocess_call
from smtplib import SMTP as smtplib_SMTP
from urlparse import urlparse as urlprs_urlparse
from email.mime.text import MIMEText
from urllib import urlretrieve

reload(sys)
try:sys.setdefaultencoding('utf-8')
except:pass
sys.setcheckinterval(1287)

class N31KTE_EMAIL():
    __slots__ = ('prj_pth', 'message', 'empfanger', 'Subject')
    def __init__(self, prj_pth, message, empfanger, Subject):
        self.prj_pth = prj_pth
        self.message = message
        self.empfanger = empfanger
        self.Subject = Subject

    def check_internet(self) :
        fnull=open(os.devnull,'w')
        if os.name.startswith('nt'):reszt=subprocess_call('ping -w 600 8.8.8.8',shell=True,stdout=fnull,stderr=fnull)
        else:reszt=subprocess_call('ping -w 2 8.8.8.8',shell=True,stdout=fnull,stderr=fnull)
        fnull.close()
        return reszt

    def send_mail_chk(self, typ):       #typ = 'mail',   typ = 'could'
        if self.check_internet() !=0 :
            print('can not connect internet,skip.')
            return -1
        email_info_pth=''.join((self.prj_pth,'cloud_lnk.ini'))      #'email_address.ini'
        # print email_info_pth
        if not os.path.isfile(email_info_pth) :
            print('can not find email config file,skip.')
            return -2
        if typ == 'mail' :
            with open(email_info_pth,'r') as rid : email_adrs_info= [x.strip('\r\n') for x in rid.readlines()][1].split('::')
            if len(email_adrs_info)<4 or not '.' in email_adrs_info[0] or not '@' in email_adrs_info[2]:
                print('email cofig file is corrupted,skip.')
                return -3
            return self.send_mail_action(email_adrs_info)
        else :
            with open(email_info_pth,'r') as rid : cloud_adrs_info= [x.strip('\r\n') for x in rid.readlines()][0]
            if not cloud_adrs_info or len(cloud_adrs_info)<5 :
                print('cloud cofig file is corrupted,skip.')
                return -3
            return self.wget_py(cloud_adrs_info,self.prj_pth)

    def send_mail_action(self, email_adrs_info):
        message=str(self.message)
        msg=MIMEText(message)
        SMTPserver=email_adrs_info[0]
        port=int(email_adrs_info[1])
        sender=email_adrs_info[2]
        password=email_adrs_info[3]
        empfanger=str(self.empfanger)
        msg['Subject']=str(self.Subject)
        msg['From']=sender
        msg['To']=empfanger
        send_flag=0
        if len(message)>0 :
            try :        #
                mailserver=smtplib_SMTP(SMTPserver,port)
                mailserver.ehlo()
                mailserver.starttls()
                mailserver.login(sender,password)
                mailserver.sendmail(sender,[empfanger],msg.as_string())
                mailserver.quit()
                mailserver.close()
                send_flag=1
            except:send_flag=0
        else:send_flag=0
        return send_flag

    def wget_py(self, url, dwn_pth):
        filename = os.path.basename(urlprs_urlparse(url).path) or 'download_file.txt'
        opt_pth = os.path.join(dwn_pth, filename)
        dwn_stat = 0
        try:
            (opt_pth, headers) = urlretrieve(url, opt_pth, None )
            dwn_stat = 1
        except:    print ("Can't download {0}".format(opt_pth))        #
        return dwn_stat