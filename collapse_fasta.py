import sys
import collections
import gzip


class Fasta:
    def __init__(self, fasta, ftype='None'):
        self.source = fasta
        self.ftype = ftype

    def __str__(self):
        return "Fasta object:" + self.source

    @staticmethod
    def openfile(filename):
        if filename.endswith(".gz"):
            return gzip.open(filename, 'rt', encoding='utf-8')
        else:
            return open(filename, 'r')

    @staticmethod
    def export(header,seq,type):
        if type == 'None':
            return header + "\n" + seq
        elif type == 't':
            return header.lstrip(">") + "\t" + seq

    def __iter__(self):
        with self.openfile(self.source) as FH:
            header = ''
            seq = ''
            for line in FH:
                line = line.rstrip("\r\n")
                if line.startswith(">"):
                    if header:
                        yield self.export(header,seq,self.ftype)
                    seq = ''
                    header = line
                else:
                    seq += line
            yield self.export(header, seq, self.ftype)


file = "D:/Python_script/NGS_tools/mature.fa.gz"
Fa = Fasta(file)
Fa.ftype='t'
tags = [tag for tag in Fa]




def collapse():
    text = collections.defaultdict(int)
    for line in sys.stdin:
        if line.startswith(">"):
            continue
        else:
            text[line.rstrip()] += 1
    num = 0
    for seq, time in text.items():
        print(">" + str(num) + "-" + str(time) + "\n" + eval(seq))
        num += 1


def decollapse():
    pass


collapse()
