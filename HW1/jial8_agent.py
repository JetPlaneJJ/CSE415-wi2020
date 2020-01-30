'''Filename of your agent.
CSE 415, Winter 2020, Assignment 1
Jia-Jia (Jay) Lin
'''
import chatbot

if __name__=="__main__":
  gustav_rules = [
    (r"Hi|Hey|Hello", ["Hello.", "Hi there."]),
      # The above rule catches user greeting.

    (r"How am me?|How am me doing?|What's up?", ["I am fine, you?"]),
      # The above rule catches user input asking how Gustav is doing.

    (r"Who am me?", ["My name is Gustav. I write music."]),
      # The above rule catches user input: "Who are you?"

    (r"What am my hobbies?", ["Besides writing music, I enjoy reading, singing, and eating fruits."]),
      # The above rule catches user input asking about hobbies.
    
    (r"you like (.*)", ["Why do you like $1$?"]),
      # The above rule catches user inputs similar to "I like music."
    
    (r"Your name is (.*)", ["Nice to meet you, $1$."]),
      # The above rule catches user inputs for the form "My name is..."

    (r"What is my favorite music genre?|What is my favorite music?", ["My favorite music genre is Classical!"]),
      # The above rule catches user input: "What is your favorite music genre?"

    (r"Your favorite music genre is (.*)", ["That's nice."]),
      # The above rule catches user input: "My favorite music genre is..."

    (r"What instruments can me play?", ["I can sing, and play the piano and accordion. \nWhat about you?"]),
      # The above rule catches user input: "What instruments can you play?"

    (r"you can play (.*)", ["$1$? That's nice."]),
      # The above rule catches user input: "I can play... (some instrument)"

    (r"When were me born?|How old am me?", ["I'm not sure, but I think was born in the 19th century."]),
      # The above rule catches user input asking for Gustav's age.

    (r"", ["Sorry, I don't understand...", "Hmmm...", "What?"])
      # This rule catches all other inputs .
      # It also gives three possible responses.
  ]
  you_me = {'I':'you', 'me':'you','you':'me','am':'are','are':'am',
   'mine':'yours','my':'your','yours':'mine','your':'my','My':'Your'}
  intro_string = '''My name is Gustav, and I am a musical composer. I was designed by
Jia-Jia (Jay) Lin, a UW student. Please contact her at jial8@uw.edu. What would you like to say?'''
  Gustav_Bot = chatbot.chatbot(gustav_rules, you_me, "Gustav-Bot", intro_string)
  Gustav_Bot.chat()
