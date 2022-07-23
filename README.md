fuzz_generator (how it works):

    [гугл переводчик сила]

    1. Words are generated from the alphabet into the basic list "basic_symbols_of_alphabet_as_list"
    ( in a loop we fill the words with the first character from the alphabet according to the desired length of the word
    and add them to the "words_list" list)


    2.1/2 - If the number of given words is less than the number of characters in the alphabet.
    Give out the list "words_list", trimming by the number of necessary words

    2.2/2 - If the number of given words is greater than the number of characters in the alphabet:
    In an endless loop (until we get the desired number of words in the "words_list")
    copy the required number of words from the "words_list" list.
    Further the copy and the alphabet are started up on a double cycle.
    With the first loop we get a word from the list, with the second loop we add a character from the alphabet to each word
    With each character a new word is added to the "words_list".
    Give out the list "words_list", trimming by the number of necessary words.


    In short:
    
    Create from a word from the alphabet -> if not enough, copy what you have and how much you need
    and from this create more words until there is enough.