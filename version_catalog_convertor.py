#!/usr/bin/python
# Filename: version_catalog_convertor.py

import sys

strings = sys.argv[1]
splinted = strings.split(':')
group = splinted[0]
artifact = splinted[1]
version = splinted[2]

print("group = " + group)
print("artifact = " + artifact)
print("version = " + version)

if group.split('.')[-1] == artifact.split('-')[0]:
    alias = group + '.' + artifact[len(group.split('.')[-1]):]

print('')
version_catalog = "alias(\"" + alias.replace('.', '-') + "\")" \
                  + ".to(\"" + group + "\", \"" + artifact + "\")" \
                  + ".version(\"" + version + "\")"
print(version_catalog)
deps = "implementation(" + alias + ")"
print('')
print(deps)
