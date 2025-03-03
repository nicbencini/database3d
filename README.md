`database3d` is an SQL-based library for recursivly storing and retrieving class objects. It provides a set of tools to create, manage, and interact with SQLite databases.

## Features

- Create and manage SQLite database tables for class objects.
- Dynamically generate tables based on object attributes.
- Perform CRUD operations on the database.

## Installation

To install the library, clone the repository and install the dependencies:

```sh
git clone https://github.com/nicbencini/database3d.git
cd database3d
pip install -r requirements.txt
```

## Usage

### Creating a Model

To create a new model, instantiate the `Model` class with the required parameters:

```python
from database3d.database.model import Model

model = Model(file_path='path/to/database.db', user='username', overwrite=True)
```

### Building Tables

The `TablesMixin` class provides methods to build and manage tables in the SQLite database:

```python
model.build_tables()
```

### Adding Data

You can add data to the database by creating objects and saving them:

```python
from database3d.database.add_mixin import WriteMixin

class MyObject:
    def __init__(self, id, name, value):
        self._id = id
        self.name = name
        self.value = value

obj = MyObject(id=1, name='example', value=42)
model.add_object(obj)
```

### Retrieving Data

Retrieve data from the database using the `ReadMixin`:

```python
from database3d.database.get_mixin import ReadMixin

data = model.get_object(MyObject, id=1)
print(data.name, data.value)
```

### Updating Data

Update existing data in the database using the `UpdateMixin`:

```python
from database3d.database.update_mixin import UpdateMixin

obj.name = 'new_name'
model.update_object(obj)
```

### Deleting Data

Delete data from the database using the `DeleteMixin`:

```python
from database3d.database.delete_mixin import DeleteMixin

model.delete_object(MyObject, id=1)
```

## Documentation

The full documentation for the library can be found in the docs directory.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on GitHub.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

For any questions or issues, please contact Nicolo Bencini at nicbencini@gmail.com.

## Links

- [Homepage](https://github.com/nicbencini/database3d)
- [Issues](https://github.com/nicbencini/database3d/issues)
# License
Distributed under the MIT License. See LICENSE.txt for more information.

# Contact
Email: nicbencini@gmail.com
LinkedIn: [Nicolo Bencini](https://www.linkedin.com/in/nicolo-bencini/)
