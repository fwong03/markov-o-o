import sys
from random import choice


class SimpleMarkovGenerator(object):

    def read_files(self, file_path_list):
        """Takes file path as string; returns text as string.
        Takes a string that is a file path, opens the file, and turns
        the file's contents as one string of text.
        """
        content = ""
        
        # Reads all of the filenames and combines all of contents in one string
        for file_path in file_path_list:
            content = content + " " + open(file_path).read()
              
        content.replace('\n', ' ')  
        
        return content


    def make_chains(self, text_string, n):
        """Takes parameters:
             a. text_string : text as string
             b. n : integer that specifies how many words in the n-grams
           Returns dictionary of markov chains.
        A chain will be a key that consists of a tuple of (word1, word2...wordn)
        and the value would be a list of the word(s) that follow those n
        words in the input text.
        For example if n=2:
            >>> make_chains("hi there mary hi there juanita")
            {('hi', 'there'): ['mary', 'juanita'], ('there', 'mary'): ['hi'], ('mary', 'hi': ['there']}
        """
        
        chains = {}
        # Creates a list of all the words in the text
        words = text_string.split()
        
        # Iterates over the list of words to creates the dictionary
        for index in range(len(words)-n): #Stops at last valid key-value pair        

            # Creates the list of n words for key
            key_list = []
            for i in range(n):
                key_list.append(words[index + i])

            # Creates the key by converting the list to a tuple 
            key = tuple(key_list)
            # Creates the value with the next word in the list
            value = words[index + n]
            
            # If the key is in the dictionary, it updates its value with 'value'
            if key in chains.keys():
                chains[key].append(value)
            # Otherwise it creates a new key-value pair    
            else:
                chains[key] = [value]
        
        return chains


    def make_text(self, chains):
        """Takes dictionary of markov chains; returns random text."""
        
        text = ""
        
        # Randomly chooses a key-value from the dictionary
        first_key = choice(chains.keys())
        next_word = choice(chains[first_key])

        # Add the words in the key and the word randomly chosen from its value
        text += " ".join(first_key) + " " + next_word + " "
        
        # Creates a new key 
        new_key = first_key[1:] + (next_word,)
        
        # Repeats all the steps until the new_key is not in the dictionary
        while new_key in chains:
            next_word = choice(chains[new_key])
            text += next_word + " "
            new_key = new_key[1:] + (next_word,)
        
        # Add '.' if last character of text is not punctuation
        if text[-1].isalpha():
            text + "."
        
        # Returns the text with the first letter capitalized
        return text[0].upper() + text[1:]



if __name__ == "__main__":

    # we should call the make_text method 5x

    # we should get list of filenames from sys.argv
    input_paths = []
    ngrams = 2

    # Loops over the list of arguments input from command line
    # Format for the command expected:
    #   'python markov.py ngrams filename_1.txt ... filename_n.txt'
    # If arguments are not provided, program uses default ones
    if len(sys.argv) >= 3:
       ngrams = int(sys.argv[1])  
       for arg in sys.argv[2:]:
           input_paths.append(arg)
    else:
        input_paths.append("green-eggs.txt")
        ngrams = 2
        print "Default text: green-eggs.txt, ngrams: 2"

    # Created an instance of the class, SimpleMarkovGenerator.
    markov_generator = SimpleMarkovGenerator()

    # Call read_files method with the list of filenames.
    text = markov_generator.read_files(input_paths)
    chains_dict = markov_generator.make_chains(text, ngrams)

    for i in range(5):
        print markov_generator.make_text(chains_dict)
        print
