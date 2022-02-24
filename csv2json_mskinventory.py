#!/usr/bin/python
import csv
import json
import re
import sys, getopt


def main(argv):
    inputfile = None
    outputfile = None
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('convert_to_json.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('convert_to_json.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    print('Input file  : ', inputfile)
    print('Output file : ', outputfile)
    if inputfile is None:
        print('convert_to_json.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    make_json(inputfile, outputfile)


def make_json(csvFilePath, jsonFilePath):
    data = {}
    starttblstr = "[{"
    endtblstr = "}]"
    startcolstr = "\"columns\": ["
    endcolstr = "]"
    tabstr = None
    colstr = None
    colString = None
    fullcolstr = startcolstr
    finaljsonstr = None
    firstcolinlist = 0

    # Open a csv reader called DictReader
    with open(csvFilePath, encoding='utf-8') as csvf:
        i = 0
        writefile = 0
        prevtab = None
        nexttab = None
        for rows in csvf:
            if i > 0:
                rowarr = rows.split(",")

                if i == 1:
                    table_name = rowarr[2]
                    prevtab = table_name
                    nexttab = table_name
                    tabstr = starttblstr + '"tableName": "{}",'.format(table_name)
                    jsonFilePath = "{}.json".format(table_name)
                elif i > 1:
                    table_name = rowarr[2]
                    nexttab = table_name
                    #print("prevtab:{}, nexttab:{}".format(prevtab, nexttab))
                    if prevtab != nexttab:
                        finaljsonstr = "{} {} {} {}".format(tabstr, fullcolstr, endcolstr, endtblstr)
                        #print(finaljsonstr)
                        json_object = json.loads(finaljsonstr)
                        with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
                             #print(json.dumps(json_object, indent=4, sort_keys=True))
                             jsonf.write(json.dumps(json_object, indent=4))

                        prevtab = nexttab
                        tabstr = starttblstr + '"tableName": "{}",'.format(table_name)
                        jsonFilePath = "{}.json".format(table_name)
                        firstcolinlist = 0
                        fullcolstr = startcolstr


                if rowarr[3] == 'PK IX':
                    writefile = 1
                    columnName = rowarr[5]
                    data_type = rowarr[6]
                    dataType = data_type.split(" ")[0]
                    pattern = ".*\((.*?)\)"
                    dataSize = re.search(pattern, data_type).group(1)
                    colString = '{{"columnName": "{}", "dataType": "{}", "length": {}}}'.format(
                        columnName, dataType, dataSize)
                    if firstcolinlist == 0:
                        fullcolstr = "{}{}".format(fullcolstr, colString)
                        firstcolinlist = 1
                    else:
                        fullcolstr = "{},{}".format(fullcolstr, colString)
                else:
                    if rowarr[8] != '-':
                        writefile = 1
                        columnName = rowarr[5]
                        data_type = rowarr[6]
                        dataType = data_type.split(" ")[0]
                        pattern = ".*\((.*?)\)"
                        dataSize = re.search(pattern, data_type).group(1)
                        algoName = rowarr[8]
                        colString = '{{"columnName": "{}", "dataType": "{}", "length": {}, "algorithmInstanceName": "{}"}}'.format(
                            columnName, dataType, dataSize, algoName)

                        if firstcolinlist == 0:
                            fullcolstr = "{}{}".format(fullcolstr, colString)
                            firstcolinlist = 1
                        else:
                            fullcolstr = "{},{}".format(fullcolstr, colString)

            i = i + 1

        if writefile == 1:
            finaljsonstr = "{} {} {} {}".format(tabstr, fullcolstr, endcolstr, endtblstr)
            #print(finaljsonstr)
            json_object = json.loads(finaljsonstr)
            with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
                #print(json.dumps(json_object, indent=4, sort_keys=True))
                jsonf.write(json.dumps(json_object, indent=4))

if __name__ == "__main__":
    main(sys.argv[1:])

# csvFilePath = r'ALFA_Inventories/ALFA_MISCINFO_WA_RS_182112420303.csv'
# jsonFilePath = r'ALFA_MISCINFO_WA_RS_182112420303.json'

# # Call the make_json function
# make_json(csvFilePath, jsonFilePath)