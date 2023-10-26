'Задание 1'
'Считайте файл согласно вашему варианту и подсчитайте частоту каждого слова в тексте. '
'В результирующем файле выведите полученные данные в порядке убывания:'
'word1:freq1'
'word2:freq2'
'word3:freq3'
'wordN:freqN '

filename = 'text_1'
with open(filename) as file:
    lines = file.readlines()

word_stat = dict()
for line in lines:
    print(line.strip())
    row = (line.strip()
        .replace("!", " ")
        .replace("?", " ")
        .replace(",", " ")
        .replace(".", " ")
        .strip())
    print(row)
    words = row.split(" ")
    print(words)
    for word in words:
        if word in word_stat:
            word_stat[word] +=1
            'Если слово встречалось, добавляем в словарь +1'
        else:
            word_stat[word] =1
            'Если не встречалось присваеваем 1'
    print(word_stat)
    'Порядок убывания'
    word_stat=(dict(sorted(word_stat.items(),reverse=True, key=lambda item: item[1])))
    print(word_stat)

    with open('r_text_1.txt', 'w') as result:
        for key, value in word_stat.items():
            result.write(key+":"+str(value)+"\n")

