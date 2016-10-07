import sys, maxwalksat, simulatedannealer,de

file = "osyczka.xml"
#file = "schaffer.xml"
#file = "Kursawe.xml"
#print("\n",maxwalksat.mws(file))
#print("\n",simulatedannealer.annealer(file))
print(de.diffevolve(file))
print("Done")