from errbot import BotPlugin, botcmd, arg_botcmd
from simple_salesforce import Salesforce


class SFDC(BotPlugin):
    
    def activate(self):
        """
        Triggers a plugin activation
        """

        super(SFDC, self).activate()
        self.log.info('booting Salesforce')
    
    def get_configuration_template(self):
        """
        Defines the configuration structure this plugin supports
        """
        return {'username': None,
                'password': None,
                'security_token': None
                }

    def get_salesforce(self):
        """
        Get an instance of Salesforce.
        Username, password and security come from self.config
        :return a `Salesforce` instance
        """

        sf = Salesforce(username=self.config['username'],
                        password=self.config['password'], 
                        security_token=self.config['security_token'])
        return sf

    @botcmd  
    def contact(self, msg, args):
        """
        This command retrieves a Salesforce Contact given its Name
        :return Name, Email and Phone number of the Contact
        """

        sfdc_api = self.get_salesforce()

        query = sfdc_api.query("SELECT Id, Email, Phone, Name " 
                               "FROM Contact " 
                               "WHERE Name = '{}'".format(args))

        records = query['records']
        name = records[0]['Name']
        email = records[0]['Email']
        phone = records[0]['Phone']

        return 'Here {} email address {} \n and here the phone {}'.format(name, email, phone)

    @arg_botcmd('lastname', type=str)
    @arg_botcmd('-ph', '--phone', dest='phone', type=str)
    @arg_botcmd('-em', '--email', dest='email', type=str)
    def create(self, msg, lastname=None, phone=None, email=None):
        """
        This command create a new Salesforce Contact with a give LastName,
        Phone and Email address
        """

        sfdc_api = self.get_salesforce()

        newcontact = sfdc_api.Contact.create({'LastName': lastname, 
                                              'Phone': phone, 
                                              'Email': email})

        return 'New Contact created Id: {}'.format(newcontact['id'])
