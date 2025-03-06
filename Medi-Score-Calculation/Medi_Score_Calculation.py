from enum import Enum
import os
from typing import Any
from datetime import datetime

##test data to be used (change through each test)


class MediScore:
    score = 0
    @classmethod
    def updateScore(self, scores: int):
        self.score += scores

##sets enum value for if patient is on air or oxygen
class AirOxygen(Enum):
    air = 0
    oxygen = 2

##sets enum value for if patient is conscious or not
class Consciousness(Enum):
    alert = 0
    cvpu = 3

##creates an object which stores the respiration of the patient and assigns the score
class RespirationRange:
    respiration = 0
    score = 0
    def getRespiration(self, resp: int) -> Any:
        self.respiration = resp

    def setScore(self) -> Any:
        if self.respiration <= 8:
            self.score = 3
        elif 9 <= self.respiration <= 11:
            self.score = 1
        elif 12 <= self.respiration <= 20:
            self.score = 0
        elif 21 <= self.respiration <=24:
            self.score = 2
        elif 25<= self.respiration:
            self.score = 3
        return self.score

## creates an object which stores the SpO2 % and assigns a score
## this takes into account if the patient is on oxygen or not
class BloodOxygen:
    bloodOxygenLevel = 0
    score = 0
    onOxygen: bool = False

    def getBloodOxygen(self, bloodOx: int, oxygen: int) -> Any:
        self.bloodOxygenLevel = bloodOx
        if oxygen == 0:
            self.onOxygen = False
        elif oxygen ==2:
            self.onOxygen = True

    def setScore(self) -> Any:
        if self.bloodOxygenLevel <= 83:
            self.score = 3
        elif 84 <= self.bloodOxygenLevel <= 85:
            self.score = 2
        elif 86 <= self.bloodOxygenLevel <= 87:
            self.score = 1
        elif 88 <= self.bloodOxygenLevel <=92:
            self.score = 0
        elif 88<= self.bloodOxygenLevel <= 93 and not self.onOxygen:
            self.score = 0
        elif 93<=self.bloodOxygenLevel<=94 and self.onOxygen:
            self.score = 1
        elif 95<=self.bloodOxygenLevel<=96 and self.onOxygen:
            self.score = 2
        elif 97 <= self.bloodOxygenLevel and self.onOxygen:
            self.score = 3
        return self.score

## creates an object which stores the temperature of the patient and assigns score
class Temperature:
    temperature: float = 0.1
    score = 0

    def getTemperature(self, temp: float) -> Any:
        self.temperature = round(temp,1)

    def setScore (self):
        if self.temperature <= 35.0:
            self.score = 3
        elif 35.1 <= self.temperature <= 36.0:
            self.score = 1
        elif 36.1 <= self.temperature <= 38.0:
            self.score = 0
        elif 38.1 <= self.temperature <= 39.0:
            self.score = 1
        elif 39.1 <= self.temperature:
            self.score = 2
        return self.score


def processTestData(airOxygenVal, conscious, respirationValue, bloodOxygenValue, temperatureValue):
    ## sort the data into relevant variables
    airOxygen = AirOxygen[airOxygenVal]  
    consciousness = Consciousness[conscious]

    ##initialises the objects
    respirationRange = RespirationRange()
    bloodOxygen = BloodOxygen()
    temperatureClass = Temperature()

    ##sets the score for respiration
    respirationRange.getRespiration(respirationValue)
    respirationScore = respirationRange.setScore()
    MediScore.updateScore(respirationScore)

    ##sets score for SpO2 levels
    bloodOxygen.getBloodOxygen(bloodOxygenValue, airOxygen.value)
    bloodOxygenScore = bloodOxygen.setScore()
    MediScore.updateScore(bloodOxygenScore)

    ##sets score for temperature
    temperatureClass.getTemperature(temperatureValue)
    temperatureScore = temperatureClass.setScore()
    MediScore.updateScore(temperatureScore)

    ##sets score for consciousness and air/oxygen
    MediScore.updateScore(consciousness.value)
    MediScore.updateScore(airOxygen.value)

    print("Total MediScore:", MediScore.score)
    return (MediScore.score)

def main():
    name = input("Enter patient's full name: ")
    firstName, surName = name.split()
    firstName = firstName.capitalize()
    surName = surName.capitalize()
    name = firstName+surName

    airOxygen = input("Enter air or oxygen: ").lower()
    conscious = input("Enter alert or CVPU: ").lower()
    respirationValue = int(input("Enter respiration range: "))
    bloodOxygenValue = int(input("Enter blood oxygen %: "))
    temperatureValue = float(input("Enter temperature: "))
    finalScore = processTestData(airOxygen, conscious, respirationValue, bloodOxygenValue, temperatureValue)

    fileName = name+".txt"
    currentDate = datetime.now()
    
    ##checks if file exists
    if os.path.exists(fileName):
        mostRecent = ''

        ##fetches previous entry
        with open (fileName, 'r') as readFile:
            lines = readFile.readlines()
            if lines:
                mostRecent = lines[-1].strip()
            readFile.close()
        ##writes new data to file
        with open(fileName, 'a') as patientFile:  
            patientFile.write("\n" + str(finalScore) + " " + str(currentDate))

        ##parses the data from previous entry
        previousScore, previousDate, previousTime = mostRecent.split()
        previousScore = int(previousScore)  
        previousDate = datetime.strptime(previousDate, "%Y-%m-%d")
        previousTime = datetime.strptime(previousTime, "%H:%M:%S.%f").time()
        previousDateTime = datetime.combine(previousDate, previousTime)

        ##clalculates the time difference
        timeDifference = currentDate - previousDateTime

        ##pops the alert if score has increased in 24hr period
        if finalScore >= previousScore + 2 and timeDifference.total_seconds() <= 86400:  
                print("Alert: Score has increased by 2 in the last 24 hours!")
    
    ##if file doesn't exist, a file is created and data entered
    else:
        with open(fileName, 'w') as patientFile:
             patientFile.write(str(finalScore) + " " + str(currentDate))

main()
