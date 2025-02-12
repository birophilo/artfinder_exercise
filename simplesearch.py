import argparse
import glob
import string
import sys
from collections import defaultdict


class WordSearcher:

    def __init__(
        self,
        dir: str = "tests/directory",  # directory to search
        ranking_system: str = "basic",  # or "advanced"
        test_mode: bool = False
    ):

        filepath_list = glob.glob(f"{dir}/*")

        self.test_mode = test_mode
        self.ranking_system = ranking_system

        self.word_indexes = {}

        # create word index for each file, but skip if it cannot be parsed as text
        for filepath in filepath_list:
            word_index = self.build_word_index_for_file(filepath)
            if word_index is not None:
                self.word_indexes[filepath] = word_index

        # if no files can be parsed, exit the search terminal
        if self.word_indexes == {}:
            print(f"Error: No text files could be parsed in the specified directory {dir}. Exiting...")
            sys.exit(1)

        print("Starting search terminal...")
        print("Enter text to search, or enter ':quit' to exit (or press Ctrl + C).")

        self.results = {filename: None for filename in self.word_indexes.keys()}

        if test_mode is False:
            self.request_input()

    def parse_file_into_text(self, filepath: str):
        try:
            with open(filepath) as f:
                return f.read()
        except Exception as e:
            print(f'Warning: Could not parse {filepath} into text - skipping file. Received error: "{e}"')
        return None

    def build_word_index_for_file(self, filepath: str) -> dict:
        """
        Build a dict of words in each file and counts of each word, e.g.
        {"this": 2, "that": 1, "other": 4}
        """
        text = self.parse_file_into_text(filepath)
        if text is None:
            return None

        word_list = self.get_formatted_word_list(text)
        word_index = defaultdict(int)

        for word in word_list:
            word_index[word] += 1

        return word_index

    def get_search_results(self, input_word_list: list):
        """
        :input_word_list: the user input words parsed as a list, e.g.
        ["to", "be", "or", "not", "to", "be"]
        """
        for filepath in self.word_indexes:
            word_counts = []
            for word in input_word_list:
                n = self.word_indexes[filepath][word]
                word_counts.append(n)
            result = self.score_results(word_counts, input_word_list)
            self.results[filepath] = result

    def request_input(self):
        text_input = input("search > ")
        self.handle_input(text_input)

    def get_formatted_word_list(self, text: str):
        return [word.strip(string.punctuation).lower() for word in text.split()]

    def handle_input(self, text: str):
        """
        The main workflow:
        - receive the user's text and format it
        - get search results in each file for the user's text
        - rank the file results
        - output the results in the terminal
        - prompt the user for the next search

        args:
        :text: str - the text entered by the user in the prompt
        """
        if text.strip() == ":quit":
            print("Exiting...")
            return

        input_word_list = self.get_formatted_word_list(text)

        if len(input_word_list) == 0:
            print("No words entered. Please try again.")
            self.request_input()

        self.get_search_results(input_word_list)

        # different search ranking systems are applied here
        if self.ranking_system == "advanced":
            output_to_print = self.rank_results_advanced()
        else:
            output_to_print = self.rank_results_basic()

        # if in test mode, capture results and return instead of prompting again
        if self.test_mode is True:
            return output_to_print

        if len(output_to_print) == 0:
            print("No matches found")

        # output results in terminal
        for line in output_to_print:
            print(line)

        # return to user prompt
        self.request_input()

    def score_results(self, word_counts: list, word_input_list: list):
        matching_words = len([c for c in word_counts if c > 0])
        total_matching_words = sum([c for c in word_counts])
        return {
            "match_ratio": matching_words/len(word_input_list),
            "total_matches": total_matching_words
        }

    def rank_results_basic(self):
        # basic search ranking: the % of user's words that appear in file
        ratios = {k: v["match_ratio"] for k, v in self.results.items()}
        filtered_results = {k: v for k, v in ratios.items() if v > 0}
        ordered_results = dict(
            # sort matches, highest scores first, limit to 10 results
            sorted(filtered_results.items(), key=lambda x: x[1], reverse=True)[:10]
        )

        output = []

        for filepath, result in ordered_results.items():
            output.append(f"{filepath.split('/')[-1]}: {result:.0%}")

        return output

    def rank_results_advanced(self):
        # alternative approach: a score based on % of words matched and number of occurrences
        ratios = {k: v["match_ratio"] * v["total_matches"] for k, v in self.results.items()}
        filtered_results = {k: v for k, v in ratios.items() if v > 0}
        ordered_results = dict(
            sorted(filtered_results.items(), key=lambda x: x[1], reverse=True)[:10]
        )

        output = []

        for filepath, result in ordered_results.items():
            output.append(f"{filepath.split('/')[-1]}: {result:.2f}")

        return output


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory")
    parser.add_argument("-r", "--rank")

    args = parser.parse_args()
    ranking_system = args.rank or "basic"
    directory = args.directory or "tests/directory"

    WordSearcher(dir=directory, ranking_system=ranking_system)
