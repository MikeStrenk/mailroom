import logging
import sys

import datetime as dt
from jinja2 import Template
import os
# import pandas as pd
# import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from exchangelib import Account, Credentials, ServiceAccount, \
    HTMLBody, DELEGATE, Configuration, Message, FileAttachment

# from config import sender, username, password

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch = logging.StreamHandler(sys.stdout)
ch.setFormatter(format)
logger.addHandler(ch)





class EmailMessage(object):
    '''
    '''

    def __init__(self, subject, config):
        self.date = dt.date.today().strftime("%m-%d-%y")
        self.html_body = ''

        if type(subject) is str:
            self.subject = subject
        else:
            raise TypeError('self.subject argument not a string')
        
        if config:
            self.config = config


    def add_html_element(self, filepath):
        '''
        Reads .html files from a relative filepath (String) and returns the file
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
        Work In Progress
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

        def attach_images(self):
            for image in self.images:
                with open(image, 'rb') as fp:
                    m.attach(FileAttachment(
                        name=image, content=fp.read(), is_inline=True, content_id=image))
    
        def send_email(self, attachment=None):
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
    
                print(f'Attaching {attachment} to the report')
                m.attach(FileAttachment(name=attachment,
                                        content=binary_file_content))
    
            if self.images:
                self.attach_images()
    
            m.send()
    
            logger.info(f'\n--> Email sent with subject: "{self.subject}"\n')


class Alert(EmailMessage):
    '''
    '''

    def __init__(self, subject):
        EmailMessage.__init__(self, subject)
        logger.info(f'Alert Subject: "{subject}"')





class Log(object):
    '''
    Captures the starting timestamp to check how much time elapses during the scripts.
    '''

    def __init__(self, debug=False):
        self.start_time = dt.datetime.now()
        self.debug = debug

    def log_stop_time(self):
        '''
        Passes report metadata to the database. Metadata includes:
        -report subject
        -sender
        -send date
        -how long the script took to run
        '''
        self.endtime = dt.datetime.now() - self.start_time

        if self.debug:
            print(f'The script took {self.endtime.seconds} seconds to run')


class Email(object):
    '''
    Instantiates an Email body object
    '''

    def __init__(self,  email_config, debug=False):
        self.email_config = email_config
        self.debug = debug
        self.date = dt.date.today().strftime("%m-%d-%y")
        self.subject = f'Standard Report {self.date}'
        self.from_address = email_config['user_email_address']
        self.to_address = email_config['user_email_address']
        self.images = ['html_templates\\imgs\\logo.png']
        self.html_body = ''

        template_filepath = os.path.join(
            os.getcwd(), 'html_templates', 'default_report_template.html')
        html_file = open(template_filepath, 'r')
        self.template = Template(html_file.read())

        # logo_filename = 'logo.png'
        # logo_filepath = os.path.join(
        #     os.getcwd(), 'html_templates', 'imgs', logo_filename)
        # with open(logo_filepath, 'rb') as fp:
        #     self.logoimg = FileAttachment(
        #         name=logo_filename, content=fp.read(), is_inline=True, content_id=logo_filename)

        if self.debug:
            print(
                f"\n{'-'*45}\nEmail configuration profile set as {email_config['user_email_address']}")
            print(f"{'-'*45}\nSubject: {self.subject}")

    def add_html_element(self, filepath):
        '''
        Reads .html files from a relative filepath (String) and returns the file
        '''
        if type(filepath) is str:
            absolute_filepath = os.path.join(
                os.getcwd(), 'html_templates', filepath)
            html_file = open(absolute_filepath, 'r')
            self.html_body += html_file.read()
            html_file.close()

            if self.debug:
                print(f'{filepath} has been appended to the html body')

        else:
            raise TypeError('Function argument not a string')

    def add_image(self, filepath):
        '''
        Work In Progress
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

    def connect_to_exchange(self):
        '''
        Sets up the exchangelib connection to the exchange server
        '''
        credentials = Credentials(
            self.email_config['username'], self.email_config['password'])
        self.ews_account = Account(self.email_config['user_email_address'], credentials=credentials,
                                   autodiscover=True, access_type=DELEGATE)

        ews_url = self.ews_account.protocol.service_endpoint
        ews_auth_type = self.ews_account.protocol.auth_type

        # if you need to impersonate, change from primary_account to alias_account
        primary_smtp_address = self.ews_account.primary_smtp_address

        config = Configuration(service_endpoint=ews_url,
                               credentials=credentials, auth_type=ews_auth_type)

        a = Account(
            primary_smtp_address=primary_smtp_address,
            config=config, autodiscover=False,
            access_type=DELEGATE,
        )

    def attach_images(self):
        for image in self.images:
            with open(image, 'rb') as fp:
                m.attach(FileAttachment(
                    name=image, content=fp.read(), is_inline=True, content_id=image))

    def send_email(self, attachment=None):
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

            print(f'Attaching {attachment} to the report')
            m.attach(FileAttachment(name=attachment,
                                    content=binary_file_content))

        if self.images:
            self.attach_images()

        m.send()

        logger.info(f'\n--> Email sent with subject: "{self.subject}"\n')

    # def send_notification(self, text):
    #     notification = Email(self.email_config, debug=True)
    #     notification.subject = text
    #     notification.send_email()

# class Chart(name, title):
#     '''
#     '''

#     def __init__(self, name, title):
#         self.filename = name
#         # instance_var1 is a instance variable
#         self.title = title
#         # instance_var2 is a instance variable
#     xlabel = 'xlabel test'
#     ylabel = 'ylabel test'

#     def make_bar(data):
#         plt.bar(data)
#         plt.xlabel(xlabel)
#         plt.ylabel(ylabel)
#         plt.savefig(f'{filename}.png')

#         filename = f'{filename}.png'

#     def make_line( data, xlabel='', ylabel=''):
#         plt.plot(data)
#         plt.xlabel(xlabel)
#         plt.ylabel(ylabel)
#         plt.savefig(f'{filename}.png')

#         filename = f'{filename}.png'


if __name__ == '__main__':
    print("Test mode print, compose.py called directly")
    logging.info('\nCompose.py has been called directly')
    # from test_config import test_config

    # test_report = Email(email_config=test_config, debug=True)
    # test_report.send_email()
