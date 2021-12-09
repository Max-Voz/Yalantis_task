import re

from .models import Driver, Vehicle


def check_empty_field(fieldname, entity, _json):
    if _json[f'{fieldname}'] == '' or not _json[f'{fieldname}']:
        return {'message': f'You must provide not empty {fieldname}'
                           f' of the {entity}'}, 400
    return {}, 'Ok'


def vehicle_checking_plate(_json):
    if Vehicle.query.filter_by(
            plate_number=_json['plate_number']
    ).all():
        return {'message': f'Vehicle with plate number '
                           f'{_json["plate_number"]} '
                           f'already exists'}, 400

    if not re.match(r'^[ABCEHIKMOPTX, АВСЕНІКМОРТХ]{2}\s\d{4}'
                    r'(?<!0000)\s[ABCEHIKMOPTX, АВСЕНІКМОРТХ]{2}$',
                    _json['plate_number']):
        return {'message': f'Plate number '
                           f'\'{_json["plate_number"]}\' '
                           f'is not valid. '
                           f'Plate number should contain only '
                           f'ABCEHIKMOPTX letters (both latin and cyrillic). '
                           f'Example - \'AA 1234 OO\''}, 400

    return {}, 'Ok'


def vehicle_checking_driver_id(_json):
    if len(Driver.query.filter(
            Driver.id == _json['driver_id']
    ).all()) == 0:
        return {'message': f'driver with driver_id {_json["driver_id"]}'
                           f' does not exist'}, 400

    if len(Vehicle.query.filter(
            Vehicle.driver_id == _json['driver_id']
    ).all()) != 0:
        vehicle = str(
            Vehicle.query.with_entities(
                Vehicle.id, Vehicle.plate_number
            ).filter_by(
                driver_id=_json['driver_id']
            ).first())[1:-1].replace("'", '').replace(",", '')
        return {'message': f'driver with driver_id {_json["driver_id"]}'
                           f' already belongs to vehicle id {vehicle}'}, 400

    return {}, 'Ok'
