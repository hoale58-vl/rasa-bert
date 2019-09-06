
import re
from google_api import Text2Speed
input_training_file = "../domain.yml"

input_file = open(input_training_file, 'r')
data = input_file.read()
input_file.close()
T2S = Text2Speed()
matches = re.findall("  (\w+):\n((?:  - text: \"(?:.*)\"\s*\n)+)", data)
for match in matches:
    org = match[0]
    if "_vi" == org[-3:]: 
        contents = re.findall("- text: \"(.*)\"\s*\n", match[1])
        i = 0
        for content in contents:
            name = org + "_" + str(i)
            if content.strip() != "":
                print(name)
                print(content)
                print()
                T2S.downloadFile(name, content)
                i += 1
