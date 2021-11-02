from sys import argv
import csv
import time

crimesFile = argv[1]
suspectsFile = argv[2]
solutionFile = argv[3]

def run():
  """
  In this function I make sure the user is inputting three files, one for the crimes file, the second for the suspects file, the third for the solution file. I then get the dictionary of crimes matched to each suspect by calling the function getCrimesandSuspects() and name the variable "crimes" and use crimes as a parameter in the function writeNewFile(crimes) to write the dictionary to the solution file.
  """
  if len(argv) < 3:
    print(f"Usage: python3 crimesFile suspectsFile solutionFile")
    return
  crimes = getCrimesandSuspects()
  writeNewFile(crimes)
  return

def writeNewFile(crimes):
  """
  The purpose of this function is to take the parameter crimes (which is a dictionary) and write it to a new File. First I create the new file named solutionFile and write the headers 'Suspect' and 'Crimes'. I then inicialize a dictionary named "final" and iterated through each item in crimes, in "final" I set the suspect name equal to the key and set the crimes equal to the value while adding commas inbetween each crime. I then wrote final to the new file.  
  """
  with open(solutionFile, 'w', newline='') as newFile:
    fieldnames = ['Suspect', 'Crimes']
    csvNew = csv.DictWriter(newFile, fieldnames=fieldnames, dialect='excel')
    csvNew.writeheader()
    final = {}
    for key, value in crimes.items():
      final['Suspect'] = key
      final['Crimes'] = ",".join(value)
      csvNew.writerow(final)
  return


def getCrimesandSuspects():
  """
  The purpose of this function is to get a dictionary of suspects and the name of crime scenes their DNA matches with. First, this function opens the crimes file that includes the CrimeIDs and the DNA sequences and how many times the sequence showed up at each crime. I then get the fieldNames to be able to read the DNA sequences. I get a list of people (variable name = people) in a list with their name and the number of time each sequence showed up in their DNA by calling the function checkSuspects(fieldNames). I then iterate though each crime in the crimes file I opened, convert it into a list of the values, since it was originally in a dictionary (variable name = crimeList), iterate through each person in the list people, and check if crimeList (not including the CrimeID) equals person (not including their name). If they are equal I append the personas name and the  name of the crime that their sequence matched to the list named crimes, and if they are not equal I append the persons name and a blank string. The final part of the function is to convert the list into a dictionary (variable name = crimesDict) by creating a key of the persons name and setting the value equal to the crime they matched with and if the key was already in the dictionary (if the person matched with more than one crime) I would append the other crimes to the value of the person. I then removed any empty strings and returned the dictionary crimesDict. 
  """
  with open(crimesFile, newline='') as original:
    csvCrimes = csv.DictReader(original, dialect='excel')
    sequences = csvCrimes.fieldnames
    people = checkSuspects(sequences)
    crimes = []
    crimeList = []
    for crime in csvCrimes:
      crimeList = list(crime.values())
      for i in range(1, len(crimeList)): 
        crimeList[i] = int(crimeList[i]) 
      for person in people:
        if crimeList[1:] == person[1:]:
          crimes.append(person[0])
          crimes.append(crime['CrimeID'])
        else:
          crimes.append(person[0])
          crimes.append('')
  crimesDict = {}
  for i in range(0, len(crimes), 2):
    if crimes[i] in crimesDict:
      crimesDict[crimes[i]].append(crimes[i + 1])
    else:
      crimesDict[crimes[i]] = [crimes[i + 1]]
  for key, value in crimesDict.items():
    while '' in value:
      value.remove('')
  return crimesDict

def checkSuspects(sequences):
  """
  The purpose of this function is to return the number of the longest consequtive string of the DNA sequences in the parameter "sequences" for each crime for each suspect. First I open the file that has the suspect name and their DNA sequence. Then I iterate through each suspect and their sequence and add their name to the previously inicialized list "people". I then iterate through the DNA sequences (in the variable sequences) found for each crime and set the individual one equal to the variable "pattern". I then go through "individualsDNA" (a variable with a persons DNA sequence (which is changed per person)) and look for the pattern. Once it is found, a variable count (initalized earlier) is increased by one and the seq is added to pattern to find if the seq is consecutive in individualsDNA. After that is complete, I append count to the list "person", which already includes the suspects name. Each person is appended to the list people which in the end includes a list of each person and the numbers of the consecutive sequences found in their DNA. The list "people" is then returned.
  """
  with open(suspectsFile, newline='') as original:
    csvSuspect = csv.DictReader(original, dialect='excel')
    people = []
    count = 0
    for row in csvSuspect:
      person = [row['Suspect']]
      for seq in sequences[1:]:
        individualsDNA = row['Sequence']
        pattern = seq
        while pattern in individualsDNA:
          count += 1
          pattern += seq
        person.append(count)
        count = 0
      people.append(person)
  return people

if __name__ == "__main__":
  start = time.perf_counter()
  run()
  end = time.perf_counter()
  print(f"Time used: {end-start} seconds")