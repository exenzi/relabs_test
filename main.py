import json
import itertools
from aiohttp import web, WSMsgType
from responses import html_response

routes = web.RouteTableDef()

@routes.get('/')
async def index(request):
    # отправка контента файла html
    return html_response('index.html')


@routes.get('/ws')
async def websocket_handler(request):
    ws = web.WebSocketResponse()

    # make pre-check to don't hide it by do_handshake() exceptions
    await ws.prepare(request)

    counter = itertools.count(start=1)

    async for msg in ws:
        if msg.type == WSMsgType.TEXT:
            req_data = json.loads(msg.data)
            print("recieved:", req_data['msg'])

            res_data = {
                'counter': next(counter),
                'msg': req_data['msg']
            }
            await ws.send_json(res_data)
        elif msg.type == WSMsgType.ERROR:
            print('соединение закрыто с исключением', ws.exception())

    print('соединение закрыто')
    return ws

app = web.Application()
app.add_routes(routes)

if __name__ == '__main__':
    web.run_app(app)
