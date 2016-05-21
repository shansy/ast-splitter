# -*- coding: utf-8 -*-
import string
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
import math
import re

word_re = re.compile(u'([a-z0-9\\-öβüä]*)', re.I)
def process(text, pref_tree, suff_tree, comp_list, all_words):
    splits = []
    tokens = word_re.findall(text.lower())
    count_splitted = 0.0
    count_long = 0.0
    done = []
    done_split = []
    for split in tokens[:]:
        if len(split) > 3:
            count_long = count_long + 1

        if split in done:
            if split in done_split:
                count_splitted = count_splitted + 1
        else:
            word_p = split.lower()
            word_s = word_p[::-1]

            done.append(word_p)

            previous_p = float("inf")
            previous_s = 0.0
            max_measure = 0.0

            best_pref = word_p
            best_suff = u''
            suff_index = 0
            if len(word_p) >= 8:
                    pref_tree.add(word_p[::-1])
                    suff_tree.add(word_s)

                    prefixes = [word_p[i+3::-1] for i in range(len(word_p)-7)]
                    suffixes = [word_s[i+3::-1] for i in range(len(word_s)-7)]
                    suffixes = suffixes[::-1] 

                    for p in prefixes:

                        s = suffixes[suff_index]
                        suff_index = suff_index + 1

                        freq_p = 0.0
                        freq_s = 0.0

                        if len(pref_tree.search(p+u'$')) == len(p+u'$'):
                            freq_p = pref_tree.search(p+u'$')[-1].freq

                        if len(suff_tree.search(s+u'$')) == len(s+u'$'):
                            freq_s = suff_tree.search(s+u'$')[-1].freq

                        if freq_p > previous_p or freq_s < previous_s:
                            continue
                        else:
                            previous_p = freq_p
                            previous_s = freq_s

                            len_measure = abs(1-len(p)/len(s)) + 1
                            freq_measure = math.sqrt(freq_p * freq_s)
                            current_measure = freq_measure/len_measure

                            if current_measure > max_measure:
                                best_pref = p[::-1]
                                best_suff = s[::]
                                max_measure = current_measure

            if not best_suff in all_words:
                best_pref = word_p
                best_suff = u''

            if len(best_pref) < len(word_p):

                if best_suff[0] == u's' and best_pref[-1] == u'g':
                    best_suff = best_suff[1:]
                else:
                    if (best_suff[0] == u'n' or best_suff[0] == u'r') and best_pref[-1] == u'e':
                        best_suff = best_suff[1:]
                if not best_suff in all_words:
                    best_pref = word_p
                    best_suff = u''
                    if len(word_p) >= 15:
                        count_splitted = count_splitted + 1
                        done_split.append(word_p)
                else:
                    count_splitted = count_splitted + 1
                    done_split.append(word_p)
                    splits.append({ 'full': word_p[0].upper() + word_p[1:], 'prefix': best_pref[0].upper() + best_pref[1:], 'suffix': best_suff[0].upper() + best_suff[1:] })

    if count_long < 70:
        style = 'undefined (the text is too short)'

    else:
        percent = count_splitted/count_long
        style = 'formal'
        if percent < 0.06:
            style = 'informal'

    return {
        'splits': splits,
        'style': style
    }
