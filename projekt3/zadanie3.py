def gll(seed,a,c,m,N,czy_przedzial):
    x = seed
    for i in range(N):
        x =  (a*x+c)%m
        if czy_przedzial == True:
            yield x/m
        else:
            yield x
            
        

seed = 1
a = 5
c = 3
m = 16
N = 3

gen = gll(seed,a,c,m,N,czy_przedzial=True)

print(f'Pierwsza liczba: {next(gen)}')
print(f'Druga liczba: {next(gen)}')
print(f'Trzecia liczba: {next(gen)}')


gen_for = gll(seed,a,c,m,N,czy_przedzial=True)

liczby = []

for liczba in gen_for:
    liczby.append(liczba)

print(liczby)