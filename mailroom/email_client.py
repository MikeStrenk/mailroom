import logging
import sys
import smtplib
from exchangelib import (
    Account,
    Credentials,
    ServiceAccount,
    HTMLBody,
    DELEGATE,
    Configuration,
    Message,
    FileAttachment,
)

###################################################
# Setting up the Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch = logging.StreamHandler(sys.stdout)
ch.setFormatter(format)
logger.addHandler(ch)
###################################################


def send_exchange(email_config):
    """
        Sets up the exchangelib connection to the exchange server
        """
    credentials = Credentials(
        self.email_config["username"], self.email_config["password"]
    )
    self.ews_account = Account(
        self.email_config["user_email_address"],
        credentials=credentials,
        autodiscover=True,
        access_type=DELEGATE,
    )

    ews_url = self.ews_account.protocol.service_endpoint
    ews_auth_type = self.ews_account.protocol.auth_type

    # if you need to impersonate, change from primary_account to alias_account
    primary_smtp_address = self.ews_account.primary_smtp_address

    config = Configuration(
        service_endpoint=ews_url, credentials=credentials, auth_type=ews_auth_type
    )

    a = Account(
        primary_smtp_address=primary_smtp_address,
        config=config,
        autodiscover=False,
        access_type=DELEGATE,
    )


def send_smtp(self, server, port, image=False):
    """
    """
    msg = MIMEMultipart("alternative")
    msg["Subject"] = self.subject
    msg["From"] = self.from_address
    msg["To"] = self.to_address

    # Create the body of the message (a plain-text and an HTML version).
    # Record the MIME types of both parts - text/plain and text/html.
    print(type(self.html_body))
    # part1 = MIMEText("nothing in the plain text email", 'plain')
    part2 = MIMEText(self.html_body, "html")

    msg.attach(part2)

    # This example assumes the image is in the current directory
    # if image == True:
    #     cwd = os.path.dirname(os.path.abspath(__file__))
    #     image_path = os.path.join(cwd, image)
    #     print(image_path)
    #     fp = open(image_path, 'rb')
    #     msgImage = MIMEImage(fp.read())
    #     fp.close()

    #     # Define the image's ID as referenced above
    #     msgImage.add_header('Content-ID', '<image1>')
    #     msg.attach(msgImage)

    # Send the message via local SMTP server.

    mail = smtplib.SMTP(server, port)
    mail.ehlo()
    mail.starttls()

    mail.login(username, password)
    mail.sendmail(self.from_address, self.from_address, msg.as_string())
    mail.quit()

    if self.debug:
        print(f'\n--> Email sent with subject: "{self.subject}"\n')


def send_gmail(self, email_config, image=False):
    server = "smtp.gmail.com"
    port = 587
    self.send_smtp(server=server, port=port)


def send_notification(self, text, image=False):
    notification = Email(debug=True)
    notification.subject = text
    notification.send(image)


def send_smtp(self, attachment=None, server=''):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = self.subject
    msg['To'] = self.to_field
    msg['From'] = self.from_field

    logger.debug(print('the html_body is a ' + type(self.html_body) + ' datatype.')

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
        logger.error('Failed to connect to gmail')

def send_gmail(self, email_config, server='smtp.gmail.com', port=587, image=False):
    '''Reuses the send_smtp func to add the gmail default settings'''
    self.send_smtp(server=server, port=port)


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