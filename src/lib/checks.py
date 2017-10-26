import pgpy
import clamd
from six import BytesIO


def check_gpg(public_key):
    try:
        key, _ = pgpy.PGPKey.from_blob(public_key)
    except ValueError:
        return False

    if not key.is_expired and key.is_public:
        return True

    return False


def check_clamav_stream(stream):
    cd = clamd.ClamdUnixSocket()
    result = cd.instream(BytesIO(stream.encode()))
    if result['stream'][0] == 'FOUND':
        return False
    return True
