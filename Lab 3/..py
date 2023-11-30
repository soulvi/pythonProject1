props = soup.find_all('div', class_='section-product-specifications__row')
        for prop in props:
            name_element = prop.find('div', class_='section-product-specifications__name')
            value_element = prop.find('div', class_='section-product-specifications__value')
            name = name_element.text.strip().split(':')[0].strip()
            value = value_element.text.strip()
            item[name] = value
#Попытка написания цикла для 1 части 5 задания