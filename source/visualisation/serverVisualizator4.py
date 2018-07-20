ARR_LEN = 64
SEC_LEN = 32
DISCR_F = 200
AMP_THR = 200
EMG_THR = 230
MOVE_THR = 50
AMP_F_THR = 6000
CNT = 2
RESET_TIME = 15
MODIF = 12 #20

import matplotlib.pyplot as plt
from tkinter import filedialog
from matplotlib import animation
from matplotlib.widgets import Button
from math import ceil, sqrt
#import serial
from requests import get
from base64 import b64decode, b64encode
from json import loads

from random import randint
from time import time

# com = serial.Serial('/dev/ttyACM0', 115200, timeout = 1)

# while True:
#   print(com.readline().decode()[:-2])

fig = plt.figure()
fig.canvas.set_window_title('Tremor monitor')

# f = open('data.txt','r')

a1 = [0 for i in range(ARR_LEN)]
g1 = [0 for i in range(ARR_LEN)]
e1 = [0 for i in range(ARR_LEN)]

a2 = [0 for i in range(ARR_LEN)]
g2 = [0 for i in range(ARR_LEN)]
e2 = [0 for i in range(ARR_LEN)]

timea = [0 for i in range(SEC_LEN)]

metka1 = [[250], [250]]
metka2 = [[0], [0]]
metka3 = [[0], [0]]

f1 = plt.subplot2grid((4, 2),(0,0), xticks=[], yticks=[], ylabel = 'Движение')
f2 = plt.subplot2grid((4, 2),(1,0), xticks=[], yticks=[], ylabel = 'Поворот')
f3 = plt.subplot2grid((4, 2),(0,1), xticks=[], yticks=[], ylabel = 'ЭМГ')
f4 = plt.subplot2grid((4, 2),(2,0), xticks=[], yticks=[], rowspan = 2, ylim = (0, 400), xlim = (0, 370))
f7 = plt.subplot2grid((4, 2),(1,1), xticks=[], yticks=[], ylabel = '', xlim=(0,500), ylim=(0,500), rowspan=3)
f8 = plt.subplot2grid((18, 15),(17,7), xticks=[], yticks=[])

f3.plot([EMG_THR for i in range(ARR_LEN)], color='black', lw=1)
f3.plot([255-EMG_THR for i in range(ARR_LEN)], color='black', lw=1)

f4.plot([-10, 1000], [195, 195], color='black', lw=1)
f4.plot([-10, 1000], [320, 320], color='black', lw=1)

p71, = f7.plot(metka1[0], metka1[1], color = 'darkmagenta')
p72, = f7.plot(metka2[0], metka2[1], color = 'forestgreen')
p73, = f7.plot(metka3[0], metka3[1], color = 'midnightblue')

p1, = f1.plot(a1, color = 'darkred')
p2, = f2.plot(g1, color = 'darkblue')
p3, = f3.plot(e1, color = 'green')

tp1 = f4.text(10, 10,'None')
tp2 = f3.text(0, 260 - EMG_THR, '')
tbp = f4.text(10, 330, 'Болезнь Паркинсона  0%')
tts = f4.text(10, 210, '|\n|\n|')

f1.set_ylim(-7000, 8000)
f2.set_ylim(-7000, 8000)
f3.set_ylim(0, 255)

t_p = 'Нет'
t_k = 'Нет'
t_s = 'Нет'

bp_rating = 0

rst_t = 0

def rst(wtf = None):
  global rst_t, t_k, t_p, t_s, bp_rating, metka1
  metka1 = [[250], [250]]
  t_p = 'Нет'
  t_k = 'Нет'
  t_s = 'Нет'
  bp_rating = 0
  print('\nRESET\n')
butt = Button(f8, 'RST')
butt.on_clicked(rst)

# g1.set_title('Accelerometer')
# g4.set_title('Gyroscope')

# g1.ylabel('X')
# g2.ylabel('Y')
# g3.ylabel('Z')

def calcData(data):
  # data = [rdata[0]]
  # for i in range(1, len(rdata)):
  #   data.append(data[i-1]*0.5+rdata[i]*0.5)
  go_up = True
  peaks = 0
  amps = []
  delta = data[0]
  for i in range(1, len(data)):
    # print(data[i])
    if (data[i] > data[i-1]) and not go_up:
      go_up = True
      a = abs(delta-data[i])
      if a > AMP_THR:
        amps.append(a)
        delta = data[i]
        peaks += 1
    elif (data[i] < data[i-1]) and go_up:
      go_up = False
      a = abs(delta-data[i])
      if a > AMP_THR:
        amps.append(a)
        delta = data[i]
        peaks += 1
  peaks = ceil(abs(peaks - 1) / 2)
  # peaks = abs(peaks - 1)
  # amps.pop(0)
  if amps == []: amp = 0
  else: amp = amps[-1] #sum(amps) / len(amps)
  if amp == 0: peaks = 0
  return peaks, amp

maxv = [0,0,0,0,0,0]
minv = [0,0,0,0,0,0]

def animate(i):
  global rst_t, t_k, t_p, t_s, bp_rating
  # d = [int(i) for i in com.readline().decode().split()]  
  # if len(d) < 6: return p1, p2, p3, p4, p5, p6, pp1, pa1, pp2, pa2, pp3, pa3, pp4, pa4, pp5, pa5, pp6, pa6

  d = loads(get('http://192.168.43.102/{}'.format(b64encode('get_esp_4 {}'.format(CNT).encode('utf-8')).decode('utf-8'))).text)
  dcv = loads(get('http://192.168.43.102:4444/{}'.format(b64encode('get_opencv {}'.format(CNT).encode('utf-8')).decode('utf-8'))).text)
  dcv[0]['x'] = 0
  dcv[1]['x'] = 0
  # d = [{'ax':randint(-3000,3000),'ay':randint(-3000,3000),'az':randint(-3000,3000),'gx':randint(-3000,3000),'gy':randint(-3000,3000),'gz':randint(-3000,3000),'time':time(),'emg':randint(0,255),'m1':[randint(0,500),randint(0,500)],'m2':[randint(0,500),randint(0,500)],'m3':[randint(0,500),randint(0,500)]}]
  #d = [{'ax':randint(-3000,3000),'ay':randint(-3000,3000),'az':randint(-3000,3000),'gx':randint(-3000,3000),'gy':randint(-3000,3000),'gz':randint(-3000,3000),'time':time(),'emg':randint(0,255)}]
  #dcv = [{'x':randint(0,500),'y':randint(0,500)}]

  #print(d)
  #print(dcv)

  d = d[0]
  dcv = dcv[0]
  timea.append(d['time'])
  timea.pop(0)

  a1.append(d['ax']+d['ay']+d['az'])
  g1.append(d['gx']+d['gy']+d['gz'])
  e1.append(d['emg'])
  
  s = sqrt((metka1[0][-1]-dcv['x'])**2 + (metka1[1][-1]-dcv['y'])**2)

  metka1[0].append(dcv['x'])
  metka1[1].append(dcv['y'])
  # metka2[0].append(d['m2'][0])
  # metka2[1].append(d['m2'][1])
  # metka3[0].append(d['m3'][0])
  # metka3[1].append(d['m3'][1])

  p71.set_data(metka1[0], metka1[1])
  # p72.set_data(metka2[0], metka2[1])
  # p73.set_data(metka3[0], metka3[1])

  calc1 = calcData(a1[-SEC_LEN:])
  calc2 = calcData(g1[-SEC_LEN:])
  ps = calc1[0] + calc2[0]
  ams = calc1[1] + calc2[1]
  if d['emg'] > EMG_THR or d['emg'] < 255-EMG_THR: mio = True
  else: mio = False
  freq = ps/max(0.0001,timea[-1]-timea[0])
  tp1.set_text('Мышцы напряжены   {}\nПеремещение             {}\nПики                            {}\nАмплитуда                  {}\nЧастота                       {}'.format(
    'Да' if mio else 'Нет',
    round(s, 2), ps, round(ams/6, 2), round(freq,2)))

  if ams > AMP_F_THR:
    # print('\n\nAAAAAAAAAAAAA {} {} {}\n\n'.format(t_p, t_k, t_s))
    rst_t = time()
    if mio:
      if s > MOVE_THR and t_k != 'Да':
        print('Кинетический тремор')
        t_k = 'Да'
        bp_rating += 0.2
        if freq >= 4 and freq <= 9: bp_rating += 0.5
      elif t_s != 'Да':
        print('Постуральный тремор')
        t_s = 'Да'
        bp_rating += 0.2
        if freq >= 4 and freq <= 9: bp_rating += 0.5
    elif t_p != 'Да':
      print('Тремор покоя')
      bp_rating += 2
      t_p = 'Да'
      if freq >= 4 and freq <= 9: bp_rating += 0.5
  elif time() - rst_t > RESET_TIME:
    t_p = 'Нет'
    t_k = 'Нет'
    t_s = 'Нет'
    bp_rating = 0
    print('\nRESET\n')
  # print('\n\ggggg {} {} {}\n\n'.format(t_p, t_k, t_s))
  tts.set_text('Тремор покоя             {}\nКинетический            {}\nПостуральный            {}'.format(t_p, t_k, t_s))
  tbp.set_text('Болезнь Паркинсона  {}%'.format(round(bp_rating*MODIF, 1)))

  if d['emg'] > EMG_THR or d['emg'] < 255-EMG_THR: tp2.set_text('TRIGGERED')
  else: tp2.set_text('')

  a1.pop(0)
  g1.pop(0)
  e1.pop(0)

  p1.set_data(range(ARR_LEN), a1[-ARR_LEN:])
  p2.set_data(range(ARR_LEN), g1[-ARR_LEN:])
  p3.set_data(range(ARR_LEN), e1[-ARR_LEN:])

  return p1, p2, p3, tp1, tp2, p71, p72, p73, tts, tbp

# com.readline()

input('PRESS ENTER TO START')

anim = animation.FuncAnimation(fig, animate, frames = 200, interval = 50, blit = True)

plt.show()
