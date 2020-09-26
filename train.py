# From https://github.com/jsvine/markovify
import markovify
from random import shuffle
import language_tool_python


from dataset import DATASETS


def make_data():
    data = []
    data += DATASETS["reviews"].sample(0)
    data += DATASETS["shakespeare"].sample(0)
    data += DATASETS["stackoverflow"].sample(0)
    data += DATASETS["toptweets"].sample(0)
    data += DATASETS["bible"].sample(1000)
    data += DATASETS["worm"].sample(10000)
    shuffle(data)
    return data


if __name__ == "__main__":
    lines = make_data()

    # Build the model.
    text_model = markovify.NewlineText("\n".join(lines), state_size=3)

    # Print three randomly-generated sentences of no more than 280 characters
    count = 0
    tool = language_tool_python.LanguageTool('en-US')
    while count < 10:
        sentence = text_model.make_short_sentence(280)
        if len(sentence) > 80 and len(tool.check(sentence)) < 3:
            print(tool.correct(sentence))
            count += 1
