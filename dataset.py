import pandas as pd
from bs4 import BeautifulSoup
import re
from random import sample

try:
    with open("banlist.txt", "r") as f:
        BANNED_WORDS = [a.strip() for a in f.readlines()]
except FileNotFoundError:
    BANNED_WORDS = []


class Dataset:
    min_line_length = 4

    def __init__(self, path):
        self.path = path
        self.dir = '/'.join(self.path.split('/')[:-1])
        self.list = self.get_lines()

    def get_lines(self):
        raise NotImplementedError

    @staticmethod
    def clean_line(line: str):
        line = line.strip()
        line = line.lower()
        line = "".join(filter(lambda c: 0 < ord(c) < 128, line))
        line = re.sub(r"[0-9]*:[0-9]*", "", line)
        line = re.sub(r"[#@]", "", line)
        line = " ".join(filter(lambda x: "//" not in x, line.split()))
        return f"{line}\n" if len(line) > Dataset.min_line_length else None

    @staticmethod
    def censor(text):
        for word in BANNED_WORDS:
            if word in text:
                return False
        return True

    def process(self):
        with open(f"{self.dir}/raw_lines.txt", "w+", encoding="utf-8") as f:
            f.writelines(filter(self.censor, filter(lambda x: x is not None,
                                map(Dataset.clean_line, self.list))))

    def sample(self, n):
        with open(f"{self.dir}/raw_lines.txt", encoding="utf-8") as f:
            return sample(f.readlines(), n)


class ReviewDataset(Dataset):
    def get_lines(self):
        reviews = pd.read_csv(self.path)
        reviews_raw = reviews["review"].to_list()
        return [f"{BeautifulSoup(t, features='lxml').get_text()}\n"
                for t in reviews_raw]


class ShakespeareDataset(Dataset):
    def get_lines(self):
        shakespeare = pd.read_csv(self.path)
        return [f"{l}\n" for l in shakespeare["PlayerLine"].to_list()]


class StackOverflowDataset(Dataset):
    def get_lines(self):
        answers = pd.read_csv("data/stackoverflow/Answers.csv",
                              encoding="latin-1")
        answer_raw = answers["Body"].to_list()
        answer_raw = sample(answer_raw, 20000)
        return [f"{BeautifulSoup(t, features='lxml').get_text()}\n"
                for t in answer_raw]


class TopTweetsDataset(Dataset):
    def get_lines(self):
        tweets = pd.read_csv("data/top20tweets/tweets.csv")
        raw_tweets = tweets["content"].to_list()
        return [f"{l}\n" for l in raw_tweets]


class BibleDataset(Dataset):
    def get_lines(self):
        with open(self.path, "r") as f:
            return f.readlines()


class WormDataset(Dataset):
    def get_lines(self):
        with open(self.path, "r", encoding="utf-8") as f:
            return f.readlines()


class MovieDataset(Dataset):
    def get_lines(self):
        with open(self.path, "r", encoding="windows-1252") as f:
            return [line for i, line in enumerate(f.readlines()) if i % 4 == 2]


class VisualNovelDataset(Dataset):
    @staticmethod
    def _remove_brackets(text):
        count = 0
        out = []
        for c in text:
            if c == "[":
                count += 1
            if count == 0:
                out.append(c)
            if c == "]":
                count -= 1
        return "".join(out)

    def get_lines(self):
        vninfo = pd.read_csv(self.path, sep='\t', header=None)
        vndescs = vninfo[6]
        vndescs = [desc.replace("\\n", " ")
                   for desc in vndescs if type(desc) is not float]
        vndescs = [self._remove_brackets(desc) for desc in vndescs]
        return [desc + "\n" for desc in vndescs]

DATASETS = {
    "reviews": ReviewDataset("data/reviews/IMDB Dataset.csv"),
    "shakespeare": ShakespeareDataset("data/shakespeare/Shakespeare_data.csv"),
    "stackoverflow": StackOverflowDataset("data/stackoverflow/Answers.csv"),
    "toptweets": TopTweetsDataset("data/top20tweets/tweets.csv"),
    "bible": BibleDataset("data/bible/bible.txt"),
    "worm": WormDataset("data/worm/worm.txt"),
    "movies": MovieDataset("data/movies/moviequotes.memorable_quotes.txt"),
    "vn": VisualNovelDataset("data/visualnovels/vn")
}


if __name__ == "__main__":
    VisualNovelDataset("data/visualnovels/vn").process()
