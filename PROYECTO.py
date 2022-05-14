# Import Pandas
import pandas as pd

# Load Movies Metadata
metadata = pd.read_csv('C:\\SCCBB\DATASETS\BIKE_DETAILS.csv', low_memory=False)

# Print the first three rows
print(metadata.head(3))
#Replace NaN with an empty string
metadata['ex_showroom_price'] = metadata['ex_showroom_price'].fillna('')

# Calculate mean of kilometers average column
C = metadata['km_driven'].mean()
print(f"\nThe average kilometers of the bikes in the dataset is {C} km")

# If we want the lowest price, we set the quantile really low. If we want motorcycles with high price, we set the quantile high.
m = metadata['selling_price'].quantile(0.1)
print(m)

# Now, we save in another DataFrame those motorcycles.
# We set the percentile low (to get the cheapest motorbikes) and then we make that the price has to be equal or lower.
cheap_moto = metadata.copy().loc[metadata['selling_price'] <= m]
print(cheap_moto.shape)
print(metadata.shape)

cheap_moto = cheap_moto.sort_values('selling_price', ascending=False)


# #########################CONTENT_BASED_RECCOMENDATOR###########################



#Import TfIdfVectorizer from scikit-learn
from sklearn.feature_extraction.text import TfidfVectorizer

#Define a TF-IDF Vectorizer Object.
tfidf = TfidfVectorizer()

# #Construct the required TF-IDF matrix by fitting and transforming the data
tfidf_matrix = tfidf.fit_transform(metadata['name'])

# #Output the shape of tfidf_matrix
print(tfidf_matrix.shape)


# #Array mapping from feature integer indices to feature name.
print(tfidf.get_feature_names_out()[10:60])

# # Import linear_kernel
from sklearn.metrics.pairwise import linear_kernel

# # Compute the cosine similarity matrix
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

print(cosine_sim.shape)

print(cosine_sim[1])

#Construct a reverse map of indices and motorbikes names
indices = pd.Series(metadata.index, index=metadata['owner'])

#print(indices[:10])


# Function that takes in motorcycle name as input and outputs most similar motorbikes
def get_recommendations(owner, cosine_sim=cosine_sim):
    # Get the index of the motorbike that matches the name
    idx = indices[owner]

    # Get the pairwsie similarity scores of all motobikes with that motorbike
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the motorbikes based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1].any(), reverse=True)

    # Get the scores of the 10 most similar motorbikes
    sim_scores = sim_scores[1:11]

    # Get the bikes indices
    name_indices = [i[0] for i in sim_scores]

    # Return the top 10 most similar bikes
    return metadata['owner'].iloc[name_indices]

print(get_recommendations('1st owner'))

#print(get_recommendations('Honda CB Hornet 160R'))


# Load keywords and credits
# credits = pd.read_csv('C:\\SCCBB\DATASETS\credits.csv')
# keywords = pd.read_csv('C:\\SCCBB\DATASETS\keywords.csv')

# Remove rows with bad IDs.
# metadata = metadata.drop([19730, 29503, 35587])

# Convert IDs to int. Required for merging
# keywords['id'] = keywords['id'].astype('int')
# credits['id'] = credits['id'].astype('int')
# metadata['id'] = metadata['id'].astype('int')

# # Merge keywords and credits into your main metadata dataframe
# metadata = metadata.merge(credits, on='id')
# metadata = metadata.merge(keywords, on='id')
# metadata.head(2)


# # Parse the stringified features into their corresponding python objects
# from ast import literal_eval

# features = ['cast', 'crew', 'keywords', 'genres']
# for feature in features:
#     metadata[feature] = metadata[feature].apply(literal_eval)
    
#     # Import Numpy
# import numpy as np

# def get_director(x):
#     for i in x:
#         if i['job'] == 'Director':
#             return i['name']
#     return np.nan


# def get_list(x):
#     if isinstance(x, list):
#         names = [i['name'] for i in x]
#         #Check if more than 3 elements exist. If yes, return only first three. If no, return entire list.
#         if len(names) > 3:
#             names = names[:3]
#         return names

#     #Return empty list in case of missing/malformed data
#     return []


# # Define new director, cast, genres and keywords features that are in a suitable form.
# metadata['director'] = metadata['crew'].apply(get_director)

# features = ['cast', 'keywords', 'genres']
# for feature in features:
#     metadata[feature] = metadata[feature].apply(get_list)
    
# # Print the new features of the first 3 films
# metadata[['title', 'cast', 'director', 'keywords', 'genres']].head(3)


# # Function to convert all strings to lower case and strip names of spaces
# def clean_data(x):
#     if isinstance(x, list):
#         return [str.lower(i.replace(" ", "")) for i in x]
#     else:
#         #Check if director exists. If not, return empty string
#         if isinstance(x, str):
#             return str.lower(x.replace(" ", ""))
#         else:
#             return ''
# # Apply clean_data function to your features.
# features = ['cast', 'keywords', 'director', 'genres']

# for feature in features:
#     metadata[feature] = metadata[feature].apply(clean_data)
    
    
# def create_soup(x):
#     return ' '.join(x['keywords']) + ' ' + ' '.join(x['cast']) + ' ' + x['director'] + ' ' + ' '.join(x['genres'])
# # Create a new soup feature
# metadata['soup'] = metadata.apply(create_soup, axis=1)
# metadata[['soup']].head(2)

# # Import CountVectorizer and create the count matrix
# from sklearn.feature_extraction.text import CountVectorizer

# count = CountVectorizer(stop_words='english')
# count_matrix = count.fit_transform(metadata['soup'])
# count_matrix.shape


# # Compute the Cosine Similarity matrix based on the count_matrix
# from sklearn.metrics.pairwise import cosine_similarity

# cosine_sim2 = cosine_similarity(count_matrix, count_matrix)
# # Reset index of your main DataFrame and construct reverse mapping as before
# metadata = metadata.reset_index()
# indices = pd.Series(metadata.index, index=metadata['title'])

# get_recommendations('The Dark Knight Rises', cosine_sim2)

# print(get_recommendations('The Godfather', cosine_sim2))