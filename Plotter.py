import tkinter
import segyio
from threading import Thread
from time import sleep
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

'''Создаем граффический интерфейс, и вставляем в него 5 окон из матплотлиба'''
root = tkinter.Tk()
root.wm_title("Track plotter")

fig_A1, ax_A1 = plt.subplots(figsize=(3, 4))
'Перестовляем оси коардинат на нужные места'
ax_A1.spines['left'].set_position('center')
ax_A1.spines['bottom'].set_position(('axes', 1))
ax_A1.spines['top'].set_visible(False)
ax_A1.spines['right'].set_visible(False)
canvas = FigureCanvasTkAgg(fig_A1, master=root)  # A tk.DrawingArea.
canvas.draw()
canvas.get_tk_widget().grid(row=1, column=0)


fig_A2, ax_A2 = plt.subplots(figsize=(3, 4))
ax_A2.spines['left'].set_position('center')
ax_A2.spines['bottom'].set_position(('axes', 1))
ax_A2.spines['top'].set_visible(False)
ax_A2.spines['right'].set_visible(False)
canvas1 = FigureCanvasTkAgg(fig_A2, master=root)  # A tk.DrawingArea.
canvas1.draw()
canvas1.get_tk_widget().grid(row=1, column=1)


fig_X, ax_X = plt.subplots(figsize=(3, 4))
ax_X.spines['left'].set_position('center')
ax_X.spines['bottom'].set_position(('axes', 1))
ax_X.spines['top'].set_visible(False)
ax_X.spines['right'].set_visible(False)
canvas2 = FigureCanvasTkAgg(fig_X, master=root)  # A tk.DrawingArea.
canvas2.draw()
canvas2.get_tk_widget().grid(row=1, column=2)


fig_Y, ax_Y = plt.subplots(figsize=(3, 4))
ax_Y.spines['left'].set_position('center')
ax_Y.spines['bottom'].set_position(('axes', 1))
ax_Y.spines['top'].set_visible(False)
ax_Y.spines['right'].set_visible(False)
canvas3 = FigureCanvasTkAgg(fig_Y, master=root)  # A tk.DrawingArea.
canvas3.draw()
canvas3.get_tk_widget().grid(row=1, column=3)

fig_par, ax_par = plt.subplots(figsize=(3, 4))
ax_par.spines['left'].set_position('center')
ax_par.spines['bottom'].set_position('center')
ax_par.spines['top'].set_visible(False)
ax_par.spines['right'].set_visible(False)
ax_par.set_xlabel('X')
ax_par.set_xlabel('Y')
ax_par.set_xlabel('X', loc='right')
ax_par.set_ylabel('Y', loc='top')
canvas4 = FigureCanvasTkAgg(fig_par, master=root)  # A tk.DrawingArea.
canvas4.draw()
canvas4.get_tk_widget().grid(row=1, column=4)

'Создаем функцию для загрузки данных из файла'
def load_data():
    global a_1, a_2, time, err, mem_ang
    'Берем из поля для ввода текста имя файла'
    pach = Ef.get()
    'Берем из поля для ввода текста номера треков и обрабатываем ошибку при неправильном вводе номеров'
    try:
        num = E.get()
        i = int(num.split(',')[0])
        j = int(num.split(',')[1])
        err['text'] = ''
    except ValueError:
        err['text'] = 'не верные номера трасс'
    'открываем файл обрабатывая ошибку'
    try:
        with segyio.open(pach, ignore_geometry=True) as f:
            a_1 = f.trace[i]
            a_2 = f.trace[j]
            time = f.samples
            err['text'] = ''
    except:
        err['text'] = 'Неудалось открыть файл'
    'Строим граффики A1 и A2'
    ax_A1.clear()
    ax_A1.spines['left'].set_position('center')
    ax_A1.spines['bottom'].set_position(('axes', 1))
    ax_A1.spines['top'].set_visible(False)
    ax_A1.spines['right'].set_visible(False)
    ax_A1.invert_yaxis()
    ax_A1.plot(a_1, time)
    canvas.draw() # draw используется для обновления gui
    ax_A2.clear()
    ax_A2.spines['left'].set_position('center')
    ax_A2.spines['bottom'].set_position(('axes', 1))
    ax_A2.spines['top'].set_visible(False)
    ax_A2.spines['right'].set_visible(False)
    ax_A2.invert_yaxis()
    ax_A2.plot(a_2, time)
    canvas1.draw()
    mem_ang = None


'Создаем функцию для сохранения результатов в файл'
def save():
    global a_1, a_2, X, Y
    ang = int(slide.get())
    'Генерируем имя файла из названия входных данных и угла'
    path = f'{Ef.get()}_angle_{ang}.sgy'
    spec = segyio.spec()
    spec.samples = list(range(len(a_1)))
    spec.format = 1
    spec.tracecount = 5
    with segyio.create(path, spec) as f:
            f.trace[0] = a_1
            f.trace[1] = a_2
            f.trace[2] = X
            f.trace[3] = Y
            f.trace[4] = np.array([ang for _ in range(len(a_1))])
    'Выводим сообщение об успешном сохранении данных'
    err['text'] = f'Треки сохранены в {path}'

'Создаем функцию для рассчетов при передвижении ползунка'
def caunt_XY():
    global X, Y, mem_ang
    'Создаем бесконечный цыкл'
    while True:
        sleep(0.1)
        'Читаем угл слайдера'
        ang = np.radians(int(slide.get()))
        'С помощю переменной mem проверяем передвинулся ли слайдер'
        if ang != mem_ang:
            'Проверяем загруженны ли данные с помощю оброботки ошибок'
            try:
                'Проводим рассяеты'
                X = a_1 * np.cos(ang) + a_2 * np.sin(ang)
                Y = a_1 * -np.sin(ang) + a_2 * np.cos(ang)
                'Строим граффики предварительно удаляя старые данные'
                ax_X.clear()
                ax_X.spines['left'].set_position('center')
                ax_X.spines['bottom'].set_position(('axes', 1))
                ax_X.spines['top'].set_visible(False)
                ax_X.spines['right'].set_visible(False)
                ax_X.invert_yaxis()
                ax_X.plot(X, time)
                canvas2.draw_idle()
                ax_Y.clear()
                ax_Y.spines['left'].set_position('center')
                ax_Y.spines['bottom'].set_position(('axes', 1))
                ax_Y.spines['top'].set_visible(False)
                ax_Y.spines['right'].set_visible(False)
                ax_Y.invert_yaxis()
                ax_Y.plot(Y, time)
                canvas3.draw_idle()
                ax_par.clear()
                ax_par.spines['left'].set_position('center')
                ax_par.spines['bottom'].set_position('center')
                ax_par.spines['top'].set_visible(False)
                ax_par.spines['right'].set_visible(False)
                ax_par.set_xlabel('X', loc='left')
                ax_par.set_xlabel('Y', loc='left')
                ax_par.plot(X, Y)
                canvas4.draw_idle()
                mem_ang = ang
            except NameError:
                sleep(1)

'Создаем злементы оформления'
tkinter.Label(master=root, text="A1").grid(row=0, column=0)
tkinter.Label(master=root, text="A2").grid(row=0, column=1)
tkinter.Label(master=root, text="X").grid(row=0, column=2)
tkinter.Label(master=root, text="Y").grid(row=0, column=3)
tkinter.Label(master=root, text="Граффик параметрической кривой").grid(row=0, column=4)

err = tkinter.Label(master=root, text="")
err.grid(row=2, column=0)
tkinter.Label(master=root, text="номера трасс через запятую").grid(row=2, column=1)
tkinter.Label(master=root, text="Угол (градусы)").grid(row=2, column=2)
tkinter.Label(master=root, text="Имя фала").grid(row=2, column=3)

'Создаем поля для ввода'
s1 = tkinter.StringVar()
s1.set('0,1')
E = tkinter.Entry(master=root, textvariable=s1)
E.grid(row=3, column=1)

s2 = tkinter.StringVar()
s2.set('1580_rot.sgy')
Ef = tkinter.Entry(master=root, textvariable=s2)
Ef.grid(row=3, column=3)

'создаем кнопки'
button_delit = tkinter.Button(master=root, text="Удалить данные, и построить граффики заново", command=load_data)
button_delit.grid(row=3, column=0)

tkinter.Button(master=root, text="Сохранить", command=save).grid(row=3, column=4)

'Создаем слайдер для выбора угла'
slide = tkinter.Scale(root, orient=tkinter.HORIZONTAL, length=300, from_=0, to=90, tickinterval=10, resolution=1)
slide.grid(row=3, column=2)
'Создаем переменную для "Запоминания угла(используется в фенкции caunt_XY)"'
mem_ang = None

'Запускаем поток для рассчетов и перестроении граффиков при смене угла на слайдере'
ang_update = Thread(target=caunt_XY)
ang_update.start()

'Запускаем программу'
tkinter.mainloop()
