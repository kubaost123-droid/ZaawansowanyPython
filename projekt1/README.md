W pliku main.py jest klasa symulacja która zarządza całym działaniem programu. Konstruktor tworzy wszystkie potrzebne obiekty klasy na podstawie danych przekazanych w pliku oscylator.py. Cały plik main jest stworzony uniwersalnie - występują tam rówmież klasy abstrakcyjne, wymuszające na programiście użycie poszczególnych, ważnych dla działania programu funkcji. Klasa StepRule ma w sobie funkcję abstrakcyjną "następny_krok", która ma pobierać dane na temat obecnego kroku i zwracać nowe dane na temat następnego kroku. StepAnalyzer - analizuje potrzbne wielkości w kroku; FinalAnalyzer - wyznacza finalne statystyki; Visualizer - rysuje wykresy.

W pliku oscylator.py sa klasy @dataclass, które są zbiornikami - w każdej z nich przechowywana jest jakaś infomacja. 
W OscillatorConfig są informacje o początkowym stanie oscylatora i ważne dla symulacji wielkości - ilośc kroków, współczynnik k, masa, współczynnik tłumienia. OscillatorState przechowuje dane o stanie oscylatora (prędkość, położenie). 
OscillatorStatistics przechowuje statystyki, tzn. np. energie. 
FinalOscillatorStatustics przechowuje dane o maksymalnej predkosci i energiach. 
OscillatorResult to zbiornik na wszystkie informacje - ląduje tam config, listy historii stanów i statystyk dla każdego kroku oraz finalne statystyki.

W pliku oscylator.py występują też klasy dziedziczące po wcześniej wspomnianych klasach abstrakcyjnych z pliku main.py. W OscillatorRule występuje funkcja nastepny_krok, która bierze jako argumenty config(k,masa,wspolczynnik tlumienia,dt(mały krok czasowy)) oraz parametry obecnego kroku, i zwraca parametry nowego - sprawdza działające siły, wyznacza przyspieszenie, liczy o ile zmieni się prędkość oraz położenie przy przyspieszeniu działającym przez czas dt. 

KlasaOscillatorAnalyzer przyjmuje parametry kroku i za pomocą funkcji "analiza" wyznacza energię. 

Klasa Rysowanie jest odpowiedzialna za tworzenie wykresów - za pomocą funkcji "rysuj" przyjmuje ona dataclass OscillatorResult, odpakowuje potrzebne dane i tworzy wykresy 

Klasa AnalizerFinalnychStatystyk ma funkcję "wyznaczenie_finalnych_statystyk" która również przyjmuje obiekt klasy OscillatorResult - historia_statystyk a następnie zwraca maksymalna predkosc i energie. 

DZIAŁANIE PROGRAMU:

Na początku użytkownik jest pytany o potrzebne wielkości - masę, k, współczynnik tłumienia, ile sekund ma trwac symulacja, początkowe wychylenie i prędkość. Wszystkie te dane są zapisywane do odpowiednich dataclass. 
Następnie tworzona jest klasa Simulation, potem wywoływana funkcja startująca symulację sim.start().

Na początku config jest zapisywany do klasy z wynikami, następnie rozpoczyna się pętla, gdzie ilość kroków to czas trwania symulacji*dt, gdzie dt = 0.01. Od razu wyznaczany jest nowy stan układu za pomocą funkcji następny_krok, a krok jest zapisywany w klasie z wynikami. Następnie wyznaczane są i zapisywane statystyki układu. Na koniec pętli uaktualnia się stary stan nowym stanem układu. 

Po zakończeniu pętli wyznaczane są i zapisywane do klasy z wynikami finalne statystyki. Na sam koniec działania funkcji wywoływana jest funkcja "rysuj" odpowiedzialna za tworzenie wykresów i zapisanie ich w plikach. 

Po zakończeniu programu w terminalu wyświetlane są finalne statystyki układu, a w osobnym oknie - wykresy.