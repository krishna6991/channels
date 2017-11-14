from django.db import models
from django.utils.six import python_2_unicode_compatible
from channels import Group #in order to provide a possibility to send a message to all users who are in a particular room
import json
from .settings import MSG_TYPE_MESSAGE
@python_2_unicode_compatible
class Room(models.Model):
    title=models.CharField(max_length=255)
    staff_only = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    @property
    def websocket_group(self):
        return Group("room-%s" %self.id)
    def send_message(self, message, user, msg_type=MSG_TYPE_MESSAGE):
        #call a send a message to the room on behalf of a user
        final_msg = {'room': str(self.id), 'message': message, 'username': user.username, 'msg_type': msg_type}
        # Send out the message to everyone in the room
        self.websocket_group.send(
            {"text": json.dumps(final_msg)}
        )
