import tkinter
from tkinter.font import Font
from time import sleep
from threading import Thread


class StopwatchPage(tkinter.Tk):
    def __init__(self, parent):
        tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()
        self.thread.start()

    def initialize(self):
        self.minsize(385, 100)
        self.geometry("600x185+800+140")
        self.title("스톱워치")
        self.saved = []
        self.seconds = 0
        self.minutes = 0
        self.hours = 0
        self.time = "00:00:00"
        self.active = False
        self.kill = False
        self.left = tkinter.Frame(self)
        self.clock = tkinter.Label(
            self.left, text=str(self.time), font=Font(size=36))
        self.button_frame = tkinter.Frame(self.left)
        self.active_button = tkinter.Button(
            self.button_frame, text="시작", command=self.start)

        self.save_button = tkinter.Button(
            self.button_frame, text="랩", command=self.save)
        self.clear_button = tkinter.Button(self.button_frame, text="랩 초기화",
                                           command=self.clear)
        self.saved_canvas = tkinter.Canvas(self, width=150)
        self.saved_frame = tkinter.LabelFrame(self.saved_canvas, text="랩:")
        self.scrollbar = tkinter.Scrollbar(self, orient=tkinter.VERTICAL,
                                           command=self.saved_canvas.yview)
        self.left.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)
        self.clock.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
        self.button_frame.pack(side=tkinter.BOTTOM,
                               fill=tkinter.BOTH, expand=1)
        self.active_button.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)
        self.clear_button.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)
        self.save_button.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)
        self.saved_canvas.pack(side=tkinter.LEFT, fill=tkinter.Y, expand=0)
        self.scrollbar.pack(side=tkinter.LEFT, fill=tkinter.Y, expand=0)

        self.saved_canvas.create_window(0, 0, anchor='nw', tags="saved",
                                        window=self.saved_frame)
        self.saved_canvas.update_idletasks()
        self.saved_canvas.configure(scrollregion=self.saved_canvas.bbox('all'),
                                    yscrollcommand=self.scrollbar.set)

        self.thread = Thread(target=self.update, daemon=True)

    def update(self):
        while True:
            if self.kill:
                break
            if self.active:
                if self.seconds < 59:
                    self.seconds += 1
                elif self.seconds == 59:
                    self.seconds = 0
                    self.minutes += 1
                    if self.minutes == 60:
                        self.minutes = 0
                        self.hours += 1
                if self.minutes == 60:
                    self.minutes == 0
                    self.hours += 1
                if len(str(self.seconds)) == 1:
                    self.seconds = "0" + str(self.seconds)
                if len(str(self.minutes)) == 1:
                    self.minutes = "0" + str(self.minutes)
                if len(str(self.hours)) == 1:
                    self.hours = "0" + str(self.hours)
                self.time = f"{self.hours}:{self.minutes}:{self.seconds}"
                self.clock["text"] = self.time
                if isinstance(self.seconds, str):
                    self.seconds = int(self.seconds)
                if isinstance(self.minutes, str):
                    self.minutes = int(self.minutes)
                if isinstance(self.hours, str):
                    self.hours = int(self.hours)
                sleep(1)

    def start(self):
        self.active = True
        self.active_button.config(text="일시정지", command=self.pause)

    def pause(self):
        self.active = False
        self.active_button.config(text="시작", command=self.start)

    def save(self):
        self.saved.append(self.time)
        num = len(self.saved)
        savedTime = tkinter.Label(self.saved_frame,
                                  text=f"랩 #{num} - {self.saved[-1]}")
        savedTime.grid(row=len(self.saved), column=0, sticky="EW")
        self.saved_canvas.delete("saved")
        self.saved_canvas.create_window(0, 0, anchor='nw', tags="saved",
                                        window=self.saved_frame)
        self.saved_canvas.update_idletasks()
        self.saved_canvas.configure(scrollregion=self.saved_canvas.bbox('all'),
                                    yscrollcommand=self.scrollbar.set)

    def clear(self):
        self.saved = []
        self.saved_frame.destroy()
        self.saved_frame = tkinter.LabelFrame(
            self.saved_canvas, text="Saved Times:")
        self.saved_canvas.delete("saved")
        self.saved_canvas.create_window(0, 0, anchor='nw', tags="saved",
                                        window=self.saved_frame)
        self.saved_canvas.update_idletasks()
        self.saved_canvas.configure(scrollregion=self.saved_canvas.bbox('all'),
                                    yscrollcommand=self.scrollbar.set)
