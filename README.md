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
    - Ensure that you are inside `ner-tagging` and that your virtual environment is running
    - Enter `cd utils`
    - Generate the `vocabulary.txt` and `tags.txt` files: `python generate_vocabulary.py` (this may take a minute or two)
    - Generate the `emission_counts.txt`, `tag_counts.txt`, `emission_probabilities.txt` and `transition_probabilities.txt`:
    `python emissions_and_transitions.py`
    - The necessary files have now been generated. Test the model on the dev.txt set: `cd ../tests` and then run `python dev_test.py`
    - To generate predictions for the `test.content.txt` data, while in `/tests`, run `python test_test.py`. This will create `prediction_final.txt`
    - Deactivate your virtual environment by entering `deactivate`
