from os import scandir
from json import load
from re import findall


class Init(object):
    theme = "浅色主题"
    infile_path = ""
    outfile_path = ""
    export_path = ""
    open_folder = ""

    @classmethod
    def load_init(cls):
        try:
            with open('Data/data.ini', 'r', encoding='utf-8')as f:
                data = f.read()
        except OSError:
            data = ""

        data_list = findall(r'(theme|infile_path|outfile_path|'
                            r'open_folder|export_path) = (.*)', data)
        for left_val, right_val in data_list:
            setattr(cls, left_val, right_val)

    @classmethod
    def save_current_init(cls):
        with open('Data/data.ini', 'w', encoding='utf-8') as f:
            f.write(f"theme = {cls.theme}\n")
            f.write(f"infile_path = {cls.infile_path}\n")
            f.write(f"outfile_path = {cls.outfile_path}\n")
            f.write(f"open_folder = {cls.open_folder}\n")
            f.write(f"export_path = {cls.export_path}\n")


class Theme(object):
    init = Init()
    win_bg = ""
    main_fg = ""
    entry_bg = ""
    btn_enter_bg = ""
    switch_frame_bg: str = ""
    switch_frame_fg: str = ""
    switch_frame_unselect_bg: str = ""
    scrollbar_bg: str = ""
    scrollbar_highlight_bg: str = ""
    canvas_bg: str = ""
    progressbar_color: str = ""
    main_frame_img: str = ""
    crop_frame_img: str = ""
    search_ico = ""

    @classmethod
    def search_available_theme(cls):
        theme_files = scandir(r'Data/Theme')
        return [theme.name[:-5] for theme in theme_files if theme.name.endswith('.json')]

    @classmethod
    def load_theme(cls, theme_name):
        Init.theme = theme_name
        with open(f'Data/Theme/{theme_name}.json')as json_file:
            data = load(json_file)
        theme_picture = data["theme_picture"]
        cls.main_frame_img = theme_picture["main_frame_img"]
        cls.crop_frame_img = theme_picture["crop_frame_img"]
        cls.search_ico = theme_picture["search_ico"]
        theme_color = data["theme_color"]
        for key, val in theme_color.items():
            setattr(cls, key, val)

    @classmethod
    def load_default_theme(cls):
        Init.load_init()
        cls.load_theme(cls.init.theme)
        return cls.init.theme

    @classmethod
    def frame_btn_theme(cls, on: bool):
        frame_bg = cls.switch_frame_bg if on else cls.switch_frame_unselect_bg
        style = {
            "bg": frame_bg,
            "foreground": cls.switch_frame_fg,
            "activebackground": cls.switch_frame_bg,
            "activeforeground": cls.switch_frame_fg
        }
        return style
