import time
import numpy as np

def Decorator(czy_wyswietlac_statystyki=False,ilosc_zachowanych_statystyk = 10):
    class TimerDecorator:
        def __init__(self,func):
            self.func = func
            self.ilosc_wywolan = 0
            self.czas_dzialania_funkcji = 0
            self.historia_pomiarow = {'czasy_dzialania':[]}
            self.czy_wyswietlac_statystyki = czy_wyswietlac_statystyki
        
        def __call__(self,*args,**kwargs):
            czas_poczatkowy = time.time()
            self.ilosc_wywolan += 1
            res = self.func(*args,**kwargs)

            self.czas_dzialania_funkcji = time.time() - czas_poczatkowy
            self.historia_pomiarow['czasy_dzialania'].append(self.czas_dzialania_funkcji)

            if len(self.historia_pomiarow['czasy_dzialania'])>ilosc_zachowanych_statystyk:
                del self.historia_pomiarow['czasy_dzialania'][0]
            if self.czy_wyswietlac_statystyki == True:
                print(f'Ilosc wywolan: {len(self.historia_pomiarow["czasy_dzialania"])}')
                print(f'Najkrotszy czas dzialania: {min(self.historia_pomiarow["czasy_dzialania"])}')
                print(f'Najdluzszy czas dzialania: {max(self.historia_pomiarow["czasy_dzialania"])}')
                print(f'Sredni czas dzialania: {np.mean(self.historia_pomiarow["czasy_dzialania"])}')
            

            return res
    return TimerDecorator

@Decorator(czy_wyswietlac_statystyki=True)       #Aby wyswietlic statystyki, wpisac w nawiasy czy_wyswietlac_statystyki=true. Aby ustalic dlugosc listy z statystykami, wpisac ilosc_zachowanych_statystyk = x
def f(a,b,c):
    for i in range(10000000):
        q = a+b+c
    return q

for i in range(20):
    a = f(i,i+1,i+2)
    print(a)
print(f.historia_pomiarow)