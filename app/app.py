from aiohttp import web
from pathlib import Path
import aiohttp_jinja2
import jinja2

from views import routes


app = web.Application(debug=True)
app.add_routes(routes)
aiohttp_jinja2.setup(
    app, loader=jinja2.FileSystemLoader(str(Path(__file__).parent / "templates"))
)
web.run_app(app, host='127.0.0.2', port=8080)