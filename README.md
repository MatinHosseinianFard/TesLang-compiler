# Teslang Compiler

This is a compiler project for the Teslang programming language. The compiler is designed to perform three main stages: lexical analysis, semantic analysis, and intermediate code generation.

## Features

The Teslang compiler incorporates the following features:

1. **Lexical Analysis**: The first stage of the compiler is responsible for tokenizing the input source code and performing lexical analysis. It breaks down the source code into a stream of tokens based on the Teslang language syntax.

2. **Semantic Analysis**: The second stage of the compiler focuses on analyzing the meaning and correctness of the source code. It checks for semantic errors, performs type checking, and enforces language-specific rules and constraints.

3. **Intermediate Code Generation**: The final stage of the compiler involves generating intermediate code representation from the validated source code. This intermediate code can be further processed and optimized for execution on a specific target platform.

Additional Features:

- **Forward Referencing**: The compiler supports forward referencing, allowing references to identifiers before their declaration within the source code.

- **Error Correction and Handling**: The compiler includes mechanisms to detect and handle errors encountered during the compilation process. It provides meaningful error messages to aid in debugging and improving the code.
- **Scope**: The compiler manages variable scoping, ensuring that variables are properly declared and accessed within their respective scopes.
- **Nested Functions**: The Teslang language supports nested functions, and the compiler handles their parsing, scoping, and code generation.

## Usage

To use the Teslang compiler, follow these steps:

1. Clone the repository:
```https://github.com/MatinHosseinianFard/TesLang-compiler.git```

2. Create a virtual environment:
‍‍‍‍```python3 -m venv venv```

3. Activate the virtual environment

4. Install the required dependencies:
```pip install -r requirements.txt```

5. Execute the `compile.py` file to compile the Teslang source code:
```python compile.py```

After the compilation process is complete, the intermediate code will be generated in the `generated_IR.out` file. You can execute this intermediate code using the Teslang Virtual Machine (tsvm) available at [https://github.com/aligrudi/tsvm](https://github.com/aligrudi/tsvm).

To execute the intermediate code using tsvm, follow these steps:

1. Download and compile the `tsvm.c` file.
2. Run the compiled `tsvm` executable with the following command:
```tsvm generated_IR.out```


Thanks to [mtnrzna](https://github.com/mtnrzna)
