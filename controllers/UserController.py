from core import web, view
from aiohttp.web import Response

class UserController:

    @web.get('/login')
    @view.json
    def login(self, request):
        return Response(body=b'Fack the system')

    @web.get('/blog/{id}')
    @view.json
    def blog(self, id):
        return Response(body=b'{}'.format(id))