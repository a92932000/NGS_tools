import gzip
import sys
import re
def main(file=None):
    fq2fa(file)


def fq2fa(file=None):
    if file == None :
        file = "sra_data.fastq.gz"

    if file.endswith(".gz") :
        f = gzip.open(file, 'rt',encoding='utf-8')
    else:
        f = open(file, 'rb')
    line_num = 0
    content = []
    for line in f:
        line_num += 1
        content.append((line.rstrip()) )
        if (line_num % 4 == 0):
            print( re.sub("^@",">", "\n".join(content[0:2])))
            content = []
        if (line_num == 8):
            break
    f.close()


if __name__ == '__main__':
    main()