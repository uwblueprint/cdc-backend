import db_client as client
import tornado.web


class SampleHandler(tornado.web.RequestHandler):
    async def get(self):
        self.write("Hello, world")
        client.get_assets()
        await self.finish()


class SampleHandler2(tornado.web.RequestHandler):
    async def get(self):
        # Example for returning JSON, tornado will auto-convert dict to JSON response
        response_dict = {"exampleJSON": "Hello world 2"}
        await self.finish(response_dict)
