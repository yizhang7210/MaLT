# MaLT Development Guideline

MaLT has a relatively straightforward development process.

### Development
Write quality, modular code. Do the right thing.

### Documentation
Each package (including test packages) must have a brief description in its
`__init__.py` file. Each module, class, method, function must have its
appropriate doc string. High level documentations reside in the `docs`
directory.

### Tests
We use `nose` for unit testing. Make sure any module has a corresponding test
file in the appropriate `test` directory that tests the major functionalities
of the module. Make sure all tests pass when running `nosetests -v malt` under
the root directory.

### Lint
We use pylint for styling and static analysis. Make sure the pylint results
contain `TODO`s only when running `pylint malt` under the root directory.

### Related information
- For details about MaLT's software architecture,
see [MaLT Architecture](architecture.md).
- For details about MaLT's individual packages,
see their corresponding `__init__.py` files.


