from app.routes.base import BaseAdminAPIHander, BaseUserAPIHander


class SampleHandler(BaseAdminAPIHander):
    async def get(self):
        self.write("Hello, world")
        await self.finish()


class SampleHandler2(BaseUserAPIHander):
    async def get(self):
        # Example for returning JSON, tornado will auto-convert dict to JSON response
        response_dict = {"exampleJSON": "Hello world 2"}
        await self.finish(response_dict)
