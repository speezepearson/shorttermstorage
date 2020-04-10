"""Short-Term Storage server. `POST /` to write arbitrary content, `GET /` to read and delete.
"""

import argparse
import typing as t
from aiohttp import web

class Server:
    def __init__(self) -> None:
        self.content = None

    def routes(self) -> t.Iterable[web.RouteDef]:
        return [
            web.RouteDef(method='POST', path='/', handler=self.write_content, kwargs={}),
            web.RouteDef(method='GET', path='/', handler=self.read_content, kwargs={}),
        ]

    async def write_content(self, request: web.BaseRequest) -> web.StreamResponse:
        self.content = await request.read()
        return web.Response(status=204)

    async def read_content(self, request: web.BaseRequest) -> web.StreamResponse:
        if self.content is None:
            return web.Response(status=404)
        content, self.content = self.content, None
        return web.Response(status=200, body=content)

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port', type=int, default=8080)
parser.add_argument('-H', '--host', default='localhost')

if __name__ == '__main__':
    args = parser.parse_args()

    app = web.Application()
    app.add_routes(Server().routes())

    web.run_app(app, host=args.host, port=args.port)
