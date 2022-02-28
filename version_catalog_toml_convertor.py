#!/usr/bin/python

import sys
import re


def is_valid_alias(alias):
    if alias is None:
        return False
    if "alias(" not in alias:
        return False
    if ".to(" not in alias:
        return False
    if ".version(" not in alias and ".versionRef(" not in alias:
        return False
    return True


def version_to_toml(string):
    string = string.strip()
    version_ref = re.search(r'(?<=version\(\")[\w-]+', string).group(0)
    version = re.search(r'(?<=", )[".\w-]+', string).group(0)
    return version_ref + " = " + version


def alias_to_toml(alias):
    alias = alias.replace("\n", "")
    alias = alias.replace(" ", "")
    if not is_valid_alias(alias):
        return "ERROR"
    alias_ref = re.findall(r'(?<=alias\()"(.*?)"', alias)[0]
    group = re.findall(r'(?<=to\()"(.*?)"', alias)[0]
    if ".versionRef" in alias:
        version = re.findall(r'(?<=versionRef\()"(.*?)"', alias)[0]
        artifact = re.findall(r'(?<=,)"(.+?)"(?=\)\.versionRef)', alias)[0]
        return alias_ref + " = { module = \"" + group + ":" + artifact + "\", version.ref = \"" + version + "\" }"
    else:
        version = re.findall(r'(?<=version\()"(.*?)"', alias)[0]
        artifact = re.findall(r'(?<=,)"(.+?)"(?=\)\.version)', alias)[0]
        return alias_ref + " = \"" + group + ":" + artifact + ":" + version + "\""


def bundles_to_toml(string):
    string = string.strip()
    bundles_ref = re.search(r'(?<=bundle\(")[\w-]+', string).group(0)
    string = re.search(r'(?<=listOf\()"(.*)"', string).group(0)
    bundles = re.findall(r'"[\w-]+"', string)
    ret = bundles_ref + " = ["
    cnt = 0
    for bundle in bundles:
        cnt += 1
        ret += bundle
        if cnt != len(bundles):
            ret += ', '
    return ret + ']'


def pick_up_version_lines(array):
    ret_lines = []
    tmp = ""
    for item in array:
        striped_line = item.strip()
        if striped_line.startswith("version(\""):
            tmp = striped_line
        if re.search(r'version\("([\w\W]+?)",\s([\S])+\)', tmp):
            ret_lines.append(tmp)
            tmp = ""
    return ret_lines


def pick_up_alias_lines(array):
    ret_lines = []
    tmp = ""
    to_be_full_fill = False
    for item in array:
        striped_line = item.strip()
        if to_be_full_fill:
            tmp = tmp + striped_line
        elif striped_line.startswith("alias"):
            tmp = striped_line
        if tmp == "":
            continue
        if re.search(r'\.version(Ref)?\("\S+"\)', tmp):
            ret_lines.append(tmp)
            tmp = ""
            to_be_full_fill = False
        else:
            to_be_full_fill = True
    return ret_lines


def pick_up_bundles_lines(array):
    ret_lines = []
    tmp = ""
    to_be_full_fill = False
    for item in array:
        striped_line = item.strip()
        if to_be_full_fill:
            tmp = tmp + striped_line
        elif striped_line.startswith("bundle"):
            tmp = striped_line
        if tmp == "":
            continue
        if re.search(r'bundle\("[\w-]+",\W?listOf\(("([\w-]+)"[, ]?)+\)\)', tmp):
            ret_lines.append(tmp)
            tmp = ""
            to_be_full_fill = False
        else:
            to_be_full_fill = True

    return ret_lines


with open(sys.argv[1], 'r') as reader:
    lines = reader.readlines()
    reader.close()
output_file_path = sys.argv[2]
if not output_file_path.endswith('.toml'):
    exit(1)
output_file = open(output_file_path, "w")
output_file.write("# generated from \"" + sys.argv[1] + "\"\n")
output_file.close()

# versions
output_file = open(output_file_path, "a")
output_file.write("[versions]\n")
for line in pick_up_version_lines(lines):
    res = version_to_toml(line)
    output_file.write(res + "\n")
output_file.write('\n')

# libraries
output_file.write("[libraries]\n")
output_file.close()
output_file = open(output_file_path, "a")
for line in pick_up_alias_lines(lines):
    res = alias_to_toml(line)
    if res == "ERROR":
        exit(1)
    output_file.write(res + "\n")
output_file.write('\n')

# bundles
output_file = open(output_file_path, "a")
output_file.write("[bundles]\n")
for line in pick_up_bundles_lines(lines):
    res = bundles_to_toml(line)
    output_file.write(res + "\n")
output_file.write('\n')

output_file.close()
