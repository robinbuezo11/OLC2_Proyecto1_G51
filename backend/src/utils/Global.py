from utils.ManageXml import ManageXml

xml = ManageXml("backend\\files\data.xml")
global usedDatabase
usedDatabase = None

def setUsedDatabase(database: str) -> None:
    global usedDatabase
    usedDatabase = database

def getUsedDatabase() -> str:
    global usedDatabase
    return usedDatabase