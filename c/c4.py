#!/usr/bin/python3

age = int(input("input number："))
print("")
if age < 0:
    print("kidding")
elif age == 1:
    print("almost 14")
elif age == 2:
    print("almost 22")
elif age > 2:
    tage = 22 + (age - 2) * 5
    print("almost:", tage)
##exit
input("input exit")
