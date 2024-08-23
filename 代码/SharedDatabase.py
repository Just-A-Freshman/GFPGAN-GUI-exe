"""There is the most important dynamic public variable and I choose not to load data into txt file."""
import sqlite3
import zipfile
from os import path, getpid
from time import sleep
import psutil


class SharedVariable(object):
    # Share data:
    task_list = None
    execute_entry = None  # it's the main-function and touch the process
    save_setting = None  # it's the crop mode's save_setting function share to main frame
    working = False

    @classmethod
    def kill_subprocess(cls):
        parent_pid = getpid()
        parent = psutil.Process(parent_pid)
        children = parent.children(recursive=True)
        for child in children:
            try:
                child.kill()
            except Exception as e:
                with open(path.abspath("Data/Error_log.txt"), 'a', encoding="utf-8")as f:
                    f.write(f"Error shut down the subprocess: {e}")


class SendData(object):
    # send data
    extension_dict = {"spg": "jpg", "speg": "jpeg", "sng": "png"}
    infile, outfile = "", ""
    infile_id, outfile_id = 0, 0
    scale = 2
    extension = "auto"

    @classmethod
    def clear_all_table(cls):
        connect = sqlite3.connect(path.abspath("Data/init.db"))
        cursor = connect.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS 'Task';")
        cursor.execute(f"DROP TABLE IF EXISTS 'fileContrast';")
        connect.commit()

    @classmethod
    def initialize_all_table(cls):
        connect = sqlite3.connect(path.abspath("Data/init.db"))
        cursor = connect.cursor()
        initialize_sqls = ("""CREATE TABLE IF NOT EXISTS "fileContrast"(
                                file_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                file_path TEXT UNIQUE);""",
                           """CREATE TABLE IF NOT EXISTS "Task" (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                infile_id INTEGER,
                                in_format TEXT,     
                                outfile_id INTEGER,
                                out_format TEXT,
                                expand_scale INTEGER,
                                basename TEXT);""",
                           )
        # in_format分为6种，正常的: jpg png jpeg | SPG的: spg sng speg
        for sql in initialize_sqls:
            cursor.execute(sql)
        connect.commit()

    @classmethod
    def refresh_file_id(cls, file_path, cite: str):
        # use for send_data
        setattr(cls, cite, file_path)
        connect = sqlite3.connect(path.abspath("Data/init.db"))
        cursor = connect.cursor()
        select_sql = f"SELECT file_id FROM 'fileContrast' WHERE file_path = ?"
        insert_file_sql = "INSERT INTO 'fileContrast' (file_path) VALUES (?);"
        try:
            cursor.execute(insert_file_sql, (file_path,))
            setattr(cls, f"{cite}_id", cursor.lastrowid)
        except sqlite3.IntegrityError:
            cursor.execute(select_sql, (file_path,))
            setattr(cls, f"{cite}_id", cursor.fetchone()[0])
        finally:
            setattr(cls, cite, file_path)
            connect.commit()

    @classmethod
    def write_in_task_list(cls, file_path):
        # jpg png jpeg | SPG的: spg sng speg
        connect = sqlite3.connect(path.abspath("Data/init.db"))
        cursor = connect.cursor()
        basename, ext = path.splitext(file_path)
        in_format = ext[1:]
        real_extension = in_format
        if in_format == "spg":
            with zipfile.ZipFile(path.join(cls.infile, file_path), 'r') as zip_ref:
                real_extension = zip_ref.read("ext").decode("utf-8")
                in_format = "s" + real_extension[1:]
        out_format = real_extension if cls.extension == "auto" else cls.extension
        insert_fields = '(infile_id, in_format, outfile_id, out_format, expand_scale, basename)'
        insert_sql = f"INSERT INTO Task {insert_fields} VALUES (?, ?, ?, ?, ?, ?)"
        insert_content = (cls.infile_id, in_format, cls.outfile_id, out_format, cls.scale, basename)
        cursor.execute(insert_sql, insert_content)
        connect.commit()

    @classmethod
    def select_finish_deal_img(cls, img_id):
        connect = sqlite3.connect(path.abspath("Data/init.db"))
        cursor = connect.cursor()
        cursor.execute("select * from 'Task';")
        select_sql = "SELECT * FROM 'Task' where id = (?);"
        cursor.execute(select_sql, (img_id, ))
        _, infile_id, in_format, outfile_id, out_format, _, basename = cursor.fetchone()
        searcher = ReceiveData()
        infile, outfile = searcher.read_from_file_contrast(cursor, infile_id, outfile_id)
        connect.commit()
        in_format = cls.extension_dict[in_format] if in_format in cls.extension_dict.keys() else in_format
        infile_img = path.join(infile, f"{basename}.{in_format}")
        outfile_img = path.join(outfile, "restored_images", f"{basename}.{out_format}")
        return infile_img, outfile_img


class ReceiveData(object):
    def __init__(self):
        self.__before_id = 0

    def prefetching(self):
        connect = sqlite3.connect(path.abspath("Data/init.db"))
        cursor = connect.cursor()
        prefetching_sql = "SELECT MAX(id) from 'Task';"
        cursor.execute(prefetching_sql)
        result = cursor.fetchone()
        self.__before_id = result if result is None else result[0]

    @staticmethod
    def read_from_file_contrast(cursor, infile_id, outfile_id):
        select_file_sql = "SELECT file_path FROM 'fileContrast' WHERE file_id = ?"
        cursor.execute(select_file_sql, (infile_id, ))
        yield cursor.fetchone()[0]
        cursor.execute(select_file_sql, (outfile_id, ))
        yield cursor.fetchone()[0]

    def read_from_task(self):
        # 先看看使用直接搜索速度如何，不行就上缓存
        infile = in_format = outfile = out_format = expand_scale = basename = ""
        connect = sqlite3.connect(path.abspath("Data/init.db"))
        cursor = connect.cursor()
        select_task_sql = "SELECT * FROM 'Task' ORDER BY id DESC LIMIT 1;"
        sleep(0.05)
        for _ in range(8):
            cursor.execute(select_task_sql)
            results = cursor.fetchone()
            if results is None or results[0] == self.__before_id:
                sleep(0.25)
            else:
                self.__before_id, infile_id, in_format, outfile_id, out_format, expand_scale, basename = results
                infile, outfile = self.read_from_file_contrast(cursor, infile_id, outfile_id)
                break
        connect.commit()
        return infile, in_format, outfile, out_format, expand_scale, basename
