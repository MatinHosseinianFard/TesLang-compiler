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

Thanks to [mtnrzna](https://github.com/mtnrzna)
