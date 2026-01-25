import tkinter as tk


class FlatButton(tk.Label):
    def __init__(self, *args, enter_bg="#99D9EA", **kwargs):
        super().__init__(*args, **kwargs)
        self.image = ""
        self.__focus: bool = False
        self.__enter_bg = enter_bg
        self.__bg = self.cget("bg")
        self.bind('<Enter>', self.__enter)
        self.bind('<Leave>', self.__leave)
        self.bind('<Button-1>', self.__swap_color)

    def config_img(self, img_path):
        from PIL import ImageTk
        img = ImageTk.PhotoImage(file=img_path)
        self.image = img
        self.config(image=img)

    def __enter(self, _):
        super().config(bg=self.__enter_bg, cursor='hand2')
        self.__focus = True

    def __leave(self, _):
        super().config(bg=self.__bg)
        self.__focus = False

    def __swap_color(self, _):
        temp = self.__bg
        self.__bg = self.__enter_bg
        self.__enter_bg = temp
        super().config(bg=self.__enter_bg, cursor='hand2')

    def config(self, *args, **kwargs):
        if "command" in kwargs:
            self.bind("<ButtonRelease-1>", self.click_handle(kwargs["command"]))
            kwargs.pop("command")
        if "enter_bg" in kwargs:
            self.__enter_bg = kwargs["enter_bg"]
            kwargs.pop("enter_bg")
        if "bg" in kwargs:
            self.__bg = kwargs["bg"]
        super().config(*args, **kwargs)

    def click_handle(self, func):
        def inner(event, *args, **kwargs):
            self.__swap_color(0)
            if self.__focus:
                func(event, *args, **kwargs)
        return inner


if __name__ == "__main__":
    def click(event):
        print("click me!")
    root = tk.Tk()
    root.geometry("320x100+500+300")
    flat_btn = FlatButton(root, text="十 新建", fg="white", font=("微软雅黑", 13))
    flat_btn.config(command=click, bg="#1E5FC7", enter_bg="#1F69E0")
    flat_btn.place(x=40, y=30, width=230, height=30)
    root.mainloop()
