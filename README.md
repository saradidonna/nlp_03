## Segment vs. Document level Machine Translation 

### Description
This project aims to explore current limitations in machine translation models trained on sentence-level data. 
A [Marian MT](https://huggingface.co/docs/transformers/model_doc/marian) transformer was used to translate two texts of similar nature from English into Italian. 
Data was evaluated by leveraging [COMET](https://github.com/Unbabel/COMET) default model "Unbabel/wmt22-comet-da" and [Unbabel Qi](https://qi.unbabel.com/).


### Dependencies
In order to run the scripts, the following items should be installed:
- Python 3.10.12 or higher 
- pytorch
- sacremoses
- transformers
- unbabel-comet

### Author
Sara Di Donna
