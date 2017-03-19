
def read_file(title):
    result = {}

    reader = open(title, "r")

    #title
    result['title'] = title

    reader.readline()  # wrongly filled in
    result['games played'] = 50

    reader.readline()  # skip this

    # end scores
    result['end_scores'] = {}
    for i in range(3):
        line = reader.readline().split(" : ")
        result['end_scores'][line[0]] = line[1].replace("\n","")

    reader.readline()  # empty line
    result['duration'] = reader.readline().split(": ")[1].replace("\n","")

    reader.readline()  # empty line

    def read_description(desc_string):
        desc_string = desc_string.replace("\n","")
        desc_string = desc_string.replace("HEURISTIC_ROBOT","/HEURISTIC_ROBOT")
        desc_string = desc_string.replace("HEURISTIC_OPPONENT","/HEURISTIC_OPPONENT=")
        result = {}
        descs = desc_string.split("/")
        for desc in descs:
            thing = desc.split("=")
            result[thing[0]] = thing[1]
        return result


    reader.readline()  # see next line
    result['additional_details'] = {}
    for i in range(2):
        descr = reader.readline().split(" : ")
        result['additional_details'][descr[0]] = read_description(descr[1])

    return result


import sys, os, glob
sys.path.insert(0, os.path.abspath("."))


def print_best_scores():
    for file in glob.glob("Games/Results/*.txt"):
        reading = read_file(file)
        if int(reading['end_scores']['MinmaxRobot']) == 50:
            print(file + " " + str(reading['additional_details']['MinmaxRobot']))

def print_sorted_by_score():
    scores = {}
    for file in glob.glob("Games/Results/*.txt"):
        reading = read_file(file)
        score = reading['end_scores']['MinmaxRobot']
        if score in scores:
            scores[score].append(reading['additional_details']['MinmaxRobot'])
        else:
            scores[score] = [reading['additional_details']['MinmaxRobot']]

    for key in sorted(scores):
        print(key)
        for value in scores[key]:
            print("\t" + str(value))

def print_to_one_file_with_json():
    result = {}
    result['tests'] = []
    os.chdir("../Games/Results/")
    for file in glob.glob("*.txt"):
        if file != 'JsonTestResults_A.txt':
            reading = read_file(file)
            result['tests'].append(reading)

    import json
    result_json = json.dumps(result, indent=4)

    with open('JsonTestResults_A.txt','w') as writer:
        writer.write(result_json)


print_to_one_file_with_json()

#print(result)
#import json
#j = json.dumps(result)
#print(j)
#print(result['end_scores']['MinmaxRobot'])