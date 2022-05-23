# Import Pandas
import pandas as pd
import random

# Load motorbikes Metadata
data = pd.read_csv('C:\\SCCBB\DATASETS\MOTORBIKE_DATABASE.csv', low_memory=False)

#Extract the features of the interest​​ ​​ 

data = data[['brand','model', 'year', 'fuel', 'price']]

print(data.head())

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
print("What do you want to do? \n(1) Get recomendations from a motorbike")
print("(2) Get recomendations\n(3) Money")
option = int(input())

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

    motorbikes = motorbikes[(motorbikes['brand'] == brand) &
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
    
        motorbikes = motorbikes[(motorbikes['brand'] == brand) &
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
    
    if low_price == 0:
        
        if high_price == 0:
            
            return 0
        
        else:
            
            motorbikes = motorbikes[(motorbikes['price'] <= high_price)]
    else:
        
        if high_price == 0:
            
            motorbikes = motorbikes[(motorbikes['price'] >= low_price)]
            
        else:
            
            motorbikes = motorbikes[(motorbikes['price'] >= low_price) &
                                    (motorbikes['price'] <= high_price)]

    motorbikes = motorbikes.sort_values('price', ascending=False)
    
    return motorbikes



if option == 1:
    print(get_recomendations_all_data(percentile=0.8).head(10))
    
if option == 2:
    print(get_motorbike_by_anything_we_want().head(10))
    
if option == 3:
    motorbike = get_motorbike_by_money()
    if motorbike is 0:
        print("There is no motorbike with prize 0$!")
    else: 
        print(motorbike.head(10))