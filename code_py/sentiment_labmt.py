# -*- coding: utf-8 -*-
"""

@author: kln
"""
import pandas as pd
### import labMT's dictionary from PLOSOne
url = 'http://www.plosone.org/article/fetchSingleRepresentation.action?uri=info:doi/10.1371/journal.pone.0026752.s001'
labmt = pd.read_csv(url, skiprows=2, sep='\t', index_col=0)
# raw scores
dictionary = labmt.happiness_average.to_dict()
# zero center
labmtbar = labmt.happiness_average.mean()
dictionary_0 = (labmt.happiness_average - labmtbar).to_dict()
# function for string input
def sent_scr(string):
    tokens = string.split()
    return sum([dictionary_0.get(token.lower(), 0.0) for token in tokens]) / len(tokens)
    #return sum([dictionary.get(token.lower(), 0.0) for token in tokens]) / len(tokens)# for comparison

### example
#sent_scr('nigger')
print sent_scr('some hate')
#sent_scr('some love and some hate')
## bag of words problem
#sent_scr('love to hate') == sent_scr('hate to love')
