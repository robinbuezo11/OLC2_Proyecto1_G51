import xml.etree.ElementTree as ET
import os

class ManageXml:
    def __init__(self, path) -> None:
        self.__path = path
        self.__tree = None
        self.__root = None
        self.loadXml()

    def loadXml(self):
        try:
            if os.path.exists(self.__path):
                self.__tree = ET.parse(self.__path)
                self.__root = self.__tree.getroot()
            else:
                self.__root = ET.Element("root")
                self.__tree = ET.ElementTree(self.__root)
                self.writeXml()
        except:
            print("Error: No se pudo cargar ni crear el archivo xml")

        
    def getTree(self):
        return self.__tree
    
    def getRoot(self):
        return self.__root
    
    def writeXml(self):
        self.__tree.write(self.__path, encoding="utf-8", xml_declaration=True)

    def createDataBase(self, name):
        database = ET.SubElement(self.__root, "database")
        database.set("name", name)
        self.writeXml()

    def createTable(self, database, name):
        for db in self.__root:
            if db.get("name") == database:
                table = ET.SubElement(db, "table")
                table.set("name", name)
                self.writeXml()
                return True
        return False

    def createColumn(self, database, table, name, type):
        for db in self.__root:
            if db.get("name") == database:
                for tb in db:
                    if tb.get("name") == table:
                        column = ET.SubElement(tb, "column")
                        column.set("name", name)
                        column.set("type", type)
                        self.writeXml()
                        return True
        return False

    def createRow(self, database, table, data):
        for db in self.__root:
            if db.get("name") == database:
                for tb in db:
                    if tb.get("name") == table:
                        row = ET.SubElement(tb, "row")
                        for d in data:
                            value = ET.SubElement(row, "value")
                            value.set("column", d["column"])
                            value.text = str(d["value"])
                        self.writeXml()
                        return True
        return False
    

    def select(self, database, table):
        for db in self.__root:
            if db.get("name") == database:
                for tb in db:
                    if tb.get("name") == table:
                        rows = []
                        for row in tb:
                            values = []
                            for value in row:
                                values.append({"column": value.get("column"), "value": value.text})
                            if len(values) > 0:
                                rows.append(values)
                        return rows
        return None
    
    def dropDatabase(self, database):   
        # Verificar si la base de datos existe
        db_to_remove = next((db for db in self.__root if db.get("name") == database), None)
        if db_to_remove is None:
            print(f"La base de datos '{database}' no existe.")
            return False

        # Eliminar la base de datos
        self.__root.remove(db_to_remove)
        self.writeXml()
        print(f"La base de datos '{database}' ha sido eliminada exitosamente.")
        return True

    
    def dropTable(self, database, table):
        # Verificar si la base de datos existe
        db_to_modify = next((db for db in self.__root if db.get("name") == database), None)
        if db_to_modify is None:
            print(f"La base de datos '{database}' no existe.")
            return False

        # Verificar si la tabla existe en la base de datos
        table_to_remove = next((tb for tb in db_to_modify if tb.get("name") == table), None)
        if table_to_remove is None:
            print(f"La tabla '{table}' no existe en la base de datos '{database}'.")
            return False

        # Eliminar la tabla
        db_to_modify.remove(table_to_remove)
        self.writeXml()
        print(f"La tabla '{table}' ha sido eliminada de la base de datos '{database}' exitosamente.")
        return True
    
    def insert(self, database, table, data):
        # Verificar si la base de datos existe
        db_to_modify = next((db for db in self.__root if db.get("name") == database), None)
        if db_to_modify is None:
            print(f"La base de datos '{database}' no existe.")
            return False

        # Verificar si la tabla existe en la base de datos
        table_to_modify = next((tb for tb in db_to_modify if tb.get("name") == table), None)
        if table_to_modify is None:
            print(f"La tabla '{table}' no existe en la base de datos '{database}'.")
            return False

        # Insertar datos en la tabla
        row = ET.SubElement(table_to_modify, "row")
        for d in data:
            value = ET.SubElement(row, "value")
            value.set("column", d["column"])
            value.text = str(d["value"])
        
        self.writeXml()
        print(f"Datos insertados en la tabla '{table}' de la base de datos '{database}' exitosamente.")
        return True
    
    def alterTable(self, database, tableOld, tableNew):
    # Verificar si la base de datos existe
        db_to_modify = next((db for db in self.__root if db.get("name") == database), None)
        if db_to_modify is None:
            print(f"La base de datos '{database}' no existe.")
            return False

        # Verificar si la tabla existe en la base de datos
        table_to_modify = next((tb for tb in db_to_modify if tb.get("name") == tableOld), None)
        if table_to_modify is None:
            print(f"La tabla '{tableOld}' no existe en la base de datos '{database}'.")
            return False

        # Cambiar el nombre de la tabla
        table_to_modify.set("name", tableNew)
        self.writeXml()
        print(f"El nombre de la tabla '{tableOld}' ha sido cambiado a '{tableNew}' en la base de datos '{database}' exitosamente.")
        return True
    
    def truncate (self, database, table):
        # Verificar si la base de datos existe
        db_to_modify = next((db for db in self.__root if db.get("name") == database), None)
        if db_to_modify is None:
            print(f"La base de datos '{database}' no existe.")
            return False

        # Verificar si la tabla existe en la base de datos
        table_to_modify = next((tb for tb in db_to_modify if tb.get("name") == table), None)
        if table_to_modify is None:
            print(f"La tabla '{table}' no existe en la base de datos '{database}'.")
            return False

        # Eliminar todas las filas de la tabla
        for row in table_to_modify.findall("row"):
            table_to_modify.remove(row)

        self.writeXml()
        print(f"Todas las filas de la tabla '{table}' en la base de datos '{database}' han sido eliminadas exitosamente.")
        return True
    
    def updateRow(self, database, table, new_data):
        # Verificar si la base de datos existe
        db_to_modify = next((db for db in self.__root if db.get("name") == database), None)
        if db_to_modify is None:
            print(f"La base de datos '{database}' no existe.")
            return False

        # Verificar si la tabla existe en la base de datos
        table_to_modify = next((tb for tb in db_to_modify if tb.get("name") == table), None)
        if table_to_modify is None:
            print(f"La tabla '{table}' no existe en la base de datos '{database}'.")
            return False

        # Actualizar datos en la tabla
        for row in table_to_modify.findall("row"):
            for d in new_data:
                column_name = d["column"]
                value_text = str(d["value"])

                # Buscar el elemento "value" con la columna correspondiente y actualizar su texto
                value_to_update = next((value for value in row.findall("value") if value.get("column") == column_name), None)
                if value_to_update is not None:
                    value_to_update.text = value_text

        self.writeXml()
        print(f"Datos actualizados en la tabla '{table}' de la base de datos '{database}' exitosamente.")
        return True