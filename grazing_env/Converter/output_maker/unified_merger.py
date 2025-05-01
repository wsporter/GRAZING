

# -----------------------------Analysis---------------------------------- ##

import os #use os.listdir
import numpy as np
import re
import pandas as pd
import glob

#return all the file name in Data folder

output_file = input()

def FileName(generated_file):
    filenamearr = [generated_file]
    print("Using unified file:", filenamearr)
    return filenamearr

#import the data content of a given file
def ImportData(filename):
    # data format:
    # 0           1        2
    # charge  neutron crosssection
    
    data = np.loadtxt(filename, skiprows=2)
    return data

#read in halflife data
def HalfLife():
    # data = np.loadtxt('halflife3.txt', skiprows=1)
    data=np.genfromtxt('halflife2.txt', dtype='str',skip_header=1)
    return data

#modify thickness if radioactivity too large
def ModifyX(filename):
    namesplit = filename.split('_')
    namesplit2 = re.split(r'(\d+)', namesplit[1])

    A = int(FindA(filename))
    Na = 6.022e23
    # activity below 50mCi/cm^2
    activity_ci = 50e-3
    activity_bq = activity_ci * 3.7e10  # per second


    halflife=HalfLife()
    
    thickness=5 # target thickness in mg per cm^2

    for i in range (0,len(halflife)-1+1): # Make target 5 mg instead of 10
        if halflife[i][0]==namesplit2[1] and halflife[i][1]==namesplit2[2].upper():
            activity_lamda = np.log(2) / float(halflife[i][10]) # per second
            target_particle_per_area = activity_bq / activity_lamda / 1 #per cm^2
            x0 = target_particle_per_area * (A/Na) * 1e3 #mg per cm^2
            if x0<thickness:
                x=x0
            else:
                x=thickness
            print('adjusted thickness '+''+namesplit[1]+' '+str(x))
        else:
            x=thickness
    return x

#calculate reaction rate from cross section, input and output are both just a number
def RateFromCross(cross, filename, x):

    # A = atomic mass of the target in g / mol
    # x = mass per surface, target thickness in mg / cm ^ 2
    # Ip = primary beam current in puA, p means particle charge is 1
    # q = elementary charge in C
    # data = {Z, N, sigma}, where sigma is the cross - section in mbarn = 10 ^ -27 cm ^ 2
    # eff = extraction efficiency
    # Na = Avogadro's number in atoms/mol

    A = int(FindA(filename))
    # print(A)
    # x0 = 10
    Ip = 0.5 # 500 pnA for proposals
    eff = 0.075 # Normally 0.15
    # x=ModifyX(filename,x0)

    Na = 6.022e23
    q = 1.602e-19

    incident_particle_rate=Ip * 1e-6/ q #paricle/s
    cross_section=cross * 1e-3 * 1e-24 #cm^2
    target_particle_per_area=x * 1e-3 / (A/Na)   #particle/cm^2

    scattered_particle_rate=incident_particle_rate * cross_section * target_particle_per_area *eff #particle/s
    # print(scattered_particle_rate)

    return scattered_particle_rate

#extract A from filename
def FindA(filename):
    namesplit=filename.split('_')
    # print(namesplit)
    namesplit2=re.split('(\d+)',namesplit[1])
    A=namesplit2[1]
    return A

#write to the output file
def ConvertFile(filename):
    # data format:
    # 0           1        2
    # charge  neutron cross section

    data=ImportData(filename)
    # FindA(filename)

    x=ModifyX(filename)

    ratelist=[]

    for i in range (0,len(data)-1+1):
        ratelist.append(RateFromCross(data[i][2],filename,x))
    
    filename = filename[7:]
    namesplit = filename.split('_')

    f = open("output.txt", "a")
    for i in range(0, len(data) - 1 + 1):
        # f.write("%d",% (data[i][0]))
        f.write(str(int(data[i][1]))+' '+str(int(data[i][0]))+' '+str(ratelist[i])+' '+ namesplit[0] +'+' +namesplit[1]+ '\n')
    f.close()


    # open and read the file after the appending:
    # f = open("output.txt", "r")
    # print(f.read())

#loop through all data file in the Data folder
def AllFile(generated_file):
    filenamearr = FileName(generated_file)
    for i in range(len(filenamearr)):
        ConvertFile(filenamearr[i])


# def Halflife(cross,filename):
#
#
#     # A = atomic mass of the target in g / mol
#     # x = mass per surface, target thickness in mg / cm ^ 2
#     # Ip = primary beam current in puA, p means particle charge is 1
#     # q = elementary charge in C
#     # data = {Z, N, sigma}, where sigma is the cross - section in mbarn = 10 ^ -27 cm ^ 2
#     # eff = extraction efficiency
#     # Na = Avogadro's number in atoms/mol
#
#     A = int(FindA(filename))
#     # print(A)
#     x0 = 10
#     Ip = 5
#     eff = 0.15
#     # x=ModifyX(x0)
#
#     Na = 6.022e23
#     q = 1.602e-19
#
#     incident_particle_rate=Ip * 1e-6/ q #paricle/s
#     cross_section=cross * 1e-3 * 1e-24 #cm^2
#     target_particle_per_area=x * 1e-3 / (A/Na)   #particle/cm^2
#
#     # activity below 50mCi/cm^2
#     activity_ci = 50e-3
#     activity_bq = activity_ci * 3.7e10  # per second
#     activity_lamda = activity_bq / target_particle_per_area #per second per cm^2
#     halflife=np.log(2)/activity_lamda
#     # hallifelist=[]
#     # hallifelist.append(halflife)
#     return halflife

def SortOutput():
    data=np.genfromtxt('output.txt', dtype='str')
    df=pd.DataFrame(data, columns = ['n', 'p', 'rate' , 'reaction'])
    df = df.astype({'n': int, 'p': int})
    df.sort_values(by=['n','p'], inplace=True)
    df.to_csv(r'./sortedoutput.csv', index=False)


if __name__ == '__main__':
    AllFile(output_file)
    # SortOutput()

    # f = open("output.txt", "w")
    # f.close()


    # ConvertFile('136Xe_241Am_9.txt')

    # ConvertFile(filenamearr[0])
