import io
import os
import PIL.ImageGrab
import sqlite3
import time
import tkinter

class window_main(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title("Screen Shot")
        self.create_widgets()
    def create_widgets(self):
        self.button_st = tkinter.Button(self)
        self.button_st["text"] = "Screen Shot"
        self.button_st["height"] = 2
        self.button_st["width"] = 13
        self.button_st["command"] = self.screen_shot
        self.button_st.grid(row = 0, column = 0,
                            padx = 5, pady = 5)
        self.button_exit = tkinter.Button(self)
        self.button_exit["text"] = "Exit"
        self.button_exit["height"] = 2
        self.button_exit["width"] = 13
        self.button_exit["command"] = self.event_exit
        self.button_exit.grid(row = 1, column = 0,
                              padx = 5, pady = 5)
    def screen_shot(self):
        self.withdraw()
        self.sub_app = window_full_screen(self)
        self.sub_app.mainloop()
    def event_exit(self):
        self.destroy()

class window_full_screen(tkinter.Tk):
    def __init__(self, window_main = tkinter.Tk):
        super().__init__()
        self.window_main = window_main
        self.attributes("-fullscreen", True)
        self.attributes("-alpha", 0.6)
        self.wm_attributes("-transparentcolor", "gray")
        self.create_canvas()
        self.create_widgets()
        self.bind("<Escape>", self.event_exit)
        self.bind("<B1-Motion>", self.event_create_rectangle)
        self.bind("<ButtonRelease-1>", self.event_save_rectangle)
        self.rec_exist = False
        self.save_exist = False
    def create_canvas(self):
        self.canvas = tkinter.Canvas(self,
                                     width = self.winfo_screenwidth(),
                                     height = self.winfo_screenheight())
        self.canvas.place(x = 0, y = 0)
    def create_widgets(self):
        self.button_save = tkinter.Button(self)
        self.button_save["text"] = "SAVE"
        self.button_save["command"] = self.get_screenshot
    def event_exit(self, event):
        self.window_main.deiconify()
        self.destroy()
    def event_create_rectangle(self, event):
        if not self.rec_exist:
            self.x0 = event.x
            self.y0 = event.y
            self.canvas.create_rectangle(self.x0, self.y0, self.x0, self.y0,
                                         fill = "gray", outline = "red",
                                         tag = "rec")
            self.attributes("-alpha", 0.25)
        if self.save_exist:
            self.button_save.place_forget()
        self.rec_exist = True
        self.canvas.delete("rec")
        self.x2 = event.x
        self.y2 = event.y
        if self.x0 > self.x2:
            self.x1, self.x2 = self.x2, self.x0
        else:
            self.x1, self.x2 = self.x0, self.x2
        if self.y0 > self.y2:
            self.y1, self.y2 = self.y2, self.y0
        else:
            self.y1, self.y2 = self.y0, self.y2
        self.canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2,
                                     fill = "gray", outline = "red", tag = "rec")
    def event_save_rectangle(self, event):
        self.attributes("-alpha", 0.6)
        if self.x2 > self.winfo_screenwidth() - 50 \
            or self.y2 > self.winfo_screenheight() - 50:
            self.save_x1 = self.x1 - 40
            self.save_y1 = self.y1 - 40
            self.button_save.place(x = self.save_x1, y = self.save_y1)
        else:
            self.save_x1 = self.x2 + 10
            self.save_y1 = self.y2 + 10
            self.button_save.place(x = self.save_x1, y = self.save_y1)
        self.rec_exist = False
        self.save_exist = True
    def get_screenshot(self):
        conn = sqlite3.connect("compare_pattern")
        sql = "select max(ID) from image"
        rows = []
        for row in conn.execute(sql):
            rows.append(row)
        max_index = rows[0][0] + 1
        self.image_corp_screen = PIL.ImageGrab.grab(bbox = (self.x1, self.y1,
                                                       self.x2, self.y2))
        output = io.BytesIO()
        self.image_corp_screen.save(output, format = "PNG")
        self.image_binary = output.getvalue()
        self.image_pattern = (max_index, self.x1, self.y1, self.x2, self.y2,
                              self.image_binary)
        sql = "insert into image values (?, ?, ?, ?, ?, ?)"
        conn.execute(sql, self.image_pattern)
        conn.commit()
        conn.close()
        self.window_main.deiconify()
        self.destroy()

app = window_main()
app.mainloop()