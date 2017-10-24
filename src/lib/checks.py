import gnupg
import clamd
from six import BytesIO


def check_gpg(public_key):
    gpg = gnupg.GPG()
    import_result = gpg.import_keys(public_key)
    if import_result.results[0]['fingerprint'] is not None:
        return True
    return False


def check_clamav_stream(stream):
    cd = clamd.ClamdUnixSocket()
    result = cd.instream(BytesIO(stream.encode()))
    if result['stream'][0] == 'FOUND':
        return False
    return True
