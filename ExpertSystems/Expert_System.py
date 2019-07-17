from pyknow import *

def expert1():
    LowOfSuger = ["shakiness", "hunger", "sweating", "headache", "pale"]
    HighOfSuger = ["thirst", "blurred vision", "headache", "dry mouth", "smelling breath", "shortness of breath"]
    listinput = list()

    def checkAge(age):
        if int(age) < 6:
            return 1
        else:
            return 0
    def checkSuger(check):
        if check > 2:
            return 1
        else:
            return 0
    def check(NameOfCheck):
        count = 0
        for i in listinput:
            for j in NameOfCheck:
                if i == j:
                    count += 1
        if count > 2:
            return 1
        else:
            return 0


    class Patient(Fact):
        pass


    class Doctor(KnowledgeEngine):
        @Rule(AND(Patient(age=1, low=1)))
        def Low_Suger(self):
            print("he/she has signs of low sugar.")

        @Rule(Patient(age=1,high=1))
        def High_Suger(self):
            print("he/she has signs of High sugar.")

        @Rule((Patient(age=1,low=1,diabeticparents="t")))
        def diabetic_parents(self):
            print("the patient could be diabetic")

        @Rule((Patient(runnynose="t",harshcough="t")))
        def has_cold(self):
            print("patient has signs of cold")

        @Rule((Patient(age=1 , runnynose="t", harshcough="t", brownishpinkrash="t", highandfasttemperature="t"
                          ,bloodshoteyes="t", whitespots="t")))
        def has_cold1(self):
            print(" he/she has a measles.")

        @Rule((Patient(age=1 , moderatetemperature="t" , salivaNotnormal="t", swollenlymphnodesneck="t", mouthdry="t"))
                )
        def has_cold2(self):
            print(" he/she has mumps")

        @Rule((Patient(age=1, runnynose="t", harshcough="t", conjunctives="t", strongbodyaches="t", weakness="t",
                       sorethroat="t", sneezing="t")))
        def has_cold3(self):
            print("he/she has a child-flu ")

        @Rule((Patient(age=0, runnynose="t" ,  harshcough="t",  conjunctives="t",  strongbodyaches="t",  weakness="t", sorethroat="t",  sneezing="t")))
        def has_cold4(self):
            print("he/she has a adult-flu ")


    engine = Doctor()
    engine.reset()
    CountLowOfSuger = 0
    CountHighOfSuger = 0
    a=int(input("Enter Your Age "))
    for i in LowOfSuger:
        print("Are You have " + i + " T or F")
        x = input()
        if x == "t":
            CountLowOfSuger += 1

    for i in HighOfSuger:
        print("Are You have " + i + " T or F")
        x = input()
        if  x == "t":
            CountHighOfSuger += 1
    print(CountLowOfSuger)
    print(CountHighOfSuger)
    engine.declare(Patient( age=int(checkAge(a)),low=checkSuger(CountLowOfSuger), high=checkSuger(CountHighOfSuger)
                           , diabeticparents=input("you have diabeticparents T or F"),
                           runnynose=input("you have runny nose T or F"),
                           harshcough=input("you have harshcough T or F"),
                           brownishpink_rash=input("you have browing_pink_rash T or F"),
                           highandfasttemperature=input("you have high and fast temperature T or F"),
                           bloodshoteyes=input("you have blood shot eyes T or F"),
                           whitespots=input("you have white spots T or F"),
                           moderatetemperature=input("you have moderate temperature T or F"),
                           salivaNotnormal=input("are your saliva not normal  T or F"),
                           swollenlymphnodesneck=input("are your swollen lymphnodes in neck T or F"),
                           conjunctives=input("you have conjunctives T or F "),
                           strongbodyaches=input("you havestrong body aches"),
                           weakness=input("you have weakness T or F "),
                           sorethroat=input("you have sore throat T or F "),
                           sneezing=input("you have sneezing T or F "),
                           mouthdry=input("you have mouth dry T or F")
                           ))
    engine.run()



def expert2():
    high_temperaturelist = ['normal', 'high', 'low']

    class Plant(Fact):
        pass

    class Doctor1(KnowledgeEngine):
        @Rule(AND(Plant(high_temperature="high", humidity="normal", tupercolor="reddish brown", tuperhas="spots")))
        def Black_Heart(self):
            print("the plant has black heart.")

        @Rule(AND(Plant(high_temperature="low", humidity="high", tuperstatue="normal", tuperhas="spots")))
        def Late_Blight(self):
            print("the plant has late blight.")

        @Rule(AND(Plant(high_temperature="high", humidity="normal", tuperstatue="dry", tuperhas="circles")))
        def Dry_Rot(self):
            print("the plant has dry rot.")

        @Rule(AND(Plant(high_temperature="normal", humidity="normal", tupercolor="brown", tuperhas=" wrinkles ")))
        def Early_Blight(self):
            print("the plant has early blight.")

    engine = Doctor1()
    engine.reset()
    engine.declare(Plant(high_temperature=input("how your ( temperature ) enter(normal,high,low ) ?").lower()
                         , humidity=input("how your( humidity ) enter(normal , high) ?").lower(),
                         tupercolor=input("waht is color of( tuber ) enter(reddish brown , brown ,unknown)").lower(),
                         tuperstatue=input("waht is statue of( tuber ) enter(dry , normal ,unknown)").lower(),
                         tuperhas=input("waht is your (tuber) has  enter(circles , wrinkles ,spots,unknown)").lower()))
    engine.run()


x = input("choose expert 1 or 2")
if(x == "1"):
    expert1()
else:
    expert2()