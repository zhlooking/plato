from flask import Blueprint, make_response, jsonify, request
from sqlalchemy import exc

from plato import db
from plato.api.utils import authenticate, is_admin
from plato.model.domain import Domain

domains_blueprint = Blueprint('domains', __name__, template_folder='./templates')


@domains_blueprint.route('/domains', methods=['POST'])
@authenticate
def add_domain(resp):
    '''add domain info'''
    if is_admin(resp):
        response_object = {
            'status': 'error',
            'message': 'You have no permission to do that.'
        }
        return make_response(jsonify(response_object)), 403
    post_data = request.get_json()
    if not post_data:
        response_object = {
            'status': 'fail',
            'message': f'Invalid payload'
        }
        return make_response(jsonify(response_object)), 400
    domain_val = post_data.get('domain')
    ip = post_data.get('ip')
    master = post_data.get('master')
    try:
        domain = Domain.query.filter_by(domain=domain_val).first()
        if not domain:
            db.session.add(Domain(domain=domain_val, ip=ip, master=master))
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': f'{domain_val} was added!'
            }
            return make_response(jsonify(response_object)), 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'Sorry, that domain already exists.'
            }
            return make_response(jsonify(response_object)), 400
    except exc.IntegrityError as e:
        db.session().rollback()
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload'
        }
        return make_response(jsonify(response_object)), 400
    except ValueError as e:
        db.session().rollback()
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload'
        }
        return make_response(jsonify(response_object)), 400


@domains_blueprint.route('/domain/<domain_id>', methods=['GET'])
def get_domain(domain_id):
    '''get domain info'''
    response_object = {
        'status': 'fail',
        'message': 'Domain does not exist.'
    }
    try:
        domain = Domain.query.filter_by(id=int(domain_id)).first()
        if not domain:
            return make_response(jsonify(response_object)), 404
        else:
            response_object = {
                'status': 'success',
                'data': {
                    'id': domain.id,
                    'ip': domain.ip,
                    'domain': domain.domain,
                    'master': domain.master
                }
            }
            return make_response(jsonify(response_object)), 200
    except ValueError:
        return make_response(jsonify(response_object)), 404


@domains_blueprint.route('/domains', methods=['GET'])
def get_all_domains():
    '''get all domain list'''
    domains = Domain.query.order_by(Domain.ip.desc()).all()
    domains_list = []
    for domain in domains:
        domain_object = {
            'id': domain.id,
            'ip': domain.ip,
            'domain': domain.domain,
            'master': domain.master
        }
        domains_list.append(domain_object)

    response_object = {
        'status': 'success',
        'data': {
            'domains': domains_list
        }
    }
    return make_response(jsonify(response_object)), 200
