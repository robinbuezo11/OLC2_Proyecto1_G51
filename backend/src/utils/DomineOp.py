from utils.Type import Type

plus = [
    [Type.BIT,      Type.INT,      Type.DECIMAL,  Type.NULL, Type.NULL, Type.NCHAR,    Type.NVARCHAR],
    [Type.INT,      Type.INT,      Type.DECIMAL,  Type.NULL, Type.NULL, Type.NCHAR,    Type.NVARCHAR],
    [Type.DECIMAL,  Type.DECIMAL,  Type.DECIMAL,  Type.NULL, Type.NULL, Type.NCHAR,    Type.NVARCHAR],
    [Type.NULL,     Type.NULL,     Type.NULL,     Type.NULL, Type.NULL, Type.NULL,     Type.NULL],
    [Type.NULL,     Type.NULL,     Type.NULL,     Type.NULL, Type.NULL, Type.NULL,     Type.NULL],
    [Type.NCHAR,    Type.NCHAR,    Type.NCHAR,    Type.NULL, Type.NULL, Type.NCHAR,    Type.NVARCHAR],
    [Type.NVARCHAR, Type.NVARCHAR, Type.NVARCHAR, Type.NULL, Type.NULL, Type.NVARCHAR, Type.NVARCHAR]
]

minus = [
    [Type.NULL,    Type.INT,     Type.DECIMAL, Type.NULL, Type.NULL, Type.NULL, Type.NULL],
    [Type.INT,     Type.INT,     Type.DECIMAL, Type.NULL, Type.NULL, Type.NULL, Type.NULL],
    [Type.DECIMAL, Type.DECIMAL, Type.DECIMAL, Type.NULL, Type.NULL, Type.NULL, Type.NULL],
    [Type.NULL,    Type.NULL,    Type.NULL,    Type.NULL, Type.NULL, Type.NULL, Type.NULL],
    [Type.NULL,    Type.NULL,    Type.NULL,    Type.NULL, Type.NULL, Type.NULL, Type.NULL],
    [Type.NULL,    Type.NULL,    Type.NULL,    Type.NULL, Type.NULL, Type.NULL, Type.NULL],
    [Type.NULL,    Type.NULL,    Type.NULL,    Type.NULL, Type.NULL, Type.NULL, Type.NULL]
]

mult = [
    [Type.BIT,     Type.INT,     Type.DECIMAL, Type.NULL,     Type.NULL,     Type.NULL,  Type.NULL],
    [Type.INT,     Type.INT,     Type.DECIMAL, Type.NULL,     Type.NULL,     Type.NULL,  Type.NULL],
    [Type.DECIMAL, Type.DECIMAL, Type.DECIMAL, Type.NULL,     Type.NULL,     Type.NULL,  Type.NULL],
    [Type.NULL,    Type.NULL,    Type.NULL,    Type.NULL,     Type.NULL,     Type.NCHAR, Type.NVARCHAR],
    [Type.NULL,    Type.NULL,    Type.NULL,    Type.NULL,     Type.NULL,     Type.NCHAR, Type.NVARCHAR],
    [Type.NULL,    Type.NULL,    Type.NULL,    Type.NCHAR,    Type.NCHAR,    Type.NULL,  Type.NULL],
    [Type.NULL,    Type.NULL,    Type.NULL,    Type.NVARCHAR, Type.NVARCHAR, Type.NULL,  Type.NULL]
]

div = [
    [Type.NULL,    Type.INT,     Type.DECIMAL, Type.NULL,     Type.NULL,     Type.NULL,  Type.NULL],
    [Type.INT,     Type.INT,     Type.DECIMAL, Type.NULL,     Type.NULL,     Type.NULL,  Type.NULL],
    [Type.DECIMAL, Type.DECIMAL, Type.DECIMAL, Type.NULL,     Type.NULL,     Type.NULL,  Type.NULL],
    [Type.NULL,    Type.NULL,    Type.NULL,    Type.NULL,     Type.NULL,     Type.NCHAR, Type.NVARCHAR],
    [Type.NULL,    Type.NULL,    Type.NULL,    Type.NULL,     Type.NULL,     Type.NCHAR, Type.NVARCHAR],
    [Type.NULL,    Type.NULL,    Type.NULL,    Type.NCHAR,    Type.NCHAR,    Type.NULL,  Type.NULL],
    [Type.NULL,    Type.NULL,    Type.NULL,    Type.NVARCHAR, Type.NVARCHAR, Type.NULL,  Type.NULL]
]