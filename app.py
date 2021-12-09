from app import app, db
from app.models import Driver, Vehicle
from app.functions import check_empty_field, vehicle_checking_plate, \
    vehicle_checking_driver_id
from datetime import datetime
from flask import jsonify, request


@app.route('/drivers/driver/', methods=['GET'])
def get_drivers():
    if not request.args:
        result = {'Drivers': []}
        for item in Driver.query.all():
            result['Drivers'].append({'driver': str(item)})
        return jsonify(result), 200

    if 'created_at__gte' in request.args:
        result_gte = {'Drivers': []}
        comparison_time_lesser = datetime.strptime(
            request.args['created_at__gte'],
            "%d-%m-%Y")
        for item in Driver.query.filter(
                Driver.created_at >= comparison_time_lesser).all():
            result_gte['Drivers'].append({'driver': str(item)})

        return jsonify(result_gte), 200

    elif 'created_at__lte' in request.args:
        result_lte = {'Drivers': []}
        comparison_time_greater = datetime.strptime(
            request.args['created_at__lte'],
            "%d-%m-%Y")
        for item in Driver.query.filter(
                Driver.created_at < comparison_time_greater).all():
            result_lte['Drivers'].append({'driver': str(item)})

        return jsonify(result_lte), 200
    else:
        return {'message': f'Query {request.args.to_dict()} '
                           f'is not allowed. Allowed queries - '
                           f'created_at__lte=\'%d/%m/%Y\', '
                           f'created_at__gte=\'%d/%m/%Y\''}, 400


@app.route('/drivers/driver/<int:driver_id>', methods=['GET'])
def get_driver_by_id(driver_id):
    try:
        return jsonify(
            {'driver': str(Driver.query.filter_by(id=driver_id)[0])}), 200
    except IndexError:
        return {}, 404


@app.route('/drivers/driver/', methods=['POST'])
def create_driver():
    if 'first_name' not in request.json:
        return {'message': 'You must provide at least first name'
                           ' of the driver'}, 400

    request_checking = check_empty_field('first_name', 'driver', request.json)
    if request_checking[1] == 400:
        return request_checking
    new_driver = {
        'first_name': request.json['first_name'],
        'last_name': request.json['last_name']
    }
    created_driver = Driver(**new_driver)
    db.session.add(created_driver)
    db.session.commit()
    return new_driver, 201


@app.route('/drivers/driver/<int:driver_id>', methods=['PATCH'])
def update_driver_by_id(driver_id):
    if 'first_name' in request.json:
        request_checking = check_empty_field(
            'first_name', 'driver', request.json
        )
        if request_checking[1] == 400:
            return request_checking

    try:
        if Driver.query.filter_by(id=driver_id)[0]:
            Driver.query.filter_by(id=driver_id).update(request.json)
            db.session.commit()
            return {}, 204
    except IndexError:
        return {}, 404


@app.route('/drivers/driver/<int:driver_id>', methods=['DELETE'])
def delete_driver_by_id(driver_id):
    try:
        if Driver.query.filter_by(id=driver_id)[0]:
            if len(Vehicle.query.filter(
                    Vehicle.driver_id == driver_id
            ).all()) != 0:
                Vehicle.query.filter(
                    Vehicle.driver_id == driver_id
                ).first().driver_id = None

            Driver.query.filter_by(id=driver_id).delete()

            db.session.commit()
            return {}, 204
    except IndexError:
        return {}, 404


@app.route('/vehicles/vehicle/', methods=['GET'])
def get_vehicles():
    if not request.args:
        result = {'Vehicles': []}
        for item in Vehicle.query.all():
            result['Vehicles'].append({'vehicle': str(item)})
        return jsonify(result), 200

    if 'with_drivers' in request.args:
        result_vehicles = {'Vehicles': []}
        if request.args['with_drivers'] == 'yes':
            for item in Vehicle.query.filter(
                    Vehicle.driver_in.is_(True)
            ).all():
                result_vehicles['Vehicles'].append({'vehicle': str(item)})
        elif request.args['with_drivers'] == 'no':
            for item in Vehicle.query.filter(
                    Vehicle.driver_in.is_(False)
            ).all():
                result_vehicles['Vehicles'].append({'vehicle': str(item)})
        else:
            return {'message': f'Value of query with_drivers '
                               f'{request.args["with_drivers"]} '
                               f'is not allowed. Allowed values - '
                               f'<yes>, <no>'}, 400
        return jsonify(result_vehicles), 200
    else:
        return {'message': f'Query {request.args.to_dict()} '
                           f'is not allowed. Allowed queries - '
                           f'<with_drivers=yes>, <with_drivers=no>'}, 400


@app.route('/vehicles/vehicle/<int:vehicle_id>', methods=['GET'])
def get_vehicle_by_id(vehicle_id):
    try:
        return jsonify(
            {'vehicle': str(Vehicle.query.filter_by(id=vehicle_id)[0])}), 200
    except IndexError:
        return {}, 404


@app.route('/vehicles/vehicle/', methods=['POST'])
def create_vehicle():
    if 'make' not in request.json or 'model' not in request.json \
            or 'model' not in request.json or 'driver_id' not in request.json:
        return {'message': 'You must provide driver_id, make, model and '
                           'plate number of the car'}, 400

    for field in ['make', 'model', 'driver_id', 'plate_number']:
        request_checking = check_empty_field(field, 'vehicle', request.json)
        if request_checking[1] == 400:
            return request_checking

    driver_id_checking = vehicle_checking_driver_id(request.json)
    if driver_id_checking[1] == 400:
        return driver_id_checking
    plate_checking = vehicle_checking_plate(request.json)
    if plate_checking[1] == 400:
        return plate_checking

    new_vehicle = {
        'driver_id': request.json['driver_id'],
        'make': request.json['make'],
        'model': request.json['model'],
        'plate_number': request.json['plate_number']
    }
    created_vehicle = Vehicle(**new_vehicle)
    db.session.add(created_vehicle)

    try:
        db.session.commit()
    except Exception as e:
        return jsonify({'exception': f'{e}'}), 404
    return new_vehicle, 201


@app.route('/vehicles/vehicle/<int:vehicle_id>', methods=['PATCH'])
def update_vehicle_by_id(vehicle_id):
    for field in ['make', 'model', 'driver_id', 'plate_number']:
        if field in request.json:
            request_checking = check_empty_field(
                field, 'vehicle', request.json
            )
            if request_checking[1] == 400:
                return request_checking
            if field == 'driver_id':
                try:
                    if Vehicle.query.filter_by(
                            id=vehicle_id).first().driver_id != int(
                            request.json['driver_id']):
                        driver_id_checking = vehicle_checking_driver_id(
                            request.json)
                        if driver_id_checking[1] == 400:
                            return driver_id_checking
                except ValueError:
                    return {
                        'message': f'driver_id <{request.json["driver_id"]}> '
                                   f'is not walid, driver_id must be integer'}

            if field == 'plate_number':
                if Vehicle.query.filter_by(
                        id=vehicle_id).first().plate_number != (
                        request.json['plate_number']):
                    plate_checking = vehicle_checking_plate(request.json)
                    if plate_checking[1] == 400:
                        return plate_checking
    try:
        if Vehicle.query.filter_by(id=vehicle_id)[0]:
            Vehicle.query.filter_by(id=vehicle_id).update(request.json)
            db.session.commit()
            return {}, 204
    except IndexError:
        return {}, 404


@app.route('/vehicles/set_driver/<int:vehicle_id>', methods=['POST'])
def set_driver_to_vehicle_by_id(vehicle_id):
    try:
        if Vehicle.query.filter_by(id=vehicle_id)[0]:
            _vehicle = Vehicle.query.filter_by(id=vehicle_id).first()
            _vehicle.driver_in = not _vehicle.driver_in
            db.session.commit()
        return {}, 204
    except IndexError:
        return {}, 404


@app.route('/vehicles/vehicle/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle_by_id(vehicle_id):
    try:
        if Vehicle.query.filter_by(id=vehicle_id)[0]:
            Vehicle.query.filter_by(id=vehicle_id).delete()
            db.session.commit()
            return {}, 204
    except IndexError:
        return {}, 404


if __name__ == '__main__':
    app.run()
