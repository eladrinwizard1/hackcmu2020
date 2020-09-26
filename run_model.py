import json
import markovify

COUNT = 5

if __name__ == "__main__":
    with open("model.json", "r") as f:
        text_model = markovify.NewlineText.from_json(json.load(f))
    words = input("Enter sentence start... \n").split()
    head, tail = words[:-text_model.state_size], words[-text_model.state_size:]
    for _ in range(COUNT):
        gen_words = text_model.make_sentence_with_start(" ".join(tail))
        print(" ".join(head), gen_words)
