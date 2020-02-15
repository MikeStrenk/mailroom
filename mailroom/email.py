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


class Email(object):
    '''
    '''

    def __init__(self, subject="Report ", secrets=None):
        self.date = dt.date.today().strftime("%m-%d-%y")
        self.html_body = ''
        self.to_field = ''
        self.from_field = ''
        self.cc_field = ''
        self.bcc_field = ''

        if type(subject) is str:
            self.subject = subject + self.date
        else:
            raise TypeError('self.subject argument not a string')

        if secrets:
            self.secrets = secrets

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


    def add_html_element(self, filepath):
        '''
        Reads .html files from a relative filepath (String)
        and returns the file.
        '''
        if type(filepath) is str:
            absolute_filepath = os.path.join(
                os.getcwd(), 'templates', filepath)
            html_file = open(absolute_filepath, 'r')
            self.html_body += html_file.read()
            html_file.close()

            logger.info(f'{filepath} has been appended to the html body')

        else:
            raise TypeError('Function argument not a string')

    def add_image(self, filepath):
        '''
        '''
        if type(filepath) is str:
            absolute_filepath = os.path.join(
                os.getcwd(), filepath)
            # with open(absolute_filepath, 'rb') as fp:
            #     img = FileAttachment(name=absolute_filepath, content=fp.read())

            self.images.append(absolute_filepath)
            self.html_body += f'''
            <table
                align="center"
                cellspacing="0"
                cellpadding="0"
                border="0"
                width="100%">
                <tr>
                    <td align="center" widthstyle="padding: 0px 0;"><td>
                        <img
                        src="cid:{filepath}"
                        alt="image"
                        border="0"
                        display: inline;"
                    />
                    </td>
                </tr>
            </table>'''

            if self.debug:
                print(f'{filepath} image has been attached to the email')

        else:
            raise TypeError('Function argument not a string')

    def add_attachment(self):
        pass

    def attach_images(self):
        for image in self.images:
            with open(image, 'rb') as fp:
                m.attach(FileAttachment(
                    name=image, content=fp.read(), is_inline=True, content_id=image))


if __name__ == '__main__':
    pass
