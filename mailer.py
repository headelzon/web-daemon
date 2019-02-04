import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate


class Mailer(object):

    def __init__(self, address, logger, subject="", text="", url="", files=None):
        if files is None:
            files = []
        self.logger = logger

        self.subject = subject
        self.address = address
        self.text = text
        self.files = files
        self.msg = MIMEMultipart()

        if not subject:
            self.subject = "Web Daemon Website Monitoring Notification"

        if not text:
            self.text = "Changes have been detected on the website you are monitoring:\n"
            self.text += url + "\n" if url else "\n"

    def _construct_message(self):
        msg = MIMEMultipart()
        msg['From'] = "web-daemon website monitoring"
        msg['To'] = self.address
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = self.subject

        msg.attach(MIMEText(self.text))

        for f in self.files or []:
            with open(f, "rb") as fil:
                part = MIMEApplication(
                    fil.read(),
                    Name=basename(f)
                )

            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
            msg.attach(part)

        return msg

    def send_mail(self):
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.starttls()
        smtp.login("webdaemon032@gmail.com", "sUjcat-2tizxe-soqput")
        msg = self._construct_message()
        smtp.sendmail(msg['From'], self.address, msg.as_string())
        smtp.close()
