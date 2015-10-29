import inspect
import asyncio
from aiohttp.web import Application, Response, StreamResponse

def test(action):
    print('def test(action):')
    return action

class Web:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.routes = []


    def get(self, rule):
        def decorator(action):

            @asyncio.coroutine
            def wrapped(self, *args):
                return action(self)

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


class View:

    def __init__(self):
        pass

    def json(self, action):
        return action

    def html(self, action):
        return action

    def xml(self, action):
        return action


web = Web('127.0.0.1', 8000)
view = View()

class UserController:

    @web.get('/login')
    @view.json
    def login(self):
        return Response(body=b'Fack the system')


    @web.get('/blog/{id}')
    @view.json
    def blog(self, id):
        print(id)

web.run()