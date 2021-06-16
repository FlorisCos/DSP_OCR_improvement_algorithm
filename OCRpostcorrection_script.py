# -*- coding: utf-8 -*-

import numpy
import re

""" Data Science Project - OCR post-correction code"""

"""Part 1: Preparations."""

"""Download Transformers module.

The line below should only be executed when the algorithm is not run within a virtual environment!
"""
#!pip install transformers 

"""Download language model 'Robbert'."""
from transformers import pipeline
pipeline = pipeline("fill-mask", model="pdelobelle/robbert-v2-dutch-base", top_k=10)

def cijfers_en_namen_toevoegen():
  """Add numbers 0 to 300 and names to your lexicon.

  Open connections to a file with your lexicon, a file with the names you want to be recognized and a new file that will be your new lexicon file.
  """
  wordlist_orig=open("wordlist.txt", mode="r").read()
  wordlist_aangepast=open("wordlist_aangepast.txt", mode="w")
  namen=open("naamsvarianten.txt", mode="r")
  """Write the old lexicon to the new lexicon file, with only lowercase characters."""
  wordlist_aangepast.write(wordlist_orig)
  wordlist_orig=wordlist_orig.lower()
  
  def voeg_cijfers_toe(wordlist):
    """Write number 0 to 300 to the new lexicon file."""
    for i in range(301):
      i=str(i)
      wordlist_aangepast.write(i+"\n")
  
  def voeg_namen_toe(wordlist):
    """Write all names in the file with names to the new lexicon file."""
    for line in namen:
      wordlist.write(line)

  voeg_cijfers_toe(wordlist_aangepast)
  voeg_namen_toe(wordlist_aangepast)

  wordlist_aangepast.close()
  namen.close()


def paginanummers_fixen_en_verwijderen(titel):
  """Remove pagenumbers.

  input: String that contains the name of your text file.
  output: A new text file without page numbers called 'beter.txt'. 
  """
  import re
  

  tekst = open(titel,"r")
  nieuw_bestand = open("beter.txt","w")

  def vind_paginanummers(line):
    """Find lines that contain a misread page number."""
    line = line.strip()
    if len(line) < 5:
      line=re.sub(pattern=" ",repl="",string=line)
    if len(line) < 4:
      """Check if the line contains the following pattern:

      1. any non digit character -- [^\d]
      2. followd by any character, zero or more times -- .*
      3. followed by a character that's none of the following characters -- .!?’'"/-:)K
      4. followed by the end of the line.
      """
      if len(re.findall(pattern="[^\d].*[^\.!\?’'\"/\-:\)K]$",string=line)) > 0:
        origineel = line
        """Repair a misread page number."""
        if len(re.findall(pattern="[^VXIL]",string=line)) > 0:
          line=re.sub(pattern="[JIiTj*l!rïxX»«']",repl="1",string=line)
          line=re.sub(pattern="[nMH\"u”]",repl="11",string=line)
          line=re.sub(pattern="[oO°óÓ]",repl="0",string=line)
          line=re.sub(pattern="\?",repl="7",string=line)
          line=re.sub(pattern="g",repl="9",string=line)
          line=re.sub(pattern="a",repl="2",string=line)
          line=re.sub(pattern="\.",repl="",string=line)
        if len(re.findall(pattern="^I+$",string=line)) > 0:
          line=re.sub(pattern="I",repl="1",string=line)
        if len(re.findall(pattern="[^\dVXIL]",string=line)) > 0:
          line = origineel

    return(line)

  def verwijder_paginering(line):
    """Write all lines that are not a page number to your new text file."""
    if not (len(line)<6 and len(re.findall(pattern="[^\dVXIL]",string=line))==0):
      nieuw_bestand.write(line+"\n")

  for line in tekst:
    line = vind_paginanummers(line)
    verwijder_paginering(line)

  nieuw_bestand.close()

"""Part 2: corrections on line-level"""

def spatieoplossing(line):
  """Fix two white space errors.
  input: a line (string) from the textfile.
  output: a (string) line from the textfile with less white space errors.
  """
  line = line.strip()

  spaties = 0
  andere = 0

  for character in line:
    """Count the number of spaces and the number of non-spaces in each line.
    
    Key arguments:
    spaties -- integer variable with the number of spaces 
    andere -- integer variable with the number of non-spaces
    """
    if character == " ":
      spaties += 1
    else:
      andere += 1

  """Split line on white spaces."""
  line = line.split()
  zin = ""

  for word in line:
    """Remove spaces inbetween isolated characters.
    
    Key arguments:
    line -- list of words (characters separated by spaces) that make up your line.
    zin -- string variable that will contain the new line.

    Add all words in 'line' to 'zin' with spaces inbetween, unless there's more than one isolated character in a row. Then, put no spaces inbetween these characters.
    """
    if len(word)!=1:
      if len(zin) == 0:
        zin += (word+" ")
      else:
        zin += (" "+word+" ")
    elif len(re.findall(string=word,pattern="[.,!?]"))>0:
      zin += (word+" ")
    else:
      zin += word
  
  """Replace multiple successive spaces with only a single space."""
  line = re.sub(string=zin, pattern=" {2,}",repl=" ") 
  """If a line ends with a space, remove this whites space"""
  if line.endswith(" "):
    line = line[0:(len(line)-1)]

  """If the percentage of spaces in the line is more than 37, remove all spaces."""
  if(spaties/(spaties+andere)>0.37):
    beginpunt = 0
    line_los = ""
    """Add spaces to form longest possible words.
    
    Key arguments:
    beginpunt -- integer variable that contains the index of the character in the old line without spaces that the next word in the new line starts with.
    line_los -- string variable that will be the new line by adding words and spaces.
    tijdelijk -- string variable that contains an increasingly smaller part of the initial line without spaces.
    """
    while beginpunt < len(line):
      """
      If 'tijdelijk' is in your lexicon, add 'tijdelijk' to 'line_los.
      If 'tijdelijk' is not in your lexicon, or is a puntuation character, or is just one character long, Remove one character from 'tijdelijk'.
      """
      for i in range(len(line)):
        tijdelijk = line[beginpunt:len(line)-i]
        if "\n"+tijdelijk.lower()+"\n" in wordlist:
          beginpunt = len(line)-i
          break
        elif tijdelijk in "([-—.,:;!\?'\(\) ])":
          beginpunt = len(line)-i
          break
        elif len(tijdelijk)==1:
          beginpunt = len(line)-i
          break
      line_los += tijdelijk+" "
    line_los+="\n"
    """Replace multiple successive white spaces with only a single white space."""
    line_los = re.sub(string=line_los, pattern=" {2,}",repl=" ")
    """If a line ends with a white space, remove this whites space"""
    line_los = re.sub(string=line_los, pattern=" ([-—.,:;!\?\(\) ])",repl="\\1")  
    return(line_los)

  line += "\n"
  return(line)


def verwijder_regelafbrekingen(line, deel1, regelafbraak):
  """Remove end-of-line hyphenation and glue the broken off word back together.  
  
  Key arguments:
  regelafbraak -- boolean variable that is set to 'True' when end-of-line hyphenation is found and is set back to 'False' when the broken off word is glued together again.
  deel1 -- string variable that contains the first part of the broken off word.

  input: 
  1. 'line', containing the line.
  2. 'deel1' (empty at first), containing the first part of a broken off word. 
  3. 'regelafbraak' (default is 'False'), containing a boolean that says if there has been a detection of end-of-line hyphenation in the previous line.
 
  Set 'regelafbraak to 'False' when the previous sentence contained end-of-line hyphenation."""
  if regelafbraak==True:
    strippedline=line.strip()
    #for when there's only a linenumber on a line:
    if not strippedline.isdigit():
      regelafbraak=False
      #plakt woorddelen aan elkaar:
      "Paste the first part of the word in front of the second part of the word."
      line=deel1+line 
  """
  Check if line ends with end-of-line hyphenation.
  If so, assign the first part of the broken off word in 'deel1', set 'regelafbraak' to 'True'.
  """
  if line.endswith("-\n") and not line.endswith(" -\n"):
    """
    Check if the following pattern is in the line:
    1. a space
    2. then any letter in the alphabet one or more times
    3. then a hyphen
    4. then an end-of-line character
    """
    match=re.findall(string=line, pattern=" [a-z]+-\n",flags=re.IGNORECASE)
    if len(match)>0:
      regelafbraak=True
      deel1=match[0]
      """Remove the first part of the broken off word."""
      line=line.replace(deel1,"\n")
      """Assign the first part of the broken off word to 'deel1'."""
      deel1=re.sub(string=deel1, pattern=" ([a-z]+)-\n", repl="\\1")

  return(line, deel1, regelafbraak)


def fix_paginanummers_eindvdzin(line, deel1, paginanummereind):
  """Paste broken off words together that have been separated by a page number at the end of a sentence. 
  For example: 'sep48\narated'.

  Key arguments:
  paginanummereind -- boolean variable that is set to 'True' when a case is found and is set back to 'False' when the broken off word is glued together again.
  deel1 -- string variable that contains the first part of the broken off word.

  input: 
  1. 'line', containing the line.
  2. 'deel1' (empty at first), containing the first part of a broken off word. 
  3. 'paginanummereind' (default is 'False'), containing a boolean that says if there has been a detection of a case in the previous line.
  
  Paste the first part of the broken off word in front of the second part of the word,, and then set paginanummereind to False, when a case has been detected.
  """
  if paginanummereind:
    line=deel1+line
    paginanummereind=False
  """
  Check if the following pattern is in the line:
  1. a space
  2. then any letter in the alphabet one or more times
  3. then any number between 0 and 9 one or more times
  4. then an end-of-line character

  If so, remove that part of the line and assign the first part of the word to 'deel1'.
  """
  matches=re.findall(pattern=" [a-z]+[0-9]+\n",string=line)
  if len(matches)>0:
    paginanummereind=True
    deel1=matches[0]
    line=line.replace(deel1,"\n")
    deel1=re.sub(string=deel1, pattern=" ([a-z]+)[0-9]+\n", repl="\\1")

  return (line,deel1,paginanummereind)


def leestekens_losmaken(line, wordlist):
  """Separates punctuation characters from the words.
  
  input: 
  1.'line' with a string containing the line.
  2. 'wordlist', containing the lexicon as a string.
  output: 'line', with a string containing the line, but now with spaces around the punctuation characters.
  
  Remove excessive spaces."""
  line = re.sub(pattern=" {2,}",repl=" ",string=line)
  """Replace all different kinds of quotation mark for a single kind"""
  line = re.sub(pattern='"|’|‘|”|«|»|„|“|”',repl="'",string=line)
  line = aanhalingstekens_fixen(line, wordlist)
  line = line.strip()
  """Place white spaces around punctuation characters. (This is in order to separate the punctuation characters from the words. This will later be turned back.)
  """
  line = re.sub(pattern="([-—.,:;!\?'\(\)])",repl=" \\1 ",string=line)
  return(line)

def aanhalingstekens_fixen(line, wordlist):
  """Fix wrongly recognized quotation marks.
  
  Key arguments:
  linelist -- list that contains your line, split by white spaces, so every position in the list contains a new word or punctuation mark.
  new_linelist -- (starts out empty.) list that will contain the a list of alle the words and puntuation marks in the line.
  startswithquotation -- (default is set to 'False' with every line.) a boolean that says if the current line starts with a quotation mark.
  """
  linelist=line.split()
  new_linelist=[]
  
  for word in linelist:
    startswithquotation = False

    """Remove the quotation mark if a word starts with a quotation mark. """
    if word.startswith("'"):
      word=word[1:]
      startswithquotation = True

    """Check if word is not in your lexicon."""
    aant_in_wordlist=re.findall(pattern=re.escape(word.lower())+"\n", string=wordlist)
    if len(aant_in_wordlist)==0:

      """Check if the word contains the following pattern:
      1. any letter in the alphabet
      2. followed by one of the characters that are often mistaken for a close quote: '*', '/', 'e', 'c', or any digit.
      """
      pattern_in_word=re.findall(pattern="[a-z][*/ec\d]$", string=word)
      """Check if the word contains the following pattern:
      1. any letter in the alphabet
      2. followed by '!','?' or '.'
      3. followed by one of the characters that are often mistaken for a close quote: '*', '/', 'e', 'c', or any digit.
      """
      pattern_with_punct_in_word=re.findall(pattern="[a-z][!\.\?][*/ec\d]$", string=word)
      if len(pattern_with_punct_in_word)>0:
        """Check if the word without the last two characters is in the lexion."""
        punctuation=word[-2]
        word_til_last_char=word[:-2]
        pattern_in_wordlist=re.findall(pattern=re.escape(word_til_last_char.lower())+"\n", string=wordlist)
        if len(pattern_in_wordlist)>0:
          """If so, overwrite word with the actual word + the punctuation mark + a close quote."""
          word=word_til_last_char+punctuation+"'"
      elif len(pattern_in_word)>0:
        """Check if the word without the last character is in the lexicon."""
        word_til_last_char=word[:-1]
        pattern_in_wordlist=re.findall(pattern=re.escape(word_til_last_char.lower())+"\n", string=wordlist)
        if len(pattern_in_wordlist)>0:
          """If so, overwrite word with the actual word + the punctuation mark + a close quote."""
          word=word_til_last_char+"'"
    if startswithquotation:
      """If the word started with a quotation mark, add it again."""
      word="'"+word
    """Append every word to the new list."""
    new_linelist.append(word)

  """Turn the list containing the line into a string again by joining the words with a space inbetween."""
  line=" "
  line=line.join(new_linelist)
  line+="\n"
          
  return(line)

"""# Hardcoding op lineniveau"""

def losse_beginletter_fixen (line, wordlist):
  """
  Fix words from which the first letter has been separated by the rest of the word by a white space. 
  For example: 's eparated'.

  Check if the following pattern is in the line:
  1. first, a spacce
  2. followed by one of these letters: 'abcdefghijklmnopqrtvwxyz' once.
  3. followed by a space.
  4. followed by two or more letters of the alphabet.
  """
  patroon=" ([abcdefghijklmnopqrtvwxyz]{1}) ([a-z]{2,})"
  matches=re.findall(pattern=patroon, string=line)
  aantal_gevallen=len(matches)
  """
  For every match to the pattern in the line, do the following: 

  1. save the isolated character in 'eersteletter' and the rest of the letters in 'restvanwoord'.
  2. if 'restvanwoord' is not in the lexicon and if 'eersteletter'+'restvanwoord' is, remove the white space.
  """
  if aantal_gevallen>0:
    for i in range(aantal_gevallen):
      geval=matches[i]
      eersteletter=geval[0]
      restvanwoord=geval[1]
      if "\n"+restvanwoord.lower()+"\n" not in wordlist.lower():
        if "\n"+eersteletter.lower()+restvanwoord.lower()+"\n" in wordlist.lower():
          line=re.sub(string=line, pattern=eersteletter+" "+restvanwoord, repl=eersteletter+restvanwoord)
  return(line)

#Positie van spaties nemen en van de line een lijst maken waarvan de woorden per positie gecontroleerd kunnen worden
def neem_spatieposities(line):
  """Turn the string into a list and save the position of where the spaces were in the list in 'spatiepos'.
  
  input: 'line': a string that contains the line.
  output: 1. 'lijst': a list that contains the line, with at every position a new word. 
          2. spatiepos: a dictionary with as keys: indexes of the positions of the words after which a number of spaces is removed by splitting the line into a list of words;
                                    and as values: the number of spaces that has been lost at that position by splitting.
  """

  import re
  
  lijst = line.split()
  spatiepos = {}

  index = 0
  aantal_spaties = 0
  woord = False
  
  """
  Key variables:
  
  1. lijst -- list of the line (string), split on whitespace characters.
  2. spatiepos -- dictionary with positions of the words in 'lijst' as keys and the number of spaces that originally preceded the word in the line it are recorded as values.
  3. index -- integer variable that keeps track of what word in the line the number of spaces are currently being recorded.
  4. aantal_spaties -- integer variable that keeps track of how many spaces come before a word. Reset to 0 after each word.
  5. woord -- boolean variable that keeps track of whether the for-loop looping through the line by character is currently in a word or not
  
  """

  if line.startswith(" "):
    for character in line:
    """
    For each character in the original line:
    
    1. Check whether it is a space or not;
    2. If it is, set 'Woord' to False;
    3. Increase the number of spaces recorded by 1
    4. If the character is not a space, a word starts:
      - Set word to True
      - Increase the index by 1
      - Add the number of spaces recorded prior to the current word, represented by the index, to the dictionary
      - Reset the 'aantal_spaties' variable to 0.    
    """
      if character != " ":
        if not woord:
          woord = True
          index += 1
          spatiepos[index] = aantal_spaties
          aantal_spaties = 0
      elif character == " ":
        woord = False
        aantal_spaties+=1
  else:
    for character in line:
      if character != " ":
        if not woord:
          woord = True
          index += 1
          spatiepos[index] = aantal_spaties
          aantal_spaties = 0
      elif character == " ":
        woord = False
        aantal_spaties+=1

  """
  If a line ends in a space (i.e. there is a space that is not followed by a word of which the position kan be used as a key), add this final space to the dictionary as well, with a custom key value.
  """

  if re.search(pattern="[^\s] +$",string=line)!=None:
    spatiepos["eindspatie"] = 1
  
  return (lijst,spatiepos)

"""Part 3: Fixes on word-level."""

def hardcoding_op_woordniveau(lijst, wordlist):
  index=0
  for word in lijst:
    """
    Replace the often misrecognized character 'ç' in 'curaçao' or 'Curaçao'.

    Replace the following pattern:
    1. first 'C' or 'c'.
    2. then 'ura'.
    2. then any character.
    3. then 'ao'.
    by part 1, 2 and 4, and in stead of part 3, place a 'ç'.
    """
    word=re.sub(pattern="([Cc]ura).(ao)", repl="\\1ç\\2", string=word)
  
    """Replace the pattern - starts and ends with 'TK' or 'Tk'- by 'Ik'."""
    word=re.sub(pattern="^TK$|^Tk$", repl="Ik", string=word)
    
    lijst[index]=word
    index+=1
  
  return lijst

"""Part 3.1: Recognize compounds and add them to the lexicon."""

def charposition(string, char):

    pos = [] #list to store positions for each 'char' in 'string'
    for n in range(len(string)):
        if string[n] == char:
            pos.append(n)
    return pos

def samenstellingen(lijst,words):
    """Recognize compounds.
    input: 1. 'lijst', containing the line in list format. 2. 'words', containing the lexicon in string format.

    Open a connection with mode 'append' to the lexicon file.
    """
    words_incl_samenstellingen = open("wordlist_aangepast.txt", mode="a")
    """
    #There are four kinds of compounds this algoritm recognizes. All options, numbered 1 to 4, work about the same:
    For every word in the list, do the following:
    1. Check if the word is in the lexicon.
    2. If so, check for every position in the word if the characters before that position form a word in the lexicon and if the characters after that position also form a word in the lexicon.
    3. If so, add the word to the lexicon.
    """
    
    """ OPTION 1: for words without interfix."""
    for word in lijst:
        matches=re.search(pattern=re.escape("\n"+word+"\n"),string=words)
        if matches==None:
            for i in range(3,len(word)):
                samenstelling = [word[:i], word[i:]]
                matches=re.search(pattern=re.escape("\n"+samenstelling[0]+"\n"), string=words)
                matches2=re.search(pattern=re.escape("\n"+samenstelling[1]+"\n"), string=words)
                if matches!=None and matches2!=None:
                        if (len(samenstelling[0])>3 and len(samenstelling[1])>3):
                            words_incl_samenstellingen.write(word+"\n")
                            break
    """ OPTION 2: for words with an 's' as interfix"""
    for word in lijst:
        matches=re.search(pattern=re.escape("\n"+word+"\n"),string=words)
        if matches==None:
            if 's' in word:
                i = charposition(word, 's')
                for n in i:
                    samenstelling = [word[:n], word[n+1:]]
                    #if samenstelling[0] not in words or samenstelling[1] not in words:
                    matches=re.search(pattern=re.escape("\n"+samenstelling[0]+"\n"), string=words)
                    matches2=re.search(pattern=re.escape("\n"+samenstelling[1]+"\n"), string=words)
                    if matches!=None and matches2!=None:
                        if (len(samenstelling[0])>3 and len(samenstelling[1])>3):
                            words_incl_samenstellingen.write(word+"\n")
                            break
    
    """ OPTION 3: for words with an 'e' as interfix"""
    for word in lijst:
        matches=re.search(pattern=re.escape("\n"+word+"\n"),string=words)
        if matches==None:
            if 'e'in word:
                i = charposition(word, 'e')
                for n in i:
                    samenstelling = [word[:n+1] + 'n', word[n+1:]]
                    #if samenstelling[0] not in words or samenstelling[1] not in words:
                    matches=re.search(pattern=re.escape("\n"+samenstelling[0]+"\n"), string=words)
                    matches2=re.search(pattern=re.escape("\n"+samenstelling[1]+"\n"), string=words)
                    if matches!=None and matches2!=None:
                        if (len(samenstelling[0])>3 and len(samenstelling[1])>3):
                            words_incl_samenstellingen.write(word+"\n")
                            break
    
    """ OPTION 2: for words with an 'er' as interfix"""
    for word in lijst:
        matches=re.search(pattern=re.escape("\n"+word+"\n"),string=words)
        if matches==None:
            if 'er' in word:
                i = charposition(word, 'r')
                for n in i:
                    samenstelling = [word[:n-1], word[n+1:]]
                    #if samenstelling[0] not in words or samenstelling[1] not in words:
                    matches=re.search(pattern=re.escape("\n"+samenstelling[0]+"\n"), string=words)
                    matches2=re.search(pattern=re.escape("\n"+samenstelling[1]+"\n"), string=words)
                    if matches!=None and matches2!=None:
                        if (len(samenstelling[0])>3 and len(samenstelling[1])>3):
                            words_incl_samenstellingen.write(word+"\n")
                            break
                    
    
    words_incl_samenstellingen.close()

"""Part 3.2: the language model."""

def check_woorden(lijst, wordlist, woordennaarbertdict, pipeline):
  import re

  """Run all words that are not in the lexicon through the language models.
  input: 
  1. 'lijst', list with on every position a separate word or punctuation mark of the line.
  2. 'wordlist', a string containing the lexicon (supplemented with the found compounds).
  3. 'woordennaarbertdict' (starts empty), a dictionary with in the keys the words that have been processed by the language model and in the values the word that the language model changed these words into.
  4. 'pipeline', an argument the language model needs.
  output: 'lijst' and 'woordennaarbertdict', containing the same as when they were input, but now updated.
  """
  index=0
  for word in lijst:
    """Check if this position in the list contains no punctuation mark."""
    if word not in "-—.,:;!?'()":
      """Check if the word is in the lexicon."""
      if re.search(pattern=re.escape("\n"+word.lower()+"\n"),string=wordlist.lower())==None:
        """Check if the word is in the lexicon when you replace all k's for c's."""
        wordcvoork=re.sub("k", "c", word)
        if "\n"+wordcvoork+"\n" in wordlist:
          word=wordcvoork
          lijst[index]=word
          """Check if the word is not a name (i.e. if the word does not start with an upper case character)."""
        elif not word[0].isupper():
          """
          Check if the word has previously been processed by the language model. (i.e. if the word is already in 'woordennaarbertdict'
          """
          if not word in woordennaarbertdict.keys():
            """If the word has not previously been processed by the language model, create input for the language model"""
            first_words, input_word, last_words=input_voor_bert(index, lijst)
            """Let the word with it's context be processed by the language model."""
            bwio = bert_to_words(first_words, input_word, last_words, pipeline) #NB: pipeline has to be executed separately before running the rest of the script.
            """Add the output to the dictionary with previously processed words."""
            woordennaarbertdict[word]=bwio
            """Insert the corrected word in the right place in the list. """
            lijst[index]=bwio
          else:
            lijst[index]=woordennaarbertdict[word]

    index+=1
  return (lijst, woordennaarbertdict)


def input_voor_bert(index, lijst):
  lijstlengte=len(lijst)
  """Create context for the language model.
  input: 1. 'index', containing the index in the list of the to be corrected word. 2. 'lijst', the list containing the line.
  output: 
  1. 'first_words', string containing the part of the line previous to the to be corrected word.
  2. 'input_word', string containing the to be corrected wordlist.
  3. 'last_words', string containing the part of the line after the to be corrected word.
  """
  #hele regel context
  first_words=" ".join(lijst[0:index])
  input_word=lijst[index]
  last_words=" ".join(lijst[index+1:lijstlengte])
  return (first_words, input_word, last_words)

#This part is for testing the language model apart from the rest of the program:

#zin="Typ hier een zin. Het liefst een beetje een lange"
#lijst=zin.split()
#index=5 #of iets anders dan 5
#first_words, input_word, last_words=input_voor_bert(index, lijst)
#bwio = bert_to_words(first_words, input_word, last_words, pipeline) #vergeet niet pipeline te runnen
#print(bwio)

"""Part 3.2.2: The lexicon-based model."""

def levenshteinDistanceMatrix(token1, token2):
  """Calclulate the distance between the current word from the lexicon and the input word.

  input: 'token1', containing the input word, 'token2', containing the current word from the lexicon.
  output: integer, containing the distance between 'token1' (input word) and 'token2'.

  Calculate the distance by adding up the number of modifications a word needs to become another word. (So the lower the distance, the more similar the word.)
  """
  distances = numpy.zeros((len(token1) + 1, len(token2) + 1))

  for t1 in range(len(token1) + 1):
      distances[t1][0] = t1

  for t2 in range(len(token2) + 1):
      distances[0][t2] = t2
      
  a = 0
  b = 0
  c = 0
  
  for t1 in range(1, len(token1) + 1):
      for t2 in range(1, len(token2) + 1):
          if (token1[t1-1] == token2[t2-1]):
              distances[t1][t2] = distances[t1 - 1][t2 - 1]
          else:
              a = distances[t1][t2 - 1]
              b = distances[t1 - 1][t2]
              c = distances[t1 - 1][t2 - 1]
              
              if (a <= b and a <= c):
                  distances[t1][t2] = a + 1
              elif (b <= a and b <= c):
                  distances[t1][t2] = b + 1
              else:
                  distances[t1][t2] = c + 1

  return distances[len(token1)][len(token2)]

def calcDictDistance(word):
    """Calculate the distance between every word in the lexicon and the input word.
    input: 'word' containing the input word
    output: 'closest_words', containing a list with the top 10 words in the lexicon that are most similar to the input word.
    """
    #file = open('wordlist_na_samenstellingen.txt', 'r') 
    file = open('wordlist_aangepast.txt', 'r') 
    lines = file.readlines() 
    file.close()
    dictWordDist = {}
    
    """For each word in the lexicon, calculate the distance to the input word."""
    for line in lines:
        wordDistance = levenshteinDistanceMatrix(word, line.strip())
        dictWordDist[line.strip()] = wordDistance

        
    dictWordDist = {k: v for k, v in sorted(dictWordDist.items(), key=lambda item: item[1])}
    
    dict_items = dictWordDist.keys()
    
    closest_words = list(dict_items)[:10]
    return (closest_words)

"""Part 3.2.1: The context-based model."""

def bert_to_words(first_words, input_word, last_words, pipeline):
  """  Run the language models.
  input:
  1. 'first_words', string containing the part of the line previous to the to be corrected word.
  2. 'input_word', string containing the to be corrected wordlist.
  3. 'last_words', string containing the part of the line after the to be corrected word.
  output: 
  1. 'best_word', if the language model succeeded in finding a better word. 'input_word', if the language model has not found a better fit.
  
  Key variables:
  'best_words_in_order' -- list containing the best fitting words in order of best fit according to the context-based model.
  'lev_dis' -- list containing the most similar words in order of similarity according to the lexicon-based model.

  Bring context in the appropriate format."""
  seq = format(first_words + " " + "<mask>" + " " + last_words)
  """Call the pipeline. (i.e. run the context based language model)."""
  output = pipeline(seq)
  best_words_in_order = []
  i = 0 
  """Append the most likely matches to the list with best fitting words according to the context-based model."""
  for entry in output:
    best_words_in_order.append(entry["token_str"])
    i += 1
  
  """Run the lexicon-based model."""
  lev_dis = calcDictDistance(input_word)

  """Check if there's a match in the lists with best fitting words according to each model. If so, return this match as the new, corrected word."""
  for i in best_words_in_order:
    for j in lev_dis:
      if i.strip() == j.strip():
        best_word = i
        return best_word
  
  """When there's no match between the lists with best fitting words according to each model, return the original word."""
  return input_word 


"""Part 4: reconstruction of original sentence format."""

"""Convert the list containing the line to a string again, with white spaces in the original positions in the string.
input: 
1. 'lijst', list containing the line. 
2. 'spatiepos' dictionary with on every position of the list the number of spaces that needs to be placed back.
output:
1. 'line', string containing the line.
"""
def zet_spaties_terug(lijst,spatiepos):
  line=""
  for key,value in spatiepos.items():
    if key != "eindspatie":
      line += value*" "+lijst[int(key)-1]
    else:
      line += " "
  
  return (line)

"""Remove the excessive spaces around the punctuation marks."""
def plak_leestekens(line):
  line = re.sub(pattern=" ([-—.,:;!\?'\(\)]) ",repl="\\1",string=line)
  return(line)
  
if __name__== "__main__":  
  """Part 0: The overarching function."""

  """Add names and numbers to the lexicon."""
  #This function is executed only once.
  cijfers_en_namen_toevoegen()

  """Open a (readable) connection to a text file with on every line the file name of a text you want to process."""
  boekenlijst = open("boeknamen.txt","rt")

  """For every text, run the entire algorithm."""
  for titel in boekenlijst:
    titel = titel.strip()

    paginanummers_fixen_en_verwijderen(titel)

    #Opent benodigde bestanden:
    test = open("beter.txt","rt")
    klaar = open(file=(titel+"_verbeterd.txt"),mode="wt")
    wordlist = open("wordlist_aangepast.txt", "r").read()
    #vreemde_talen = open("vreemde_talen_verminderd.txt","r").read()

    #Starting variables:
    regelafbraak=False
    deel1=""
    deel1vanwoord=""
    paginanummereind=False
    woordennaarbertdict={}

    #Correct texts line by line:
    for line in test:
      #1. Fix words consisting of loose letters ('c h i l d' becomes'child').
      line = spatieoplossing(line)

      #2.0 Repair words that have been split in twain by end of line hyphenation. ('sep-\narate' becomes '\nseparate').
      line,deel1,regelafbraak = verwijder_regelafbrekingen(line,deel1,regelafbraak)
      #2.1 Repair words that have been split in twain by a page number at the end of a line. ('sep44\narate' becomes '\nseparate').
      line,deel1vanwoord,paginanummereind=fix_paginanummers_eindvdzin(line, deel1vanwoord, paginanummereind)
    
      #3. Put spaces between words and punctuation marks, so that every word can be found in the lexicon ('dog.' becomes 'dog . ').
      #3.1. Repairs frequently misread quotation marks. ('Hallo?/ becomes 'Hallo?').
      line = leestekens_losmaken(line, wordlist)

      #3.2 Fix loose first letters, like in 'l etter'.
      line=losse_beginletter_fixen(line, wordlist)

      #4. Turn the string with the line into a list with on every position a word. Store the position of the spaces in 'spatiepos'.
      lijst,spatiepos = neem_spatieposities(line)

      #4.1. Do some hardcoding on frequent mistakes.
      lijst = hardcoding_op_woordniveau(lijst, wordlist)

      #5. Check if a word that's not in the lexicon is actually a compound. If so, add it to the lexicon.
      samenstellingen(lijst,wordlist)

      #Re-open the wordlist after adding compounds in the last function.
      wordlist = open("wordlist_aangepast.txt", "r").read()  
      
      #6. Run words that are not in the lexicon through the the language models.
      lijst,woordennaarbertdict = check_woorden(lijst,wordlist,woordennaarbertdict,pipeline)

      #7. Turn the list into a string and restore spacing.
      line = zet_spaties_terug(lijst,spatiepos)

      #8. Remove excessive spacing around punctuation marks.
      line = plak_leestekens(line)

      klaar.write(line+"\n")

    test.close()
    klaar.close()