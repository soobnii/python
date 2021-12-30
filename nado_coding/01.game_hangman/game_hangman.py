
import random

fruit = ["apple","banana","orange"]
answer = random.choice(fruit)
result = ""
value = ""

while True:
	result =  "".join(result)
	for index in range(0, len(answer)) :
		if(value == ""):
			result += "_"
		elif(value == answer[index]):
			result = list(result)
			result[index] = value

	print(" ".join(result))
	
	if("_" not in result):
		print("Success")
		break
	value = input("INPUT >> ")
	if(value in answer):
		print("Correct")
	else:
		print("Wrong")
