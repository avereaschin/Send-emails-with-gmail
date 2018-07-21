
# coding: utf-8

# In[155]:

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from hurry.filesize import verbose 
import os 

# Change path to location of files to be attached to the email
# _PATH = ''
# os.chdir(_PATH)

def send_gmail(_login, _password, _to, _cc='', _bcc='', _subject='', _message='', _attachments=None):    
    
    """Send emails with attachments from a gmail account"""
    
    # Throw a TypeError if _to, _cc, _bcc or _attachments are not lists
    for field in (_to, _cc, _bcc):
        if field and not isinstance(field, list):
            raise TypeError('_to, _cc and _bcc should be included within separate lists')
        
    if not isinstance(_attachments, list):
        raise TypeError('_attachments should be included within a list')
    
    msg = MIMEMultipart()

    # Body of the email 
    msg['Subject'] = _subject
    msg['From'] = _login
    msg['To'] = ', '.join(_to)    
    msg['cc'] = ', '.join(_cc)
    msg['bcc'] = ', '.join(_bcc)
    
    msg.attach(MIMEText(_message))
    
    # Attachment part of the email
    if _attachments:
        
        # Check if attachment extension is blocked by gmail (see: https://support.google.com/mail/answer/6590?hl=en)
        # Throw a CustomError if blocked extension found
        blocked_ext = """.ADE, .ADP, .BAT, .CHM, .CMD, .COM, .CPL, .DLL, .DMG, .EXE, .HTA, .INS, 
        .ISP, .JAR, .JS, .JSE, .LIB, .LNK, .MDE, .MSC, .MSI, .MSP, .MST, .NSH, .PIF, .SCR, .SCT, .SHB, 
        .SYS, .VB, .VBE, .VBS, .VXD, .WSC, .WSF, .WSH, .CAB
        
        """
        
        extensions = [i.lower().strip('\n') for i in blocked_ext.split(', ')]

        for file in _attachments():
            if file.endswith(tuple(extensions)):
                raise CustomError('File {0} is blocked by gmail. Can\'t attach files with this extension'.format(file))

        # Check if attachment size is within gmail's 25mb limit. Throw a CustomError if above limit. 
        class CustomError(Exception):
            pass
                   
        _size = 0
        for file in _attachments:
            _size += os.stat(file).st_size
            if _size > 25 * 1024 ** 2:
                raise CustomError('Attachement size: {0} exceeds gmail\'s 25mb limit'.format(size(_size, system=verbose)))
                    
        # Add attachments to the email
        for file in _attachments:
            fp = open(file, 'rb')
            attachment = MIMEBase('application', 'octet-stream')
            attachment.set_payload(fp.read())
            encoders.encode_base64(attachment)
            attachment.add_header('Content-Disposition', 'attachment', filename=file)
            msg.attach(attachment)
            fp.close()

    # Connect to gmail's smtp server
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
    except:
        print('ERROR: Couldn\'t connect to the SMTP server')
            
    server.login(_login, _password)
    server.sendmail(_login, [_to, _cc, _bcc], msg.as_string())
    server.quit()

