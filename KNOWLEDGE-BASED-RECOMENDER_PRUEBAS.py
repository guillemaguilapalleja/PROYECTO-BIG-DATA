# Import Pandas
import pandas as pd
import random

# Load motorbikes Metadata
data = pd.read_csv('C:\\SCCBB\DATASETS\MOTORBIKE_DATABASE.csv', low_memory=False)
list_of_brands_total = pd.read_csv('C:\\SCCBB\DATASETS\Brands.csv', low_memory=False)

list_of_brands = pd.DataFrame()
list_of_brands = data['brand']

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

def chart_building(brand,low_price,high_price,low_year,high_year,fuel,percentile=0.8):

    #Define a new motorbikes variable to store the preferred motorbikes. Copy the contents of gen_df to motorbikes
    motorbikes = data.copy()

    #Filter based on the condition
    if brand is None:
        brand_random = random.choice(list_of_brands)
        motorbikes = motorbikes[(motorbikes['brand'] == brand_random) &
        (motorbikes['price'] >= low_price) &
        (motorbikes['price'] <= high_price) &
        (motorbikes['year'] >= low_year) &
        (motorbikes['year'] <= high_year) &
        (motorbikes['fuel'] == fuel)]

    if low_price > high_price:
        return 'The low price can not be higher than the lower price.'
    
    if low_year > high_year:
        return 'The low year can not be higher than the lower year.'
    
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

#Ask for preferred genres

print("Input preferred brand")

brand = input()

#Ask for lower limit of duration

print("Input lowest price")

low_price = int(input())

#Ask for upper limit of duration

print("Input highest price")

high_price = int(input())

#Ask for lower limit of timeline

print("Input earliest year")

low_year = int(input())

#Ask for upper limit of timeline

print("Input latest year")

high_year = int(input())

print("Input type of fuel (1 = 95 fuel, 2 = 98 fuel, 3 = Diesel)")

fuel = int(input())

#Generate the chart for top animation movies and display top 5.

motorbikes_recomended = chart_building(brand=brand,low_price=low_price,high_price=high_price,
                                       low_year=low_year,high_year=high_year, fuel=fuel)

#KBS=KBS.model

#motorbikes_recomended=motorbikes_recomended.reset_index(drop=True)

if type(motorbikes_recomended) == str:
    print(motorbikes_recomended)
else:
    if motorbikes_recomended.empty == True:
        print("There is not a motorbike with such characteristics. Try again with diferent parameters.")
    else:
        print(motorbikes_recomended)