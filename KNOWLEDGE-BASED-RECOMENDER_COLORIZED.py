import pandas as pd
import random
from colorama import Fore
from colored import fg, bg, attr

data = pd.read_csv('C:\\SCCBB\DATASETS\MOTORBIKE_DATABASE.csv', low_memory=False)

data = data[['brand','model', 'year', 'fuel', 'price']]

def convert_int(x):
    try:
        return int(x)
    except:
        return 0

data['year'] = data['year'].apply(convert_int)
data['fuel'] = data['fuel'].apply(convert_int)
data['price'] = data['price'].apply(convert_int)

def convert_string(x):
    try:
        return str(x)
    except:
        return None

data['brand'] = data['brand'].apply(convert_string)
data['model'] = data['model'].apply(convert_string)


motorbikes = data.copy()

sample = motorbikes.sample(axis = 0)
brandRand = sample['brand'].values[0]
      

def get_recomendations_all_data(percentile=0.8):
    
    motorbikes = data.copy()

    print("Input preferred brand")  
    brand = str(input())
    
    print("Input lowest price")  
    low_price = int(input())
    
    print("Input highest price") 
    high_price = int(input())
    
    print("Input earliest year") 
    low_year = int(input())
    
    print("Input latest year") 
    high_year = int(input())
    
    print("Input type of fuel (1 = 95 fuel, 2 = 98 fuel, 3 = Diesel)") 
    fuel = int(input())

    motorbikes = motorbikes[(motorbikes['brand'] == brand.upper()) &
        (motorbikes['price'] >= low_price) &
        (motorbikes['price'] <= high_price) &
        (motorbikes['year'] >= low_year) &
        (motorbikes['year'] <= high_year) &
        (motorbikes['fuel'] == fuel)]

    m = motorbikes['price'].quantile(percentile)

    q_motorbikes = motorbikes.copy().loc[motorbikes['price'] <= m]

    q_motorbikes = q_motorbikes.sort_values('price', ascending=False)
    
    return q_motorbikes


def get_motorbike_by_anything_we_want():

    motorbikes = data.copy()

    print("Write what would your ideal motorbike be:\n")

    print("Input preferred brand") 
    brand = str(input())
    
    print("Input lowest price")
    low_price = int(input())
    
    print("Input highest price")
    high_price = int(input())
    
    print("Input earliest year")
    low_year = int(input())
    
    print("Input latest year")
    high_year = int(input())
    
    print("Input type of fuel (1 = 95 fuel, 2 = 98 fuel, 3 = Diesel):")
    fuel = int(input())
    
    if low_price == 0:
        low_price = motorbikes['price'].min() 
    if high_price == 0:
        high_price = motorbikes['price'].max() 
    if low_year == 0:
        low_year = motorbikes['year'].min()
    if high_year == 0:
        high_year = motorbikes['year'].max()
    if fuel == 0:
        fuel = random.randint(1,3)  
    
    if brand != '':
    
        motorbikes = motorbikes[(motorbikes['brand'] == brand.upper()) &
            (motorbikes['price'] >= low_price) &
            (motorbikes['price'] <= high_price) &
            (motorbikes['year'] >= low_year) &
            (motorbikes['year'] <= high_year) &
            (motorbikes['fuel'] == fuel)]
    else:
        
        motorbikes = motorbikes[(motorbikes['price'] >= low_price) &
            (motorbikes['price'] <= high_price) &
            (motorbikes['year'] >= low_year) &
            (motorbikes['year'] <= high_year) &
            (motorbikes['fuel'] == fuel)]

    motorbikes = motorbikes.sort_values('price', ascending=False)
    
    return motorbikes

def get_motorbike_by_money():

    motorbikes = data.copy()
    
    print("Input lowest price")
    low_price = int(input())
    
    print("Input highest price")
    high_price = int(input())
    
    n = 0
    
    if low_price == 0:    
        if high_price == 0:
            n = 1
            motorbikes = motorbikes.empty
        else: 
            ascending = True
            motorbikes = motorbikes[(motorbikes['price'] <= high_price)]
    else:  
        if high_price == 0:
            ascending = False
            motorbikes = motorbikes[(motorbikes['price'] >= low_price)]     
        else:  
            ascending = True
            motorbikes = motorbikes[(motorbikes['price'] >= low_price) &
                                    (motorbikes['price'] <= high_price)]

    if n == 0:
        motorbikes = motorbikes.sort_values('price', ascending=ascending)
        return motorbikes
    elif n == 1:
        return 0

def get_prize_from_my_motorbike():

    motorbikes = data.copy()
    message = ''
    print("Write what would your ideal motorbike be:\n")

    print("Input your motorbikes brand") 
    brand = str(input())
    
    print("\nInput your motorbikes year")
    year = int(input())
    
    print("\nInput type of fuel of your motorbike (1 = 95 fuel, 2 = 98 fuel, 3 = Diesel):")
    fuel = int(input())
    
    if brand == '':
        message += '\nWe need the brand of your motorbike to know its price!'
    if year == 0:
        message += '\nWe need the year of your motorbike to know its price!'
    if fuel == 0:
        message += '\nWe need the type of fuel of your motorbike to know its price!'
    
    if brand != '' and year != 0 and fuel != 0:
        motorbikes = motorbikes[(motorbikes['brand'] == brand.upper()) &
            (motorbikes['year'] == year) &
            (motorbikes['fuel'] == fuel)]
    
        price = round(motorbikes['price'].mean(),2)
        if pd.isna(price) == True:
           message = ('\n%s%sOops! We cant see the price of your motorbike!%s' % (fg('white'), bg('red'), attr('reset')))
        else:
            message = f"\nYour motorbike would be worth aprox {price}$\n"
    return message
    
    


while(1):
    red = fg('red')
    print("\n\nWhat do you want to do? \n\n(1) Get recomendations from a motorbike")
    print("(2) Get recomendations by any parameter\n(3) Money")
    print("(4) How much does your motorbike cost?\n(5) Exit")
    option = int(input())
    
    if option == 1:
        motorbike = get_recomendations_all_data(percentile=0.8)
        if motorbike.empty == True:
            print('\n%s%sCant look at any look-a-like motorbike!%s' % (fg('white'), bg('red'), attr('reset')))
        else:
            print(f'%s%s{motorbike}%s' % (attr('bold'),fg(118), attr('reset')))
        
    if option == 2:
        motorbike = get_motorbike_by_anything_we_want()
        if motorbike.empty == True:
            print('\n%s%sOops! Could not find any recomendations with the written parameters!%s' % (fg('white'), bg('red'), attr('reset')))
        else:
            print(f'%s%s{motorbike}%s' % (attr('bold'),fg(118), attr('reset')))
        
    if option == 3:
        motorbike = get_motorbike_by_money()
        if type(motorbike) is int:
            print('\n%s%sThere is no motorbike with prize 0$!%s' % (fg('white'), bg('red'), attr('reset')))
        elif motorbike.empty == True:
            print('\n%s%sOops! Could not find any motorbike between those prices!%s' % (fg('white'), bg('red'), attr('reset')))
        
        else:
            print(f'%s%s{motorbike}%s' % (attr('bold'),fg(118), attr('reset')))
    
    if option == 4:
        print(f'%s%s{get_prize_from_my_motorbike()}%s' % (attr('bold'),fg('orchid'), attr('reset')))
    
    if option == 5:
        print('\n%s%s%sExiting...%s' % (attr('bold'), fg('white'), bg(5), attr('reset')))
        break