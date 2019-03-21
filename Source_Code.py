import csv

# Fungsi untuk Read Data Train
def openDataTrain():
    age = []
    work = []
    edu = []
    martial = []
    occupation = []
    relationship = []
    hoursperweek = []
    income = []

    with open('TrainsetTugas1ML.csv') as data:
        reader = csv.DictReader(data)
        for row in reader:
            age.append(row['age'])
            work.append(row['workclass'])
            edu.append(row['education'])
            martial.append(row['marital-status'])
            occupation.append(row['occupation'])
            relationship.append(row['relationship'])
            hoursperweek.append(row['hours-per-week'])
            income.append(row['income'])

    return age,work,edu,martial,occupation,relationship,hoursperweek,income

# Fungsi untuk Read Data Test
def openDataTest():
    age = []
    work = []
    edu = []
    martial = []
    occupation = []
    relationship = []
    hoursperweek = []

    with open('TestsetTugas1ML.csv') as data:
        reader = csv.DictReader(data)
        rowlen = 0
        for row in reader:
            age.append(row['age'])
            work.append(row['workclass'])
            edu.append(row['education'])
            martial.append(row['marital-status'])
            occupation.append(row['occupation'])
            relationship.append(row['relationship'])
            hoursperweek.append(row['hours-per-week'])
            rowlen += 1
    
    return age,work,edu,martial,occupation,relationship,hoursperweek,rowlen

# Fungsi untuk Mencari Atribut Unik mgenggunakan Set
def getUniqueSet(age,work,edu,martial,occupation,relationship,hoursperweek,income):
    setAge = set(age)
    setWork = set(work)
    setEdu = set(edu)
    setMartial = set(martial)
    setOccupation = set(occupation)
    setRelationship = set(relationship)
    setHours = set(hoursperweek)
    setIncome = set(income)

    return setAge,setWork,setEdu,setMartial,setOccupation,setRelationship,setHours,setIncome

# Fungsi untuk menghitung jumlah dari setiap pasangan attribut dan Kelas dan juga jumlah dari setiap Kelas
def countAttribClass(age,work,edu,martial,occupation,relationship,hoursperweek,income):
    
    # Inisiasi Dictionary untuk Menghitung Jumlah Setiap Pasangan Atribut dan Kelas(Income)
    attrib_class = {}
    for ages in setAge:
        for inc in setIncome:
            attrib_class[ages,inc] = 0

    for works in setWork:
        for inc in setIncome:
            attrib_class[works,inc] = 0

    for edus in setEdu:
        for inc in setIncome:
            attrib_class[edus,inc] = 0

    for martials in setMartial:
        for inc in setIncome:
            attrib_class[martials,inc] = 0

    for occu in setOccupation:
        for inc in setIncome:
            attrib_class[occu,inc] = 0

    for relations in setRelationship:
        for inc in setIncome:
            attrib_class[relations,inc] = 0

    for hours in setHours:
        for inc in setIncome:
            attrib_class[hours,inc] = 0

    # Inisiasi Dictionary untuk Mencari Jumlah Dari Setiap Kelas
    tot_class = {}

    # Hitung Jumlah Setiap Class
    for inc in setIncome:
        tot_class[inc] = income.count(inc)

    # Hitung Total Dari Setiap Pasangan Atribut dengan Class
    for i in range(len(income)):
        attrib_class[ age[i],income[i] ] += 1
        attrib_class[ work[i],income[i] ] += 1
        attrib_class[ edu[i],income[i] ] += 1
        attrib_class[ martial[i],income[i] ] += 1
        attrib_class[ occupation[i],income[i] ] += 1
        attrib_class[ relationship[i],income[i] ] += 1
        attrib_class[ hoursperweek[i],income[i] ] += 1

    return attrib_class,tot_class

# Fungsi untuk menghitung probabilitas
def countProbBayes(age,work,edu,martial,occu,relation,hour):
    prob = 0
    maks = prob
    kelas = ""
    for income in setIncome:
        prob_age = attrib_class[age,income]/tot_class[income]                                       # Hitung Likelihood Age
        prob_work = attrib_class[work,income]/tot_class[income]                                     # Hitung Likelihood Work
        prob_edu = attrib_class[edu,income]/tot_class[income]                                       # Hitung Likelihood Education
        prob_martial = attrib_class[martial,income]/tot_class[income]                               # Hitung Likelihood Martial-Status
        prob_occu = attrib_class[occu,income]/tot_class[income]                                     # Hitung Likelihood Occupation
        prob_relation = attrib_class[relation,income]/tot_class[income]                             # Hitung Likelihood Relationship
        prob_hour = attrib_class[hour,income]/tot_class[income]                                     # Hitung Likelihood Hours-per-week
        prior = tot_class[income]/sum(tot_class.values())                                           # Hitung Prior
        prob = prob_age*prob_work*prob_edu*prob_martial*prob_occu*prob_relation*prob_hour*prior     # Hitung Probabilitas
        
        # Cari Probabilitas Terbesar dari tiap Kelas
        if maks<prob :
            maks = prob
            kelas = income
    
    return kelas

if __name__ == '__main__':
    # Read data train
    ageTrain,workTrain,eduTrain,martialTrain,occupationTrain,relationshipTrain,hoursperweekTrain,incomeTrain = openDataTrain()
    # Read data test
    ageTest,workTest,eduTest,martialTest,occupationTest,relationshipTest,hoursperweekTest,dataLength = openDataTest()
    
    # Ambil Set setiap attribut dan class
    setAge,setWork,setEdu,setMartial,setOccupation,setRelationship,setHours,setIncome = getUniqueSet(ageTrain,workTrain,eduTrain,martialTrain,occupationTrain,relationshipTrain,hoursperweekTrain,incomeTrain)

    # Hitung jumlah setiap pasangan attribut dan class dan jumlah setiap class
    attrib_class, tot_class = countAttribClass(ageTrain,workTrain,eduTrain,martialTrain,occupationTrain,relationshipTrain,hoursperweekTrain,incomeTrain)

    # Write hasil tebakan ke dalam file "TebakanTugas1ML.csv"
    with open('TebakanTugas1ML.csv', 'w', newline='') as csvfile:
        fieldnames = ['Kelas/Income']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for i in range(dataLength):
            writer.writerow({'Kelas/Income': countProbBayes(ageTest[i],workTest[i],eduTest[i],martialTest[i],occupationTest[i],relationshipTest[i],hoursperweekTest[i])})