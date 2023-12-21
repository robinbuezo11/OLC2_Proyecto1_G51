from utils.ManageXml import ManageXml

def main():
    xml = ManageXml("backend\\files\\data.xml")

    xml.createDataBase("test")
    xml.createTable("test", "demo")
    # xml.createTable("test", "tablaprueba")

    xml.createColumn("test", "demo", "id", "int")
    xml.createColumn("test", "demo", "name", "str")
    xml.createColumn("test", "demo", "hint", "str")

    xml.createRow("test", "demo", [{"value": 1, "column": 'id'}, {"value": 'Grupo51', "column": 'name'}, {"value": 'Los Cabrones', "column": 'hint'}])
    #xml.dropTable("test", "demo")
    #xml.insert("test", "demo", [{"value": 2, "column": 'id'}, {"value": 'Grupo515', "column": 'name'}, {"value": 'XD', "column": 'hint'}])
    
    #xml.alterTable("test", "demo2", "demo3")

    #xml.dropDatabase("test")
    xml.updateRow("test", "demo", [{"value": 255555, "column": 'id'}, {"value": 'Grupo515', "column": 'name'}, {"value": 'XD', "column": 'hint'}])
    
    #rows = xml.select("test", "demo")

    #xml.select("test", "demo")
    #
    #xml.update("test", "demo", [{"value": 2, "column": 'id'}, {"value": 'Grupo515', "column": 'name'}, {"value": 'XD', "column": 'hint'}])
    #xml.select("test", "demo")

    #rows = xml.select("test", "demo")
    ## Obtener las columnas únicas
    #data = []
#
    #columns = []
    #for row in rows[0]:
    #    columns.append(row.get("column"))
    #data.append(columns)  
    #for row in rows:
    #    values = []
    #    for value in row:
    #        values.append(value['value'])
    #    data.append(values)    
    #print(data)

main()