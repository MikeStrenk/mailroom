import exchangelib
import smtplib



def exchange(email_config):
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