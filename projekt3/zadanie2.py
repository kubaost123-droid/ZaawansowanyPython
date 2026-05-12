class Temperature:
    zero_c = -273.15
    def __init__(self,t):
        self.celsius = t

    @property
    def celsius(self):
        return self._celsius
    
    @celsius.setter
    def celsius(self,t):
        if(t>=self.zero_c):
            self._celsius = t
        else:
            self._celsius = self.zero_c

    @property
    def fahrenheit(self):
        return self.celsius*1.8 + 32
    
    @fahrenheit.setter
    def fahrenheit(self,t):
        self.celsius = (t-32) / 1.8

    @property
    def kelwin(self):
        return self._celsius - self.zero_c
    
    @kelwin.setter
    def kelwin(self,t):
        self.celsius = t + self.zero_c

    def __repr__(self):
        return f'Temperatura w stopniach celsjusza wynosi {self.celsius} °C \nTemperatura w stopniach fahrenheita wynosi {self.fahrenheit} °F \nTemperatura w kalwinach wynosi {self.kelwin} K'

    @property
    def wrzenie(self):
        return self.celsius>=100
    
    @property
    def zamarazanie(self):
        return self.celsius<=0
    
    @property
    def stan_skupienia(self):
        if self.celsius>100:
            return 'Stan gazowy'
        if 0<self.celsius<=100:
            return 'Stan ciekly'
        else:
            return 'Stan staly'
    


t = Temperature(30)

print(t)

if t.wrzenie:
    print('Woda sie gotuje!')
else:
    print('Woda sie nie gotuje!')

if t.zamarazanie:
    print('Woda zamarla!')
else:
    print('Woda nie zamarzla!')

print(t.stan_skupienia)

    

    

    