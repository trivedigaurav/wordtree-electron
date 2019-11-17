import re
import os, getopt, sys
import json

debug = False

def doSplit(root, inFile="docList.txt"):
    global debug

    if (not root):
        # print "Error: No root word provided!"
        return

    f = open(inFile, "rb")
    try:
        filelist = f.readlines()
    finally:
        f.close()
    
    total = len(filelist)
    # print "Searching for", '"'+root+'"', "in" , total, "files." 
 
    phrases = []

    count = 0
    docid = 0
    sentenceid = 0

    for filename in filelist:

        # print filename
        filename = os.path.abspath(filename.rstrip("\r\n"))
        # print filename

        f = open(filename, 'r')
        try:
            docid += 1

            report = f.read()
            report = report.replace("\r\n", "\n")
            regex = r"([^.:]*?"+root+"[^.\n]*\.)"

            matches = re.findall(regex, report)
            numfound = len(matches)

            if(numfound):
                count += 1

            # TODO: calculate TF-IDF
            for match in matches:
                sentenceid += 1
                phrases.append({"doc": docid, "id": sentenceid, "sentence": match})
        finally:
            f.close()
          
    
    # print phrases

    tree = []
    for key in phrases:
        p = key['sentence']
        p = p.replace("\' s", "'s")
        p = p.replace("\n", " ")
        p = p.strip(' \t\n')
        
        if (p[-1] == "."):
            p = p[:-1]
        
        left = re.findall(r"[\w']+|[.,!?;]", p[:p.rfind(root)].strip())
        right = re.findall(r"[\w']+|[.,!?;]", p[p.rfind(root)+len(root):].strip())

        tree.append({"left": left, "right": right, "doc": key["doc"], "id": key["id"]})

    # if(debug):
        # for node in tree:
            # print node['left'], "-", root, "-", node['right']

    # print "Documents included: ", count, "/", total, "(", round(100.0 * count / total, 2), "% )"

    return (tree,count,total)

def prepareData(tree, root, matches, total):
    global debug
    
    # if (tree == []):
    #     print "Warning: Empty tree!"

    data = {}
    
    data['matches'] = matches
    data['total'] = total

    data['query'] = root

    data['lefts'] = []

    for node in tree:
        printnode = node.copy()
        printnode.pop("right")
        printnode["sentence"] = printnode.pop("left")
        data['lefts'].append(printnode)


    data['rights'] = []


    for node in tree:
        printnode = node.copy()
        printnode.pop("left")
        printnode["sentence"] = printnode.pop("right")
        data['rights'].append(printnode)


    return data

def writeFile(data, prefix, outFile="sample"):

    global debug
    
    print json.dumps(data)

    sys.stdout.flush()


def main(argv):
    global debug

    usage = sys.argv[0] + ' -w <word-root> [-i <docList.txt>] [-o <outfile>]'
    root = None
    outFile = None
    inFile = "docList.txt"

    try:
        opts, args = getopt.getopt(argv, "hdi:w:o:", ["ifile"])
    except getopt.GetoptError:
        print usage
        sys.exit(2)
    for opt, arg in opts:
        if opt in ["-h", "--help"]:
            print usage
            sys.exit(0)
        elif opt in ("-i", "--infile"):
            inFile = os.path.abspath(arg)
        elif opt in ("-w", "--word"):
            root = arg
        elif opt in ("-d", "--debug"):
            debug = True
        elif opt in ("-o", "--outfile"):
            outFile = arg

    if (not root or not inFile):
        print usage
        sys.exit(2)

    if (not outFile):
        outFile = root

    (tree,matches,total) = doSplit(root=root, 
                                inFile=inFile)

    data = prepareData(tree=tree,
                    root=root,
                    matches=matches,
                    total=total)

    writeFile(data=data,
            prefix="tree",
            outFile=outFile)

#This is for standalone execution
if __name__ == "__main__":
    main(sys.argv[1:])