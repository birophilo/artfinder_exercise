

# Artfinder exercise



## Install

```bash
# clone the repo
$ git clone git@github.com:birophilo/artfinder_exercise.git
$ cd artfinder_exercise

# create and initialize a virtual environment
$ python -m venv env
$ source env/bin/activate

# install the requirements
$ pip install -r requirements.txt
```



## Run

```bash
# start searcher specifying the directory to use
$ python simplesearch.py -d <my_dir>

# or pass no directory to use the test directory by default
$ python simplesearch.py

# specify ranking system ("basic" the default, or "advanced")
$ python simplesearch.py -r advanced
```



## Search Ranking system

A choice of two simple scoring systems:

### Basic

A percentage - the percentage of user inputted words present in each file

```bash
$ search > france germany italy
# results
file_02.txt: 100%
file_04.txt: 67%
file_03.txt: 67%
file_05.txt: 33%
```



### Advanced

A decimal number - higher is better. The total number of matching words in each file multiplied by the percentage ratio above, so that files with more occurrences of the input words score higher.

```bash
$ search > france germany italy
# results
file_02.txt: 11.00
file_03.txt: 8.00
file_04.txt: 6.00
file_05.txt: 0.33
```



## Tests

```bash
python -m pytest
```

To see some example inputs and outputs, see `tests/fixtures.py`.

To run the `WordSearcher` class in Python

```python
from simplesearch import WordSearcher

# run in test mode to try out class methods manually; without test mode, it returns an input prompt after init
searcher = WordSearcher(test_mode=True)
```



## Error handling

Errors anticipated and handled:

- if a file cannot be parsed as text (e.g. emoji.png in test directory)
- if no files in the directory can be parsed
- if user input is blank or empty after formatting
