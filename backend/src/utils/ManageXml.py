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
        # Verificar si la base de datos ya existe
        existing_database = next((db for db in self.__root if db.get("name") == name), None)
        if existing_database:
            print(f"La base de datos '{name}' ya existe.")
            return False

        # Crear nueva base de datos
        new_database = ET.SubElement(self.__root, "database")
        new_database.set("name", name)

        self.writeXml()
        print(f"Nueva base de datos '{name}' creada exitosamente.")
        return True

    def createTable(self, database, name):
        # Verificar si la base de datos existe
        db_to_modify = next((db for db in self.__root if db.get("name") == database), None)
        if db_to_modify is None:
            print(f"La base de datos '{database}' no existe.")
            return False

        # Verificar si la tabla ya existe en la base de datos
        table_exists = any(tb.get("name") == name for tb in db_to_modify)
        if table_exists:
            print(f"La tabla '{name}' ya existe en la base de datos '{database}'.")
            return False

        # Crear nueva tabla en la base de datos
        new_table = ET.SubElement(db_to_modify, "table")
        new_table.set("name", name)

        self.writeXml()
        print(f"Nueva tabla '{name}' creada en la base de datos '{database}' exitosamente.")
        return True


    def createColumn(self, database, table, name, type):
        # Verificar si la base de datos existe
        db_to_modify = next((db for db in self.__root if db.get("name") == database), None)
        if db_to_modify is None:
            print(f"La base de datos '{database}' no existe.")
            return False

        # Verificar si la tabla ya existe en la base de datos
        table_exists = any(tb.get("name") == table for tb in db_to_modify)
        if not table_exists:
            print(f"La tabla '{table}' no existe en la base de datos '{database}'.")
            return False

        # Verificar si la columna ya existe en la tabla
        column_exists = any(col.get("name") == name for tb in db_to_modify if tb.get("name") == table for col in tb.findall("column"))
        if column_exists:
            print(f"La columna '{name}' ya existe en la tabla '{table}'.")
            return False

        # Crear nueva columna en la tabla
        new_column = ET.SubElement(db_to_modify, table)
        new_column.set("name", name)
        new_column.set("type", type)

        self.writeXml()
        print(f"Nueva columna '{name}' creada en la tabla '{table}' de la base de datos '{database}' exitosamente.")
        return True

    def createRow(self, database, table, data):
        # Verificar si la base de datos existe
        db_to_modify = next((db for db in self.__root if db.get("name") == database), None)
        if db_to_modify is None:
            print(f"La base de datos '{database}' no existe.")
            return False

        # Verificar si la tabla ya existe en la base de datos
        table_exists = any(tb.get("name") == table for tb in db_to_modify)
        if not table_exists:
            print(f"La tabla '{table}' no existe en la base de datos '{database}'.")
            return False

        # Verificar si ya existe una fila con los mismos valores en la tabla
        existing_rows = [row for tb in db_to_modify if tb.get("name") == table for row in tb.findall("row")]
        if existing_rows:
            for existing_row in existing_rows:
                existing_values = [{"column": value.get("column"), "value": value.text} for value in existing_row.findall("value")]
                if existing_values == data:
                    print("Ya existe una fila con los mismos valores en la tabla.")
                    return False

        # Crear nueva fila en la tabla
        new_row = ET.SubElement(db_to_modify, table)
        for d in data:
            value = ET.SubElement(new_row, "value")
            value.set("column", d["column"])
            value.text = str(d["value"])

        self.writeXml()
        print(f"Nueva fila creada en la tabla '{table}' de la base de datos '{database}' exitosamente.")
        return True

    def select(self, database, table):
        # Verificar si la base de datos existe
        db_to_select = next((db for db in self.__root if db.get("name") == database), None)
        if db_to_select is None:
            print(f"La base de datos '{database}' no existe.")
            return None

        # Verificar si la tabla existe en la base de datos
        table_to_select = next((tb for tb in db_to_select if tb.get("name") == table), None)
        if table_to_select is None:
            print(f"La tabla '{table}' no existe en la base de datos '{database}'.")
            return None

        rows = []
        for row in table_to_select.findall("row"):
            values = []
            for value in row.findall("value"):
                values.append({"column": value.get("column"), "value": value.text})
            if len(values) > 0:
                rows.append(values)

        # Mostrar los resultados en la consola
        if len(rows) > 0:
            for row in rows:
                print(row)
            return rows
        else:
            print("No hay datos en la tabla.")
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
    
    def deleteColumn(self, database, table, columns):
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

        # Eliminar columnas de la tabla
        for row in table_to_modify.findall("row"):
            values = row.findall("value")
            for value in values:
                column_name = value.get("column")
                if column_name in columns:
                    row.remove(value)

        self.writeXml()
        print(f"Columnas eliminadas en la tabla '{table}' de la base de datos '{database}' exitosamente.")
        return True

    def deleteRow(self, database, table, columns):
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

        # Eliminar filas de la tabla
        for row in table_to_modify.findall("row"):
            values = row.findall("value")
            for value in values:
                column_name = value.get("column")
                if column_name in columns:
                    row.remove(value)

        self.writeXml()
        print(f"Datos eliminados en la tabla '{table}' de la base de datos '{database}' exitosamente.")
        return True
    

