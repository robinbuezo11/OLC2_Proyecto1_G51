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