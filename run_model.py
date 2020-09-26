import json
import markovify

COUNT = 5

if __name__ == "__main__":
    with open("model.json", "r") as f:
        text_model = markovify.NewlineText.from_json(json.load(f))
    while True:
        try:
            words = input("\nEnter sentence start... \n").split()
            if len(words) == 0:
                for _ in range(COUNT):
                    if (sent := text_model.make_sentence()) is not None:
                        print(sent)
            else:
                head = words[:-text_model.state_size]
                tail = words[-text_model.state_size:]
                for _ in range(COUNT):
                    gen = text_model.make_sentence_with_start(" ".join(tail))
                    if gen is not None:
                        print(" ".join(head), gen)
        except (KeyError, markovify.text.ParamError):
            pass
