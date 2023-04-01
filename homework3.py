import numpy as np
import math
from tkinter import *
import tkinter
import cv2
import PIL.Image, PIL.ImageTk
from transform import transform

# Объявление глобальных меременных
st, up_left, up_right, down_left, down_right, zx, zy = 0, 0, 0, 0, 0, 0, 0


class App:
    # Создание и настройка окна интерфейса
    def __init__(self, vsource):
        self.window = Tk()
        self.window.title("Robot localization")
        self.btn = Button(self.window, text="Start/Stop", command=self.start).grid(column=0, row=0)
        self.photo = tkinter.PhotoImage(height=1, width=1)
        self.canvas = tkinter.Canvas(self.window, height=720, width=1280)
        self.canvas.create_image(0, 0, anchor='nw', image=self.photo)
        self.canvas.grid(row=1, column=0)
        self.canvas.bind("<Button-1>", self.ul)
        self.canvas.bind("<Button-3>", self.ur)
        self.canvas.bind("<Shift-Button-1>", self.dl)
        self.canvas.bind("<Shift-Button-3>", self.dr)
        self.canvas.bind("<Control-Button-1>", self.zero)
        self.vid = cv2.VideoCapture(vsource)
        self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.update()
        self.window.mainloop()

    # Запуск программы
    def start(self):
        global st
        if st:
            st = 0
            print("Stop")
        else:
            st = 1
            print("Start")

    # Определение первой точки матрицы преобразования
    def ul(self, event):
        global up_left
        up_left = [event.x, event.y]
        print("Верхний левый угол: ", up_left)

    # Определение второй точки матрицы преобразования
    def ur(self, event):
        global up_right
        up_right = [event.x, event.y]
        print("Верхний правый угол: ", up_right)

    # Определение третьей точки матрицы преобразования
    def dl(self, event):
        global down_left
        down_left = [event.x, event.y]
        print("Нижний левый угол: ", down_left)

    # Определение четвёртой точки матрицы преобразования
    def dr(self, event):
        global down_right
        down_right = [event.x, event.y]
        print("Нижний правый угол: ", down_right)

    # Определение начала координат
    def zero(self, event):
        global zx, zy
        zx, zy = event.x, event.y

    # Обновление окна с изображением
    def update(self):
        ret, frame, f, b = self.get_frame()
        if ret:
            self.canvas.delete('all')
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
            if f and b:
                nv = np.array([0, 1])
                rv = np.array([f[0] - b[0], f[1] - b[1]])
                sp = np.dot(nv, rv)
                cf = sp / ((f[0] - b[0]) ** 2 + (f[1] - b[1]) ** 2) ** 0.5
                fi = round(math.acos(cf), 1)
                fi = fi * 180 / 3.14
                fi = round(fi, 1)
                xr = (b[0] + f[0] - 2 * zx) / 200
                xr = round(xr, 1)
                yr = (b[1] + f[1] - 2 * zy) / 200
                yr = round(yr, 1)
                if f[0] < b[0]:
                    fi = -fi
                self.canvas.create_text((b[0] + f[0]) / 2, (b[1] + f[1]) / 2,
                                        text=str(xr) + ', ' + str(yr) + ', ' + str(fi),
                                        fill='#000000')
        self.window.after(10, self.update)

    # Захват кадра с камеры
    def get_frame(self):
        global st
        ret, frame = self.vid.read()
        if ret:
            frame = cv2.resize(frame, (1280, 720))
            if st:
                frame, f, b = transform(frame, up_left, up_right, down_left, down_right)
                return ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), f, b
            else:
                return ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), None, None
        else:
            return ret, None


App('2.mp4')