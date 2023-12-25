class C3DGen:
    def __init__(self):
        self.labelCount: int = 0
        self.temporalCount: int = 0
        self.name: str
        self.C3DCode: list = []
        self.C3DCall: list = []
        self.C3DNatives: list = []
        self.C3DFunctions: list = []
        self.C3DGlobals: list = []
        self.temporalsSaved: dict[str, str] = {}
        self.temporals: list = []
        self.declarations: list = []
        