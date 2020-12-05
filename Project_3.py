'''Semantic Similarity: starter code

Author: Michael Guerzhoy. Last modified: Nov. 14, 2016.
'''

import math


# def norm(vec):
#     '''Return the norm of a vector stored as a dictionary,
#     as described in the handout for Project 3.
#     '''

#     sum_of_squares = 0.0
#     for x in vec:
#         sum_of_squares += vec[x] * vec[x]

#     return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2):
  numerator = 0
  denominator_l = 0
  denominator_r = 0
  for elem in vec1:
    denominator_l += vec1[elem]**2
    if elem in vec2:
      numerator += vec1[elem] * vec2[elem]
  for elem in vec2:
    denominator_r += vec2[elem]**2
  return numerator / math.sqrt(denominator_r * denominator_l)
def b_alt(sentences):
  print(sentences)

def build_semantic_descriptors(sentences):
    s = {}
    e = {}
    for sentence in sentences:
      d = dict.fromkeys(sentence, 1)
      for key in d:
        if s.get(key) == None:
          s[key] = d.copy()
          s[key].pop(key)
        else:
          e = d.copy()
          for key2 in d:
            if key2 != key:
              if key2 in s[key]:
                s[key][key2] += 1
                e.pop(key2)
            else:
              e.pop(key2)
        s[key].update(e)
        e.clear()
    return s

def build_semantic_descriptors_from_files(filenames):
  full_text = ''
  for i in range(len(filenames)):
    with open(filenames[i], 'r', encoding='latin1')as f: text = f.read()
    full_text += text
  full_text = strip_text(full_text)
  return build_semantic_descriptors(full_text)

def strip_text(text):
  word = ''
  words = []
  sentences = []
  text = text.lower()

  special_char_array = ['.', '?', '!', ' ', '\n', ',', ':', ';', '-', '--']
  for i in range(len(text)):
    if text[i] in special_char_array:
      if text[i] != None:
        if word != '':
          words.append(word)
          word = ''
    if text[i] in special_char_array[:3]:
      if len(words):
        if '' in words:
          words.remove('')
        sentences.append(words.copy())
        words.clear()
    if text[i] not in special_char_array:
      word += text[i]
  return sentences

def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
  max = 0
  max_choice = ''
  word_vec = semantic_descriptors.get(word)
  for elem in choices:
    elem_vec = semantic_descriptors.get(elem)
    if word_vec != None and elem_vec != None:
      n = similarity_fn(word_vec, elem_vec)
      if n > max:
        max = n
        max_choice = elem
  return max_choice

def run_similarity_test(filename, semantic_descriptors, similarity_fn):
  with open(filename, 'r', encoding='latin1')as f: text = f.read().split('\n')
  count_num = 0
  count_den = len(text)
  for i in range(len(text)):
    if(text[i]):
      text[i] = text[i].split(" ")
      print("TEXT: ", text[i])
      word1 = text[i][0]
      choices1 = text[i][2:]
      n = most_similar_word(word1, choices1, semantic_descriptors, similarity_fn)
      print("CHOICE: ", text)
      if n == text[i][1]:
        count_num += 1
      elif n == '':
        count_den -= 1
      else:
        count_den -= 1
  return count_num / count_den * 100


if __name__ == '__main__':
  #vec1 = {"a": 1, "b": 2, "c": 3}
  #vec2 = {"b": 4, "c": 5, "d": 6}
  #print(cosine_similarity(vec1, vec2))
  #print(build_semantic_descriptors([["i", "am", "a", "sick", "man", "man"]]))
  #print(build_semantic_descriptors_from_files(['input.txt']))
  #print(most_similar_word("man", ['you', 'war', 'hand', 'battle', 'foot', 'eyes', 'face', 'woman', 'boot', 'where'], build_semantic_descriptors_from_files(["war_and_peace.txt", "swanns_way.txt"]), cosine_similarity))
  print(run_similarity_test("test.txt", build_semantic_descriptors_from_files(["war_and_peace.txt", "swanns_way.txt"]), cosine_similarity))