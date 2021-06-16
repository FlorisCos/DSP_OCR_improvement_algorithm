# Dutch OCR post-correction

In the python script OCRpostcorrection_script.py you will find an algorithm that identifies and repairs mistakes in Dutch OCR constructed texts. We used a combination of a lexicon-based model and a context-based model, together with some hard coding. A complete explanation of our code and our project as well as an evaluation of the performance of our algorithm are in the ‘DSP_OCR_finalreport.pdf’ file.

## When to use this script?
Our code is based on common OCR mistakes we identified by hand in some Dutch novels from the 1960’s. Other OCR methods may lead to other kinds of mistakes. Therefore, it is inadvisable to use our code blindly, without checking the kind of errors your OCR has made. The method we used could still be an inspiration and parts of our code could be copied, but it would be wise to use a tailor-made version of our code, specific to the kinds of mistakes the used OCR method makes.

## User guide

### Input materials:
All input materials need to be uploaded to the virtual environment folder.
All text files should be coded in UTF-8.

1. One .txt file containing the exact file names of all the texts you want to process, each file name on a new line. The file should be named ‘boeknamen.txt’.
2. All texts you want to process, in .txt format.
3. A Dutch lexicon or word list in .txt format. Each word should be on a new line. The file should be named ‘wordlist.txt’. We used https://github.com/OpenTaal/opentaal-wordlist ourselves.
4. A .txt file with (proper) names that (often) occur in your texts, each name on a new line. You’ll have to construct this file yourself, tailor-made for your texts. The file should be named ‘naamsvariantend.txt’. A list of names must be included to make sure character names will not be changed erroneously.
5. The .py file containing the algorithm ‘OCRpostcorrection_script.py’.
6. A shell script executing the python script (not required, but strongly advised because of long running times).

### Required packages:
- torch
- Flax
- TensorFlow (version 2.0 or higher)
- transformers
- scipy
- (re and numpy are imported when the script is run)

### Output:
For each file you process, the algorithm outputs a corrected file with the old file name followed by ‘_verbeterd.txt’.

### Road map:
1. Install all needed packages.
2. Run the script or when you use a shell script, run the shell script.

### Pipeline:

![Pipeline](/Users/floriscos/Documents/Universiteit/pipeline.png)
