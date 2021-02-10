from fastapi import FastAPI
from neo4j import GraphDatabase

app = FastAPI()
driver = GraphDatabase.driver("bolt://host[:7474]", auth=("neo4j", "abcd1234"))
driver.close()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/delete_all")
def delete_all():
    """
    MATCH (n) 
    DELETE n
    """
    return "deleted"

@app.put("/create_vendor{name}")
def create_vendor(vendor_name: str):
    """
    CREATE (v:Vendor) {name:{vendor_name}}) 
    RETURN v
    """
    pass

@app.get("/get_vendor{name}")
def get_vendor(vendor_name):
    """
    MATCH (v:Vendor) 
    WHERE v.name = {vendor_name} 
    RETURN v
    """
    pass

@app.put("/update_vendor{name}")
def update_vendor(vendor_name: str, property: str, updated_value: str):
    """
    MATCH (v:Vendor) 
    WHERE v.name = {vendor_name}
    SET v.{property} = {updated_value}
    """

@app.put("/delete_vendor{name}") # PUT OR POST?
def delete_vendor(vendor_name: str):
    """
    MATCH (v:Vendor) 
    WHERE v.name = {vendor_name} 
    DELETE v
    """

@app.put("/create_client{name}")
def create_client(client_name: str):
    """
    CREATE (c.Client) {name: client_name, emp_count:client.employee_count}) 
    RETURN c
    """

@app.get("/get_client{name}")
def get_client(client_name: str):
    """
    MATCH (c:Client) 
    WHERE c.name = {client_name} 
    RETURN c
    """

@app.put("/update_client{client_name}")
def update_client(client_name: str, property: str, new_value: str):
    """ 
    MATCH (c:Client) 
    WHERE c.name = {client_name}
    SET p.{property} = {new_value}
    """

@app.put("/delete_client{client_name}")
def delete_client(client_name:str):
    """
    MATCH (c.Client) 
    WHERE c.name = client_name 
    DELETE c
    """

@app.put("/add_relationship")
def add_relationship(vendor_name:str, client_name:str, direction:str, frequency:str):
    
    if direction == "input":
        """ 
        MATCH v:Vendor 
        WHERE v.name = {vendor_name}
        MATCH c:Client
        WHERE c.name = {client_name}
        CREATE (v)-[:{frequency}]->(c)
        """

    if direction == "output":
        """ 
        MATCH v:Vendor 
        WHERE v.name = {vendor_name}
        MATCH c:Client
        WHERE c.name = {client_name}
        CREATE (v)<-[:{frequency}]-(c)
        """

@app.get("/get_vendors{client_name}")
def list_vendors(client_name: str):
    """ 
    List vendors for each of Inputs and Outputs
    Order by Schedule frequency (1. Daily, 2. Weekly, 3. Monthly)
    """
    pass

@app.get("/get_clients{vendor_name}")
def list_clients(vendor_name: str):
    """ 
    List the delivery schedule(s) to/from the clients to which the vendor
    is connected
    """
    pass

@app.get("/unique_employees{vendor_name}")
def get_unique_employees(vendor_name: str):
    pass