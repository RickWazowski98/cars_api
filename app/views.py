from aiohttp import web
from bson import json_util
import json
import aiohttp_jinja2

from db import Db


routes = web.RouteTableDef()


@routes.get('/api/')
async def cars_list(request):
    cars_info_list = Db().show_documents()
    return web.Response(text=json.dumps(cars_info_list, indent=4), status=200)


@routes.post('/api/')
async def add_car(request):
    j_data = await request.json()
    try:
        Db().insert_document(j_data)
        resp = {'car': str(j_data)}
        return web.Response(text=json.dumps(resp, indent=4), status=200)
    except Exception as err:
        return web.Response(text=str(json.dumps({"err_info": "Car don't be added \n reason: {}".format(str(err))})), status=400)


@routes.get('/api/{vim}')
async def car_detail(request):
    result = Db().collection.find({"VIM":request.match_info['vim']},{"_id":0})
    return web.Response(text=json.dumps([r for r in result], indent=4))


@routes.put('/api/{vim}')
async def change_car_detail(request):
    req_data = await request.json()
    vim = request.match_info['vim']
    result = Db().update_document({"VIM":vim},req_data)
    return web.Response(text=str(json.dumps(req_data, indent=4)), status=200)


@routes.delete('/api/{vim}')
async def delete_car(request):
    Db().collection.delete_one({"VIM":request.match_info['vim']})
    return web.Response(text=str(json.dumps({"info":"Car by VIM: {} has been deleted".format(request.match_info['vim'])})), status=204)


@routes.get('/api/search_by/{key}={value}')
async def search_car_by(request):
    search_query = {str(request.match_info['key']): str(request.match_info['value'])}
    search_result = Db().collection.find(search_query, {"_id":0})
    return web.Response(text=str(json.dumps([r for r in search_result], indent=4)), status=200)


@routes.get('/client/')
@aiohttp_jinja2.template('cars_list.html')
async def client_cars_list(request):
    context = {"cars": Db().show_documents()}
    return context


@routes.get('/client/delete/{vim}')
@aiohttp_jinja2.template('car_deleted.html')
async def client_delete_car(request):
    Db().collection.delete_one({"VIM": request.match_info['vim']})
    context = {"vim": request.match_info['vim']}
    return context


@routes.view('/client/add_car/')
@aiohttp_jinja2.template('add_car.html')
class AddCarView(web.View):

    async def post(self):
        data = await self.request.post()
        j_data = {
            "manufacturer": data['manufacturer'],
            "model": data['model'],
            "year_of_issue": data['year_of_issue'],
            "colour": data['colour'],
            "VIM": data['VIM'],
        }
        Db().insert_document(j_data)
    
    async def get(self):
        return self.request

@routes.view('/client/{vim}')
@aiohttp_jinja2.template('car_detail.html')
class CarDetailView(web.View):

    async def get(self):
        car_info = Db().collection.find_one({"VIM":self.request.match_info['vim']},{"_id":0})
        context = {"car": car_info}
        return context

    async def post(self):
        data = await self.request.post()
        car_info = Db().collection.find_one({"VIM":self.request.match_info['vim']},{"_id":0})
        context = {
            "car": car_info,
            "vim": self.request.match_info['vim']
        }
        j_data = {
            "manufacturer": data['manufacturer'],
            "model": data['model'],
            "year_of_issue": data['year_of_issue'],
            "colour": data['colour'],
            "VIM": data['VIM'],
        }
        Db().update_document({"VIM":data['VIM']}, j_data)
        return context


@routes.view('/client/change_info/{vim}')
@aiohttp_jinja2.template('change_info.html')
class ChangeCarInfo(web.View):

    async def get(self):
        car_info = Db().collection.find_one({"VIM":self.request.match_info['vim']},{"_id":0})
        context = {
            "car": car_info,
            "vim": self.request.match_info['vim']
        }
        return context

