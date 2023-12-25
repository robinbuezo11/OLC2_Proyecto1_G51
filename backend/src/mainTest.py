from utils.ManageXml import ManageXml

def main():
    xml = ManageXml("backend\\files\\data.xml")

    # xml.createDataBase("test")
    # xml.createTable("test", "demo")
    # xml.createTable("test", "tablaprueba")

    # xml.createColumn("test", "demo", "id", "int")
    # xml.createColumn("test", "demo", "name", "str")
    # xml.createColumn("test", "demo", "hint", "str")

    # xml.createRow("test", "demo", [{"value": 1, "column": 'id'}, {"value": 'Grupo51', "column": 'name'}, {"value": 'Los Cabrones', "column": 'hint'}])
    # xml.createRow("test", "demo", [{"value": 2, "column": 'id'}, {"value": 'Grupo511', "column": 'name'}, {"value": 'Los Cabroness', "column": 'hint'}])
    # xml.createRow("test", "demo", [{"value": 3, "column": 'id'}, {"value": 'Grupo5111', "column": 'name'}, {"value": 'Los Cabronesss', "column": 'hint'}])
    # xml.createRow("test", "demo", [{"value": 4, "column": 'id'}, {"value": 'Grupo51111', "column": 'name'}, {"value": 'Los Cabronessss', "column": 'hint'}])
    
    # xml.createDataBase("test2")
    # xml.createTable("test2", "demo2")

    # xml.createColumn("test2", "demo2", "id", "int")
    # xml.createColumn("test2", "demo2", "name", "str")
    # xml.createColumn("test2", "demo2", "hint", "str")

    #xml.createRow("test2", "demo2", [{"value": 2, "column": 'id'}, {"value": 'Grupo515', "column": 'name'}, {"value": 'XD', "column": 'hint'}])

    #xml.dropDatabase("test2")
    #xml.insert("test", "demo2", [{"value": 1, "column": 'id'}, {"value": 'Grupo51555555', "column": 'name'}, {"value": 'XDXXXDDD', "column": 'hint'}])
    
    #xml.alterTable("test", "demo", "demo2")
    #xml.truncate("test", "demo2")

    #xml.dropDatabase("test")
    #xml.updateRow("test", "demo", [{"value": 1, "column": 'id'}, {"value": 'Grupo51', "column": 'name'}, {"value": 'Hola', "column": 'hint'}])
    #xml.deleteRow("test", "demo", [{"value": 1, "column": 'id'}, {"value": 'Grupo51', "column": 'name'}, {"value": 'Los Cabrones', "column": 'hint'}])
    #xml.deleteRow("test", "demo", [{"value": 2, "column": 'id'}])
    xml.deleteRow("test", "demo", [{"value": 'Grupo5111', "column": 'name'}, {"value": 'Los Cabronesss', "column": 'hint'}])
    #xml.deleteColumn("test", "demo2", "id")
    #xml.deleteColumn("test", "demo2", "name")
    #rows = xml.select("test", "demo")

    #xml.select("test", "demo")
    #xml.updateRow("test", "demo2", [{"value": 2, "column": 'id'}, {"value": 'Grupo515', "column": 'name'}, {"value": 'XD', "column": 'hint'}])
    
#<<<<<<< HEAD
    #salidaWhere = xml.selectWhere("test", "demo", [{"column": 'id', "value": 4}, {"column": 'name', "value": 'Grupo51111'}])
    #salidaWhere1 = xml.selectWhere("test", "demo", [{"column": 'id', "value": 3}])
    #salidaWhere2 = xml.selectWhere("test", "demo", [{"column": 'id', "value": 2}])
    #print(salidaWhere)
    #print(salidaWhere1)
    #print(salidaWhere2)
#=======
    # salidaWhere = xml.selectWhere("test", "demo", [{"column": 'id', "value": 4}, {"column": 'name', "value": 'Grupo51111'}])
    # salidaWhere1 = xml.selectWhere("test", "demo", [{"column": 'id', "value": 3}])
    # salidaWhere2 = xml.selectWhere("test", "demo", [{"column": 'id', "value": 2}])
    # print(salidaWhere)
    # print(salidaWhere1)
    # print(salidaWhere2)
#>>>>>>> d6de5daf695121cadf9236295fc7452aa41cfb5c

    # xml.select("test", "demo")
    # rows = xml.select("test", "demo")
    # Obtener las columnas únicas
    # data = []
    # columns = []
    # for row in rows[0]:
    #    columns.append(row.get("column"))
    # data.append(columns)  
    # for row in rows:
    #    values = []
    #    for value in row:
    #        values.append(value['value'])
    #    data.append(values)    
    # print(data)
    #xml.createDataBase("test")

main()