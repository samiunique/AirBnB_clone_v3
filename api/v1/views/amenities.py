#!/usr/bin/python3
'''This script contains the amenities view for the API.'''
from flask import jsonify, request
from werkzeug.exceptions import NotFound, MethodNotAllowed, BadRequest

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


ALLOWED_METHODS = ['GET', 'DELETE', 'POST', 'PUT']
'''Methods allowed for the amenities endpoint.'''


@app_views.route('/amenities', methods=ALLOWED_METHODS)
@app_views.route('/amenities/<amenity_id>', methods=ALLOWED_METHODS)
def handle_amenities(amenity_id=None):
    '''The method handler for the amenities endpoint.
    '''
    handlers = {
        'GET': get_amenities,
        'DELETE': remove_amenity,
        'POST': add_amenity,
        'PUT': update_amenity,
    }
    if request.method in handlers:
        return handlers[request.method](amenity_id)
    else:
        raise MethodNotAllowed(list(handlers.keys()))


def get_amenities(amenity_id=None):
    '''Gets the amenity with the given id or all amenities.
    '''
    amenity_all = storage.all(Amenity).values()
    if amenity_id:
        res = list(filter(lambda x: x.id == amenity_id, amenity_all))
        if res:
            return jsonify(res[0].to_dict())
        raise NotFound()
    amenity_all = list(map(lambda x: x.to_dict(), amenity_all))
    return jsonify(amenity_all)


def remove_amenity(amenity_id=None):
    '''Removes a amenity with the given id.
    '''
    amenity_all = storage.all(Amenity).values()
    res = list(filter(lambda x: x.id == amenity_id, amenity_all))
    if res:
        storage.delete(res[0])
        storage.save()
        return jsonify({}), 200
    raise NotFound()


def add_amenity(amenity_id=None):
    '''Adds a new amenity.
    '''
    data = request.get_json()
    if type(data) is not dict:
        raise BadRequest(description='Not a JSON')
    if 'name' not in data:
        raise BadRequest(description='Missing name')
    amenty_nw = Amenity(**data)
    amenty_nw.save()
    return jsonify(amenty_nw.to_dict()), 201


def update_amenity(amenity_id=None):
    '''Updates the amenity with the given id.
    '''
    xkeys = ('id', 'created_at', 'updated_at')
    amenity_all = storage.all(Amenity).values()
    res = list(filter(lambda x: x.id == amenity_id, amenity_all))
    if res:
        data = request.get_json()
        if type(data) is not dict:
            raise BadRequest(description='Not a JSON')
        amenty_old = res[0]
        for key, value in data.items():
            if key not in xkeys:
                setattr(amenty_old, key, value)
        amenty_old.save()
        return jsonify(amenty_old.to_dict()), 200
    raise NotFound()
