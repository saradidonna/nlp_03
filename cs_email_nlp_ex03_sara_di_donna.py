# -*- coding: utf-8 -*-
"""CS EMAIL -- NLP_ex03_Sara Di Donna.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19h1l-4bYesTeQWT3wMw8f84Q_EWn0tTx
"""

!pip install unbabel-comet
!pip install sacremoses
!python -m pytorch_lightning.utilities.upgrade_checkpoint ../root/.cache/huggingface/hub/models--Unbabel--wmt22-comet-da/snapshots/371e9839ca4e213dde891b066cf3080f75ec7e72/checkpoints/model.ckpt
from transformers import MarianMTModel, MarianTokenizer
import os
import sacremoses
import re
from comet import download_model, load_from_checkpoint

os.environ['HF_TOKEN'] = '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' # token needed to access transformer model from Hugging Face

# Load the MarianMT model and tokenizer for translation between English and Italian
model_name = 'Helsinki-NLP/opus-mt-en-it'  # English to Italian translation model
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

# define a function for segment-level translation
def segment_level_translation(text_segments, model, tokenizer, max_length=700):
    translations = []
    for segment in text_segments:
        inputs = tokenizer.encode(segment, return_tensors="pt", max_length=max_length, truncation=True)
        outputs = model.generate(inputs, max_length=max_length, num_beams=4, early_stopping=True)
        translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        translations.append(translated_text)
    return translations

#Text to be translated
text = "Dear team, This is Sara from the Customer Service department. I hope you’re well. Upon verification, we noticed that the customer received the order on June 21 and on the next day contacted our department informing us that the shirt was dirty and had a strong smell. The customer claimed he was very disappointed and will not order another one. He also sent photos that you can find attached. We can see on the photos that there are stains and tags are attached. Therefore, we kindly ask you to accept the return on your side. I am grateful for your continuous support and cooperation. Kind regards."

# Regular expression to split the text in sentences
segments = re.split(r'(?<=[^A-Z].[.?])\s+', text)

# Perform segment-level translation
translations = segment_level_translation(segments, model, tokenizer)

# Print the translations
print("Customer Service email - segment level translation:")
for i, translation in enumerate(translations):
    print(f"Segment {i+1} (Source): {segments[i]}")
    print(f"Segment {i+1} (Target): {translation}\n")

def document_level_translation(document, model, tokenizer):
    # Tokenize the entire document
    input_ids = tokenizer.encode(document, return_tensors="pt", truncation=True)

    # Generate translations for the entire document
    max_length = 2500  # Maximum length for the generated output
    outputs = model.generate(input_ids, max_length=max_length, num_beams=10, early_stopping=True)

    # Decode the translations
    translated_document = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return translated_document

# Perform document-level translation
translated_document = document_level_translation(text, model, tokenizer)

# Print the translated document
print("Customer Service email - document level translation:")
print("Source:")
print(text)
print("\nTarget:")
print(translated_document)

###COMET: Customer Service email - SEGMENT-LEVEL

model_path = download_model("Unbabel/wmt22-comet-da")
model = load_from_checkpoint(model_path)

# Translation data, where: "src" is the English source text, "mt" is the machine translation output provided by the segment-level translation function and "ref" is the corresponding translation nugget by nugget produced by a native
doc_data = [
    {
        "src": "Dear team, This is Sara from the Customer Service department.",
        "mt": "Caro team, sono Sara del Servizio Clienti.",
        "ref": "Caro team, sono Sara del Servizio Clienti."
    },
    {
        "src": "I hope you’re well.",
        "mt": "Spero che tu stia bene.",
        "ref": "Spero che stiate bene."
    },
      {
        "src": "Upon verification, we noticed that the customer received the order on June 21 and on the next day contacted our department informing us that the shirt was dirty and had a strong smell.",
        "mt": "Dopo la verifica, abbiamo notato che il cliente ha ricevuto l'ordine il 21 giugno e il giorno successivo ha contattato il nostro reparto informandoci che la camicia era sporca e aveva un forte odore.",
        "ref": "Dopo aver verificato, abbiamo notato che il cliente ha ricevuto l'ordine il 21 giugno e il giorno successivo ha contattato il nostro dipartimento informandoci che la camicia era sporca e aveva un forte odore."
    },
      {
        "src": "The customer claimed he was very disappointed and will not order another one.",
        "mt": "Il cliente ha affermato di essere molto deluso e non ordinerà un altro.",
        "ref": "Il cliente ha affermato di essere molto deluso e non ne ordinerà un'altra."
    },
      {
        "src": "He also sent photos that you can find attached.",
        "mt": "Ha anche inviato foto che si possono trovare allegato.",
        "ref": "Ha anche inviato delle foto che potete trovare in allegato."
    },
      {
        "src": "We can see on the photos that there are stains and tags are attached.",
        "mt": "Possiamo vedere sulle foto che ci sono macchie e tag sono allegati.",
        "ref": "Possiamo vedere sulle foto che ci sono delle macchie e le etichette sono attaccate."
    },
      {
        "src": "Therefore, we kindly ask you to accept the return on your side.",
        "mt": "Pertanto, vi chiediamo gentilmente di accettare il ritorno dalla vostra parte.",
        "ref": "Pertanto, vi chiediamo gentilmente di accettare il reso."
    },
      {
        "src": "I am grateful for your continuous support and cooperation.",
        "mt": "Sono grato per il vostro continuo sostegno e cooperazione.",
        "ref": "Vi sono grata per il vostro continuo sostegno e cooperazione."
    },
      {
        "src": "Kind regards.",
        "mt": "Buongiorno.",
        "ref": "Cordiali saluti."
    }
]
doc_model_output = model.predict(doc_data, batch_size=8, gpus=1)
print (doc_model_output)

###COMET: Customer service email - DOC-LEVEL

model_path = download_model("Unbabel/wmt22-comet-da")
model = load_from_checkpoint(model_path)

# Translation data, where "src" is the English source text, "mt" is the machine translation output provided by the document-level translation and "ref" is a human produced translation
doc_data = [
    {
        "src": "Dear team, This is Sara from the Customer Service department. I hope you’re well. Upon verification, we noticed that the customer received the order on June 21 and on the next day contacted our department informing us that the shirt was dirty and had a strong smell. The customer claimed he was very disappointed and will not order another one. He also sent photos that you can find attached. We can see on the photos that there are stains and tags are attached. Therefore, we kindly ask you to accept the return on your side. I am grateful for your continuous support and cooperation. Kind regards.",
        "mt": "Caro team, questo è Sara del Servizio Clienti. Spero che tu stia bene. Dopo la verifica, abbiamo notato che il cliente ha ricevuto l'ordine il 21 giugno e il giorno successivo ha contattato il nostro reparto informandoci che la camicia era sporca e aveva un forte odore. Il cliente ha affermato che era molto deluso e non ordinerà un altro. Ha anche inviato foto che si possono trovare allegato. Possiamo vedere sulle foto che ci sono macchie e tag sono allegati. Pertanto, vi chiediamo gentilmente di accettare il ritorno dalla vostra parte. Sono grato per il vostro continuo supporto e la cooperazione. Cordiali saluti.",
        "ref": "Caro team, sono Sara del Servizio Clienti. Spero che stiate bene. Dopo aver verificato, abbiamo notato che il cliente ha ricevuto l'ordine il 21 giugno e il giorno successivo ha contattato il nostro dipartimento informandoci che la camicia era sporca e aveva un forte odore. Il cliente ha affermato di essere molto deluso e non ne ordinerà un'altra. Ha anche inviato delle foto che potete trovare in allegato. Possiamo vedere sulle foto che ci sono delle macchie e le etichette sono attaccate. Pertanto, vi chiediamo gentilmente di accettare il reso. Vi sono grata per il vostro continuo sostegno e cooperazione. Cordiali saluti."
    }
]
doc_model_output = model.predict(doc_data, batch_size=8, gpus=1)
print (doc_model_output)