from aiohttp import web

def html_response(filepath):
    # отправка контента файла html
    try:
        with open(filepath, "r") as f:
            html = f.read()
    except FileNotFoundError:
        print('No such file:', filepath)
        return web.HTTPInternalServerError()
    return web.Response(text=html, content_type='text/html')
