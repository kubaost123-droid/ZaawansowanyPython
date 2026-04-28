import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from numba import njit
import time
N = 100
J = 1.0
beta = 0.4
B = 0
M = 100


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


def siatka(N):
    return np.random.choice([-1,1],size = (N,N))

def deltaE(siatka,wiersz,kolumna,J,B):
    s = siatka[wiersz][kolumna]
    suma_spinow_sasiadow = siatka[(wiersz-1)%N][(kolumna-1)%N] + siatka[(wiersz-1)%N][(kolumna)%N] + siatka[(wiersz-1)%N][(kolumna+1)%N] + siatka[(wiersz)%N][(kolumna-1)%N] + siatka[(wiersz)%N][(kolumna+1)%N] + siatka[(wiersz+1)%N][(kolumna-1)%N] + siatka[(wiersz+1)%N][(kolumna)%N] + siatka[(wiersz+1)%N][(kolumna+1)%N]
    dE = 2*s*(J*(suma_spinow_sasiadow)+B)
    return dE


def E(siatka,J,B):
    H = 0
    suma_wszystkich_spinow = 0
    for wiersz in range(N):
        for kolumna in range(N):
            suma_wszystkich_spinow += siatka[wiersz][kolumna]
            suma_spinow_sasiadow = siatka[(wiersz-1)%N][(kolumna-1)%N] + siatka[(wiersz-1)%N][(kolumna)%N] + siatka[(wiersz-1)%N][(kolumna+1)%N] + siatka[(wiersz)%N][(kolumna-1)%N] + siatka[(wiersz)%N][(kolumna+1)%N] + siatka[(wiersz+1)%N][(kolumna-1)%N] + siatka[(wiersz+1)%N][(kolumna)%N] + siatka[(wiersz+1)%N][(kolumna+1)%N]
            H = H -J*suma_spinow_sasiadow*siatka[wiersz][kolumna]
    H = H/2 - B*suma_wszystkich_spinow
    return H

def Magnetyzacja(siatka,N):
    suma_wszystkich_spinow = 0
    for wiersz in range(N):
        for kolumna in range(N):
            suma_wszystkich_spinow += siatka[wiersz][kolumna]
    return (1/(N**2))*suma_wszystkich_spinow


siatka = siatka(N)
    
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12, 5))
obraz = ax1.matshow(siatka, cmap = 'coolwarm',vmin = -1, vmax = 1)
ax1.axis('off')
ax1.set_title('Ewolucja spinów')


E_wykres, = ax2.plot([],[],color = 'magenta')
kroki = []
energia_historia = []
ax2.set_title('Całkowita energia')
ax2.set_xlabel('makrokrok')
ax2.set_ylabel('Energia całkowita')
ax2.set_xlim(0, M)


M_wykres, = ax3.plot([],[],color = 'red')
magnetyzacja_historia = []
ax3.set_title('Magnetyzacja')
ax3.set_xlabel('makrokrok')
ax3.set_ylabel('Magnetyzacja')
ax3.set_xlim(0, M)

def update(klatka):
    for krok in range(N**2):
        kolumna = np.random.choice(N)
        wiersz = np.random.choice(N)
        dE = deltaE(siatka,wiersz,kolumna,J,B)
        if dE<0:
            siatka[wiersz,kolumna] = -siatka[wiersz,kolumna]
        else:
            p = np.exp(-(beta*dE))
            war = np.random.rand(1)
            if(war<p):
                siatka[wiersz,kolumna] = -siatka[wiersz,kolumna]
            else:
                pass
    obraz.set_data(siatka)
    kroki.append(klatka)
    energia_historia.append(E(siatka,J,B))
    E_wykres.set_data(kroki,energia_historia)

    magnetyzacja_historia.append(Magnetyzacja(siatka,N))
    M_wykres.set_data(kroki,magnetyzacja_historia)
    ax2.set_ylim(min(energia_historia) - 1000, max(energia_historia) + 1000)
    ax3.set_ylim(min(magnetyzacja_historia), max(magnetyzacja_historia))
    return obraz, E_wykres, 

animacja = FuncAnimation(fig,update,frames=M, interval = 10,blit = False)
plt.tight_layout()
plt.show()


