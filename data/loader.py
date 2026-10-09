from datasets import load_dataset


def loader():
    ds = load_dataset("AGBonnet/augmented-clinical-notes")
    data = ds['train']
    data.to_json("data/dataset.jsonl", lines=True)
    return "Done"

if __name__ == "__main__":
    print(loader())