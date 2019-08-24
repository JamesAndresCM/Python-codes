import imaplib
import email
import re
import os

def connect(server, user, password):
    m = imaplib.IMAP4_SSL(server)
    m.login(user, password)
    m.select()
    return m

def downloaAttachmentsInEmail(m, emailid, outputdir):
    resp, data = m.fetch(emailid, "(BODY.PEEK[])")
    email_body = data[0][1]
    mail = email.message_from_string(email_body)

    emailRegex = re.search(r'[\w\.-]+@[\w\.-]+', mail['From'])
    emailFrom = emailRegex.group(0)

    if mail.get_content_maintype() != 'multipart':
        return

    for part in mail.walk():
        if part.get_content_maintype() != 'multipart' and part.get('Content-Disposition') is not None:
            print "Correo desde: " + emailFrom
            open(outputdir + '/' + part.get_filename(), 'wb').write(part.get_payload(decode=True))

def downloadAllAttachmentsInInbox(server, user, password, outputdir, new_mail=False):
    m = connect(server, user, password)
    tipo = "(ALL)"
    if new_mail:
        tipo = "(UNSEEN)"
    resp, items = m.search(None, tipo)

    items = items[0].split()
    for emailid in items:
        downloaAttachmentsInEmail(m, emailid, outputdir)

downloadAllAttachmentsInInbox('imap.gmail.com', os.getenv(EMAIL_ADDRESS), os.getenv(EMAIL_PASSWORD), os.getenv(PATH), new_mail=True)
