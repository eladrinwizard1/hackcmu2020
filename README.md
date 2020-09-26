# hackcmu2020

# dataset.py
To add a new dataset, add a new subfolder in the data directory and subclass 
the Dataset base class to implement the `get_lines` method.

Before a dataset can be used for training, the `Dataset.process` method must be
called with the source material to create a `raw_lines.txt`.

# train.py
To train a model, combine samples of the dataset as desired in `make_data`, then
run the main script.

# run_model.py
A command-line tool for generating model text, optionally based on an input.

# tweet.py
Automatically tweet generated descriptions.

# Datasets for experimentation
bible: https://www.gutenberg.org/cache/epub/10/pg10.txt

movies: https://www.cs.cornell.edu/~cristian/memorability.html

reviews: https://www.kaggle.com/lakshmi25npathi/imdb-dataset-of-50k-movie-reviews

shakespeare: https://www.kaggle.com/kingburrito666/shakespeare-plays

stackoverflow: https://www.kaggle.com/stackoverflow/stacksample

top20tweets: https://dataverse.harvard.edu/dataset.xhtml?id=3047332

vndb: https://dl.vndb.org/dump/
