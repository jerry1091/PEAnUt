
import os

# import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from core import mail


def gen_password(length=8, charset="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()"):
    random_bytes = os.urandom(length)
    len_charset = len(charset)
    indices = [int(len_charset * (ord(byte) / 256.0)) for byte in random_bytes]
    return "".join([charset[index] for index in indices])


def save_picture(form_picture):
    random_hex = gen_password()
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/assets/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
#     msg.body = f'''To reset your password, visit the following link:
# {url_for('users.reset_token', token=token, _external=True)}

# If you did not make this request then simply ignore this email and no changes will be made.
# '''

    msg.body = '''To reset your password, visit the following link:
{}

If you did not make this request then simply ignore this email and no changes will be made.
'''.format({url_for('users.reset_token', token=token, _external=True)})

    mail.send(msg)
