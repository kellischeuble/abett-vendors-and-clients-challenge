from fastapi import FastAPI
from src.db import Commands


uri = "bolt://localhost:7687"
user = "neo4j"
password = "password"

app = FastAPI()


@app.get("/")
def read_root():
    """ 
    Health check endpoint
    """
    return {"Hello": "World"}


@app.post("/create_vendor")
def create_vendor(vendor_name: str):
    """
    Endpoint to create a vendor node

    Args:
        vendor_name (str): the vendor's name

    Returns:
        json object of node created
        # TODO: should return message if vendor
        already exists
    """
    n = Commands(uri, user, password)
    result = n.create_vendor(vendor_name.strip().lower())
    n.close()
    return result


@app.get("/get_vendor")
def get_vendor(vendor_name: str):
    """
    Endpoint to get a vendor's information

    Args:
        vendor_name (str): vendor's name

    Returns:
        json object of node returned
        # TODO: should return message if no such
        vendor exists (right now just returns empty object)
    """
    n = Commands(uri, user, password)
    result = n.get_vendor(vendor_name)
    n.close()
    return result


@app.post("/update_vendor")
def update_vendor(vendor_name: str, property: str, updated_value: str):
    """
    Endpoint to update a vendor's information 

    Args:
        vendor_name (str): vendor's name
        property (str): property of information to be updated
        updated_value (str): updated value to be changed

    Returns:
        json object of the updated vendor node
        # TODO: returns message/error if property doesn't exist
        # TODO: returns message/error if vendor doesn't exist
    """
    n = Commands(uri, user, password)
    result = n.update_vendor(vendor_name, property, updated_value)
    n.close()
    return result


@app.post("/delete_vendor")
def delete_vendor(vendor_name: str):
    """
    Endpoint to delete a vendor node

    Args:
        vendor_name (str): vendor's name

    Returns:
        empty object
        # TODO: return message if vendor node was successfully deleted
        # TODO: return message if vendor node was does not exist
    """
    n = Commands(uri, user, password)
    result = n.delete_vendor(vendor_name)
    n.close()
    return result


@app.post("/create_client")
def create_client(client_name: str, employee_count: int):
    """
    Endpoint to create a client node

    Args:
        client_name (str): the client's name

    Returns:
        json object of node created
        # TODO: should return message if client already exists
    """
    n = Commands(uri, user, password)
    result = n.create_client(client_name, employee_count)
    n.close()
    return result


@app.get("/get_client")
def get_client(client_name: str):
    """
    Endpoint to get a client's information

    Args:
        client_name (str): client's name

    Returns:
        json object of node returned
        # TODO: should return message if no such
        client exists (right now just returns empty object)
    """
    n = Commands(uri, user, password)
    result = n.get_client(client_name)
    n.close()
    return result


@app.post("/update_client")
def update_client(client_name: str, property: str, new_value: str):
    """
    Endpoint to update a client's information 

    Args:
        client_name (str): client's name
        property (str): property of information to be updated
        updated_value (str): updated value to be changed

    Returns:
        json object of the updated client node
        # TODO: returns message/error if property doesn't exist
        # TODO: returns message/error if client doesn't exist
    """
    n = Commands(uri, user, password)
    result = n.update_client(client_name, property, new_value)
    n.close()
    return result


@app.post("/delete_client")
def delete_client(client_name: str):
    """
    Endpoint to delete a client node

    Args:
        client_name (str): client's name

    Returns:
        empty object
        # TODO: return message if client node was successfully deleted
        # TODO: return message if client node was does not exist
    """
    n = Commands(uri, user, password)
    result = n.delete_client(client_name)
    n.close()
    return result


@app.post("/add_relationship")
def create_transfer(vendor_name: str, client_name: str, direction: str, frequency: str):
    """
    Endpoint to add a directed transfer connection between a vendor
    and a client

    Args:
        vendor_name (str): vendor's name
        client_name (str): client's name
        direction (str): direction of information transfer from client's perspective
                        (should be "in" or "out")
        frequency (str): schedule (daily, weekly, monthly)

    Returns:
        json object representing of the node's + relationship
        # TODO: make return statement more readable
        # TODO: return error message if vendor or client does not exist (or specifies
        # that a vendor or client did not already exist so it created one)
        # TODO: checks for valid inputs (direction and frequency)
    """
    n = Commands(uri, user, password)
    result = n.create_transfer(vendor_name, client_name, direction, frequency)
    n.close()
    return result


@app.get("/get_vendors")
def get_list_of_vendors(client_name: str):
    """
    Endpoint to return all vendors for a given client
    Organized by inputs and outputs, ordered by schedule frequency

    Args:
        client_name (str): client's name

    Returns:
        json object
        # TODO: plan out JSON structure
        # TODO: return error message if client does not exist
    """

    n = Commands(uri, user, password)
    # TODO: look at cypher to see if this can be done at once
    # instead of looking at each relationship individually
    outputs = n.get_list_of_output_vendors(client_name)
    inputs = n.get_list_of_input_vendors(client_name)
    # TODO: create function to reformat outputs & inputs
    n.close()
    return outputs + inputs


@app.get("/get_delivery_schedule")
def get_delivery_schedule(vendor_name: str):
    """
    Endpoint to get the delivery schedule for a given vendor

    Args:
        vendor_name (str): vendor's name

    Returns:
        json object
        # TODO: plan out JSON structure
        # TODO: return error message if vendor does not exist
    """
    n = Commands(uri, user, password)
    result = n.get_all_vendor_connections(vendor_name)
    n.close()
    return result


@app.get("/unique_employees")
def get_unique_employees(vendor_name: str) -> int:
    """
    Endpoint to list the number of unique employees a given
    vendor's data covers

    Args:
        vendor_name (str): vendor's name

    Returns:
        int: number of employees
        # TODO: return error message if vendor does not exist
        # TODO: plan out JSON return structure
        # TODO: use get_all_vendor_connections to return all client nodes
        # TODO: iterate over them and reformat to add up customers
    """
    n = Commands(uri, user, password)
    result = n.get_all_vendor_connections(vendor_name)
    n.close()
    return result
