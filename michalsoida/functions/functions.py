from flask import make_response
from magic import Magic

magic = Magic(mime=True)
get_mimetype = magic.from_buffer


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
