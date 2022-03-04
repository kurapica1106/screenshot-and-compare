import io
import os
import PIL
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
        
        conn = sqlite3.connect("compare_pattern")
        cur = conn.cursor()
        sql = "select ID from image"
        cur.execute(sql)
        results = cur.fetchall()
        t_ids = [r[0] for r in results] if len(results) > 0 else [-1]
        conn.commit()
        conn.close()
        self.var = tkinter.IntVar()
        self.var.set(t_ids[0])
        self.optm_pic_id = tkinter.OptionMenu(self, self.var, *t_ids)
        self.optm_pic_id.grid(row = 0, column = 1,
                              padx = 5, pady = 5)
        
        self.btn_compare = tkinter.Button(self)
        self.btn_compare["text"] = "Compare"
        self.btn_compare["command"] = self.screen_compare
        self.btn_compare.grid(row = 1, column = 1, padx = 5, pady = 5)
    def screen_shot(self):
        self.withdraw()
        self.sub_app = window_full_screen(self)
        self.sub_app.mainloop()
    def event_exit(self):
        self.destroy()
    def screen_compare(self):
        conn = sqlite3.connect("compare_pattern")
        cur = conn.cursor()
        
        sql = " \
            select image, x1, y1, x2, y2 from image \
            where ID = %d\
            " % self.var.get()
        cur.execute(sql)
        results = cur.fetchall()
        #img = PIL.Image.new("RGB", (0, 0))
        #img_postn = [int(), int(), int(), int()]
        
        img = results[0][0]
        img_postn = [results[0][1], results[0][2], results[0][3], results[0][4]]
        img = io.BytesIO(img)
        img = PIL.Image.open(img)
        img_trgt = PIL.ImageGrab.grab(img_postn)
        is_same = img.histogram() == img_trgt.histogram()
        print(is_same)
        
        conn.commit()
        conn.close()

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
        cur = conn.cursor()
        
        sql = "select max(ID) from image"
        cur.execute(sql)
        results = cur.fetchall()
        max_index = 1 if results[0][0] == None else results[0][0] + 1
        
        self.image_corp_screen = PIL.ImageGrab.grab(bbox = (self.x1 + 1, self.y1 + 1,
                                                            self.x2, self.y2))
        output = io.BytesIO()
        self.image_corp_screen.save(output, format = "PNG")
        self.image_binary = output.getvalue()
        self.image_pattern = (max_index, self.x1 + 1, self.y1 + 1, self.x2, self.y2,
                              self.image_binary)
        sql = "insert into image values (?, ?, ?, ?, ?, ?)"
        conn.execute(sql, self.image_pattern)
        
        sql = "select ID from image"
        cur.execute(sql)
        results = cur.fetchall()
        t_ids = [r[0] for r in results]
        self.window_main.var.set(t_ids[0])
        self.window_main.optm_pic_id["menu"].delete(0, "end")
        for t_id in t_ids:
            self.window_main.optm_pic_id["menu"].add_command(label = t_id,
                                                             command = tkinter._setit(self.window_main.var,
                                                                                      t_id))
        
        conn.commit()
        conn.close()
        self.window_main.deiconify()
        self.destroy()

app = window_main()
app.mainloop()