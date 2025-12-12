import csv

with open('./agencias.csv', 'r', encoding='utf-8') as infile, open('./agencias_modificado.csv', 'w', encoding='utf-8', newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile, delimiter=';')

    for row in reader:
        writer.writerow(row)