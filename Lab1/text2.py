'Считайте файл согласно вашему варианту и подсчитайте сумму чисел, по каждой строке. В результирующем файле выведите полученные данные:'
'sum1,'
'sum2'
'sum3 '
'sumN '

filename= 'text_2'
with open(filename) as file:
    lines=file.readlines()

sum_lines=list()
for line in lines:
    print(line.strip())
    nums=line.split(",")
    print(nums)
    sum_line=0
    for num in nums:
        sum_line += int(num)

    sum_lines.append(sum_line)
print(sum_lines)
with open('r_text_2.txt', 'w') as result:
    for value in sum_lines:
        result.write(str(value)+"\n")