import requests
import random


def filter_words(self, word_list):
    """Removes a word out of the list if it has another word in it"""

    # There was a problem with other words going green, and I couldn't be bothered to find a better way of solving it
    words_to_remove = []

    for word1 in word_list:
        for word2 in word_list:
            if word1 != word2 and word1 in word2:
                words_to_remove.append(word1)

    return [word for word in word_list if word not in words_to_remove]


class RandomWordsGenerator:

    def get_random_words(self):
        """Gets random words from an API and returns a set list of words if the user has no internet"""

        # Parameters for the API request
        params = {
            "number": "100",
            "length": "5"
        }

        try:
            response = requests.get("https://random-word-api.herokuapp.com/word?number=100", params=params)
            random_words = response.json()

            return filter_words(self, random_words)

        except:
            # For when the user doesn't have internet access
            offline_words = [
                "apple", "banana", "orange", "grape", "kiwi",
                "watermelon", "mango", "strawberry", "blueberry", "raspberry",
                "pineapple", "pear", "peach", "plum", "apricot",
                "cherry", "lemon", "lime", "coconut", "pomegranate",
                "avocado", "melon", "fig", "guava", "papaya",
                "tangerine", "cantaloupe", "nectarine", "cranberry", "blackberry",
                "raspberry", "grapefruit", "dragonfruit", "passionfruit", "honeydew",
                "persimmon", "rhubarb", "lychee", "boysenberry", "gooseberry",
                "kiwifruit", "mulberry", "quince", "starfruit", "kumquat",
                "date", "durian", "elderberry", "jamberry", "ackee",
                "carambola", "feijoa"
            ]
            random.shuffle(offline_words)

            return filter_words(self, offline_words)

