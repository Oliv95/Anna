import discord,logging,re,subprocess,sys,os,mci,anna

exit_code = 0

def main():
    help_text = r"""
                    The following commands and features are available:

                    Echo command will echo back what you typed, example !echo hello Anna
                    Say command will display random text of the given length, example !say 5 (text will be 5 words)
                    Help command will display this help message example !help
                    About command will display uptime and a list of contributors, example !about
                    Reboot command will cause me to attempt a reboot, example !reboot
                    Exit command will cause me to become very turned off, example !exit (admins only)
                    Add command will add an admin, example !add <name> (admins only)
                    Rm command will remove an admin example !rm <name> (admins only)
                    Roll command will give back a random number between 0 and the input, example !roll 100
                    Nick command will give a magic card a nickname that it can be more easliy fetched,
                    example !nick bob->dark confidant (admins only)
                    Rm nick command will remove a card nick, example !rm nick bob (admins only)
                    List nick command will list all current card nicks, example !list nick
                    ------------------------------------------------------------------
                    You can also type the name of a magic card withing square brackets 
                    and have me fetch an image of that card, example [forest]
                    You can also use double square brackets for a search using magiccards.info syntax,
                    example [[o:flashback]],this method of searching is considerately faster.
                    See website for more info regarding syntax. 
                    -------------------------------------------------------------------
                    My source code and licence is available on github.com/Oliv95/Anna"""
    client = discord.Client()
    bot = anna.Anna(client,help_text,markov_file)

    @client.event
    def on_ready():
        print("admins are: " + str(bot.admins))
        print("head admins are: " + str(bot.head_admins))
        print("logged in as")
        print(client.user.name)
        print("id is ")
        print(client.user.id)
        print("servers connected to: " + str(client.servers))
        print('--------')

    @client.event
    def on_message(message):
        global exit_code
        bot.log_msg(message)
        if message.author.name == 'Anna':
            return
        elif '[' in message.content:
            bot.fetch_card(message)
        elif message.content.startswith('!echo'):
            bot.echo_msg(message)
        elif message.content.startswith('!list nick'):
            bot.lnick(message)
        elif message.content.startswith('!nick'):
            bot.anick(message)
        elif message.content.startswith('!rm nick'):
            bot.rnick(message)
        elif message.content.startswith('!help'):
            bot.help_msg(message)
        elif message.content.startswith('!about'):
            bot.about_msg(message)
        elif message.content.startswith('!add'):
            bot.add_admins(message)
        elif message.content.startswith('!roll'):
            bot.roll(message)
        elif message.content.startswith('!rm'):
            bot.rm_admins(message)
        elif message.content.startswith('!reboot'):
            bot.reboot(message)
            exit_code = 100
        elif message.content.startswith('!exit'):
            if bot.exit(message):
                exit_code = 1

    client.run()
    return exit_code
