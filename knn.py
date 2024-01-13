from datasets import load_dataset
import gzip
import math 

dataset = load_dataset("ag_news")

def compress(x, mem):
    if (x in mem):
        return mem[x] 
    mem[x] = len(gzip.compress(x.encode())) 
    return mem[x]

def distance(x1,x2,mem={}):
    cx1 = compress(x1, mem)  
    cx2 = compress(x2, mem)
    x1x2 = x1 + " " + x2 
    cx1x2 = compress(x1x2, mem)

    mn = min(cx1, cx2)
    mx = max(cx1, cx2) 

    return (cx1x2 - mn)/mx; 

mem = {} 
class_labels = ["world", "sports", "business", "sci/tech"]
for test in dataset["test"]:
    test_text = test["text"]
    overall_min = math.inf; 
    klass = -1

    for train in dataset["train"]:
        train_text = train["text"]         
        dist = distance(test_text, train_text, mem) 
        if (overall_min > dist):
            klass = train["label"] 
            overall_min = dist 

    print(test_text, " is: ", class_labels[klass], "\tactual: ", class_labels[test["label"]])

        