import zipfile
import os
import hashlib
import requests
import re



def line_cleaning(line, counter):
    line = re.sub(r'<div class=[^>]{0,}>', '', line)
    line = re.sub(r' <span[^\)]{0,}\)', '', line)
    line = re.sub(r'</div>$', '', line)
    line = re.sub(r'</span>', '', line)
    line = re.sub(r'<[/]{0,}strong>', '', line)
    if counter == 205 or counter == 217:
        line = re.sub(r'^...', '', line)
    elif counter != 0:
        line = re.sub(r'^....', '', line)    
    return line


directory = 'D:\\tiff_unpacked'
arch_file = 'D:\\tiff-4.2.0_lab1.zip'
test_zip = zipfile.ZipFile(arch_file)
test_zip.extractall(directory)
print('\nTASK 1: Archive is unpacked, content is extracted')



txt_files = []
for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith('.txt'):
            txt_files.append(root + '\\' + file)
            
hash_txt_files = []
for file in txt_files:
    hash_file = open(file,'rb').read()
    hash_txt_files.append(hashlib.md5(hash_file).hexdigest())

print('\nTASK 2:')
for i in range(len(txt_files)):
    print(txt_files[i] + ' - ' + hash_txt_files[i])



target_file = ''
target_file_data = ''
target_hash = '4636f9ae9fef12ebd56cd39586d33cfb'
for root, dirs, files in os.walk(directory):
    for file in files:
        if hashlib.md5(open(root + '\\' + file,'rb').read()).hexdigest() == target_hash:
            target_file = root + '\\' + file
            target_file_data = open(target_file,'rb').read()
            break
print('\nTASK 3:')
print(target_file)
print(target_file_data)



r = requests.get(target_file_data)
headers = []
table = {}
counter = 0
lines = re.findall(r'<div class="Table-module_row__3TH83">.*?</div>.*?</div>.*?</div>.*?</div>.*?</div>', r.text)

for line in lines:
    line = line_cleaning(line, counter)
    if counter == 0:
        headers = line.split('</div>')
    else:
        country, line = line.split('</div>', 1)
        str(country)
        line = re.sub('\\xa0', '', line)
        line = re.sub('\*', '', line)
        line = re.sub('_', '-1', line)
        values = []
        for value in line.split('</div>'):
            values.append(int(value))
        table[country] = values
    counter += 1
print('\nTASK 4: Table compiled')



output = open('data.csv', 'w')
output.write(headers[0] + ';' + headers[1] + ';' + headers[2] + ';' + headers[3] + ';' + headers[4] + '\n')
for country, values in table.items():
    output.write(country + ';' + str(values[0]) + ';' + str(values[1]) + ';' + str(values[2]) + ';' + str(values[3]) + '\n')
output.close()
print('\nTASK 5: table written to file data.csv')



print('\nTASK 6:')
while (True):
    target_country = input('Enter country name or \'stop\': ')
    if target_country == 'stop':
        break
    existence = False
    for country in table.keys():
        if country == target_country:
            existence = True
            break
    if existence == True:
        print('--------------------------------\n' + 
              '{}\n{}: {}\n{}: {}\n{}: {}\n{}: {}'.format(target_country,
                                                          headers[1], table[target_country][0], 
                                                          headers[2], table[target_country][1], 
                                                          headers[3], table[target_country][2], 
                                                          headers[4], table[target_country][3]) + 
              '\n--------------------------------')
    else:
        print('Nothing found...')
print('Goodbye!')