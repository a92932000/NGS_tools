import pandas as pd
import numpy as np
import time
from itertools import chain
import timeit
def parseGFFAttributes(attributeString):
    # Parse the GFF3 attribute column and return a dict
    if attributeString == ".": return {}
    res = dict([x.split("=") for x in attributeString.split(";") if len(x) > 0])
    return res


def parseGFF(gffFile):
    # Parse GFF3, and return pd.data.frame
    gff_df = pd.read_csv(gffFile, sep="\t",
                         names=["seqid", "source", "type", "start", "end", "score", "strand", "phase", "attributes"])
    gff_df["attributes"] = gff_df["attributes"].apply(parseGFFAttributes)
    gff_df = pd.concat([gff_df.drop(['attributes'], axis=1), pd.DataFrame(gff_df["attributes"].tolist())], axis=1)
    return gff_df


def main():
    S_time = time.time()
    gffFilePath = "TAIR10_GFF3_genes_transposons.gff"
    parseGFF(gffFilePath)
    print("Run time : %d sec" % (time.time() - S_time))


if __name__ == '__main__':
    main()


def overlap(range, range2):
    return (range[0] <= range2[1]) & (range[1] >= range2[0])

A = [1, 3]
B = [2, 5]
overlap(B, A)


def aligner(GrangeX, GrangeY, startX='start', endX='end', startY='start', endY='end'):
    GrangeX = GrangeX.rename(columns={startX: 'start_X', endX: 'end_X'})
    GrangeY = GrangeY.rename(columns={startX: 'start_Y', endX: 'end_Y'})
    cat = pd.DataFrame.merge(GrangeX, GrangeY, how='left',on='seqid')
    overlap = (cat.start_X <= cat.start_Y) & (cat.end_X >= cat.end_Y)
    return cat[overlap].reset_index().drop('index',axis=1)


Feature = pd.DataFrame({
    'seqid': ['chr1', 'chr2', 'chr3', 'chr4'],
    'start': [1, 100, 500, 1000],
    'end': [50, 200, 700, 1600],
    'type': ['Exon'] * 4})

Grange = pd.DataFrame({
    'seqid': ['chr1', 'chr2', 'chr3', 'chr4']*2,
    'start': [10, 50, 500, 1000]*2,
    'end': [30, 60, 510, 1100]*2,
    'type': ['Exon'] * 4 *2})

# aligner(Feature, Grange)

olpRef = [Feature.seqid == x for x in Grange.seqid]
olpS = [Feature.start <= x for x in Grange.start ]
olpE = [Feature.end >= x for x in Grange.end]
olp = [x&y&z for x,y,z in zip(olpRef, olpS , olpE)]

df_list=[ pd.DataFrame.merge(Feature[F],Grange.loc[G:G],on=['seqid']) for F in olp if F.any() for G in Grange.index]
concatDF(df_list)

def concatDF(dflist):
    return pd.concat(dflist)

def dictcatDF(dflist):
    COLUMN_NAMES = dflist[0].columns
    df_dict = dict.fromkeys(COLUMN_NAMES, [])
    def fast_flatten(input_list):
        return list(chain.from_iterable(input_list))
    for col in COLUMN_NAMES:
        # Use a generator to save memory
        extracted = (df[col] for df in df_list)
        # Flatten and save to df_dict
        df_dict[col] = fast_flatten(extracted)

    return pd.DataFrame.from_dict(df_dict)[COLUMN_NAMES]

concatDF(df_list)
print('test_gen_time() takes {0} sec'
          .format(timeit.timeit(concatDF(df_list), number=1)))