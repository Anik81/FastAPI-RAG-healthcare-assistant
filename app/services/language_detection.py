from langdetect import detect, DetectorFactory
DetectorFactory.seed = 0


def detect_language(text):
    code = detect(text)
    if code.startswith("ja"):
        return "ja"
    return "en"


translator_models = {}


def load_translator(src, tgt):
    key = (src, tgt)
    if key not in translator_models:
        from transformers import MarianMTModel, MarianTokenizer
        name = f"Helsinki-NLP/opus-mt-{src}-{tgt}"
        if src == "en" and tgt == "ja":
            name = "Helsinki-NLP/opus-mt-en-jap"
        tokenizer = MarianTokenizer.from_pretrained(name)
        model = MarianMTModel.from_pretrained(name)
        translator_models[key] = (tokenizer, model)
    return translator_models[key]


def translate(text, src, tgt):
    if src == tgt:
        return text
    tokenizer, model = load_translator(src, tgt)
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    outputs = model.generate(**inputs, max_length=512)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)