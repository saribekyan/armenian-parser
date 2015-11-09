#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import xml.etree.ElementTree as ET

import cPickle as pickle

arm_alpha = set(u'աբգդեզէըթժիլխծկհձղճմյնշոչպջռսվտրցուփքևօֆԱԲԳԴԵԶԷԸԹԺԻԼԽԾԿԽՁՂՃՄՅՆՇՈՉՊՋՌՍՎՏՐՑՈՒՓՔԵՎՕՖ -')

def is_armenian(s):
    for ch in s:
        if ch not in arm_alpha:
            return False
    return True

def extract_translation(text):
    trans = 0
    in_trans = False

    translations = { }
    for line in text.split('\n'):
        if line == '{{translation-top}}':
            if trans > 0:
                return { }
            trans += 1

            in_trans = True

        elif line == '{{translation-bot}}':
            in_trans = False
        elif in_trans:
            tokens = line[3:-2].split('|')
            if len(tokens) > 1:# and tokens[1] != '':
                translations[tokens[0]] = tokens[1:]

    return translations

def main(path, dict_path):
    tree = ET.parse(path)
    root = tree.getroot()

    page_tag  = '{http://www.mediawiki.org/xml/export-0.10/}page'
    title_tag = '{http://www.mediawiki.org/xml/export-0.10/}title'
    revision_tag = '{http://www.mediawiki.org/xml/export-0.10/}revision'
    text_tag = '{http://www.mediawiki.org/xml/export-0.10/}text'

    dictionary = { }

    for page in root.findall(page_tag):
        title = page.find(title_tag).text
        if is_armenian(title):
            revision = page.find(revision_tag)
            text = revision.find(text_tag).text

            if 'translation' in text:
                translation = extract_translation(text)
                if len(translation) > 0:
                    dictionary[title] = translation

    pickle.dump(dictionary, open(dict_path, 'wb'))
    
    return dictionary

if __name__ == '__main__':

    if len(sys.argv) != 3:
        print 'Usage: python generate_dictionary.py path/to/wiktionary_dump.xml path/to/dict/output.npy'
        sys.exit(1)

    path = sys.argv[1]
    dict_path = sys.argv[2]

    main(path, dict_path)
