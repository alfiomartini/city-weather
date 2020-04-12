import csv, json 

def printList(listDict, size):
    for i in range(0, size):
        print(listDict[i]['name'])
    print("")

def insertionSort(seq):
    size = len(seq)
    for i in range(1, size):
        j = i
        while j > 0 and seq[j - 1]['name'] > seq[j]['name']:
            seq[j-1], seq[j] = seq[j], seq[j-1]
            j -= 1
        # print(i, end=" ")

def main():
    cities = []

    # open world-cities.csv 
    # fieldnames: name,country,subcountry,geonameid
    with open("world-cities.csv", "r", encoding = 'utf-8', newline="") as csv_file:
        # fieldnames are omitted, thus the values in the first row will
        # be used as fieldnames
        csv_reader = csv.DictReader(csv_file)
        # read and insert data into dictionary 
        for row in csv_reader:
            data = {}
            data['name'] = row['name']
            data['country'] = row['country']
            data['subcountry'] = row['subcountry']
            data['geonameid'] = row['geonameid']
            cities.append(data)
    
    # for k in range(0,10):
    #    json_string = json.dumps(cities[k])
    #   print(json_string)
    printList(cities, 10)

    # sort dictionary's list
    print("Sorting 28000 lines of csv file...")
    insertionSort(cities)

    # print sorted list
    printList(cities, 10)

    # write sorted list to world-cities-sorted.csv
    print("Creating sorted output sorted file...")
    with open("world-cities-sorted.csv", "w", newline="", encoding='utf-8') as csv_sorted:
        fieldNames = ['name','country','subcountry','geonameid']
        writer = csv.writer(csv_sorted)
        writer.writerow(fieldNames)
        size = len(cities)
        for k in range(0, size):
            writer.writerow([cities[k]['name'], cities[k]['country'], 
                             cities[k]['subcountry'], cities[k]['geonameid']])



if __name__ == "__main__":
    main()
    