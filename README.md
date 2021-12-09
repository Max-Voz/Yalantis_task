# Task_Yalantis 
____
REST API for fleet of cars with drivers.

This application was created as a test task for Yalantis Python School. 

Database structure and all endpoints of the application are described below.
____
##Database structure:
____
Driver:
```
+ id: int
+ first_name: str
+ last_name: str
+ created_at: DateTime
+ updated_at: DateTime
```

Vehicle
```
+ id: int
+ driver_id: FK to Driver.id
+ make: str
+ model: str
+ plate_number: str  
+ created_at: DateTime
+ updated_at: DateTime
+ driver_in: Boolean
```

____
## Drivers endpoints:
____
+ GET /drivers/driver/ - Getting the list of all drivers 
+ GET /drivers/driver/?created_at__gte=10-11-2021 - Getting the list of all drivers, created after 10-11-2021 (or another provided date in %d/%m/%Y format)
+ GET /drivers/driver/?created_at__lte=16-11-2021 - Getting the list of all drivers, created before 16-11-2021 (or another provided date in %d/%m/%Y format)

  + On valid request returns JSON with the list of all relevant drivers:
    ```
    {
        "Drivers": [
            {
                "driver": "driver_1_description"
            },
            {
                "driver": "driver_2_description"
            }
        ]
    }
    ```
  or relevant error with description appears
---

+ GET /drivers/driver/<driver_id>/ - Getting info on driver by id

  + On valid request returns JSON with the driver's information:
    ```
    {
        "driver": "driver_description"
    }
    ```
    or relevant error with description appears
---
+ POST /drivers/driver/ - Creating a new driver (Headers - Content-Type: application/json) 
  + Valid  JSON for creating a driver (first_name is a mandatory field):
  
    ```
    {
      "first_name":"first_name",
      "last_name":"last_name"
    }
    ```
  or relevant error with description appears
---
+ PATCH /drivers/driver/<driver_id>/ - updating a driver by id (Headers - Content-Type: application/json)
  + Valid  JSON for updating a driver (without mandatory fields):
  
     ```
     {
         "first_name":"first_name",
         "last_name":"last_name"
     }
     ```
---
+ DELETE /drivers/driver/<driver_id>/ - deleting of a driver by id


____
## Vehicle endpoints:
___
+ GET /vehicles/vehicle/ - Getting the list of all vehicles
+ GET /vehicles/vehicle/?with_drivers=yes - Getting the list of all vehicles with drivers in
+ GET /vehicles/vehicle/?with_drivers=no - Getting the list of all vehicles without drivers
  + On valid request returns JSON with the list of all relevant vehicles:
    ```
    {
        "Vehicles": [
            {
                "vehicle": "vehicle_1_description"
            },
            {
                "vehicle": "vehicle_2_description"
            }
        ]
    }
    ```
    or relevant error with description appears
____
+ GET /vehicles/vehicle/<vehicle_id> - Getting info on vehicle by id 

  + On valid request returns JSON with the vehicle's information:
    ```
    {   
        "vehicle": "vehicle_description"
    }
    ```
    or relevant error with description appears
---
+ POST /vehicles/vehicle/ - Creating a new vehicle (Headers - Content-Type: application/json) 
  + Valid  JSON for updating a vehicle (all fields are mandatory):
  
     ```
     {   
         "make": "make",
         "model":"make",
         "driver_id":<driver_id>,
         "plate_number":"plate_number"
     }
     ```
    or relevant error with description appears
  
---
+ PATCH /vehicles/vehicle/<vehicle_id>/ - updating a vehicle by id (Headers - Content-Type: application/json)
  + Valid  JSON for updating a vehicle (without mandatory fields):
  
     ```
     {   
	     "make": "make",
	     "model":"model",
	     "driver_id":<driver_id>,
	     "plate_number":"plate_number"
     }
     ```
    or relevant error with description appears
---
+ POST /vehicles/set_driver/<vehicle_id>/ - putting the driver in a car / dropping the driver out of the car  
---
+ DELETE /vehicles/vehicle/<vehicle_id>/ - deleting of a vehicle by id
---


