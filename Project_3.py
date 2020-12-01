'''
import swanns_way
import war_and_peace
'''
'''Semantic Similarity: starter code

Author: Michael Guerzhoy. Last modified: Nov. 14, 2016.
'''

import math


# def norm(vec):
#     '''Return the norm of a vector stored as a dictionary,
#     as described in the handout for Project 3.
#     '''pProject 3


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
          # Below this is O(n^2)
          for key2 in d:
            if key2 != key:
              if key2 in s[key]:
                s[key][key2] += 1
                e.pop(key2)
            else:
              e.pop(key2)
        s[key].update(e)
    return s

def build_semantic_descriptors_from_files(filenames):
  full_text = []
  for i in range(len(filenames)):
    with open(filenames[i], 'r', encoding='latin1')as f: text = f.read()
    mid_array = [',', '-', '--', ':', ';']
    for elem in mid_array:
      if elem == '-' or elem == '--':
        text = text.replace(elem, ' ')
      text = text.replace(elem, '')
    text = text.replace('\n\n', ' ')
    text = text.replace('\n', ' ')
    end_array = ['?','!']
    for elem in end_array:
      text = text.replace(elem, '.')
    text = text.replace('. ', '.')
    text = text.lower().split('.')
    for i in range(len(text)):
      text[i] = text[i].replace('  ', ' ')
      text[i] = text[i].split(' ')
    full_text += text
  return build_semantic_descriptors(full_text)

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
    text[i] = text[i].split(" ")
    word1 = text[i][0]
    choices1 = text[i][2:]
    n = similarity_fn(word1, choices1, semantic_descriptors, cosine_similarity)
    if n == text[i][1]:
      count_num += 1
    elif n == '':
      print(text[i][0])
      count_den -= 1
  print(count_den)
  print(count_num)
  return count_num / count_den * 100


if __name__ == '__main__':
  #vec1 = {"a": 1, "b": 2, "c": 3}
  #vec2 = {"b": 4, "c": 5, "d": 6}
  #print(cosine_similarity(vec1, vec2))
  #print(build_semantic_descriptors([["i", "am", "a", "sick", "man"], ["i", "am", "a", "spiteful", "man"], ["i", 'am', 'an', 'unattractive', 'man'], ['however', 'i', 'know', 'nothing', 'at', 'all', 'about', 'my', 'disease', 'and', 'do', 'not', 'know', 'for', 'certain', 'what', 'ails', 'me']]))
  #print(build_semantic_descriptors_from_files(['war_and_peace.txt', 'swanns_way.txt']))
  #print(most_similar_word("man", ['you', 'war', 'hand', 'battle', 'foot', 'eyes', 'face', 'woman', 'boot', 'where'], build_semantic_descriptors_from_files(["war_and_peace.txt", "swanns_way.txt"]), cosine_similarity))
  print(run_similarity_test("test.txt", build_semantic_descriptors_from_files(["war_and_peace.txt", "swanns_way.txt"]), most_similar_word))