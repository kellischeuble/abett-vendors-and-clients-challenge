

def delete_all():
    """
    MATCH (n) 
    DELETE n
    """

def create_vendor(vendor_name):
    """
    CREATE (v:Vendor) {name:{vendor_name}}) 
    RETURN v
    """

def get_vendor(vendor_name):
    """
    MATCH (v:Vendor) 
    WHERE v.name = {vendor_name} 
    RETURN v
    """

def update_vendor(vendor_name, property, updated_value):
    """
    MATCH (v:Vendor) 
    WHERE v.name = {vendor_name}
    SET v.{property} = {updated_value}
    """


def delete_vendor(vendor_name):
    """
    MATCH (v:Vendor) 
    WHERE v.name = {vendor_name} 
    DELETE v
    """

def create_client(client_name):
    """
    CREATE (c.Client) {name: client_name, emp_count:client.employee_count}) 
    RETURN c
    """

def get_client(client_name):
    """
    MATCH (c:Client) 
    WHERE c.name = {client_name} 
    RETURN c
    """

def update_client(client_name, property, new_value):
    """ 
    MATCH (c:Client) 
    WHERE c.name = {client_name}
    SET p.{property} = {new_value}
    """

def delete_client(client_name):
    """
    MATCH (c.Client) 
    WHERE c.name = client_name 
    DELETE c
    """

def add_relationship(vendor_name, client_name, direction, frequency):
    
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
