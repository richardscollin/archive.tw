#!/usr/bin/env python3
# %%
import os,sys,csv,itertools
import pandas as pd
from typing import List,Tuple,Iterable
from xml.etree import ElementTree
from collections import Counter, namedtuple

Row = namedtuple('Row', ['input', 'output'])
# %%
def get_transcript(tree: ElementTree, target_speaker: str):
    # fold text in different speech nodes by the same target_speaker
    speeches = [(k,list(v)) for k,v in itertools.groupby(tree.findall('.//speech'), key=lambda e: e.attrib['by'])]

    result = []
    for (g1, g2) in zip(speeches[:-1], speeches[1:]):
        if g2[0] == target_speaker:
            input  = " ".join([(e.find('p').text or "").strip() for e in g1[1]])
            output = " ".join([(e.find('p').text or "").strip() for e in g2[1]])
            if len(output.split()) <= 4000 and len(input.split()) <= 1500:
                row = Row(input, output)
                result.append(row)
    return result

#%%
xml_files = sorted(filter(lambda fn: fn.endswith("an.xml"), os.listdir()))
# %%
transcripts = []
for fn in xml_files:
    tree = ElementTree.parse(fn)

    # '#唐鳳'
    transcript = get_transcript(tree, "#Audrey Tang")
    transcripts.extend(transcript)
transcripts = transcripts[:24000]

# %%
df = pd.DataFrame(transcripts, columns=["input", "output"])
df.to_csv("transcripts.csv", encoding='utf-8', index=False)
print(f"Wrote {len(transcripts)} records to transcripts.csv.")
# %%
