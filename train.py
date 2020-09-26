# From https://github.com/jsvine/markovify
import markovify
from random import shuffle
import language_tool_python


from dataset import DATASETS


def make_data():
    data = []
    data += DATASETS["reviews"].sample(100)
    data += DATASETS["shakespeare"].sample(100)
    data += DATASETS["stackoverflow"].sample(1000)
    data += DATASETS["toptweets"].sample(1000)
    data += DATASETS["bible"].sample(1000)
    shuffle(data)
    return data


if __name__ == "__main__":
    lines = make_data()

    # Build the model.
    text_model = markovify.NewlineText("\n".join(lines), state_size=2)

    # Print three randomly-generated sentences of no more than 280 characters
    count = 0
    tool = language_tool_python.LanguageTool('en-US')
    while count < 10:
        sentence = text_model.make_short_sentence(280, 80)
        if len(tool.check(sentence)) < 5:
            print(tool.correct(sentence))
            count += 1
