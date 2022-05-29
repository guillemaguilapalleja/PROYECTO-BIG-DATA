# Import Pandas
import pandas as pd
import random

# Load motorbikes Metadata
data = pd.read_csv('C:\\SCCBB\DATASETS\MOTORBIKE_DATABASE.csv', low_memory=False)

#Extract the features of the interest​​ ​​ 

data = data[['brand','model', 'year', 'fuel', 'price']]

#print(data.head())

#Helper function to convert NaT to 0 and all other years to integers.

def convert_int(x):
    try:
        return int(x)
    except:
        return 0

#Apply convert_int to the year feature

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

    #Compute the values of C and m for the filtered motorbikes

    m = motorbikes['price'].quantile(percentile)

    #Only consider motorbikes that have higher than m votes. Save this in a new dataframe q_motorbikes

    q_motorbikes = motorbikes.copy().loc[motorbikes['price'] <= m]

    #Sort motorbikes in descending order of their scores

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
            ascending = False
            n = 1
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
           message = "\nOops! We cant see the price of your motorbike!"
        else:
            message = f"\nYour motorbike would be worth aprox {price}$\n"
    return message
    
    


while(1):
    
    print("\n\nWhat do you want to do? \n\n(1) Get recomendations from a motorbike")
    print("(2) Get recomendations by any parameter\n(3) Money")
    print("(4) How much does your motorbike cost?\n(5) Exit")
    option = int(input())
    
    if option == 1:
        motorbike = get_recomendations_all_data(percentile=0.8)
        if motorbike.empty == True:
            print("\nCant look at any look-a-like motorbike!")
        else:
            print(motorbike)
        
    if option == 2:
        motorbike = get_motorbike_by_anything_we_want()
        if motorbike.empty == True:
            print('\nOops! Could not find any recomendations with the written parameters!')
        else:
            print(motorbike)
        
    if option == 3:
        motorbike = get_motorbike_by_money()
        if type(motorbike) is int:
            print('\nThere is no motorbike with prize 0$!')
        elif motorbike.empty == True:
            print('\nOops! Could not find any motorbike between those prices!')
        
        else:
            print(f'{motorbike}')
    
    if option == 4:
        print(get_prize_from_my_motorbike())
    
    if option == 5:
        print("\nExiting...")
        break