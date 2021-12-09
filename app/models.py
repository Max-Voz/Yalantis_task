from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Driver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80))
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(),
                           onupdate=datetime.now())

    def __repr__(self):
        rprsnt = f'id: {self.id}, ' \
                 f'Driver {self.first_name} {self.last_name}, ' \
                 f'created_at: ' \
                 f'{self.created_at.strftime("%d/%m/%Y %H:%M:%S")}'

        if self.updated_at.strftime(
                "%d/%m/%Y %H:%M:%S") != self.created_at.strftime("%d/%m/%Y "
                                                                 "%H:%M:%S"):
            rprsnt += f', updated_at: ' \
                      f'{self.updated_at.strftime("%d/%m/%Y %H:%M:%S")}'
        driv_vehicle = Vehicle.query.filter_by(driver_id=self.id).first()
        if driv_vehicle:
            rprsnt += f', attached vehicle - ' \
                      f'id {driv_vehicle.id} {driv_vehicle.make} ' \
                      f'{driv_vehicle.model} {driv_vehicle.plate_number}'
        else:
            rprsnt += f', driver has no attached vehicle'
        return rprsnt


class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.id'), unique=True)
    make = db.Column(db.String(80), nullable=False)
    model = db.Column(db.String(80), nullable=False)
    plate_number = db.Column(db.String(80), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(),
                           onupdate=datetime.now())
    driver_in = db.Column(db.Boolean, default=False)

    def __repr__(self):
        att_driver = Driver.query.filter_by(id=self.driver_id).first()
        rprsnt = f'id: {self.id}, ' \
                 f'Vehicle {self.make} {self.model}, ' \
                 f'plate_number {self.plate_number}, '

        if att_driver:
            rprsnt += f'driver id = {self.driver_id}, ' \
                      f'driver name - {att_driver.first_name} ' \
                      f'{att_driver.last_name} '

        else:
            rprsnt += f'vehicle\'s driver has been deleted, '
        rprsnt += f'created_at: ' \
                  f'{self.created_at.strftime("%d/%m/%Y %H:%M:%S")}'

        if self.updated_at.strftime(
                "%d/%m/%Y %H:%M:%S") != self.created_at.strftime("%d/%m/%Y "
                                                                 "%H:%M:%S"):
            rprsnt += f', updated_at: ' \
                      f'{self.updated_at.strftime("%d/%m/%Y %H:%M:%S")}'

        if self.driver_in:
            rprsnt += f', driver is in the vehicle'
        else:
            rprsnt += f', driver is not in the vehicle'
        return rprsnt
