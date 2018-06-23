import sqlite3
import gzip
import re


class DNA:
    def __init__(self, id, description, seq):
        self.id = id
        self.description = description
        self.seq = seq

    def __repr__(self):
        return '>%s %s\n%s' % (self.id, self.description, self.seq)

    def __str__(self):
        return '>%s %s\n%s' % (self.id, self.description, self.seq)

    def data(self, type='fasta'):
        if type == 'fasta':
            return '>%s %s\n%s' % (self.id, self.description, self.seq)
        elif type == 'tab':
            return '>%s\t%s\t%s' % (self.id, self.description, self.seq)


class Fasta:
    def __init__(self, File):
        self.filePath = File

    def __str__(self):
        return self.filePath

    def __repr__(self):
        return self.filePath

    @staticmethod
    def openfile(file):
        if file.endswith(".gz"):
            return gzip.open(file, "rt")
        else:
            return open(file, "rt")

    def __iter__(self):
        id, description, seq = '', '', ''
        header = re.compile('>(\S+)\s*(.*)')
        with self.openfile(self.filePath) as FH:
            for line in FH:
                line = line.rstrip("\n\r")
                if line.startswith(">"):
                    if seq: yield DNA(id, description, seq)
                    tag = header.search(line)
                    id = tag.group(1)
                    description = tag.group(2)
                    seq = ''
                else:
                    seq += line
            yield DNA(id, description, seq)

def main():
    filePath = "mature.fa.gz"
    Faiter = Fasta(filePath)
    recode = ((x.id, x.description, x.seq) for x in Faiter)

    # connection "memory" sqlite3 database for test.
    connection = sqlite3.connect(':memory:')

    # build cursor
    cursor = connection.cursor()

    # create table miRbase which contain two columns id and sequence
    cursor.execute('CREATE TABLE miRbase(id, description, sequence)')

    # input list of tuple values to miRbase
    cursor.executemany('INSERT INTO miRbase VALUES (?,?,?)', recode)


    # python sqlit3 don't have complete regex search function
    # create REGEXP for regex search
    def regexp(expr, item):
        reg = re.compile(expr)
        return reg.search(item) is not None


    # Custom function link to database
    connection.create_function("REGEXP", 2, regexp)

    # create index of database for speed up search
    cursor.execute('CREATE UNIQUE INDEX miRNA_id_index on miRbase (id)')

    # search data by LIKE
    for row in cursor.execute("SELECT * FROM miRbase WHERE id LIKE '%s'" % "%-miR477%"):
        print(*row, sep="\t")

    # search data by REGEXP
    # iter results from cursor
    for row in cursor.execute("SELECT * FROM miRbase WHERE id REGEXP '%s'" % '.*-miR477.*'):
        print(*row, sep="\t")

    cursor.execute("SELECT * FROM miRbase WHERE id REGEXP ?", ['^sly-miR477'])
    # fetch all result from cursor
    result = cursor.fetchall()
    print(*result, sep="\n")

    # search and substring sequence
    cursor.execute("SELECT id, substr(sequence,?,?) FROM miRbase WHERE id REGEXP ?", [1, 3, '^sly-miR477'])
    # cursor.execute("SELECT id, substr(sequence,1,3) FROM miRbase WHERE id REGEXP '^sly-miR477'")
    resultSubstr = cursor.fetchall()
    print(*resultSubstr, sep="\n")

    for x in resultSubstr: print(*x, sep="\t")

    # close database
    connection.close()
