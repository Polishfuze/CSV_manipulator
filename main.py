import csv
import time
import os


fileName = 'Test1.csv'
outputDir = 'results'

class CSVworker:
    def __init__(self, filenameIn, filenameOut, debug=False):
        self.filename = filenameIn
        self.output = filenameOut
        self.debug = debug
        self.columns = {}
        self.numCols = 0
        self.cDir = os.getcwd()
        self.oDir = filenameOut
        self.eDir = os.path.join(self.cDir, self.oDir)
        self.exclude = ['$RT_OFF$', '$RT_COUNT$', 'VarName']
        self.makeDir()
        self.firstPassSort()
        self.finalPass()

    def firstPassSort(self):
        with open(self.filename, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            numlines = 0
            for line in csv_reader:
                if line[0] not in self.columns and line[0] not in self.exclude:
                    self.columns[line[0]] = self.numCols
                    self.numCols += 1
                if numlines < 10 and self.debug:
                    print(line)
                numlines += 1
                
        if self.debug:
            print(self.columns)
    
    def genEmptyTables(self):
        return [[] for _ in range(self.numCols)]

    def finalPass(self):
        csv_file = open(self.filename)
        files = self.genEmptyTables()
        csv_reader = csv.reader(csv_file, delimiter=';')

        for line in csv_reader:
            valName = line[0]
            if line[0] in self.columns:
                filenum = self.columns[valName]
                data = [[line[0],line[1], line[4], line[2]]]
                if self.debug:
                    # print(filenum)
                    # print(data)
                    # print(files)
                    pass
                files[filenum].append(data)
        csv_file.close()
         
        for csvfile in files:
            filePath = os.path.join(self.eDir, csvfile[0][0][0]+'.csv')
            with open(filePath, mode='w', newline='') as fileItself:
                fileWriter = csv.writer(fileItself, delimiter=',')
                for line in csvfile:
                    fileWriter.writerow(line[0])

    def makeDir(self):
        try:
            os.mkdir(self.eDir)
        except FileExistsError:
            pass
        # print(self.eDir)

fileName = input("Podaj nazwe pliku z danymi z pasteryzacji: ")
fileNameIncorr = True
for name in os.listdir():
    if name.lower() == fileName.lower():
        fileNameIncorr = False
while fileNameIncorr:
    fileName = input("Bledna nazwa pliku, albo plik nie znajduje sie w tym samym folderze co program!\nPodaj nazwe pliku z danymi: ")
    for name in os.listdir():
        if name.lower() == fileName.lower():
            fileNameIncorr = False
print("Poprawny plik, poczekaj na przetworzenie danych.")
worker = CSVworker(fileName, outputDir, debug=False)
print("Plik zostal rozdzielony do pilkow w folderze 'results'")
input("Wcisnij enter aby zakonczyc program ")

exit()
