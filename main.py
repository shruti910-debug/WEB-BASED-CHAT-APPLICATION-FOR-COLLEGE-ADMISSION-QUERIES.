from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer


chatbot = ChatBot("sam", logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'threshold': 0.65,
            'default_response': 'default_value'
        }
    ],)

exit_conditions = (":q", "quit", "exit")

conversationData = []



def getQandA():
    while True:
        userQuery = input("To continue type 'yes' to exit type 'exit' : ")
        if userQuery == 'exit':
            break
        else:
            userQuestion = input("Enter question : ")
            userAnswer = input("Enter answer : ")
            conversationData.append(userQuestion)
            conversationData.append(userAnswer)



def trainChatBot():
    getQandA()
    trainer = ListTrainer(chatbot)
    trainer.train(conversationData)


def startChatbot():
    while True:
        query = input("> ")
        if query in exit_conditions:
            break
        else:
            resp = chatbot.get_response(query)
            if(resp.text == "default_value"):
                print("contact support")
            else:
                print(f"{resp.text}")


userInput = int(input("Press 1 to start bot \nPress 2 to train bot"))

if userInput == 1:
    startChatbot()
else:
    trainChatBot()
