import inspect
import asyncio
from aiohttp.web import Application, Response, StreamResponse

class Web:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.routes = []


    def get(self, rule):

        print(rule)

        def decorator(action):
            params = inspect.getargspec(action)

            print(params)

            @asyncio.coroutine
            def wrapped(request):

                print(request)

                return action(self, request)

            self.routes.append(['GET', rule, wrapped])

            return wrapped
        return decorator


    @asyncio.coroutine
    def init(self, loop):
        app = Application(loop=loop)

        for (method, rule, handler) in self.routes:
            app.router.add_route(method, rule, handler)

        handler = app.make_handler()
        srv = yield from loop.create_server(handler, self.host, self.port)

        return srv, handler


    def run(self):

        loop = asyncio.get_event_loop()
        srv, handler = loop.run_until_complete(self.init(loop))
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            loop.run_until_complete(handler.finish_connections())

