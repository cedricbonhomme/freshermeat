
from bootstrap import application

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in application['ALLOWED_EXTENSIONS']
