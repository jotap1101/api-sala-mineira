from django.utils.timezone import now
import hashlib
import os

def upload_to(instance, filename, folder):
    ext = os.path.splitext(filename)[1]
    hash_input = f'{filename}-{now().timestamp()}'.encode('utf-8')
    hashed_name = hashlib.sha256(hash_input).hexdigest()

    return f'{folder}/{hashed_name}{ext}'