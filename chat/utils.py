#declare decorators needed for error handling of errors occurs in future.

from functools import wraps
from .exceptions import ClientError
from .models import Room

def catch_client_error(func):
    #decorators to catch client error and translate it.
    @wraps(func)
    def inner(message, args,  **kwargs):
        try:
            return func(message, args,  **kwargs)
        except ClientError as e:
            e.send_to(message.reply_channel)
        return inner

def get_room_or_error(room_id, user):
    if not user.is_authenticated():
        raise ClientError("User has to Login")
    try:
        room = Room.objects.get(pk=room_id)
    except Room.DoesNotExist:
        raise ClientError("ROOM_INVALID")
    if room.staff_only and not user.is_staff: #check permissionss
        raise ClientError("ROOM_ACCESS_DENIED")
    return room
