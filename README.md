# Named Enitity Recognition Tagger

This NER tagger uses a trigram hidden-markov language model plus the viterbi algorithm to tag Chinese sentences according to 
whether they contain named entities, such as the names of people, times, places and businesses. The model achieves 96% accuracy
and an 84% f1-score on the dev.txt data.

## Requirements

* Python version: 3.5.1

## Start Developing

After cloning the repository:

* Setting up the environment：
    - `cd ner-tagging`
    - Create a virtual environmnet: `python3 -m venv venv`
    - `source venv/bin/activate`
    - Install the project dependencies：`pip install –r requirements.txt`

* Start the program:
    - Ensure that you are inside `/ner-tagging` and that your virtual environment is running
    - Enter `python models/hmm.py`. This will generate a file called `probabilities.txt`
    - After generating the `probabilities.txt` file, to test the model on the dev.txt set: run `python tests/test_dev.py`. This will output the accuracy and f1-scores for the validation data set.
    - To generate predictions for the `test.content.txt` data, while in `/ner-tagging`, run `python tests/test_test.py`. This will create `prediction.txt`
    - Deactivate your virtual environment by entering `deactivate`
