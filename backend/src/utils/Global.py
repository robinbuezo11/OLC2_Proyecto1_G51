from utils.ManageXml import ManageXml

xml = ManageXml("..\\backend\\files\\data.xml")

def setUsedDatabase(database: str) -> None:
    global usedDatabase
    usedDatabase = database

def getUsedDatabase() -> str:
    return usedDatabase