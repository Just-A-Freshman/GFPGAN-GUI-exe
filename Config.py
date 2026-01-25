import os
import json
from pathlib import Path
from enum import Enum
from typing import Dict, Tuple


class ThemeAttribute(Enum):
    THEME = "theme"
    INFILE_PATH = "infile_path"
    OUTFILE_PATH = "outfile_path"
    EXPORT_PATH = "export_path"
    OPEN_FOLDER = "open_folder"


class Init(object):
    theme = "浅色主题"
    infile_path = ""
    outfile_path = ""
    export_path = ""
    open_folder = ""

    @classmethod
    def load_init(cls):
        try:
            with open('Data/data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}

        for attr in ThemeAttribute:
            setattr(cls, attr.name.lower(), data.get(attr.value, getattr(cls, attr.name.lower())))

    @classmethod
    def save_current_init(cls):
        config = {attr.value: getattr(cls, attr.name) for attr in ThemeAttribute}
        with open('Data/data.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=4)


class Theme(object):
    init = Init()
    win_bg = ""
    button_fg = ""
    button_bg = ""
    execute_btn_bg = ""
    execute_btn_fg = ""
    entry_highlight_bg = ""
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
    style_dict: Dict[str, Dict[str, str]] = {}
    font_box: Tuple[Tuple[str, int, str], ...] = ()

    @classmethod
    def search_available_theme(cls) -> list:
        theme_files = [f.name[:-5] for f in os.scandir('Data/Theme') if f.name.endswith('.json')]
        return theme_files

    @classmethod
    def load_theme(cls, theme_name: str):
        Init.theme = theme_name
        theme_path = Path(f'Data/Theme/{theme_name}.json')
        if not theme_path.exists():
            raise FileNotFoundError(f"Theme file not found: {theme_name}")

        with theme_path.open('r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        theme_picture = data["theme_picture"]
        cls.main_frame_img = theme_picture["main_frame_img"]
        cls.crop_frame_img = theme_picture["crop_frame_img"]
        cls.search_ico = theme_picture["search_ico"]
        theme_color = data["theme_color"]
        for key, val in theme_color.items():
            setattr(cls, key, val)
        cls.config_theme_style()

    @classmethod
    def load_default_theme(cls) -> str:
        Init.load_init()
        cls.load_theme(cls.init.theme)
        return cls.init.theme

    @classmethod
    def config_theme_style(cls):
        font1 = "微软雅黑"
        font2 = "宋体"
        font3 = "Segoe UI"
        cls.font_box = (
            (font1, 12),
            (font1, 13),
            (font1, 14),
            (font1, 15),
            (font1, 16, "bold"),
            (font1, 17),
            (font1, 18),
            (font2, 18, 'bold'),
            (font2, 30),
            (font3, 36, "bold")
        )

        cls.style_dict = {

            "Label": {
                "bg": cls.win_bg, "fg": cls.main_fg
            },

            "FrameButton": {
                "foreground": cls.switch_frame_fg,
                "activebackground": cls.switch_frame_bg,
                "activeforeground": cls.switch_frame_fg
            },

            "FlatButton-1": {
                "enter_bg": cls.btn_enter_bg,
                "bg": cls.win_bg,
                "fg": cls.button_fg
            },

            "FlatButton-2": {
                "enter_bg": cls.switch_frame_unselect_bg,
                "bg": cls.button_bg,
                "fg": cls.switch_frame_fg
            },

            "FlatButton-3": {
                "bg": cls.execute_btn_bg,
                "fg": cls.execute_btn_fg,
                "enter_bg": cls.switch_frame_unselect_bg
            },

            "FlatButton-4": {
                "bg": cls.entry_bg,
                "enter_bg": cls.entry_highlight_bg,
                "fg": cls.main_fg
            },

            "Entry-1": {
                "bg": cls.entry_bg,
                "highlightbackground": cls.win_bg,
                "foreground": cls.main_fg,
                "insertbackground": cls.main_fg
            },

            "Entry-2": {
                "bg": cls.win_bg,
                "highlightbackground": cls.win_bg,
                "foreground": cls.main_fg,
                "insertbackground": cls.main_fg
            },

            "ReadonlyEntry": {
                "readonlybackground": cls.win_bg,
                "foreground": cls.main_fg
            },

            "ProgressBar": {
                "background": cls.scrollbar_bg,
                "highlightcolor": cls.scrollbar_highlight_bg,
                "bar_bg": cls.progressbar_color
            },

            "Scale": {
                "bg": cls.win_bg,
                "foreground": cls.main_fg,
                "activebackground": cls.win_bg,
                "troughcolor": cls.scrollbar_bg
            },

            "Listbox": {
                "bg": cls.win_bg,
                "foreground": cls.main_fg,
                "highlightbackground": cls.win_bg
            },

            "TreeView": {
                "background": cls.win_bg,
                "foreground": cls.main_fg
            },

            "Scrollbar": {
                "arrowcolor": cls.switch_frame_fg,
                "troughcolor": cls.win_bg,
                "thumb_color": cls.scrollbar_bg,
                "highlight_bg": cls.scrollbar_highlight_bg
            },

            "Combobox": {
                "arrowcolor": cls.main_fg,
                "foreground": cls.main_fg,
                "background": cls.scrollbar_bg,
                "lightcolor": cls.scrollbar_bg,
                "darkcolor": cls.scrollbar_bg
            },

            "TCombobox_map": {
                "background": [('active', cls.scrollbar_highlight_bg)],
                "fieldbackground": [('readonly', cls.scrollbar_bg)]
            }
        }
