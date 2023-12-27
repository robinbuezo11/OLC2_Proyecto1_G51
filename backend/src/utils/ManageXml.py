import xml.etree.ElementTree as ET
import os
from statements.Env.Env import Env
import re
from datetime import datetime

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
        except Exception as e:
            print("Error: No se pudo cargar ni crear el archivo xml" + str(e))

    def getTree(self):
        return self.__tree
    
    def getRoot(self):
        return self.__root
    
    def getStruct(self):
        struct = []
        for db in self.__root:
            struct.append({
                'name': db.get('name'),
                'child': self.getTables(db),
                'type': 'database',
                'level': '0'
            })
        return struct
    
    def getTables(self, db):
        tables = []
        for table in db:
            tables.append({
                'name': table.get('name'),
                'child': self.getColumns(table),
                'type': 'table',
                'level': '1'
            })
        return tables
    
    def getColumns(self, table):
        columns = []
        for column in table:
            if column.tag == 'column':
                columns.append({
                    'name': column.get('name'),
                    'type': 'column',
                    'dataType': column.get('type'),
                    'level': '2'
                })
        return columns
    
    def writeXml(self):
        self.__tree.write(self.__path, encoding="utf-8", xml_declaration=True)

    def createDataBase(self, name):
        # Verificar si la base de datos ya existe
        existing_database = next((db for db in self.__root if db.get("name") == name), None)
        if existing_database is not None:
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
        table_to_modify = next((tb for tb in db_to_modify if tb.get("name") == table), None)
        if table_to_modify is None:
            print(f"La tabla '{table}' no existe en la base de datos '{database}'.")
            return False

        # Verificar si la columna ya existe en la tabla
        column_exists = any(col.get("name") == name for col in table_to_modify.findall("column"))
        if column_exists:
            print(f"La columna '{name}' ya existe en la tabla '{table}'.")
            return False

        # Crear nueva columna en la tabla
        new_column = ET.SubElement(table_to_modify, "column")
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
        table_to_modify = next((tb for tb in db_to_modify if tb.get("name") == table), None)
        if table_to_modify is None:
            print(f"La tabla '{table}' no existe en la base de datos '{database}'.")
            return False

        # Convertir las filas existentes a conjuntos para facilitar la comparación
        existing_rows = [{value.get("column"): value.text for value in row.findall("value")} for row in table_to_modify.findall("row")]

        # Convertir la nueva fila a un conjunto
        new_row_values = {d["column"]: str(d["value"]) for d in data}

        # Verificar si ya existe una fila con los mismos valores en la tabla
        if new_row_values in existing_rows:
            print("Ya existe una fila con los mismos valores en la tabla.")
            return False

        # Crear nueva fila en la tabla
        new_row = ET.SubElement(table_to_modify, "row")
        for d in data:
            value = ET.SubElement(new_row, "value")
            value.set("column", d["column"])
            value.text = str(d["value"])

        self.writeXml()
        print(f"Nueva fila creada en la tabla '{table}' de la base de datos '{database}' exitosamente.")
        return True

    # def select(self, database, table):
    #     Verificar si la base de datos existe
    #     db_to_select = next((db for db in self.__root if db.get("name") == database), None)
    #     if db_to_select is None:
    #         print(f"La base de datos '{database}' no existe.")
    #         return None

    #     Verificar si la tabla existe en la base de datos
    #     table_to_select = next((tb for tb in db_to_select if tb.get("name") == table), None)
    #     if table_to_select is None:
    #         print(f"La tabla '{table}' no existe en la base de datos '{database}'.")
    #         return None

    #     rows = []
    #     for row in table_to_select.findall("row"):
    #         values = []
    #         for value in row.findall("value"):
    #             values.append({"column": value.get("column"), "value": value.text})
    #         if len(values) > 0:
    #             rows.append(values)

    #     Mostrar los resultados en la consola
    #     if len(rows) > 0:
    #         for row in rows:
    #             print(row)
    #         return rows
    #     else:
    #         print("No hay datos en la tabla.")
    #         return None
    
    # def execute_sql_function(func_name, row_values):
    #     Funciones SQL permitidas
    #     if func_name == "HOY":
    #         return datetime.now().strftime("%Y-%m-%d")
    #     elif func_name.startswith("SUBSTR"):
    #         Ejemplo: SUBSTR(column_name, start, length)
    #         match = re.match(r"SUBSTR\((\w+),(\d+),(\d+)\)", func_name)
    #         if match:
    #             column_name, start, length = match.groups()
    #             column_value = row_values.get(column_name, "")
    #             return column_value[int(start):int(start) + int(length)]
    #     Puedes agregar más funciones según sea necesario

    #     Si no se encuentra la función, devolver el valor original
    #     return func_name

    # def selectConFunciones(self, database, sql_query):
    #     Verificar si la base de datos existe
    #     db_to_select = next((db for db in self.__root if db.get("name") == database), None)
    #     if db_to_select is None:
    #         print(f"La base de datos '{database}' no existe.")
    #         return None

    #     Extraer columnas y tabla de la consulta SQL
    #     match = re.match(r"SELECT (.+?) FROM (.+)", sql_query)
    #     if not match:
    #         print("Consulta SQL no válida.")
    #         return None

    #     columns, table = match.groups()

    #     Convertir nombres de columnas a lista
    #     columns = [col.strip() for col in columns.split(",")]

    #     Verificar si la tabla existe en la base de datos
    #     table_to_select = next((tb for tb in db_to_select if tb.get("name") == table), None)
    #     if table_to_select is None:
    #         print(f"La tabla '{table}' no existe en la base de datos '{database}'.")
    #         return None

    #     rows = []
    #     for row in table_to_select.findall("row"):
    #         row_values = {value.get("column"): value.text for value in row.findall("value")}
    #         result_row = {}
    #         for col in columns:
    #             if col.startswith("SUBSTR") or col == "HOY()":
    #                 Ejecutar funciones SQL
    #                 result_row[col] = execute_sql_function(col, row_values)
    #             else:
    #                 Obtener valores directos de las columnas
    #                 result_row[col] = row_values.get(col, None)
    #         rows.append(result_row)

    #     Mostrar los resultados en la consola
    #     if len(rows) > 0:
    #         for row in rows:
    #             print(row)
    #         return rows
    #     else:
    #         print("No hay datos en la tabla.")
    #         return None


    def selectWhere(self, database, table, conditions=None):
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

        # Filtrar las filas según las condiciones si se proporcionan
        if conditions:
            for row in table_to_select.findall("row"):
                row_values = {value.get("column"): value.text for value in row.findall("value")}
                if all(row_values.get(cond["column"]) == str(cond["value"]) for cond in conditions):
                    values = [{"column": value.get("column"), "value": value.text} for value in row.findall("value")]
                    if len(values) > 0:
                        rows.append(values)
        else:
            # Si no se proporcionan condiciones, seleccionar todas las filas
            for row in table_to_select.findall("row"):
                values = [{"column": value.get("column"), "value": value.text} for value in row.findall("value")]
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
    
    
    def alterDatabase(self, databaseOld, databaseNew):
        # Verificar si la base de datos existe
        db_to_modify = next((db for db in self.__root if db.get("name") == databaseOld), None)
        if db_to_modify is None:
            print(f"La base de datos '{databaseOld}' no existe.")
            return False

        # Verificar si la nueva base de datos ya existe
        existing_database = next((db for db in self.__root if db.get("name") == databaseNew), None)
        if existing_database is not None:
            print(f"La base de datos '{databaseNew}' ya existe.")
            return False

        # Cambiar el nombre de la base de datos
        db_to_modify.set("name", databaseNew)
        self.writeXml()
        print(f"El nombre de la base de datos '{databaseOld}' ha sido cambiado a '{databaseNew}' exitosamente.")
        return True

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

        # Eliminar las definiciones de columna de la tabla
        for col in table_to_modify.findall("column"):
            if col.get("name") in columns:
                table_to_modify.remove(col)

        self.writeXml()
        print(f"Columnas eliminadas en la tabla '{table}' de la base de datos '{database}' exitosamente.")
        return True

    def deleteRow(self, database, table, conditions):
        # Verificar si la base de datos existe
        db_to_modify = next((db for db in self.__root if db.get("name") == database), None)
        if db_to_modify is None:
            print(f"La base de datos '{database}' no existe.")
            return False

        # Verificar si la tabla ya existe en la base de datos
        table_to_modify = next((tb for tb in db_to_modify if tb.get("name") == table), None)
        if table_to_modify is None:
            print(f"La tabla '{table}' no existe en la base de datos '{database}'.")
            return False

        # Obtener las filas que coinciden con las condiciones especificadas
        rows_to_delete = [row for row in table_to_modify.findall("row") if self.matchesConditions(row, conditions)]

        # Verificar si se encontraron filas para eliminar
        if not rows_to_delete:
            print("No se encontraron filas que coincidan con las condiciones especificadas.")
            return False

        # Eliminar las filas encontradas
        for row_to_delete in rows_to_delete:
            table_to_modify.remove(row_to_delete)

        self.writeXml()
        print(f"Filas eliminadas de la tabla '{table}' de la base de datos '{database}' exitosamente.")
        return True

    def matchesConditions(self, row, conditions):
        # Verificar si la fila cumple con las condiciones especificadas
        row_values = {value.get("column"): value.text for value in row.findall("value")}
        return all(row_values.get(cond["column"]) == str(cond["value"]) for cond in conditions)
    


#------------------------------------- BD TO XML && XML TO BD -------------------------------------#
#----------------------------------- IN PROGRESS TO BE FINISHED -----------------------------------#
    
    def bdToXml(self, database: Env, name: str):
        try:
            # Verificar si la base de datos existe
            db_to_save = next((db for db in self.__root if db.get("name") == name), None)
            if db_to_save is None:
                self.createDataBase(name)
                db_to_save = next((db for db in self.__root if db.get("name") == name), None)
            
            return True
        except Exception as e:
            print(f"Error: No se pudo guardar la base de datos {name} en el archivo xml" + str(e))
            return False
        

    def xmlToBd(self, name: str):
        try:
            # Verificar si la base de datos existe
            db_to_load = next((db for db in self.__root if db.get("name") == name), None)
            if db_to_load is None:
                print(f"La base de datos '{name}' no existe.")
                return False

            return True
        except Exception as e:
            print(f"Error: No se pudo cargar la base de datos {name} en el archivo xml" + str(e))
            return False