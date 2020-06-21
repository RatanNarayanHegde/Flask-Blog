import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskBlog import mail

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _,f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path,'static/profile_pics/'+picture_fn)
    ouput_size = (200,200)
    i = Image.open(form_picture)
    i.thumbnail(ouput_size)
    i.save(picture_path)

    return picture_fn


def send_reset_email(user):
    token = user.get_user_token()
    msg = Message('Password reset link', sender='noreply@demo.com',recipients=[user.email])
    msg.body = f'''To reset your password click on the below link 
        {url_for('users.reset_token',token=token,_external=True)}
    You if did not make this request ignore this. No changes will be made
    '''
    mail.send(msg)
