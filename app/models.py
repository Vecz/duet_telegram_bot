from gino import Gino
from config.config import config
db = Gino()

class User(db.Model):
    __tablename__ = "UserBot"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable = False, unique = True)
    chat_id = db.Column(db.Integer, nullable = True,unique = True)
    locale = db.Column(db.String(2), nullable = False)
    root = db.Column(db.Integer)
    printer_ip = db.Column(db.String, nullable = False)
    camera_ip = db.Column(db.String, nullable = False)

class UploadedFiles(db.Model):
    __tablename__ = "FileBot"
    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.Integer, nullable = False, unique = False)
    name = db.Column(db.String, nullable = False)

class DBfunc:  
    async def get(self, user_id):
        user = await User.query.where(User.user_id == user_id).gino.first()
        return user
    
    async def get_root(self, root = 1):
        user = await User.query.where(User.root == root).gino.first()
        return user

    async def add(self, user_id, chat_id):

            user = await self.get_root()
            check = await self.get(user_id)
            if(user != None and check == None):
                await User.create(user_id = user_id, locale = "EN", root = 0, printer_ip = user.printer_ip,
                              camera_ip = user.camera_ip, chat_id = chat_id)
            elif(user == None and check == None):
                await User.create(user_id = user_id, locale = "EN", root = 0, printer_ip = "http://127.0.0.1:8080",
                              camera_ip = "http://127.0.0.1:8080", chat_id = chat_id)

    
    async def update(self, what_update:str, where_update, new_value):
        user = await self.get(where_update)
        if (what_update == "locale"):
            await user.update(locale = new_value).apply()
        if (what_update == "root"):
            await user.update(root = new_value).apply()
        if (what_update == "printer_ip"):
            await user.update(printer_ip = new_value).apply()
        if (what_update == "camera_ip"):
            await user.update(camera_ip = new_value).apply()
    async def delete(self, user_id):
        user = await self.get(user_id)
        await user.delete()

class Filefunc: 
    async def get(self, filename):
        file = await UploadedFiles.query.where(UploadedFiles.name == filename).gino.first()
        return file
    
    async def get_id(self, id:int):
        file = await UploadedFiles.query.where(UploadedFiles.id == id).gino.first()
        return file

    async def check_new(self, file_id = 1):
        file = await UploadedFiles.query.where(UploadedFiles.file_id == file_id).gino.first()
        return file

    async def file_list(self):
        file = await UploadedFiles.query.gino.all()
        return file[::-1]

    async def add(self, filename):
        await UploadedFiles.create(name = filename, file_id = 1)

    async def update(self, what_update:str, where_update, new_value):
        file = await self.get(where_update)
        if (what_update == "file_id"):
            await file.update(file_id = new_value).apply()

async def init_db():
    await db.set_bind(config["database_url"])