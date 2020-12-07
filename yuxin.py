'''Semantic Similarity: starter code

Author: Michael Guerzhoy. Last modified: Nov. 14, 2016.
'''

import math


def norm(vec):
    '''Return the norm of a vector stored as a dictionary,
    as described in the handout for Project 3.
    '''

    sum_of_squares = 0.0
    for x in vec:
        sum_of_squares += vec[x] * vec[x]

    return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2):

    #vec2_keys = list(vec2.keys())
    dot = 0

    for key in vec1:
        if key in vec2:
            dot = dot + vec1[key]*vec2[key]

    return dot/norm(vec1)/norm(vec2)

def build_semantic_descriptors(sentences):
    dict = {}

    for sentence in sentences:
        semantics = set(sentence)

        for semantic in semantics:
            if semantic not in dict:
                dict[semantic] = {}
            for word in semantics:
                if semantic != word:
                    if word in dict[semantic]:
                        dict[semantic][word] += 1
                    else:
                        dict[semantic][word] = 1
    return dict

def build_semantic_descriptors_from_files(filenames):
    text = ""
    for file in filenames:
        text = text + open(file, "r", encoding="latin-1").read()

    text = text.lower()

    text = text.replace("\n", " ")
    punctuation = [",", "-", "--", ":", ";"]
    for symbol in punctuation:
        text = text.replace(symbol, " ")
    separator = ["!", "?"]
    for end in separator:
        text = text.replace(end, ".")
    sentences = text.split(".")

    '''
    all_sentences = []
    for sentence in sentences:
        all_sentences.append(sentence.split(" ")
    '''
    all_sentences = []
    for sentence in sentences:
        all_words = sentence.split(" ")
        while "" in all_words:
            all_words.remove("")
        all_sentences.append(all_words)

    return build_semantic_descriptors(all_sentences)

def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    max_similarity = -10
    max = 0
    if word not in semantic_descriptors:
        return choices[i]
    vec1 = semantic_descriptors[word]
    for i in range (len(choices)):
        if choices[i] not in semantic_descriptors:
            similarity = -1
        else:
            vec2 = semantic_descriptors[choices[i]]
            similarity = cosine_similarity(vec1, vec2)
        if similarity > max_similarity:
            max = i
            max_similarity = similarity
    return choices[max]

def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    text = open(filename, "r", encoding="latin-1").read()
    questions = text.split("\n")
    correct = 0

    while "" in questions:
        questions.remove("")
    num = len(questions)

    for i in range (num):
        words = questions[i].split(" ")
        word = words[0]
        answer = words[1]
        choices = words[2:]
        guess = most_similar_word(word, choices, semantic_descriptors, cosine_similarity)
        if answer == guess:
            correct += 1

    return round(correct/num*100, 1)

if __name__ == '__main__':
    sem_descriptors = build_semantic_descriptors_from_files(["pg7178.txt", "2600-0.txt"])
    res = run_similarity_test("test.txt", sem_descriptors, cosine_similarity)
    print(res, "of the guesses were correct")