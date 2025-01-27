# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 08:17:17 2025

@author: fabijans-1

Wymagania:
3 Klasy
    -1. pobiera dane od użytkownika oraz sprawdza ich poprawnosc
    -2. posiada: pola, konstruktor, metody typu getter i setter oraz zwykle metody(funkcje) przetwarzajace 
    dane pobrane od uzytkownika i wyswietlajace je na ekranie, powinny wychodzic z metod klasy pierwszej
    -3. definowanie metody prezentujaca dane w postaci wykresu, dane z klasy drugiej, 
    może posiadac wlasne dane ale nie musi

Program - opcje binarne
Handel opcjami binarnymi polega na spekulowaniu, czy cena danego aktywa wzrośnie, czy spadnie w danym przedziale czasowym.
W tym przypadku skupiamy się na fikcyjnej akcji, która może wzrosnąć bądź spasc o daną wartosc w ciagu 5 minut. 

Etap 1
Gracz zostaje zapytany o ilosc pieniedzy, ktora chce wplacic na konto maklerskie {balance}
Etap 2
Gracz ma do wyboru menu:
    1 - Zagraj
      wpisuje kwote zagrania
      wpisuje gora or dol
      pokazuje wynik i wraca do menu
    2 - Pokaz statystyki
        Saldo poczatkowe
        Saldo koncowe
        Zmiana %
        Transakcje pokolei
    3 - Pokaz wykresy
        wykres salda i transkacji
    4 - Zakończ grę

"""
from random import *
from time import sleep
import matplotlib.pyplot as plt

# Zmienne
position = 0
initial_balance = 0
transactions = []
choose = 0

# Funkcja 1 - granie w grę
def game(balance):
    position = 0
    while True:
        try:
            position = float(input("Podaj za ile chcesz grać? "))
            if position <= 0:
                raise ValueError("Wprowadź wartość większą od zera. ")
            if position >= balance:
                raise ValueError("Niewystarczające srodki. ")
        except ValueError as e:
            print(e)
        else:
            break
            
    while True:
        try:
            choice = input("Czy cena akcji pójdzie w górę (gora) czy w dół (dol)? ")
            if choice != "dol" and choice != "gora":
                raise ValueError("Wprowadź 'dol' albo 'gora'! ")
        except ValueError:
            print("Wprowadź 'dol' albo 'gora'! ")
        else:
            break

    price_change = float(randrange(50, 150))

    if price_change == 100:
        print("Cena się nie zmieniła, zwrot depozytu")
        new_balance = balance  # saldo się nie zmienia
    elif price_change > 100 and choice == 'gora':
        print(f"Wygrałeś zakład. Cena wzrosła o {price_change - 100}% ")
        new_balance = balance + position  # zwiększ saldo
    elif price_change > 100 and choice == 'dol':
        print(f"Przegrałeś zakład. Cena wzrosła o {price_change - 100}%")
        new_balance = balance - position  # zmniejsz saldo
    elif price_change < 100 and choice == 'gora':
        print(f"Przegrałeś zakład. Cena spadła o {100 - price_change}%")
        new_balance = balance - position  # zmniejsz saldo
    elif price_change < 100 and choice == 'dol':
        print(f"Wygrałeś zakład. Cena spadła o {100 - price_change}%")
        new_balance = balance + position  # zwiększ saldo
    else:
        print("Ten błąd nie powinien wystąpić, wyślij zgłoszenie do autora.")
        new_balance = balance  # domyślnie nie zmieniaj salda

    # Dodaj transakcję do listy
    transaction = position if new_balance > balance else -position
    transactions.append((transaction, new_balance))
    
    sleep(1)
    return new_balance

# Funkcja 2 - saldo i transakcje
def saldo_trans():
    print("Saldo początkowe:", initial_balance)
    print("Aktualne saldo:", balance)
    print("Zmiana o:",(balance/initial_balance)*100-100,"%")
    print("Transakcje:")
    for trans, saldo in transactions:
        print(f"Transakcja: {trans}, Saldo po transakcji: {saldo}")
    
    
    choose = input("Wpisz dowolny znak by powrócić do menu: ")
    sleep(1)
    menu()

# Funkcja 3 - wykresy
def charts():
    if not transactions:
        print("Brak transakcji do wyświetlenia.")
        input("Wpisz dowolny znak by powrócić do menu: ")
        sleep(1)
        menu()
        return

    # Przygotowanie danych do wykresu
    trans_values = [trans for trans, saldo in transactions]  # Lista wartości transakcji
    saldo_values = [saldo for trans, saldo in transactions]  # Lista sald po transakcjach
    transaction_numbers = list(range(1, len(transactions) + 1))  # Numery transakcji

    # Tworzenie wykresu
    fig, ax1 = plt.subplots()

    # Wykres transakcji
    ax1.set_xlabel('Numer transakcji')
    ax1.set_ylabel('Transakcje', color='tab:blue')
    ax1.bar(transaction_numbers, trans_values, color='tab:blue', alpha=0.6, label='Transakcje')
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    # Utworzenie drugiej osi y dla salda
    ax2 = ax1.twinx()
    ax2.set_ylabel('Saldo', color='tab:orange')
    ax2.plot(transaction_numbers, saldo_values, color='tab:orange', marker='o', label='Saldo')
    ax2.tick_params(axis='y', labelcolor='tab:orange')

    # Dodanie tytułu i legendy
    plt.title('Transakcje i Saldo po każdej transakcji')
    fig.tight_layout()  # Dostosuj rozmiar figury
    plt.show()  # Wyświetlenie wykresu

    input("Wpisz dowolny znak by powrócić do menu: ")
    sleep(1)
    menu()

# Funkcja menu wybór
def menu():
    global balance  # Zmiana globalna, aby móc aktualizować saldo
    while True:
        try:
            menu_choice = int(input("""Menu - wybierz liczbę:
                                  1. Zagraj
                                  2. Pokaż statystki
                                  3. Pokaż wykresy
                                  4. Zakończ grę
                                  
                                  Wybór: """))
            if menu_choice not in (1, 2, 3, 4):
                raise ValueError("Wprowadź wartość od 1 do 4")
            if menu_choice == 1:
                print(f"Twoje saldo to: {balance}")
                balance = game(balance)
                
            if menu_choice == 2:
                saldo_trans()
            if menu_choice == 3:
                charts()
            if menu_choice == 4:
                break
        except ValueError:
            print("Niepoprawna wartość, wprowadź liczbę od 1 do 5")

# Wyjasnienie gry
print("""Witaj,
      
W tej grze stawiasz zakłady na zmiany cen akcji. Rozpoczynasz od wpłaty na konto maklerskie, a następnie wybierasz kwotę zakładu oraz przewidujesz, czy cena akcji wzrośnie ("gora") czy spadnie ("dol").

Jeśli dobrze przewidzisz zmianę ceny, zyskujesz, w przeciwnym razie tracisz. Możesz śledzić swoje transakcje oraz saldo, a także przeglądać wykresy przedstawiające Twoje postępy.

Gra kończy się, gdy zdecydujesz się wyjść. Baw się dobrze i powodzenia!
""")

choose = input("Wpisz dowolny znak aby rozpocząć: ")
# Rozpoczęcie gry: deklarowanie wpłaty
while True:
    try:
        balance = float(input("Podaj kwotę, którą chcesz wpłacić na konto maklerskie: "))
        if balance <= 0:
            raise ValueError("Wprowadź wartość większą od zera")
        initial_balance = balance
    except ValueError:
        print("Niepoprawna wartość, wprowadź liczbę dodatnią")
    else:
        break

menu()
