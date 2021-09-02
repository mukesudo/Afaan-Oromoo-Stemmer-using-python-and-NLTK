#Author. Mukhtar Saeed      ...     github: @mukesudo

from nltk.corpus import stopwords
from nltk.tokenize import  word_tokenize




#Here Are the definitions of some useful terms


stopWords = set(stopwords.words('Oromifa'))

OromooVowels = {'a', 'e', 'i', 'o', 'u'}

repeatedVowel = ('aa', 'ee', 'ii', 'oo', 'uu')

OromooConsonants = {'b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z', '`'}

OromooEndings = ('b', 'g', 'd')

sixthCluster = ('eenya','ottaa','annoo','ummaa','nootaa','neen')

fifthCluster = ("'aa", "'e", "'u", "'ee", 'suu', 'sa', 'sse', 'nya')

fourthCluster = {'du', 'di', 'daan'}

special = 'wwan'

def IsConsonant(word,i):
    if word[i] in OromooConsonants:
        return True                    #this block of code returns true if the word[i] is a consonant,
                                        # returns false if the word is vowel
    else:
        return not IsConsonant(word,i-1)


def MeasureVC(stem):                    #This block of code tries to numerate how many vowel-consenant sequencce is there
    cv_sequence = ''                    #in the stem word after being stemmed
    for k in range(len(stem)):
        if IsConsonant(stem, k):
            cv_sequence += 'c'
        else:
            cv_sequence += 'v'
    return cv_sequence.count('vc')


def step1(word):
    word = word.lower()
    for i in sixthCluster:                          #here we would compare if the word contains the suffixes from the Sixth cluster
        if(word.endswith(i)==True):
            if (MeasureVC(word.strip(i)) >= 1):
                beforeSuffix = word[word.find(i) - 1]  # Here we would store the character before the suffix,(i.e the character just after the assumed stem
                for j in OromooConsonants:
                    if (beforeSuffix == j):
                        word = word.strip(i)
                        return word
            else:
                return word

    return word



def step2(word):
    word = word.lower()
    temp = []
    for i in fifthCluster:          # here we would compare if the word contains the suffixes from the Fifth cluster
        if (word.endswith(i) == True):
            temp=word.strip(i)
            if(MeasureVC(temp)>=1):
                print(temp.replace(i,''))
                temp1 = word.replace(i,'')
                return temp1
            else:
                temp2 = word.replace(i,'`')
                return temp2
        else:
            continue
    return word



def step3(word):
    word = word.lower()
    for i in fourthCluster:
        if(word.endswith(i)==True):
            workingPlace = word.replace(i,'')
            print(workingPlace)
            if(MeasureVC(workingPlace)>=1 and workingPlace.endswith(OromooEndings)):
                return workingPlace
            elif(MeasureVC(workingPlace)==0):
                return word.replace(workingPlace,'d')
            else:
                return word
    if(word.endswith(special)==True):
        workingPlace = word.replace(special,'')
        if(MeasureVC(workingPlace)>=1 & workingPlace.endswith(repeatedVowel)):
            return workingPlace
        else:
            return word
    else:
        return word

#Openning A File

g = open('sample-text.txt')
text = g.read()


print('Before Tokenization: ')
print(text)

tkn = word_tokenize(text)           #This code tokenizes the string tkn
print('After tokenization: ')
print(tkn)
print('length of the tokens: ')
print(len(tkn))

f = open('OromiffaStopWords.txt')   #Opens Stopword file
stopWords = f.read()

print('Stop Words : ')
print(stopWords)


wordsFiltered = []

for w in tkn:
     if w not in stopWords:
          wordsFiltered.append(w)

print('After StopWords elimination: ')
print(wordsFiltered)

print('Length of the words filtered: ')
print(len(wordsFiltered))


wordsStemmed = []

for word in wordsFiltered:
    word = step1(word)
    word = step2(word)
    word = step3(word)
    wordsStemmed.append(word)
print('Words after stemming are: ')
print('Term Frequency: '+format(len(wordsStemmed)))
