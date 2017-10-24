import gnupg


def check_gpg(public_key):
    gpg = gnupg.GPG()
    import_result = gpg.import_keys(public_key)
    if import_result.results[0]['fingerprint'] is not None:
        return True
    else:
        return False
