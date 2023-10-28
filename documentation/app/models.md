## Documentation for `models.py`

### File Description

`models.py` is a module responsible for handling database operations using the GINO library.

### Imports

- `from gino import Gino`: Imports the GINO library, which is an asynchronous ORM for Python.

- `from config.config import config`: Imports the configuration for the database.

- `db = Gino()`: Initializes a Gino instance to interact with the database.

### Class `User`

```python
class User(db.Model):
    # ... code ...
This class represents the UserBot table in the database. It has the following columns:

id: Integer, primary key.
user_id: Integer, unique, not null.
chat_id: Integer, unique, nullable.
locale: String(2), not null.
root: Integer.
printer_ip: String, not null.
camera_ip: String, not null.
Class UploadedFiles
python
Copy code
class UploadedFiles(db.Model):
    # ... code ...
This class represents the FileBot table in the database. It has the following columns:

id: Integer, primary key.
file_id: Integer, not null.
name: String, not null.
Class DBfunc
python
Copy code
class DBfunc:  
    # ... code ...
This class contains methods for interacting with the UserBot table.

get(self, user_id): Gets a user by their user_id.

get_root(self, root = 1): Gets the root user.

add(self, user_id, chat_id): Adds a new user to the database.

update(self, what_update:str, where_update, new_value): Updates a user's information.

delete(self, user_id): Deletes a user.

Class Filefunc
python
Copy code
class Filefunc: 
    # ... code ...
This class contains methods for interacting with the FileBot table.

get(self, filename): Gets a file by its name.

get_id(self, id:int): Gets a file by its id.

check_new(self, file_id = 1): Checks if there's a new file.

file_list(self): Gets a list of files.

add(self, filename): Adds a new file.

update(self, what_update:str, where_update, new_value): Updates a file's information.

Function init_db()
python
Copy code
async def init_db():
    # ... code ...
This function initializes the database by binding it to the specified URL from the configuration.