print("Welcome to Quiz game *_* \n ")
player=input("Do you want to play?")
if(player.lower()=="yes"):
    print("ok let's play \n")
else:
    quit()
print("The no of questions is  5 \n")

score=0

question=input("Question 1: How many days in a week? ")
if(question.lower()=="seven"):
    print("correct")
    score=score+1
    
else:
    print("wrong")
print("\n ")


question=input("Question 2: Which animal is known as the 'Ship of the Desert' ?")
if(question.lower()=="camel"):
    print("correct")
    score=score+1
    
else:
    print("wrong")
print("\n ")


question=input("Question 3: How many hours are there in a day?")
if(question.lower()=="24 hours"):
    print("correct")
    score=score+1
    
else:
    print("wrong")
print("\n ")



question=input("Question 4: Rainbow consist of how many colours?")
if(question.lower()=="seven"):
    print("correct")
    score=score+1
    
else:
    print("wrong")

print("\n ")


question=input("Question 5: How many letters are there in the English alphabet?")
if(question.lower()=="26 letters"):
    print("correct")
    score=score+1
    print("congrats! Your Total score is :"+ str(score))
else:
    print("wrong")
print("\n ")

questionno=5
if(questionno==5):
    print("You are win !!")
else:
    print("sorry better luck next time")
