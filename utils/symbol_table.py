from sys import maxsize

class Symbol:
    def __init__(self, name, type):
        self.name = name
        self.type = type

    def __repr__(self):
        return f"Symbol(name='{self.name}', type='{self.type}')"

class VariableSymbol(Symbol):
    def __init__(self, name, type):
        super().__init__(name, type)

class VectorSymbol(VariableSymbol):
    def __init__(self, name, type, size=maxsize):
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

    # Function to add a symbol to the symbols dictionary
    def put(self, symbol):
        # Check if the symbol name is already in the symbols dictionary
        if symbol.name in self.symbols:
            # If the symbol exists, return False
            return False
        else:
            # If the symbol doesn't exist, add it to the symbols dictionary
            self.symbols[symbol.name] = symbol
            # Return True to indicate successful addition of the symbol
            return True
    
    # Function to check if a symbol exists in the symbols dictionary
    def is_exist(self, name):
        # Check if the symbol name is in the symbols dictionary
        if name in self.symbols:
            # If the symbol exists, return True
            return True
        else:
            # If the symbol doesn't exist, return False
            return False
    
    # Function to get a symbol from the symbols dictionary
    def get(self, name, check_parent=True, check_children=False):
        # Check if the symbol name is in the symbols dictionary
        if name in self.symbols:
            # If the symbol exists, return it
            return self.symbols[name]
        elif check_parent and self.parent:
            # If the symbol doesn't exist in the current dictionary but check_parent is enabled and a parent dictionary exists,
            # recursively call the get function on the parent dictionary
            return self.parent.get(name)
        else:
            # If the symbol doesn't exist and there are no parents to check, return None
            return None
    
        

    def getParentScope(self):
        return self.parent

    def __repr__(self):
        return f"SymbolTable(name='{self.name}', symbols={self.symbols})\n\n, children={self.children})"
