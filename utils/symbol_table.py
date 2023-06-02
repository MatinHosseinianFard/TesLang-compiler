class Symbol:
    def __init__(self, name, type):
        self.name = name
        self.type = type

    def __repr__(self):
        return f"Symbol(name='{self.name}', type='{self.type}')"

class VariableSymbol(Symbol):
    pass

class VectorSymbol(Symbol):
    def __init__(self, name, type, size):
        super().__init__(name, type)
        self.size = size

    def __repr__(self):
        return f"VectorSymbol(name='{self.name}', type='{self.type}', size={self.size})"

class FunctionSymbol(Symbol):
    def __init__(self, name, type, parameters):
        super().__init__(name, type)
        self.parameters = parameters

    def __repr__(self):
        return f"FunctionSymbol(name='{self.name}', type='{self.type}', parameters={self.parameters})"

class SymbolTable:
    def __init__(self, parent, name):
        self.symbols = {}
        self.name = name
        self.parent = parent
        self.children = []

        if parent:
            parent.children.append(self)

    def put(self, symbol):
        if symbol.name in self.symbols:
            return False
        else:
            self.symbols[symbol.name] = symbol
            return True

    def get(self, name, check_parent=True):
        if name in self.symbols:
            return self.symbols[name]
        elif check_parent and self.parent:
            return self.parent.get(name)
        else:
            return None

    def getParentScope(self):
        return self.parent

    def __repr__(self):
        return f"SymbolTable(name='{self.name}', symbols={self.symbols})\n\n, children={self.children})"
