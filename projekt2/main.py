import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from numba import njit
import time
N = 130
J = 1.0
beta = 0.4
B = 0
M = 300


# print('Podaj wielkosc siatki:')
# N = int(input())
# print('Podaj stałą oddziaływania J:')
# J = float(input())
# print('Podaj parametr temperatury beta = 1/k_b*T:')
# beta = float(input())
# print('Podaj wartość zewnętrznego pola magentycznego:')
# B = float(input())
# print('Podaj liczbę makrokroków:')
# M = int(input())

def generator_siatki(N):
    return np.random.choice([-1,1],size = (N,N))

siatka = generator_siatki(N)

#################################################
#                  Bez Numby
#################################################


def deltaE_bn(siatka,wiersz,kolumna,J,B):
    s = siatka[wiersz,kolumna]
    suma_spinow_sasiadow = siatka[(wiersz-1)%N,(kolumna-1)%N] + siatka[(wiersz-1)%N,(kolumna)%N] + siatka[(wiersz-1)%N,(kolumna+1)%N] + siatka[(wiersz)%N,(kolumna-1)%N] + siatka[(wiersz)%N,(kolumna+1)%N] + siatka[(wiersz+1)%N,(kolumna-1)%N] + siatka[(wiersz+1)%N,(kolumna)%N] + siatka[(wiersz+1)%N,(kolumna+1)%N]
    dE = 2*s*(J*(suma_spinow_sasiadow)+B)
    return dE


def E_bn(siatka,J,B):
    H = 0
    suma_wszystkich_spinow = 0
    for wiersz in range(N):
        for kolumna in range(N):
            suma_wszystkich_spinow += siatka[wiersz,kolumna]
            suma_spinow_sasiadow = siatka[(wiersz-1)%N,(kolumna-1)%N] + siatka[(wiersz-1)%N,(kolumna)%N] + siatka[(wiersz-1)%N,(kolumna+1)%N] + siatka[(wiersz)%N,(kolumna-1)%N] + siatka[(wiersz)%N,(kolumna+1)%N] + siatka[(wiersz+1)%N,(kolumna-1)%N] + siatka[(wiersz+1)%N,(kolumna)%N] + siatka[(wiersz+1)%N,(kolumna+1)%N]
            H = H -J*suma_spinow_sasiadow*siatka[wiersz,kolumna]
    H = H/2 - B*suma_wszystkich_spinow
    return H


def Magnetyzacja_bn(siatka,N):
    suma_wszystkich_spinow = 0
    for wiersz in range(N):
        for kolumna in range(N):
            suma_wszystkich_spinow += siatka[wiersz,kolumna]
    return (1/(N**2))*suma_wszystkich_spinow

def sim_bn(siatka_pocz,M,J,B):
    siatka = siatka_pocz
    for q in range(M):
        for krok in range(N**2):
            kolumna = np.random.randint(0,N)
            wiersz = np.random.randint(0,N)
            dE = deltaE_bn(siatka,wiersz,kolumna,J,B)
            if dE<0:
                siatka[wiersz,kolumna] = -siatka[wiersz,kolumna]
            else:
                p = np.exp(-(beta*dE))
                war = np.random.random()
                if(war<p):
                    siatka[wiersz,kolumna] = -siatka[wiersz,kolumna]
                else:
                    pass
    return siatka

czas_pocz = time.time()
smiec = sim_bn(siatka,M,J,B)
czas_bez_numby = time.time()-czas_pocz
print(f'Czas działania programu bez numby: {czas_bez_numby:.3f}')


#################################################
#                  Z Numbą
#################################################

@njit
def deltaE(siatka,wiersz,kolumna,J,B):
    s = siatka[wiersz,kolumna]
    suma_spinow_sasiadow = siatka[(wiersz-1)%N,(kolumna-1)%N] + siatka[(wiersz-1)%N,(kolumna)%N] + siatka[(wiersz-1)%N,(kolumna+1)%N] + siatka[(wiersz)%N,(kolumna-1)%N] + siatka[(wiersz)%N,(kolumna+1)%N] + siatka[(wiersz+1)%N,(kolumna-1)%N] + siatka[(wiersz+1)%N,(kolumna)%N] + siatka[(wiersz+1)%N,(kolumna+1)%N]
    dE = 2*s*(J*(suma_spinow_sasiadow)+B)
    return dE

@njit
def E(siatka,J,B):
    H = 0
    suma_wszystkich_spinow = 0
    for wiersz in range(N):
        for kolumna in range(N):
            suma_wszystkich_spinow += siatka[wiersz,kolumna]
            suma_spinow_sasiadow = siatka[(wiersz-1)%N,(kolumna-1)%N] + siatka[(wiersz-1)%N,(kolumna)%N] + siatka[(wiersz-1)%N,(kolumna+1)%N] + siatka[(wiersz)%N,(kolumna-1)%N] + siatka[(wiersz)%N,(kolumna+1)%N] + siatka[(wiersz+1)%N,(kolumna-1)%N] + siatka[(wiersz+1)%N,(kolumna)%N] + siatka[(wiersz+1)%N,(kolumna+1)%N]
            H = H -J*suma_spinow_sasiadow*siatka[wiersz,kolumna]
    H = H/2 - B*suma_wszystkich_spinow
    return H

@njit
def Magnetyzacja(siatka,N):
    suma_wszystkich_spinow = 0
    for wiersz in range(N):
        for kolumna in range(N):
            suma_wszystkich_spinow += siatka[wiersz,kolumna]
    return (1/(N**2))*suma_wszystkich_spinow

@njit
def sim_n(siatka_pocz,M,J,B):
    siatka = siatka_pocz
    for q in range(M):
        for krok in range(N**2):
            kolumna = np.random.randint(0,N)
            wiersz = np.random.randint(0,N)
            dE = deltaE(siatka,wiersz,kolumna,J,B)
            if dE<0:
                siatka[wiersz,kolumna] = -siatka[wiersz,kolumna]
            else:
                p = np.exp(-(beta*dE))
                war = np.random.random()
                if(war<p):
                    siatka[wiersz,kolumna] = -siatka[wiersz,kolumna]
                else:
                    pass
    return siatka

smiec_rozgrzewkowy = sim_n(siatka.copy(), 1, J, B)
czas_pocz = time.time()
smiec = sim_n(siatka.copy(),M,J,B)
czas_z_numba = time.time() - czas_pocz
print(f'Czas działania programu bez numby: {czas_z_numba:.3f}')
print(f'Numba jest {czas_bez_numby/czas_z_numba:.3f} razy szybsza')

#################################################
#                  Animacja
#################################################


siatka = generator_siatki(N)
    
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(14, 5))
obraz = ax1.matshow(siatka, cmap = 'coolwarm',vmin = -1, vmax = 1)
ax1.axis('off')
ax1.set_title('Ewolucja spinów    Numer kroku:  0')


E_wykres, = ax2.plot([],[],color = 'magenta')
kroki = []
energia_historia = []
ax2.set_title('Całkowita energia')
ax2.set_xlabel('makrokrok')
ax2.set_ylabel('Energia całkowita')
ax2.set_xlim(0, M)
ax2.grid(True)


M_wykres, = ax3.plot([],[],color = 'red')
magnetyzacja_historia = []
ax3.set_title('Magnetyzacja')
ax3.set_xlabel('makrokrok')
ax3.set_ylabel('Magnetyzacja')
ax3.set_xlim(0, M)
ax3.grid(True)


def update(klatka):
    for krok in range(N**2):
        kolumna = np.random.randint(0,N)
        wiersz = np.random.randint(0,N)
        dE = deltaE(siatka,wiersz,kolumna,J,B)
        if dE<0:
            siatka[wiersz,kolumna] = -siatka[wiersz,kolumna]
        else:
            p = np.exp(-(beta*dE))
            war = np.random.random()
            if(war<p):
                siatka[wiersz,kolumna] = -siatka[wiersz,kolumna]
            else:
                pass
    obraz.set_data(siatka)
    ax1.set_title(f'Ewolucja spinów    Numer kroku:  {klatka+1}')
    kroki.append(klatka)
    energia_historia.append(E(siatka,J,B))
    E_wykres.set_data(kroki,energia_historia)

    magnetyzacja_historia.append(Magnetyzacja(siatka,N))
    M_wykres.set_data(kroki,magnetyzacja_historia)
    ax2.set_ylim(min(energia_historia) - 1000, max(energia_historia) + 1000)
    ax3.set_ylim(min(magnetyzacja_historia), max(magnetyzacja_historia))
    return obraz, E_wykres, M_wykres


animacja = FuncAnimation(fig,update,frames=M, interval = 10,blit = False, repeat = False)

plt.tight_layout()
plt.show()