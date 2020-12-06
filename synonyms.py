'''Semantic Similarity: starter code

Author: Michael Guerzhoy. Last modified: Nov. 14, 2016.
'''

import math, time, copy


def norm(vec):
    
    sum_of_squares = 0.0  
    for x in vec:
        sum_of_squares += vec[x] * vec[x]
    
    return math.sqrt(sum_of_squares)

def cosine_similarity(vec1, vec2):
    top = 0
    bottom1 = 0
    bottom2 = 0
    for item in vec1.items():
        bottom1 += item[1] ** 2
        try:
            top += (item[1] * vec2[item[0]])
            #print("TOP: ", top)
        except:
            pass
    for item in vec2.values():
        bottom2 += item ** 2
    #print(top, bottom1, bottom2)
    return (top / (math.sqrt(bottom1 * bottom2)))


def build_semantic_descriptors(sentences):
    s = {}
    words_in = set()
    for sentence in sentences:
        words = list({word.lower() for word in sentence})
        visited = [word in words_in for word in words]
        for idx, word1 in enumerate(words):
            for x in range(idx + 1, len(words)):
                if(visited[idx]):
                    if(s[word1].get(words[x]) != None):
                        s[word1][words[x]] += 1
                        s[words[x]][word1] += 1
                    else:
                        s[word1][words[x]] = 1
                        if(visited[x]):
                            s[words[x]][word1] = 1
                        else:
                            visited[x] = True
                            words_in.add(words[x])
                            s[words[x]] = {word1 : 1}
                else:
                    visited[idx] = True
                    words_in.add(word1)
                    s[word1] = {words[x] : 1}
                    if(visited[x]):
                        s[words[x]][word1] = 1
                    else:
                        words_in.add(words[x])
                        visited[x] = True
                        s[words[x]] = {word1 : 1}
    return s

def process_text(text):
    temp = ""
    sentences = []
    current_words = []
    current_word = ""
    for i in range(0, len(text)):
        #print(current_word)
        if(text[i] == '!' or text[i] == '?' or text[i] == '.'):
            if(len(current_words)):
                #print(current_words)
                if(current_word):
                    current_words.append(current_word)
                    current_word = ""
                sentences.append(copy.copy(current_words))
                #print(sentences)
                current_words.clear()
        elif(text[i] == ' ' or text[i] == '\n' or text[i] == '-' or text[i] == ',' or text[i] ==':' or text[i] == ';'):
            if(current_word):
                current_words.append(current_word)
                current_word = ""
        else:
            current_word += text[i]
    #text1 = temp.replace('\n', ' ')
    #print("PROCESSED TEXT:", sentences)
    return sentences
    

def build_semantic_descriptors_from_files(filenames):
    text = ""
    for file in filenames:
        f = open(file, "r", encoding="latin1")
        text += f.read()
        f.close()
    #print("TEXT: ", text)
    sentences = process_text(text)
    #print(sentences)
    #print("LENGTH OF SENTENCES", len(sentences))
    yee =  build_semantic_descriptors(sentences)
    #print("YEE: ", yee)
    return yee

#print(build_semantic_descriptors_from_files(["sample_case2.txt"]))
#eyyy = build_semantic_descriptors_from_files(["custom_test.txt"])
#print(eyyy)
#print(eyyy["cats"])

def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    word_dict = semantic_descriptors[word]
    current_max = -1
    current_word = choices[0]
    words = set(semantic_descriptors.keys())
    if(word in words):
        for choice in choices:
            if(choice in words):
                similarity = similarity_fn(word_dict, semantic_descriptors[choice])
                if(similarity > current_max):
                    current_max = similarity
                    current_word = choice
    return current_word


def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    f = open(filename, "r", encoding = "latin1")
    temp = f.read().split('\n')
    tests = [chunk.split(' ') for chunk in temp]
    #sprint(tests)
    tot_right = 0
    total_cnt = len(tests)
    for test in tests:
        if(len(test) > 2):
            #print(test)
            word = test[0]
            real_ans = test[1]
            options = test[2:]
            if(most_similar_word(word, options, semantic_descriptors, similarity_fn) == real_ans):
                tot_right += 1
        else:
            total_cnt -= 1
    f.close()
    return ((tot_right / (total_cnt)) * 100.0)


t0 = time.time()
sem_descriptors = build_semantic_descriptors_from_files(["wp.txt" , "sw.txt"])
print("RUNTIME YEEE: ", time.time() - t0)
#print(sem_descriptors['i'])
res = run_similarity_test("test.txt", sem_descriptors, cosine_similarity)
print(res, " percentage of the guesses were correct")
