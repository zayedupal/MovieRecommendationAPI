import pandas as pd
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class RecoContent():
    def __init__(self):
        dirname = os.path.dirname(__file__)
        self.PATH = os.path.join(dirname, 'Data/movielense-latest-small/')

        # read all the data
        self.ratings = pd.read_csv(self.PATH + 'ratings.csv')
        self.movies = pd.read_csv(self.PATH + 'movies.csv')
        self.tags = pd.read_csv(self.PATH + 'tags.csv')
        self.links = pd.read_csv(self.PATH + 'links.csv')
        # Content based reco
        movie_tags = self.tags.groupby('movieId')['tag'].apply(list).reset_index(name='tag')
        movie_tags['tag'] = movie_tags['tag'].apply(lambda x: ' '.join(x))
        movie_genres_tags = self.movies.merge(movie_tags, how='inner', on='movieId')
        self.movie_metadata = movie_genres_tags
        self.movie_metadata['genres'] = self.movie_metadata['genres'].apply(lambda x: x.replace('|', ' '))
        self.movie_metadata['meta'] = self.movie_metadata['genres'] + self.movie_metadata['tag']
        self.movie_metadata = self.movie_metadata.drop(['genres', 'tag'], 1)
        # movie_metadata['meta'] = movie_metadata['meta']

        count_vectorizer = CountVectorizer(stop_words='english')

        # Replace NaN with an empty string
        self.movie_metadata['meta'] = self.movie_metadata['meta'].fillna('')

        # Construct the required CountVectorizer matrix by fitting and transforming the data
        count_matrix = count_vectorizer.fit_transform(self.movie_metadata['meta'])



        # Compute the cosine similarity matrix
        self.cosine_sim = cosine_similarity(count_matrix, count_matrix)

        # Construct a reverse map of indices and movie ids
        self.indices = pd.Series(self.movie_metadata.index, index=self.movie_metadata['movieId'])
        print(self.indices)


    def get_movies(self):
        return self.movies

    # Function that takes in movie title as input and outputs most similar movies
    def predict(self,movie_id):
        # title = movie_df[movie_df['movieId']==movie_id]['title'].values[0]
        # print('you want recommendation for: ', title_df)
        movieId = movie_id.values[0][0]
        # print('movidId: ',movieId)
        # print('movie: ',self.movie_metadata[self.movie_metadata['movieId']==movieId])

        idx = self.indices[int(movieId)]
        # print('idx: ', idx)
        # Get the pairwsie similarity scores of all movies with that movie
        sim_scores = list(enumerate(self.cosine_sim[idx]))
        print('sim_scores: ',sim_scores)
        # Sort the movies based on the similarity scores
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Get the scores of the 10 most similar movies
        sim_scores = sim_scores[1:11]
        print('sim_scores:',sim_scores)
        # Get the movie indices
        movie_indices = [i[0] for i in sim_scores]
        print('movie_indices:',movie_indices)
        top_movie_ids = self.movie_metadata['movieId'].iloc[movie_indices].reset_index()
        top_movie_ids.columns = ['index','movieId']
        print('top_movie_ids: ', top_movie_ids)
        top_movies = pd.DataFrame(columns=['movieId','title','genres'])
        print('movies: ', self.movies)

        for index,row in top_movie_ids.iterrows():
            print(row.values)
            cur_movie_row = self.movies[self.movies['movieId']==row['movieId']]
            top_movies=top_movies.append(cur_movie_row)

        top_movies=top_movies.drop(columns='movieId')
        print('top_movies: ',top_movies)

        # Return the top 10 most similar movies
        return top_movies

    def json_to_df(self, json):
        df = pd.DataFrame(json,index=[0])
        # print(df.values[0])
        return df

