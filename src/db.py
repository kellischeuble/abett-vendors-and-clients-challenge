from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable
import logging

# TODO: these methods are repetitive.. 
# there's definitely a way to create one method so that I don't
# have to repeat that code

class Commands:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        """
        Method to close driver connection
        """
        self.driver.close()           

    def create_vendor(self, vendor_name):
        # TODO: Make sure vendors aren't added twice
        with self.driver.session() as session:
            return session.write_transaction(
                self._create_and_return_vendor, vendor_name
            )

    @staticmethod
    def _create_and_return_vendor(tx, vendor_name):
        query = (
            "CREATE (v:Vendor {name: $vendor_name}) "
            "RETURN v"
        )
        result = tx.run(query, vendor_name=vendor_name)
        try:
            return [{"v": record["v"]["name"]} for record in result]
        except ServiceUnavailable as exception:
            logging.error(f"{query} raised an error: \n {exception}")
            raise

    def create_client(self, client_name, employee_count):
        # TODO: Make sure clients aren't added twice
        with self.driver.session() as session:
            return session.write_transaction(
                self._create_and_return_client, client_name, employee_count
            )

    @staticmethod
    def _create_and_return_client(tx, client_name, employee_count):
        query = (
            "CREATE (c:Client {name: $client_name, employee_count: $employee_count}) "
            "RETURN c"
        )
        result = tx.run(query, client_name=client_name, employee_count=employee_count)
        try:
            return [{"c": record["c"]["name"]} for record in result]
        except ServiceUnavailable as exception:
            logging.error(f"{query} raised an error: \n {exception}")
            raise

    def get_vendor(self, vendor_name):
        with self.driver.session() as session:
            return session.write_transaction(
                self._get_and_return_vendor, vendor_name
            )

    @staticmethod
    def _get_and_return_vendor(tx, vendor_name):
        query = (
            "MATCH (v:Vendor) "
            "WHERE v.name = $vendor_name "
            "RETURN v"
        )
        result = tx.run(query, vendor_name=vendor_name)
        try:
            return [{"v": record["v"]} for record in result]
        except ServiceUnavailable as exception:
            logging.error(f"{query} raised an error: \n {exception}")
            raise

    def get_client(self, client_name):
        with self.driver.session() as session:
            return session.write_transaction(
                self._get_and_return_client, client_name
            )

    @staticmethod
    def _get_and_return_client(tx, client_name):
        query = (
            "MATCH (c:Client) "
            "WHERE c.name = $client_name "
            "RETURN c"
        )
        result = tx.run(query, client_name=client_name)
        try:
            return [{"c": record["c"]} for record in result]
        except ServiceUnavailable as exception:
            logging.error(f"{query} raised an error: \n {exception}")
            raise

    def update_vendor(self, vendor_name, property, updated_value):
        with self.driver.session() as session:
            return session.write_transaction(
                self._update_and_return_vendor, vendor_name, property, updated_value
            )

    # TODO: First check and make sure that vendor exists
    @staticmethod
    def _update_and_return_vendor(tx, vendor_name, property, updated_value):
        query = (
            "MATCH (v:Vendor) "
            "WHERE v.name = $vendor_name "
            "SET v.name = $updated_value "
            "RETURN v"
        )
        result = tx.run(query, vendor_name=vendor_name, property=property, updated_value=updated_value)
        try:
            return [{"v": record["v"]} for record in result]
        except ServiceUnavailable as exception:
            raise

    def delete_vendor(self, vendor_name):
        with self.driver.session() as session:
            return session.write_transaction(
                self._delete_vendor, vendor_name
            )

    @staticmethod
    def _delete_vendor(tx, vendor_name):
        query = (
            "MATCH (v:Vendor) "
            "WHERE v.name = $vendor_name "
            "DETACH DELETE v"
        )
        return tx.run(query, vendor_name=vendor_name)

    def update_client(self, client, property, updated_value):
        with self.driver.session() as session:
            return session.write_transaction(
                self._update_and_return_client, client, property, updated_value
            )

    # TODO: First check and make sure that vendor exists
    @staticmethod
    def _update_and_return_client(tx, client, property, updated_value):
        if property == "name":
            query = (
                "MATCH (c:Client) "
                "WHERE c.name = $client "
                "SET c.name = $updated_value "
                "RETURN c"
            )
        elif property == "employee_count":
            query = (
                "MATCH (c:Client) "
                "WHERE c.name = $client "
                "SET c.employee_count = $updated_value "
                "RETURN c"
            )
        result = tx.run(query, client=client, property=property, updated_value=updated_value)
        try:
            return [{"c": record["c"]} for record in result]
        except ServiceUnavailable as exception:
            raise


    def delete_client(self, client_name):
        with self.driver.session() as session:
            return session.write_transaction(
                self._delete_client, client_name
            )

    @staticmethod
    def _delete_client(tx, client_name):
        query = (
            "MATCH (c:Client) "
            "WHERE c.name = $client_name "
            "DETACH DELETE c"
        )
        return tx.run(query, client_name=client_name)

    
    def create_transfer(self, vendor_name, client_name, direction, frequency):
        with self.driver.session() as session:
            return session.write_transaction(
                self._add_client_vendor_transfer, vendor_name, client_name, direction, frequency
            )
            

    @staticmethod
    def _add_client_vendor_transfer(tx, vendor_name:str, client_name:str, direction:str, frequency:str):
        """
        Method with the query to add a transfer realtionship between vendor and client

        Args:
            vendor_name (str): vendor's name
            client_name (str): client's name
            direction (str): direction of transfer in relation to the customer -
                            must be "in" or "out"
            frequency (str): frequency of transfer - must be "daily", "weekly", or "monthly"
        """
        # TODO: Also make sure that frequency is in [daily, monthly, weekly]
        if direction.lower().strip() == "in":
            query = (
                "MATCH (v:Vendor) "
                "WHERE v.name = $vendor_name "
                "MATCH (c:Client) "
                "WHERE c.name = $client_name "
                "CREATE (v)-[:Transfer {frequency:$frequency}]->(c) "
                "RETURN v"
            )
        elif direction.lower().strip() == "out":
            query = (
                "MATCH (v:Vendor) "
                "WHERE v.name = $vendor_name "
                "MATCH (c:Client) "
                "WHERE c.name = $client_name "
                "CREATE (v)<-[:Transfer {frequency:$frequency}]-(c) "
                "RETURN v"
            )
        else:
            return "DIRECTION MUST BE 'in' or 'out'"
        return tx.run(query, vendor_name=vendor_name, client_name=client_name, direction=direction, frequency=frequency)


    def get_list_of_output_vendors(self, client_name):
        with self.driver.session() as session:
            return session.write_transaction(
                self._get_and_return_output_vendors, client_name
            )

    @staticmethod
    def _get_and_return_output_vendors(tx, client_name:str):
        """
        Mathod to return all of the vendors and outgoing relationships
        for a given client
        """
        query = (
            "MATCH (c:Client {name: $client_name})-[r:Transfer]->(v) "
            "RETURN * "
            "ORDER BY r.schedule"
        )
        return tx.run(query, client_name=client_name)


    def get_list_of_input_vendors(self, client_name):
        with self.driver.session() as session:
            return session.write_transaction(
                self._get_and_return_output_vendors, client_name
            )

    @staticmethod
    def _get_and_return_input_vendors(tx, client_name):
        """
        Method to reutrn all of the vendors and ingoing relationships
        for a given client
        """
        query = (
            "MATCH (c:Client {name: $client_name})<-[r:Transfer]-(v) "
            "RETURN * "
            "ORDER BY r.schedule"
        )
        return tx.run(query, client_name=client_name)

    def get_all_vendor_connections(self, vendor_name):
        with self.driver.session() as session:
            return session.write_transaction(
                self._get_and_return_all_connections, vendor_name
            )

    @staticmethod
    def _get_and_return_all_vendor_connections(tx, vendor_name):
        """
        mathod to return all of the connections a vendor may have
        """
        query = (
            "MATCH (v:Vendor {name: $vendor_name})-[r:Transfer]-(c)"
            "RETURN * "
            "ORDER BY c.name"
            ""
        )
        return tx.run(query, vendor_name=vendor_name)

    def get_all_client_connections(self, client_name):
        with self.driver.session() as session:
            return session.write_transaction(
                self._get_and_return_all_connections, client_name
            )

    @staticmethod
    def _get_and_return_all_client_connections(tx, client_name):
        """
        Method to return all of the connections a client may have
        """
        query = (
            "MATCH (c:Client {name: $client_name})-[r:Transfer]-(v)"
            "RETURN c"
            ""
        )
        return tx.run(query, client_name=client_name)
