#!/usr/bin/python3
import glob
import re
import time
import pprint
import collections
import functools

S_time = time.time()


def parse_GFF(file):
    # Data_dict = {}
    Data_dict = collections.defaultdict(list)
    with open(file) as FH:
        line_num = 0
        for line in FH:
            line_num += 1
            if re.search("^#", line):
                continue
            else:
                line = line.rstrip("\r\n")
                [chr, source, type, start, end, undef, strand, undef, info] = re.split("\t", line)
                if type == "chromosome":
                    continue
                # elif line_num == 500:
                #     break
                elif type not in ["gene", "protein"]:
                    if re.search("ID=", line):
                        ID = parse_GFF_info(info)['ID']
                        Data_dict[ID] = collections.defaultdict(list)
                        Data_dict[ID][type].append([chr, start, end, strand])
                        # Data_dict[ID]={type:[chr, start, end, strand]}
                    else:
                        Parent = parse_GFF_info(info)['Parent']

                        # if type in list(Data_dict[Parent].keys()):
                        Data_dict[Parent][type].append([chr, start, end, strand])
                        # else:
                        #    Data_dict[Parent].update({type: [[chr, start, end, strand]]})

    return (Data_dict)


def parse_GFF_info(text):
    info = re.split(";|=", text)
    info_dict = {}
    # info_dict = dict(zip(info[0::2], info[1::2]))
    info_dict = dict(item.split("=") for item in text.rstrip(";").split(";") if len(text) > 0)
    try:
        # info_dict['Parent'] = re.split(",",info_dict['Parent'])
        info_dict['Parent'] = re.sub("^(.+),.+", "\\1", info_dict['Parent'])
    except:
        None
    return (info_dict)


GFF_File = "TAIR10_GFF3_genes_transposons.gff"
Data_GFF = parse_GFF(GFF_File)


def split_text():
    info_dict = dict()
    text = "name1=value1;name2=value2"
    text = ""
    info_dict = dict(item.split("=") for item in text.split(";") if len(text) > 0)
    return (info_dict)


# pprint.pprint( Data_GFF )
print("Run time : %d sec" % (time.time() - S_time))


def sum(x):
    return (functools.reduce(lambda i, j: i + j, x))
