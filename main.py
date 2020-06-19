from openpyxl import load_workbook
from collections import OrderedDict

import pandas as pd
import math
def normalForm(tree, rule=''):
    rules = []
    for node in tree:
        if isinstance(node, str):
            rule += node + ','
        else:
            rules += normalForm(node, rule)
    if rules:
        return rules
    return [rule]

a=pd.ExcelFile("Test.xlsx")
df = a.parse(a.sheet_names[0], skiprows=0, index_col=None, na_values=['None'])
data_dict = df.to_dict()
table={}
for i,k in data_dict.items():
    table[i]=list(k.values())


#delete not unique values
def deleteTrash(li):
    return list(OrderedDict.fromkeys(li))

def count(table,col,el):
    return table[col].count(el)

def entropy(table,rescol):
    s=0
    for v in deleteTrash(table[rescol]):
        p = count(table, rescol, v) / float(len(table[rescol]))

        s += p * math.log(p)

    return -s


def delValues(t, ind):

    return {k: [v[i] for i in range(len(v)) if i in ind] for k, v in t.items()}

def getIndexes(table, col, v):

    li = []
    start = 0
    for row in table[col]:
        if row == v:
            index = table[col].index(row, start)
            li.append(index)
            start = index + 1
    return li


def getSubtables(t,col):
    print("Subtables",col)
    delDup= deleteTrash(t[col])
    print(delDup)
    a = [delValues(t, getIndexes(t, col, v)) for v in delDup]
    print(a)
    return a



def entropyA(table,col,rescol):
    s = 0  # sum
    for subt in getSubtables(table, col):
        s += (float(len(subt[col])) / len(table[col])) * entropy(subt, rescol)
    print(s)
    return s


def gain(table,x,rescol):
    print("gain",x)
    res=(entropy(table,rescol)-entropyA(table,x,rescol))
    print("Res: ",res,"Attribute: ",x)
    return res

def checkResultStudy(t):

    for i in t:
        if i != t[0]:
            return False
    return True

def createTree(table, result):
    col = max([(k, gain(table, k, result)) for k in table.keys() if k != result],
              key=lambda x: x[1])[0]
    print("COL: ",col)
    tree=[]
    for subt in getSubtables(table, col):
        v = subt[col][0]
        print(v,"CreateTree V")
        print(subt,"CreateTree subT",result)
        if checkResultStudy(subt[result]):
            tree.append(['%s=%s' % (col, v),
                         '%s=%s' % (result, subt[result][0])])
            print(normalForm(tree), " IF")
        else:
            print(subt, "BEFORE SUBTABLE")
            del subt[col]
            print(subt,"SUBTABLE")
            tree.append(['%s=%s' % (col, v)] + createTree(subt, result))
            print(normalForm(tree)," ELSE")

    return tree

a=createTree(table,"Play")
b=normalForm(a)
print(a)
