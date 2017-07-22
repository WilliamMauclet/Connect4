# TODO Files need to go in sub-folder docs


def _read_file(title):
    result = {}
    reader = open(title, "r")
    # title
    result['title'] = title

    reader.readline()  # wrongly filled in
    result['games played'] = 50

    reader.readline()  # skip this

    # end scores
    result['end_scores'] = {}
    for i in range(3):
        line = reader.readline().split(" : ")
        if line[0] == 'MinmaxBot':
            line[0] += str(i - 1)
        result['end_scores'][line[0]] = line[1].replace("\n", "")

    reader.readline()  # empty line
    result['duration'] = reader.readline().split(": ")[1].replace("\n", "")

    reader.readline()  # empty line

    reader.readline()  # see next line
    result['additional_details'] = {}
    for i in range(2):
        descr = reader.readline().split(" : ")
        if descr[0] == 'MinmaxBot':
            descr[0] += str(i)
        result['additional_details'][descr[0]] = _read_description(descr[1])

    return result


def _read_description(desc_string):
    desc_string = desc_string.replace("\n", "")
    result = {}
    descriptions = desc_string.split("/")
    for desc in descriptions:
        thing = desc.split("=")
        if len(thing) > 1:
            result[thing[0]] = thing[1]
    return result


import glob
import json
import os
import sys

sys.path.insert(0, os.path.abspath("."))


# def print_best_scores():
#     for file in glob.glob(RESULTS_DIRECTORY + "*.txt"):
#         reading = _read_file(file)
#         if int(reading['end_scores']['MinmaxBot1']) == 50:
#             print(file + " " + str(reading['additional_details']['MinmaxBot1']))


def _print_sorted_by_score():
    scores = {}

    for file in glob.glob("../" + RESULTS_DIRECTORY + "*.txt"):
        if "JsonTestResults" in file:
            continue
        reading = _read_file(file)
        score = reading['end_scores']['MinmaxBot1']
        if score in scores:
            scores[score].append(reading['additional_details']['MinmaxBot1'])
        else:
            scores[score] = [reading['additional_details']['MinmaxBot1']]

    for key in sorted(scores):
        print(key)
        for value in scores[key]:
            print("\t" + str(value))


# def print_to_one_file_with_json():
#     result = {'tests': []}
#     os.chdir("../" + RESULTS_DIRECTORY)
#     for file in glob.glob("*.txt"):
#         if file != 'JsonTestResults_A.txt':
#             reading = _read_file(file)
#             result['tests'].append(reading)
#
#     result_json = json.dumps(result, indent=4)
#
#     with open(TEST_RESULTS_FILE_NAME, 'w') as writer:
#         writer.write(result_json)


# def calculate_total_score_of_players():
#     os.chdir("../" + RESULTS_DIRECTORY)
#     with open(TEST_RESULTS_FILE_NAME, 'r') as reader:
#         print(json.loads(reader.read()))
#         pass
#         # TODO?


TEST = ''
RESULTS_DIRECTORY = "games/Results" + ("_" + TEST if TEST else "") + "/"
TEST_RESULTS_FILE_NAME = "JsonTestResults" + ("_" + TEST if TEST else "") + ".txt"


# def print_sorted_by_score_c():
#     scores = {}
#
#     for file in glob.glob("../" + RESULTS_DIRECTORY + "*.txt"):
#         if TEST_RESULTS_FILE_NAME in file:
#             continue
#         reading = _read_file(file)
#         score = reading['end_scores']['MinmaxBot0']
#         if score in scores:
#             scores[score].append(
#                 reading['additional_details']['MinmaxBot0'] + " vs " + reading['additional_details']['MinmaxBot1'])
#         else:  # TODO
#             scores[score] = [
#                 reading['additional_details']['MinmaxBot0'] + " vs " + reading['additional_details']['MinmaxBot1']]
#
#     for key in sorted(scores):
#         print(key)
#         for value in scores[key]:
#             print("\t" + str(value))


# TODO refactoring

_print_sorted_by_score()

# print(result)
# import json
# j = json.dumps(result)
# print(j)
# print(result['end_scores']['MinmaxBot'])
