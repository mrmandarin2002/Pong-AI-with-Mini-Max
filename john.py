
import math


def norm(vec):
    '''Return the norm of a vector stored as a dictionary,
    as described in the handout for Project 3.
    '''
    
    sum_of_squares = 0.0  
    for x in vec:
        sum_of_squares += vec[x] * vec[x]
    
    return math.sqrt(sum_of_squares)


#PART A
def cosine_similarity(vec1, vec2):
    numerator = 0.0
    denominator = 0.0
    for i in vec1:
        for j in vec2:
            if i == j:
                numerator += vec1.get(i) * vec2.get(j)
    denominator = norm(vec1)*norm(vec2)
    return (numerator / denominator)


#PART B
def build_semantic_descriptors(sentences):
    #dictionary for entire words
    small_boi = {}
    #going through all the # of sentences
    for i in range(len(sentences)):
        for j in range(len(sentences[i])):
            sentences[i][j] = sentences[i][j].lower()
        sentences[i] = list(set(sentences[i]))
        for j in range(len(sentences[i])):
            if sentences[i][j] in small_boi:
                #if the word exists in the current dictionary from a previous sentence, update value += 1
                for k in range(len(sentences[i])):
                    if sentences[i][k] in small_boi[sentences[i][j]] and sentences[i][k] != sentences[i][j]:
                        #update keys so count += 1
                        small_boi[sentences[i][j]][sentences[i][k]] += 1
                    #if the word is not in current dictionary, add a new key and value 
                    elif sentences[i][k] != sentences[i][j]:
                        small_boi[sentences[i][j]][sentences[i][k]] = 1  
            else:                  
                #dictionary for one single word
                smaller_boi = {}
                for k in range(len(sentences[i])):
                    #not counting repeating words, adds words into a sub dictionary  
                    if sentences[i][k] not in smaller_boi and sentences[i][k] != sentences[i][j]:
                        smaller_boi[sentences[i][k]] = 1       
                #adds sub dictionary to dictionary    
                small_boi[sentences[i][j]] = smaller_boi      
    return small_boi


#PART C
def build_semantic_descriptors_from_files(filenames):
    text = ""
    for i in range(len(filenames)):
        f = open(filenames[i], "r", encoding="latin1")
        text += f.read()

    cur_text = ""
    for i in range(len(text)):
        if(text[i] == '\n' or text[i] == ',' or text[i] == '-' or text[i] == ':' or text[i] == ';'):
            cur_text += ' '
        elif(text[i] == '?' or text[i] == '!'):
            cur_text += '.'
        else:
            cur_text += text[i]

    sentences = [[word for word in sentence.split(' ') if word] for sentence in cur_text.split('.') if len(sentence) != 0]

    return build_semantic_descriptors(sentences) 


#PART D
def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    values = []
    word_similarities = semantic_descriptors[word]

    for i in choices:
        if word in semantic_descriptors and i in semantic_descriptors:
            choice_similarities = semantic_descriptors[i]
            values.append(similarity_fn(word_similarities, choice_similarities))
        else:
            values.append(-1)
    return choices[values.index(max(values))]


#PART E
def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    numerator = 0.0
    
    f = open(filename)
    text = f.read()
    lines = text.split("\n")
    denominator = len(lines)
    words = [[]]*len(lines)
    for i in range(len(lines)):
        words[i] = lines[i].split(" ")
    for i in range(len(words)):
        if most_similar_word(words[i][0], words[i][2:len(words)], semantic_descriptors, similarity_fn) == words[i][1]:
            numerator += 1
    return numerator / denominator * 100

  
if __name__ == '__main__':
    sem_descriptors = build_semantic_descriptors_from_files(["wp.txt", "sw.txt"])
    res = run_similarity_test("test.txt", sem_descriptors, cosine_similarity)
    print(res, "of the guesses were correct")