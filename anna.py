import discord,logging,re,subprocess,magic,sys,os,mci

class Anna:
    def __init__(self,client):
        self.admins = []
        self.head_admins = []
        self.email = ""
        self.password = ""
        self.client = client#discord.Client()
        self.logger = None
        read_conf(self)
        login()

    def read_conf(self):
        f = open('anna.conf')
        for line in f.readlines():
            if line.startswith('admins='):
                self.admins.extend(line[7:-1].split(','))
            elif line.startswith('head_admins'):
                self.head_admins.extend(line[12:-1].split(','))
            elif line.startswith('login='):
                login = line[6:-1].split(',')
                print(str(login))
                self.email = login[0]
                self.password = login[1]
        f.close()

    def login(self):
        self.client.login(self.email,self.password)
        if not self.client.is_logged_in:
            sys.exit(2)
    
    def set_up_logger(self):
        self.logger = logging.getLogger('discord')
        selflogger.setLevel(logging.DEBUG)
        handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
        handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        selflogger.addHandler(handler)

    def add_admins(id,user_ids):
        global admins
        flag = False
        f = open('anna.conf','a')
        for user_id in user_ids:
            if id in admins and not user_id in admins:
                f.write('admins='+user_id+'\n')
                admins.append(user_id)
                flag = True
        f.close()
        return flag

    def rm_admins(id,user_ids):
        global admins
        global head_admins
        f = open('anna.conf','r')
        lines = f.read()
        f.close()
        flag = False
        f = open('anna.conf','w')
        for user_id in user_ids:
            if id in admins and (not user_id in head_admins) and user_id in lines:
                lines = lines.replace(user_id,'')
                lines = lines.replace(',,',',')
                admins.remove(user_id)
                flag = True
        lines = lines.replace('admins=\n','')
        f.write(lines)
        f.close()
        return flag

    def fetch_card_cmd(message):
            '''sends all the cards that appear in the message to discord'''
            (img_urls,msg) = mci.image_urls(message.content)
            for url in img_urls:
                client.send_message(message.channel,url)
            (file_names,failed) = magic.get_filenames(msg)
            for file_name in file_names:
                client.send_file(message.channel, file_name)
                os.remove(file_name)
                print('done with file: ' + file_name + ' will now delete it')
            for card in failed:
                client.send_message(message.channel, 'Could not find: '+card)

    def exit_cmd(admins,message,logout_msg='killing myself, goodbye cruel world',error_msg = 'fuck off'):
        '''If the author of the message is a admin, the bot will logout of discord otherwise print error msg'''
        if str(message.author.id) in admins:
            client.send_message(message.channel,logout_msg)
            client.logout()
            return True
        else:
            client.send_message(message.channel, error_msg)
            return False

    def log_msg():
        if message.channel.is_default_channel():
            user     = message.author.name + ': '
            log_msg  = content+'\n'
            mentions = ""
            #substitute the users id for their nick in the for the log
            for usr in message.mentions:
                mentions += usr.name + ','
            log_msg  = re.sub(r'<.*>',mentions,log_msg)
            with open('main_log.log','a') as f:
                f.write(user + log_msg)
                print("logging")
                print(user + log_msg)
