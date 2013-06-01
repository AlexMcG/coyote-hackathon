import csv
from datetime import datetime

def parse():
     #parses file by rows into a list
     with open('Coyote.csv', newline='') as csvfile:
          lst =  list(csv.reader(csvfile, delimiter=',', quotechar='|'))

     #fixes comma bug with location data
     for i in lst:
          i[2] = ','.join(i[2:4])
          i[2] = i[2].strip('"')
          i.pop(3)
     return lst

def search(string, lst):
     #setup
     string = string.lower()
     citiesSet = set()
     for i in lst: citiesSet.add(i[2].lower())
     resultLst = [ [], [] ]

     #if match
     if string not in citiesSet:

          #if no match
          matchLst = []
          for q in citiesSet:
               for z in range(len(string)):
                    if (q.find(string[0:z]) == -1): break
               resultLst[0].append(q)
               resultLst[1].append(z)

          #makes list of strings that match the most
          for l in range(len(resultLst[1])):
               if (resultLst[1][l] == max(resultLst[1])):
                    matchLst.append(resultLst[0][l])

          #picks smallest string that matches
          result = min(matchLst, key=len)
     
     else: result = string
          
     #finds non lowercase version
     for i in lst:
          if (result == i[2].lower()): return i[2]

def cityList(string, lst):
     #setup
     arrivals = set()
     departures = set()

     #finds arrival city
     for i in lst:
          if ((i[1] == "1") and (i[2] == string)):
               arrivals.add(i[0])

     #finds possible departures   
     for i in range(len(lst)):
          if ((lst[i][1] == "2") and (lst[i][0] in arrivals)):
               departures.add(i)

     return departures

def clPrint(output, lst):
     #formats cityList output and makes it printable
     cLst = []
     for i in output: cLst.append(lst[i][2])
     return ", ".join(cLst)

def bestTime(departures, destinationCity, lst):
     #setup
     times = []
     
     for i in departures:
          if (lst[i][2] == destinationCity):
               #parse and save time info
               start = datetime.strptime(lst[i-1][6], '%m %d %Y %I:%M%p')
               end = datetime.strptime(lst[i][5], '%m %d %Y %I:%M%p')
               times.append(end - start)
     
               #reformat and return
               if (min(times) == times[-1]): 
                    bestTime = lst[i-1][6].split()
     
     return bestTime[3]

def main():
     lst = parse()
     while (True):
          inputStart = ' '
          inputStart = input("Enter the city you are leaving from or hit q to quit: ")
          if inputStart == 'q': break
          inputStart = search(inputStart, lst)
          print("Here is a list of destination cities: ")
          output = cityList(inputStart, lst)
          print(clPrint(output, lst))
          inputEnd = input("Enter the city you are going to: ")
          inputEnd = search(inputEnd, lst)
          print("The best time to leave", inputStart, "and arrive in", inputEnd, "is:", bestTime(output, inputEnd, lst))

#script
main()
