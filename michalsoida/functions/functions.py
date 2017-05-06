from flask import make_response
from magic import Magic

# magic = Magic(mime=True)


# def make_magic_response(*args):
#     resp = make_response(*args)
#     mimetype = magic.from_buffer(resp.get_data())
#     resp.headers['Content-Type'] = mimetype
#     return resp


def make_jpg_response(*args):
    resp = make_response(*args)
    resp.headers['Content-Type'] = 'image/jpeg'
    return resp


def make_pdf_response(*args):
    resp = make_response(*args)
    resp.headers['Content-Type'] = 'application/pdf'
    return resp


def make_png_response(*args):
    resp = make_response(*args)
    resp.headers['Content-Type'] = 'image/png'
    return resp


def make_svg_response(*args):
    resp = make_response(*args)
    resp.headers['Content-Type'] = 'image/svg+xml'
    return resp
