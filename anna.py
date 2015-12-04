import discord,logging,re,subprocess,magic,sys,os,mci,markov,random,time

class Anna:
    def __init__(self,client,help_text="Help text not configured",markov_file='main_log.log'):
        self.admins = []
        self.head_admins = []
        self.email = ""
        self.password = ""
        self.help_text = help_text
        self.client = client#discord.Client()
        self.logger = None
        self.nick_dic = None
        self.read_conf()
        self.textGen = markov.Markov(open(markov_file))
        self.login()
        self.start_time = time.time()

    def is_admin(self,message):
        if not str(message.author.id) in self.admins:
            self.client.send_message(message.channel, 'not sufficient permissions')
            return False
        else:
            return True

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
        f = open('nicks.conf')
        self.nick_dic = {}
        for line in f.readlines():
            l = line[:-1:].split('->')
            key = l[0].strip().lower()
            value = l[1].strip()
            self.nick_dic[key] = value
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

    def add_admins(self,message):

        def add(self,me,ids):
            '''helper function'''
            flag = False
            f = open('anna.conf','a')
            for user_id in ids:
                if me in self.admins and not user_id in self.admins:
                    f.write('admins='+user_id+'\n')
                    self.admins.append(user_id)
                    flag = True
            f.close()
            return flag

        my_id = message.author.id
        to_add = message.content[4::].strip().split(',')
        ids = []
        for serv in self.client.servers:
            for user in serv.members:
                if user.name in to_add and not user.id in ids:
                    ids.append(user.id)
        if add(self,my_id,ids):
            self.client.send_message(message.channel, 'admins updated')
        else:
            self.client.send_message(message.channel, 'not sufficient permissions')


    def rm_admins(self,message):

        def rm(self,me,ids):
            '''helper function'''
            f = open('anna.conf','r')
            lines = f.read()
            f.close()
            flag = False
            f = open('anna.conf','w')
            for user_id in ids:
                if me in self.admins and (not user_id in self.head_admins) and user_id in lines:
                    lines = lines.replace(user_id,'')
                    lines = lines.replace(',,',',')
                    self.admins.remove(user_id)
                    flag = True
            lines = lines.replace('admins=\n','')
            f.write(lines)
            f.close()
            return flag

        my_id = message.author.id
        to_add = message.content[3::].strip().split(',')
        ids = []
        for serv in self.client.servers:
            for user in serv.members:
                if user.name in to_add and not user.id in ids:
                    ids.append(user.id)
        if rm(self,my_id,ids):
            self.client.send_message(message.channel, 'admins updated')
        else:
            self.client.send_message(message.channel, 'not sufficient permissions')

    def rnick(self,message):
        if self.is_admin(message):
            f = open('nicks.conf','r')
            lines = f.read()
            f.close()
            to_remove = message.content[8::].strip().split(',')
            nicks = lines.split('\n')
            f = lambda s: not any(map(s.startswith,to_remove))
            left = list(filter(f,nicks))
            res = "\n".join(left)
            f = open('nicks.conf','w')
            f.write(res)
            f.close()
            self.client.send_message(message.channel, 'reboot to have change take effect')

    def anick(self,message):
        if self.is_admin(message):
            pairs = message.content[5::].split(',')
            f = open('nicks.conf','a')
            for pair in pairs:
                f.write(pair.strip()+"\n")
            f.close()
            self.client.send_message(message.channel, 'reboot to have change take effect')

    def lnick(self,message):
        nicks = "\n".join([key + '->' + self.nick_dic[key] for key in self.nick_dic.keys()])
        self.client.send_message(message.channel, nicks)

    def fetch_card(self,message):
            '''sends all the cards that appear in the message to discord'''
            msg = message.content.lower()
            for key in self.nick_dic.keys():
                msg = msg.replace('[['+key+']]','[['+self.nick_dic[key]+']]')

            (img_urls,msg) = mci.image_urls(msg)
            for url in img_urls:
                self.client.send_message(message.channel,url)
            (file_names,failed) = magic.get_filenames(msg)
            for file_name in file_names:
                self.client.send_file(message.channel, file_name)
                os.remove(file_name)
                print('done with file: ' + file_name + ' will now delete it')
            for card in failed:
                self.client.send_message(message.channel, 'Could not find: '+card)

    def exit(self,message):
        '''If the author of the message is a admin, the bot will logout of discord otherwise print error msg'''
        if self.is_admin(message):
            self.client.send_message(message.channel,'Shutting down')
            self.client.logout()
            sys.exit(0)

    def reboot(self,message):
        self.client.send_message(message.channel,'Attempting to reboot')
        sys.exit(100)

    def echo_msg(self,message):
        self.client.send_message(message.channel, message.content[5::])

    def say(self,message):
        size = int(message.content[4::])
        text = self.textGen.generate_markov_text(size)
        self.client.send_message(message.channel, text)

    def help_msg(self,message):
        self.client.send_message(message.channel, self.help_text)

    def about_msg(self,message):
        now = time.time()
        uptime = int(now - self.start_time)
        mins = uptime // 60
        secs = uptime % 60
        text = "Contributors are Axel Olivecrona\n Current uptime is minutes {0} and seconds {1} \n".format(mins,secs)
        self.client.send_message(message.channel, text)

    def roll(self,message):
        limit = int(message.content[5::])
        error_string = "negative numbers not ok!"
        if 0 >= limit:
            self.client.send_message(message.channel,error_string)
        else:
            roll = random.randint(0,limit)
            self.client.send_message(message.channel, str(roll))

    def log_msg(self,message):
        if message.channel.is_default_channel():
            user     = message.author.name + ': '
            log_msg  = message.content+'\n'
            mentions = ""
            #substitute the users id for their nick in the for the log
            for usr in message.mentions:
                mentions += usr.name + ','
            log_msg  = re.sub(r'<.*>',mentions,log_msg)
            with open('main_log.log','a') as f:
                f.write(user + log_msg)
                print("logging")
                print(user + log_msg)

