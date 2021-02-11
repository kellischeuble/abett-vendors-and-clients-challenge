from fastapi import FastAPI
from src.db import Commands

#from neo4j import GraphDatabase
uri = "bolt://localhost:7687"
user = "neo4j"
password = "abcd1234"

app = FastAPI()


def return_vendor(tx, name):
    tx.run("MATCH (v:Vendor) "
            "WHERE v.name = $name "
            "RETURN v", name = name)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/create_vendor")
def create_vendor(vendor_name: str):
    n = Commands(uri, user, password)
    result = n.create_vendor(vendor_name)
    n.close()
    return result
    
@app.get("/get_vendor")
def get_vendor(vendor_name: str):
    n = Commands(uri, user, password)
    result = n.get_vendor(vendor_name)
    n.close()
    return result

@app.post("/update_vendor")
def update_vendor(vendor_name: str, property: str, updated_value: str):
    n = Commands(uri, user, password)
    result = n.update_vendor(vendor_name, property, updated_value)
    n.close()
    return result

@app.post("/delete_vendor") 
def delete_vendor(vendor_name: str):
    n = Commands(uri, user, password)
    result = n.delete_vendor(vendor_name)
    n.close()
    return result

@app.post("/create_client") 
def create_client(client_name: str, employee_count: int):
    n = Commands(uri, user, password)
    result = n.create_client(client_name, employee_count)
    n.close()
    return result

@app.get("/get_client")
def get_client(client_name: str):
    n = Commands(uri, user, password)
    result = n.get_client(client_name)
    n.close()
    return result

@app.post("/update_client")
def update_client(client_name: str, property: str, new_value: str):
    n = Commands(uri, user, password)
    result = n.update_client(client_name, property, new_value)
    n.close()
    return result

@app.post("/delete_client")
def delete_client(client_name:str):
    n = Commands(uri, user, password)
    result = n.delete_client(client_name)
    n.close()
    return result

@app.post("/add_relationship")
def create_transfer(vendor_name:str, client_name:str, direction:str, frequency:str):
    n = Commands(uri, user, password)
    result = n.create_transfer(vendor_name, client_name, direction, frequency)
    n.close()
    return result

@app.get("/get_vendors") 
def get_list_of_vendors(client_name: str):

    n = Commands(uri, user, password)
    outputs = n.get_list_of_output_vendors(client_name)
    inputs = n.get_list_of_input_vendors(client_name)
    # TODO: create function to reformat outputs & inputs
    n.close()
    return outputs + inputs

# Change name
@app.get("/get_delivery_schedule")
def get_delivery_schedule(vendor_name: str):
    """ 
    List the delivery schedule(s) to/from the clients to which the vendor
    is connected
    """
    """ 
    MATCH (v:Vendor {name: "Kelli"})-[r:Transfer]-(c)
    RETURN *
    ORDER BY c.name
    """
    n = Commands(uri, user, password)
    result = n.get_delivery_schedule(vendor_name)
    n.close()
    return result
    

@app.get("/unique_employees{vendor_name}")
def get_unique_employees(vendor_name: str):
    pass