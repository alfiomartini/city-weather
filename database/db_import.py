import cs50
import csv


db = cs50.SQL('sqlite:///cities.db')
with open("worldcities.csv", "r", newline="", encoding='utf-8') as csv_file:
    # fieldnames: Name, Code
    csv_reader = csv.DictReader(csv_file)
    # reads all lines in the file and insert into the database
    counter = 0
    for row in csv_reader:
        counter += 1
        print(counter)
        db.execute("""insert into cities(city, country, state, lat, lng, abbrev, population)
                      values(?,?,?,?,?,?,?)""", 
                      row['city'], row['country'], row['admin_name'], row['lat'], row['lng'], 
                      row['iso2'], row['population'])