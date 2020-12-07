def cosine_similarity(vec1, vec2):
    import math
    #Makes the vectors
    v1 = []
    v2 = []
    numer = 0
    denom_v1 = 0
    denom_v2 = 0
    if vec1 != None and vec2 != None:
        for key in vec1:
            if key in vec2:
                v1.append(vec1[key])
                v2.append(vec2[key])
            denom_v1 += vec1[key] ** 2

        for key in vec2:
            denom_v2 += vec2[key] ** 2

        for i in range(len(v1)):
            numer += v1[i]*v2[i]

        return numer/math.sqrt(denom_v1*denom_v2)
    return 0



#################################################################################################


def build_semantic_descriptors(sentences):
    #returns {for every word in the sentences:{other words it appears with:# of those words}}

    elem = {} #The word count for each of the words/value in sent dict.
    sent = {} #The dictionary that you end up with

    for phrase in sentences:
      dictionary = dict.fromkeys(phrase, 1)
      for k in dictionary:
        if sent.get(k) == None:
          sent[k] = dictionary.copy()
          sent[k].pop(k)
        else:
          elem = dictionary.copy()
          for k2 in dictionary:
            if k2 != k:
              if k2 in sent[k]:
                sent[k][k2] += 1
                elem.pop(k2)
            else:
              elem.pop(k2)
        sent[k].update(elem)
        elem.clear()

    return sent

##############################################################################################################
def text_strip(txt):
    symbol_list = [',', ':', ';', '-', '--', ' ', '\n', '.', '?', '!']
    w = ''
    words = []
    lines = []
    txt = txt.lower() #converts text into lowercase

    for letter in range(len(txt)):
        if txt[letter] in symbol_list:
            if w != '': #word has not reset yet, but the letter is of a symbol in symbol list
                words.append(w)
                w = ''
        if txt[letter] in symbol_list[7:]: #If the punctuation is a sentence breaker; then slicing of symbol list occurs
            if len(words) != 0: #For preventing situations such as "..." elipses; where word resets to ''
                if '' in words: words.remove('') #FAILSAFE
                lines.append(words.copy())
                words.clear()

        if txt[letter] not in symbol_list:#if it doesn't find the special cases with the punctuation - it just adds to the word string
            w += txt[letter]

    return lines



def build_semantic_descriptors_from_files(filenames):
    full_text = '' #full_text is a string that serves as a combination of all the files as strings

    for i in range(len(filenames)):
        f = open(filenames[i], "r", encoding="latin1")
        text = f.read()
        full_text += text #adding together strings for full_text

    full = text_strip(full_text) #file to be used in the build_semantic_descriptors function
    return build_semantic_descriptors(full)


###########################################################################################################

def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    w_cur = choices[0]
    w_dict = semantic_descriptors[word]
    max_cur = -1
    words = set(semantic_descriptors.keys())

    if word in words:

        for c in choices:

            if c in words:
                similarity = similarity_fn(w_dict, semantic_descriptors[c])
                if similarity > max_cur:
                    max_cur = similarity
                    w_cur = c
    return w_cur


def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    f = open(filename, "r", encoding = "latin1")
    temp = f.read().split('\n')
    trials = [chunk.split(' ') for chunk in temp]

    tot_r = 0
    tot = len(trials)
    for t in trials:
        if(len(t) > 2):
            word = t[0]
            act_ans = t[1]
            options = t[2:]
            if most_similar_word(word, options, semantic_descriptors, similarity_fn) == act_ans:
                tot_r += 1
        else:
            tot -= 1

    f.close()
    return ((tot_r / (tot)) * 100.0)
