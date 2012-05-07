from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail
from hopscotch.dram.documents import User

class Command(BaseCommand):
    args = 'username password email'
    help = 'Create a user and send an email.'

    def handle(self, *args, **options):
        if len(args) < 3:
            raise CommandError('Not enough arguments. You passed %s' % args.__str__())
        
        username = args[0]
        password = args[1]
        email = args[2]
        
        User.create_user(username, password, email)

        user = User.objects.get(username=username)

        user.first_name = email

        user.save()
        
        send_mail('Your hpsct.ch Beta invite', 
            'Welcome to the hpsct.ch beta\n\n\
            Your username is %s\n\n\n\
            Your password is the same as your username.  You can change it after you login.\n\n\
            Follow us on twitter: twitter.com/hpsct_ch\n\
            '% username, 
            'accounts@hpsct.ch',
            [email], 
            fail_silently=False)