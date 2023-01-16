FORMAT: 1A

# Documentation

## About

### This is the work for the first assignment in ICCS 372 course. You can check for latest changes in [changelog](changelog.md).

* ### Purpose 

    * To build most maintainable application for manage and tracking vending machine.

* ### Requirement
    * return json data type.
    * CRUD vending machine (name, location, etc.)
    * each vending machine has own stock

# Features
- Each vending machine has own storage and stock
- Search for machine by name and location
- Easily add, remove, and update machine data
- Easily change snack name across all machine
- Auto update vending machine status
- Add, Minus, and Set command to easily update machine stock

# Setup
1. clone this repository to your computer
   
2. open up the folder in your favorite IDE

3. install dependencies

    ``` python
    pip install -r requirements.txt
    ```

4. go into core folder

    ```python
    cd core
    ```

5. initialize django setup
   
    1.  Simplest way (For people who new to django)

        ```python
        py manage.py easy_setup

        # run this if you want to flush database
        py manage.py flush

        ```
    2. Standard way (For people who familiar with django)

        ```python
        py manage.py migrate

        #create simple sample data for testing
        py manage.py create_sample

        ```
    3. Set up your own database
   
       1. go to `core/setting.py` and config `DATABASES` variable
   
       2. install dependencies
   
       3. follow step above
   
6. run local server
   
    ``` python
    py manage.py runserver
    ```

7. now you should see something similar to this
   
    ```python
    System check identified no issues (0 silenced).
    January 15, 2023 - 14:13:12
    Django version 4.1.5, using settings 'core.settings'
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CTRL-BREAK.
    ```

# API

## Endpoint: localhost:8000/machine/

- ## **GET** Request

    ### parameter options:

    `detail: boolean` if `true` show stock of each vending machine

    `name: string` to search vending machine that contain provide string

    `location: string` to search vending machine that contain provide string

    ```python
    import requests

    url = "http://localhost:8000/machine/"

    response = requests.request("GET", url)

    print(response.json())

    # {
    #     "result": [
    #         {
    #             "id": 1,
    #             "name": "Science Building machine 1",
    #             "location": "Science Building 1 floor Mahidol University Salaya",
    #             "status": "Normal",
    #         },
    #         {
    #             "id": 2,
    #             "name": "Science Building machine 2",
    #             "location": "Science Building 2 floor Mahidol University Salaya",
    #             "status": "Normal",
    #         },
    #     ],
    #     "error": False,
    # }

    url = "http://localhost:8000/machine/?detail=True"

    response = requests.request("GET", url)

    print(response.json())

    # {
    #     "result": [
    #         {
    #             "id": 1,
    #             "name": "Science Building machine 1",
    #             "location": "Science Building 1 floor Mahidol University Salaya",
    #             "status": "Normal",
    #             "stock": [{"snack_id": 9, "snack_name": "Espresso", "quantity": 20}],
    #         },
    #         {
    #             "id": 2,
    #             "name": "Science Building machine 2",
    #             "location": "Science Building 2 floor Mahidol University Salaya",
    #             "status": "Normal",
    #             "stock": [
    #                 {"snack_id": 5, "snack_name": "7-Up", "quantity": 5},
    #                 {"snack_id": 2, "snack_name": "Mineral Water", "quantity": 5},
    #             ],
    #         },
    #     ],
    #     "error": False,
    # }
    ```
* ## **POST** Request

    Create new vending machine. This 
will return new vending machine back
    ```python
    import requests

    url = "http://localhost:8000/machine/"

    payload = {"name": "Tony", "location": "new location"}

    response = requests.request("POST", url, data=payload)

    print(response.json())

    # {
    #     "result": {
    #         "id": 21,
    #         "name": "Tony",
    #         "location": "new location",
    #         "status": "Out of Stock",
    #     },
    #     "error": False,
    # }
    ```

## Endpoint: localhost:8000/machine/\<id>/

- ## **GET** Request

    get individual information of vending machine with following id

    ### Parameter options:

    `delete: boolean` if `true` delete vending machine with following id

    ```python
    import requests

    url = "http://localhost:8000/machine/11/"


    response = requests.request("GET", url)

    print(response.json())

    # {
    #     "result": {
    #         "id": 11,
    #         "name": "MUIC Building machine 1",
    #         "location": "MUIC Building 1 floor Mahidol University Salaya",
    #         "status": "Normal",
    #         "stock": [{"snack_id": 6, "snack_name": "Fanta", "quantity": 20}],
    #     },
    #     "error": False,
    # }

    url = "http://localhost:8000/machine/21/?delete=True"

    response = requests.request("GET", url)

    print(response.json())

    # {"result": "Successfully deleted machine id=21", "error": False}

    ```

- ## **POST** Request

    Update information of vending machine. Return updated vending machine info

    ```python
    import requests

    url = "http://localhost:8000/machine/11/"

    payload = {"name": "new name", "location": "new location"}

    response = requests.request("POST", url, data=payload)

    print(response.json())

    # {
    #     "result": {
    #         "id": 11,
    #         "name": "new name",
    #         "location": "new location",
    #         "status": "Normal",
    #     },
    #     "error": False,
    # }
    ```

## Endpoint: localhost:8000/snack/

- ## **GET** Request

    get list of all available snacks' name

    ### Parameter options:

    `name: string` to search for snacks that contain provide string

    ```python
    import requests

    url = "http://localhost:8000/snack/?name=coke"

    response = requests.request("GET", url)

    print(response.json())

    # {"result": [{"id": 3, "name": "Coke"}], "error": False}
    ```

- ## **POST** Request

    Add new snack into database. Return new snack

    ```python
    import requests

    url = "http://localhost:8000/snack/"

    payload = {"name": "Orange Juice"}

    response = requests.request("POST", url, data=payload)

    print(response.json())

    # {'result': {'id': 13, 'name': 'Orange Juice'}, 'error': False}
    ```

## Endpoint: localhost:8000/snack/\<id>/

- ## **GET** Request

    get information of snack with following id

    ### Parameter options:

    `delete: boolean` if `true` delete vending machine with following id

    ```python
    import requests

    url = "http://localhost:8000/snack/13/?delete=True"

    response = requests.request("GET", url)

    print(response.json())

    # {'result': 'Successfully deleted snack id=13', 'error': False}

    ```

- ## **POST** Request

    Update information of snack. Return updated snack data.

    ```python
    import requests

    url = "http://localhost:8000/snack/3/"

    payload = {"name": "Orange Juice"}

    response = requests.request("POST", url, data=payload)

    print(response.json())

    # {'result': {'id': 3, 'name': 'Orange Juice'}, 'error': False}

    ```
