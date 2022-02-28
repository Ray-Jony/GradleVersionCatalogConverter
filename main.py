# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import re


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    line = 'alias("kotlin-test-junit5").to("org.jetbrains.kotlin", "kotlin-test-junit5"ersionRef("kotlin")'
    print(re.search(r'\.version(Ref)?\("\w+"\)', line))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
