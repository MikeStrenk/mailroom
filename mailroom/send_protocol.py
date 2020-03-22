import logging
import sys

import datetime as dt
from jinja2 import Template
import os

###################################################
# Email related imports
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from exchangelib import Account, Credentials, ServiceAccount, \
    HTMLBody, DELEGATE, Configuration, Message, FileAttachment
###################################################
# Setting up the Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch = logging.StreamHandler(sys.stdout)
ch.setFormatter(format)
logger.addHandler(ch)


def send_smtp(self, attachment=None):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = self.subject
    msg['To'] = self.to_field
    msg['From'] = self.from_field

    logger.debug(print(
        'the html_body is a ' + type(self.html_body) + ' datatype.'
        )

    part2 = MIMEText(self.html_body, 'html')
    msg.attach(part2)

    try:
        mail = smtplib.SMTP('smtp.gmail.com', 587)
        mail.ehlo()
        mail.starttls()

        mail.login(self.secrets['username'], self.secrets['password'])
        mail.sendmail(self.from_address, self.from_address,
                        msg.as_string())
        mail.quit()
        logger.info(f'\n--> Email sent with subject: "{self.subject}"\n')

    except:
        logger.error('Failed to connect to smtp server')

def send_exchange(self, attachment=None):
    '''
    Authenticates with exchave server and sends an email
    '''
    self.connect_to_exchange()

    m = Message(
        account=self.ews_account,
        subject=self.subject,
        body=HTMLBody(self.template.render(
            subject=self.subject, body=self.html_body)),
        to_recipients=[self.to_address],
        # defaults to sending yourself an email
        cc_recipients=[''],
        # bcc_recipients=[],
    )

    if type(attachment) is str:
        attachment_filepath = os.path.join(
            os.getcwd(), attachment)
        with open(attachment_filepath, 'rb') as f:
            binary_file_content = f.read()

        logger.info(f'Attaching {attachment} to the report')
        m.attach(FileAttachment(name=attachment,
                                content=binary_file_content))

    if self.images:
        self.attach_images()

    m.send()

    logger.info(f'--> Email sent with subject: "{self.subject}"')