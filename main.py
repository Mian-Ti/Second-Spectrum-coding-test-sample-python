from try_parse.utils import ParseUtils

def readFromCsv():
    """
    read csv file. and return header table data
    :return: header and table data
    """
    io = open('values.csv', 'r', encoding='UTF-8')
    lines = io.readlines()
    io.close()
    header = str(lines[0]).split(',')
    tables = list(lines[1:])
    # print(f'header: {header}')
    # print(f'tables: {tables}')
    return header, tables


if __name__ == '__main__':
    header, tables = readFromCsv()
    filtered = {}

    # date = datetime.date.fromisoformat('2015-7-18')
    # print(f'date: {date}')

    for row in tables:
        cells = row.split(',')
        name = str(cells[0])
        dateStatus, date = ParseUtils.try_parse_date(cells[1], format='%Y-%m-%d')
        valueStatus, value = ParseUtils.try_parse_float(cells[3])
        # print(f'name: {name} date: {date if dateStatus else None} value: {value if valueStatus else None}')
        if dateStatus and valueStatus:
            # if date or value is invalid, just skip the row
            if filtered.__contains__(name):
                item = filtered[name]
                firstDate = item['first']['date']
                lastDate = item['last']['date']
                if date < firstDate:
                    item['first'] = {
                        'date': date,
                        'value': value
                    }

                if date > lastDate:
                    item['last'] = {
                        'date': date,
                        'value': value
                    }

            else:
                filtered[name] = {
                    'first': {
                        'date': date,
                        'value': value
                    },
                    'last': {
                        'date': date,
                        'value': value
                    }
                }

    # print(f'filtered: {filtered}')
    result = None
    for key in filtered.keys():
        item = filtered[key]
        # print(f"name: {key} last: {item['last']['value']} first: {item['first']['value']}")
        if result:
            value = item['last']['value'] - item['first']['value']
            if value > result['value']:
                result = {
                    'name': key,
                    'value': value
                }
        else:
            value = item['last']['value'] - item['first']['value']
            result = {
                'name': key,
                'value': value
            }

    if result:
        print(f"公司: {result['name']}, 股价增值: {result['value']}")