from tkinter import *
from tkinter import messagebox
import astropy.io.fits as pyfits
import matplotlib.pyplot as plt
import numpy as np


def select():
    global a, x, y, r, r1, r2
    a = txt1.get()
    x = int(txt2.get())
    y = int(txt3.get())
    r = int(txt4.get())
    r1 = int(txt5.get())
    r2 = int(txt6.get())


def f(x, y):
    for x in range(left, right):
        for y in range(down, up):
            return scidata[x][y]


window = Tk()
window.geometry('800x500')

lbl1 = Label(window, text='Рады вас приветствовать пользователь! Для запуска введите следующие параметры:', font=("Arial Bold", 10))
lbl1.grid(column=0, row=0)


txt1 = Entry(window, width=50)
txt1.insert(INSERT, 'Путь к файлу')
txt1.grid(column=0, row=1)


txt2 = Entry(window, width=50)
txt2.insert(INSERT, 'Координата звезды х')
txt2.grid(column=0, row=2)


txt3 = Entry(window, width=50)
txt3.insert(INSERT, 'Координата звезды у')
txt3.grid(column=0, row=3)


txt4 = Entry(window, width=50)
txt4.insert(INSERT, 'Радиус по которому хотите считать свечение звезды')
txt4.grid(column=0, row=4)


txt5 = Entry(window, width=50)
txt5.insert(INSERT, 'Ближний радиус фона')
txt5.grid(column=0, row=5)


txt6 = Entry(window, width=50)
txt6.insert(INSERT, 'Дальний радиус фона')
txt6.grid(column=0, row=6)


lbl2 = Label(window, text='Далее выберите что хотите увидеть:', font=("Arial Bold", 10))
lbl2.grid(column=0, row=7)


chk_state1 = IntVar()
chk_state1.set(0)
chk1 = Checkbutton(window, text='Горизонтальный профиль', var=chk_state1)
chk1.grid(column=0, row=8)


chk_state2 = IntVar()
chk_state2.set(0)
chk2 = Checkbutton(window, text='Вертикальный профиль', var=chk_state2)
chk2.grid(column=0, row=9)


chk_state3 = IntVar()
chk_state3.set(0)
chk3 = Checkbutton(window, text='Трех-размерный график', var=chk_state3)
chk3.grid(column=0, row=10)


btn1 = Button(window, text='Выбрать', command=select)
btn1.grid(column=1, row=6)


chk_state4 = IntVar()
chk_state4.set(0)
chk4 = Checkbutton(window, text='Flux', var=chk_state4)
chk4.grid(column=0, row=11)
window.mainloop()


hdulist = pyfits.open(a)
scidata = hdulist[0].data
hdulist.close()
hor = []
vert = []
al = []
xcoord = []
ycoord = []
left = x - r
right = x + r
up = y + r
down = y - r
for i in range(left, right):
    xcoord.append(i)
for i in range(down, up):
    ycoord.append(i)
for i in range(left, right):
    z = scidata[y][i]
    hor.append(z)
for i in range(down, up):
    w = scidata[i][x]
    vert.append(w)
fig1 = plt.figure(1)
ax_1 = fig1.add_subplot(111)
ax_1.set_title("Горизонтальный профиль")
ax_1.set_ylabel('Количество отсчетов')
ax_1.set_xlabel('Координаты по горизонтали')
if chk_state1.get():
    ax_1.plot(xcoord, hor)
    plt.show()
else:
    plt.close()

fig2 = plt.figure(2)
ax_2 = fig2.add_subplot(111)
ax_2.set_title("Вертикальный профиль")
ax_2.set_ylabel('Количество отсчетов')
ax_2.set_xlabel('Координаты по вертикали')
if chk_state2.get():
    ax_2.plot(ycoord, vert)
    plt.show()
else:
    plt.close()


z = []
Z = []
fig3 = plt.figure()
ax = plt.axes(projection='3d')
a = xcoord
b = ycoord
X, Y = np.meshgrid(a, b)
for i in range(left, right):
    for j in range(down, up):
        z.append(scidata[j][i])
    z1 = np.asarray(z, dtype=int)
    Z.append(z1)
    z = []
Z = np.asarray(Z)


if chk_state3.get():
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='Blues', edgecolor='none')
    ax.set_title('surface')
    plt.show()
else:
    plt.close()

n1 = 0
circle1 = []
for i in range(x - r1, (x + r1) + 1):
    for j in range(y - r1, (y + r1) + 1):
        if ((i - x) * (i-x)) + ((j-y) * (j-y)) <= r1 * r1:
            circle1.append(scidata[j][i])
            n1 += 1
fon1 = sum(circle1) / n1

n2 = 0
circle2 = []
for i in range(x - r2, (x + r2) + 1):
    for j in range(y - r2, (y + r2) + 1):
        if ((i - x) * (i-x)) + ((j-y) * (j-y)) <= r2 * r2:
            circle2.append(scidata[j][i])
            n2 += 1
fon2 = sum(circle2) / n2

fon = (fon1 + fon2)/2

n = 0
flux = 0
star = []
for i in range(x - r, (x + r) + 1):
    for j in range(y - r, (y + r) + 1):
        if ((i - x) * (i-x)) + ((j-y) * (j-y)) <= r * r:
            star.append(scidata[j][i])
            n += 1
flux = sum(star) - n * fon

if chk_state4.get():
    messagebox.showinfo('Свечение звезды', flux)


