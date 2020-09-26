import json
import markovify
import language_tool_python

COUNT = 5

if __name__ == "__main__":
    with open("model.json", "r") as f:
        text_model = markovify.NewlineText.from_json(json.load(f))

    tool = language_tool_python.LanguageTool('en-US')

    while True:
        try:
            words = input("\nEnter sentence start... \n").split()
            if len(words) == 0:
                count = COUNT
                while count > 0:
                    sentence = None
                    while sentence is None:
                        sentence = text_model.make_sentence()
                    if len(tool.check(sentence)) < 10:
                        print(tool.correct(sentence))
                        count -= 1
            else:
                head = words[:-text_model.state_size]
                tail = words[-text_model.state_size:]
                count = COUNT
                while count > 0:
                    sentence = None
                    while sentence is None:
                        sentence = text_model.make_sentence_with_start(" ".join(tail))
                    if len(tool.check(sentence)) < 10:
                        print(" ".join(head), tool.correct(sentence))
                        count -= 1
        except (KeyError, markovify.text.ParamError):
            pass
