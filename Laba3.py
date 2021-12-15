import control.matlab as matlab
import matplotlib.pyplot as pyplot
import sys
import numpy as numpy
from numpy import *
import math
import scipy
from scipy import integrate

ky = 20
tg = 10
ty = 5
tgt = 2
w1 = matlab.tf([1], [tg, 1])
print("Wг = ", w1)
w2 = matlab.tf([0.01*tgt, 1], [0.05*tg, 1])
print("Wпт = ", w2)
w3 = matlab.tf([ky], [ty, 1])
print("Wиу = ", w3)
w4 = matlab.series(w1, w2, w3)

# Параметры регулятора
def PIDReg(Kp, Ki, Kd):
    wP = matlab.tf([Kp], [1])
    wI = matlab.tf([Ki], [1, 0])
    wD = matlab.tf([Kd, 0], [1])
    w5 = matlab.parallel(wP + wI + wD)
    return w5
w5 = PIDReg(1,0, 0)

w6 = matlab.series(w5, w4)

w = matlab.feedback(w6, 1)

print("W(p) = ", w)
time = []
for i in range(0, 6000):
    time.append(i/100)
# Строим переходную характеристику
pyplot.subplot()
pyplot.grid(True)
[y, x] = matlab.step(w, time)
pyplot.hlines(1, 0, 60, color='r', linewidth=1, linestyle='-')
pyplot.hlines(1.05, 0, 60, color='g', linewidth=1, linestyle='--')
pyplot.hlines(0.95, 0, 60, color='g', linewidth=1, linestyle='--')
pyplot.vlines(15, 0, 1.3, color='b', linewidth=1, linestyle='-')
pyplot.plot(x, y)
pyplot.title('Переходна характеристика')
pyplot.ylabel('Амплитуда')
pyplot.xlabel('Время')
pyplot.show()

# находим корни характеристичкского уравнения и определяем устойчивость системы
korny = matlab.pzmap(w)
pyplot.axis([-3, 1,-1, 1])
pyplot.show()
pole = matlab.pole(w)
print(pole)
deistv = []
for i in pole:
    kx = i.real
    deistv.append(kx)
if (min(deistv) > 0.0001):
    print("система неустйочива по корням характеристического уравнения")
elif (max(deistv) < -0.0001):
    print("система устойчива по корням характеристического уравнения")
else:
    print("система на границе устойчивости")

mag, phase, omega = matlab.bode(w6)
pyplot.plot()
pyplot.show()

w5 = PIDReg(0.321, 0.0349, 0.544)

w6 = matlab.series(w5, w4)

w = matlab.feedback(w6, 1)

print("W(p) = ", w)
time = []
for i in range(0, 6000):
    time.append(i/100)
# Строим переходную характеристику
pyplot.subplot()
yPerehHar = []
xPerehHar = []
pyplot.grid(True)
[y, x] = matlab.step(w, time)
pyplot.hlines(1, 0, 60, color='r', linewidth=1, linestyle='-')
pyplot.hlines(1.05, 0, 60, color='g', linewidth=1, linestyle='--')
pyplot.hlines(0.95, 0, 60, color='g', linewidth=1, linestyle='--')
pyplot.vlines(15, 0, 1.3, color='b', linewidth=1, linestyle='-')
pyplot.plot(x, y)
pyplot.title('Переходна характеристика')
pyplot.ylabel('Амплитуда')
pyplot.xlabel('Время')
pyplot.show()
yPerehHar.append(y)
xPerehHar.append(x)

# Время регулирование по переходной характеристики
granica1 = 1 + (1 * 0.05)
granica2 = 1 - (1 * 0.05)

yDan = []
xDan = []
j=1
for i in range(len(xPerehHar)):
    for j in range(len(xPerehHar[i])):
        if ((yPerehHar[i][j-1] >= granica1) and (yPerehHar[i][j] <= granica1)) \
                or ((yPerehHar[i][j-1] <= granica2) and (yPerehHar[i][j] >= granica2)):
            lastY = yPerehHar[i][j]
            lastX = xPerehHar[i][j]
    yDan.append(lastY)
    xDan.append(lastX)
treg = xDan[0]

print("tрег= ", treg)

#Определение перерегулирования по переходной характеристики
k = 0
for i in yPerehHar:
    for j in i:
        if (j >= k):
            k = j
perereg = (k - 1) / (1)
perereg = perereg * 100
print("Перерегулирование= ", perereg)

#Определение колебательности по переходной характеристики
koleb = 0
koleb1 = []
yy = []
j = 1
for i in range(len(yPerehHar)):
    for j in range(len(yPerehHar[i])):
        if (xPerehHar[i][j] == treg):
            break
        if (yPerehHar[i][j] > yPerehHar[i][j - 1]) and (yPerehHar[i][j] > yPerehHar[i][j + 1]):
            koleb+=1
    koleb1.append(koleb)

print("Колебательность= ", koleb1[0])
#Степень затухания
yZatuhL = []
j = 1
for i in range(len(yPerehHar)):
    for j in range(len(yPerehHar[i])):
        if (xPerehHar[i][j] == treg):
            break
        if (yPerehHar[i][j] > yPerehHar[i][j - 1]) and (yPerehHar[i][j] > yPerehHar[i][j + 1]):
            yZatuh = yPerehHar[i][j]
            yZatuhL.append(yZatuh)
    yZatuhL.append(0)
    if yZatuhL[1] != 0:
        stepzatuh = (yZatuhL[1] - yZatuhL[0]) / (yZatuhL[1])
    else:
        stepzatuh = 1
print("Степень затухания= ", stepzatuh)
# Определение величиеы и времени достижения первого максимума
yMax = 0.0
j = 1
for i in range(len(yPerehHar)):
    for j in range(len(yPerehHar[i])):
        if (yPerehHar[i][j] > yMax):
            yMax = yPerehHar[i][j]
            tMax = xPerehHar[i][j]
print("Величина первого максимума = ", yMax, "\n"
"Время достижения первого максимума = ", tMax)

# находим корни характеристичкского уравнения и определяем устойчивость системы
korny = matlab.pzmap(w)
pyplot.axis([-3, 1,-1, 1])
pyplot.show()
pole = matlab.pole(w)
print(pole)
deistv = []
for i in pole:
    kx = i.real
    deistv.append(kx)
if (min(deistv) > 0.0001):
    print("система неустйочива по корням характеристического уравнения")
elif (max(deistv) < -0.0001):
    print("система устойчива по корням характеристического уравнения")
else:
    print("система на границе устойчивости")

# Время регулирования по-корневому методу
treg = 3/abs(max(deistv))
print("Время регулирования =", treg)

# Степень колебательности
mnim = []
for i in pole:
    ky = i.imag
    mnim.append(ky)
stepenKoleb = abs(max(mnim))/abs(max(deistv))
print("Степень колебательности = ", stepenKoleb)

# Перерегулирвоание
perereg = math.e**(-math.pi/stepenKoleb)*100
print("Перерегулирвоание = ", perereg)
# Степень затухания
stepenZatuh = 1 - math.e**(-2*math.pi/stepenKoleb)
print("Степень затухания = ", stepenZatuh)

time2 = []
for i in range(0, 100):
    time2.append(i/100)
pyplot.subplot()
pyplot.grid(True)
mag, phase, omega = matlab.freqresp(w, time2)
pyplot.plot(mag)
pyplot.title('АЧХ')
pyplot.ylabel('Амплитуда')
pyplot.xlabel('угловая частота, (рад/с)')
pyplot.show()

pyplot.grid(True)
pyplot.title('ФЧХ')
pyplot.ylabel('Фаза')
pyplot.xlabel('Угловая частота, (рад/с)')
pyplot.plot(phase*180/math.pi)
pyplot.show()

# Показатель калебательности
amax = max(mag)
anol = mag[0]
m = amax/anol
print("Показатель колебательности", m)
# Время регулирования
mag1 = numpy.delete(mag, 0)
omega1 = numpy.delete(omega, 0)
for i in range(len(mag1)):
    if mag1[i] > mag[0] and mag1[i+1] < mag[0]:
        omegasrez = i
omsrez = omega1[omegasrez]
print("Омега среза", omsrez)
treg = 1*2*math.pi/omsrez
print("Время регулирования", treg)


mag, phase, omega = matlab.bode(w)
pyplot.plot()
pyplot.show()
mag1 = numpy.delete(mag, 0)
phase1 = numpy.delete(phase, 0)
for i in range(len(mag1)):
    if mag1[i] <= mag[0] and mag1[i-1] >= mag[0]:
        omegasrez = i
omsrez = phase1[omegasrez]*180/math.pi
fase = 180 - abs(omsrez)
print("Запас устойчивости по фазе через ЛАЧХ и ЛФЧХ = ", fase)
k = 0
for i in range(len(phase)):
    if phase[i] == 180:
        k==1
        indexMaxPhase = i
if k == 1:
    ampl = abs(mag[indexMaxPhase])
    print("Запас устойчивости по амплитуде через ЛАЧХ и ЛФЧХ = ", ampl)
else:
    print("Запас устойчивости по амплитуде равен бесконечности")

yy = []
for i in y:
    yy.append(1-i)
I1 = integrate.trapezoid(yy, x)
print('Интегральная оценка ', I1)


w5 = PIDReg(0.17, 0, 0)

w6 = matlab.series(w5, w4)

w = matlab.feedback(w6, 1)

print("W(p) = ", w)
time = []
for i in range(0, 6000):
    time.append(i/100)
# Строим переходную характеристику
pyplot.subplot()
yPerehHar = []
xPerehHar = []
pyplot.grid(True)
[y, x] = matlab.step(w, time)
pyplot.hlines(0.78, 0, 60, color='r', linewidth=1, linestyle='-')
pyplot.hlines(0.819, 0, 60, color='g', linewidth=1, linestyle='--')
pyplot.hlines(0.741, 0, 60, color='g', linewidth=1, linestyle='--')
pyplot.vlines(15, 0, 1.3, color='b', linewidth=1, linestyle='-')
pyplot.plot(x, y)
pyplot.title('Переходна характеристика')
pyplot.ylabel('Амплитуда')
pyplot.xlabel('Время')
pyplot.show()
yPerehHar.append(y)
xPerehHar.append(x)

# Время регулирование по переходной характеристики
granica1 = 0.78 + (0.78 * 0.05)
granica2 = 0.78 - (0.78 * 0.05)

yDan = []
xDan = []
j=1
for i in range(len(xPerehHar)):
    for j in range(len(xPerehHar[i])):
        if ((yPerehHar[i][j-1] >= granica1) and (yPerehHar[i][j] <= granica1)) \
                or ((yPerehHar[i][j-1] <= granica2) and (yPerehHar[i][j] >= granica2)):
            lastY = yPerehHar[i][j]
            lastX = xPerehHar[i][j]
    yDan.append(lastY)
    xDan.append(lastX)
treg = xDan[0]

print("tрег= ", treg)

#Определение перерегулирования по переходной характеристики
k = 0
for i in yPerehHar:
    for j in i:
        if (j >= k):
            k = j
perereg = (k - 0.78) / (0.78)
perereg = perereg * 100
print("Перерегулирование= ", perereg)

#Определение колебательности по переходной характеристики
koleb = 0
koleb1 = []
yy = []
j = 1
for i in range(len(yPerehHar)):
    for j in range(len(yPerehHar[i])):
        if (xPerehHar[i][j] == treg):
            break
        if (yPerehHar[i][j] > yPerehHar[i][j - 1]) and (yPerehHar[i][j] > yPerehHar[i][j + 1]):
            koleb+=1
    koleb1.append(koleb)

print("Колебательность= ", koleb1[0])
# #Степень затухания
# yZatuhL = []
# j = 1
# for i in range(len(yPerehHar)):
#     for j in range(len(yPerehHar[i])):
#         if (xPerehHar[i][j] == treg):
#             break
#         if (yPerehHar[i][j] > yPerehHar[i][j - 1]) and (yPerehHar[i][j] > yPerehHar[i][j + 1]):
#             yZatuh = yPerehHar[i][j]
#             yZatuhL.append(yZatuh)
#     yZatuhL.append(0)
#     if yZatuhL[1] != 0:
#         stepzatuh = (yZatuhL[1] - yZatuhL[0]) / (yZatuhL[1])
#     else:
#         stepzatuh = 1
# print("Степень затухания= ", stepzatuh)
# Определение величиеы и времени достижения первого максимума
yMax = 0.0
j = 1
for i in range(len(yPerehHar)):
    for j in range(len(yPerehHar[i])):
        if (yPerehHar[i][j] > yMax):
            yMax = yPerehHar[i][j]
            tMax = xPerehHar[i][j]
print("Величина первого максимума = ", yMax, "\n"
"Время достижения первого максимума = ", tMax)

# находим корни характеристичкского уравнения и определяем устойчивость системы
korny = matlab.pzmap(w)
pyplot.axis([-3, 1,-1, 1])
pyplot.show()
pole = matlab.pole(w)
print(pole)
deistv = []
for i in pole:
    kx = i.real
    deistv.append(kx)
if (min(deistv) > 0.0001):
    print("система неустйочива по корням характеристического уравнения")
elif (max(deistv) < -0.0001):
    print("система устойчива по корням характеристического уравнения")
else:
    print("система на границе устойчивости")

# Время регулирования по-корневому методу
treg = 3/abs(max(deistv))
print("Время регулирования =", treg)

# Степень колебательности
mnim = []
for i in pole:
    ky = i.imag
    mnim.append(ky)
stepenKoleb = abs(max(mnim))/abs(max(deistv))
print("Степень колебательности = ", stepenKoleb)

# Перерегулирвоание
perereg = math.e**(-math.pi/stepenKoleb)*100
print("Перерегулирвоание = ", perereg)
# Степень затухания
stepenZatuh = 1 - math.e**(-2*math.pi/stepenKoleb)
print("Степень затухания = ", stepenZatuh)

time2 = []
for i in range(0, 100):
    time2.append(i/100)
pyplot.subplot()
pyplot.grid(True)
mag, phase, omega = matlab.freqresp(w, time2)
pyplot.plot(mag)
pyplot.title('АЧХ')
pyplot.ylabel('Амплитуда')
pyplot.xlabel('угловая частота, (рад/с)')
pyplot.show()

pyplot.grid(True)
pyplot.title('ФЧХ')
pyplot.ylabel('Фаза')
pyplot.xlabel('Угловая частота, (рад/с)')
pyplot.plot(phase*180/math.pi)
pyplot.show()

# Показатель калебательности
amax = max(mag)
anol = mag[0]
m = amax/anol
print("Показатель колебательности", m)
# Время регулирования
mag1 = numpy.delete(mag, 0)
omega1 = numpy.delete(omega, 0)
for i in range(len(mag1)):
    if mag1[i] > mag[0] and mag1[i+1] < mag[0]:
        omegasrez = i
omsrez = omega1[omegasrez]
print("Омега среза", omsrez)
treg = 1*2*math.pi/omsrez
print("Время регулирования", treg)


mag, phase, omega = matlab.bode(w)
pyplot.plot()
pyplot.show()
mag1 = numpy.delete(mag, 0)
phase1 = numpy.delete(phase, 0)
for i in range(len(mag1)):
    if mag1[i] <= mag[0] and mag1[i-1] >= mag[0]:
        omegasrez = i
omsrez = phase1[omegasrez]*180/math.pi
fase = 180 - abs(omsrez)
print("Запас устойчивости по фазе через ЛАЧХ и ЛФЧХ = ", fase)
k = 0
for i in range(len(phase)):
    if phase[i] == 180:
        k==1
        indexMaxPhase = i
if k == 1:
    ampl = abs(mag[indexMaxPhase])
    print("Запас устойчивости по амплитуде через ЛАЧХ и ЛФЧХ = ", ampl)
else:
    print("Запас устойчивости по амплитуде равен бесконечности")

yy = []
for i in y:
    yy.append(1-i)
I1 = integrate.trapezoid(yy, x)
print('Интегральная оценка ', I1)