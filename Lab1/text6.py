from bs4 import BeautifulSoup
import json

str_json = ""
with open('text_6', encoding='utf-8') as file:
    lines = file.readlines()
    for line in lines:
        str_json += line

data = json.loads(str_json)
data = data.get('data')

print(data)

soup = BeautifulSoup("""<table>
    <tr>
        <th>name</th>
        <th>height</th>
        <th>mass</th>
        <th>hair_color</th>
        <th>skin_color</th>
        <th>eye_color</th>
        <th>birth_year</th>
        <th>gender</th>               
    </tr>
</table>""", features="html.parser")

table = soup.find("table")

for tick in (data if data is not None else []):
    tr = soup.new_tag("tr")
    for key, val in tick.items():
        td = soup.new_tag("td")
        td.string = str(val)
        tr.append(td)
    table.append(tr)

with open ('r_text_6.csv', 'w', encoding="utf-8") as result:
    result.write(soup.prettify())
    result.write("\n")