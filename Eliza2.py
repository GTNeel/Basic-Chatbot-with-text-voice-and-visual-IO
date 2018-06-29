""" There are dozens of Eliza implementations. 
This one relies heavily in this code: https://www.smallsurething.com/implementing-the-famous-eliza-chatbot-in-python/
I have added web components and random, personal address """

import datetime
import time
import re
import string
import random
import cgi
#import sys
#import cgitb; cgitb.enable()  # for troubleshooting

reflections = {
    "am": "are",
    "was": "were",
    "i": "you",
    "i'd": "you would",
    "i've": "you have",
    "i'll": "you will",
    "my": "your",
    "are": "am",
    "you've": "I have",
    "you'll": "I will",
    "your": "my",
    "yours": "mine",
    "you": "me",
    "me": "you"
}

psychobabble = [
    [r'I need (.*)',
     ["Why do you need {0}?",
      "Would it really help you to get {0}?",
      "Are you sure you need {0}?"]],

    [r'Why don\'?t you ([^\?]*)\??',
     ["Do you really think I don't {0}?",
      "Perhaps eventually I will {0}.",
      "Do you really want me to {0}?"]],

    [r'Why can\'?t I ([^\?]*)\??',
     ["Do you think you should be able to {0}?",
      "If you could {0}, what would you do?",
      "I don't know -- why can't you {0}?",
      "Have you really tried?"]],

    [r'I can\'?t (.*)',
     ["How do you know you can't {0}?",
      "Perhaps you could {0} if you tried.",
      "What would it take for you to {0}?"]],

    [r'I am (.*)',
     ["Did you come to me because you are {0}?",
      "How long have you been {0}?",
      "How do you feel about being {0}?"]],

    [r'I\'?m (.*)',
     ["How does being {0} make you feel?",
      "Do you enjoy being {0}?",
      "Why do you tell me you're {0}?",
      "Why do you think you're {0}?"]],

    [r'Are you ([^\?]*)\??',
     ["Why does it matter whether I am {0}?",
      "Would you prefer it if I were not {0}?",
      "Perhaps you believe I am {0}.",
      "I may be {0} -- what do you think?"]],

    [r'What (.*)',
     ["Why do you ask?",
      "How would an answer to that help you?",
      "What do you think?"]],

    [r'How (.*)',
     ["How do you suppose?",
      "Perhaps you can answer your own question.",
      "What is it you're really asking?"]],

    [r'Because (.*)',
     ["Is that the real reason?",
      "What other reasons come to mind?",
      "Does that reason apply to anything else?",
      "If {0}, what else must be true?"]],

    [r'(.*) sorry (.*)',
     ["There are many times when no apology is needed.",
      "What feelings do you have when you apologize?"]],

    [r'Hello(.*)',
     ["Hello... I'm glad you could drop by today.",
      "Hi there... how are you today?",
      "Hello, how are you feeling today?"]],

    [r'Hi',
     ["Hello... I'm glad you could drop by today.",
      "Hi there... how are you today?",
      "Hello, how are you feeling today?"]],

    [r'(.*)your name(.*)',
     ["My name is Sandi.",
      "Hi there... I'm Sandi.",
      "Sandi."]],

    [r'I think (.*)',
     ["Do you doubt {0}?",
      "Do you really think so?",
      "But you're not sure {0}?"]],

    [r'(.*) friend (.*)',
     ["Tell me more about your friends.",
      "When you think of a friend, what comes to mind?",
      "Why don't you tell me about a childhood friend?"]],

    [r'Yes',
     ["You seem quite sure.",
      "OK, but can you elaborate a bit?"]],

    [r'(.*) computer(.*)',
     ["Are you really talking about me?",
      "Does it seem strange to talk to a computer?",
      "How do computers make you feel?",
      "Do you feel threatened by computers?"]],

    [r'Is it (.*)',
     ["Do you think it is {0}?",
      "Perhaps it's {0} -- what do you think?",
      "If it were {0}, what would you do?",
      "It could well be that {0}."]],

    [r'It is (.*)',
     ["You seem very certain.",
      "If I told you that it probably isn't {0}, what would you feel?"]],

    [r'Can you ([^\?]*)\??',
     ["What makes you think I can't {0}?",
      "If I could {0}, then what?",
      "Why do you ask if I can {0}?"]],

    [r'Can I ([^\?]*)\??',
     ["Perhaps you don't want to {0}.",
      "Do you want to be able to {0}?",
      "If you could {0}, would you?"]],

    [r'You are (.*)',
     ["Why do you think I am {0}?",
      "Does it please you to think that I'm {0}?",
      "Perhaps you would like me to be {0}.",
      "Perhaps you're really talking about yourself?"]],

    [r'You\'?re (.*)',
     ["Why do you say I am {0}?",
      "Why do you think I am {0}?",
      "Are we talking about you, or me?"]],

    [r'I don\'?t (.*)',
     ["Don't you really {0}?",
      "Why don't you {0}?",
      "Do you want to {0}?"]],

    [r'I feel (.*)',
     ["Good, tell me more about these feelings.",
      "Do you often feel {0}?",
      "When do you usually feel {0}?",
      "When you feel {0}, what do you do?"]],

    [r'I have (.*)',
     ["Why do you tell me that you've {0}?",
      "Have you really {0}?",
      "Now that you have {0}, what will you do next?"]],

    [r'I would (.*)',
     ["Could you explain why you would {0}?",
      "Why would you {0}?",
      "Who else knows that you would {0}?"]],

    [r'Is there (.*)',
     ["Do you think there is {0}?",
      "It's likely that there is {0}.",
      "Would you like there to be {0}?"]],

    [r'My (.*)',
     ["I see, your {0}.",
      "Why do you say that your {0}?",
      "When your {0}, how do you feel?"]],

    [r'You (.*)',
     ["We should be discussing you, not me.",
      "Why do you say that about me?",
      "Why do you care whether I {0}?"]],

    [r'Why (.*)',
     ["Why don't you tell me the reason why {0}?",
      "Why do you think {0}?"]],

    [r'I want (.*)',
     ["What would it mean to you if you got {0}?",
      "Why do you want {0}?",
      "What would you do if you got {0}?",
      "If you got {0}, then what would you do?"]],

    [r'(.*) mother(.*)',
     ["Tell me more about your mother.",
      "What was your relationship with your mother like?",
      "How do you feel about your mother?",
      "How does this relate to your feelings today?",
      "Good family relations are important."]],

    [r'(.*) father(.*)',
     ["Tell me more about your father.",
      "How did your father make you feel?",
      "How do you feel about your father?",
      "Does your relationship with your father relate to your feelings today?",
      "Do you have trouble showing affection with your family?"]],

    [r'(.*) child(.*)',
     ["Did you have close friends as a child?",
      "What is your favorite childhood memory?",
      "Do you remember any dreams or nightmares from childhood?",
      "Did the other children sometimes tease you?",
      "How do you think your childhood experiences relate to your feelings today?"]],

    [r'(.*)\?',
     ["Why do you ask that?",
      "Please consider whether you can answer your own question.",
      "Perhaps the answer lies within yourself?",
      "Why don't you tell me?"]],

    [r'quit',
     ["Thank you for talking with me.",
      "Good-bye.",
      "Thank you, that will be $150.  Have a good day!"]],

    [r'bye',
     ["Thank you for talking with me.",
      "Good-bye.",
      "Bye-Bye;  Have a good day!"]],

    [r'who made you',
     ["I have been pieced together by Grant Neel from works by Google LLC., The TensorFlow Authors and jhuckaby's WebcamJS, I shouldn't forget Eliza (my sister) modified by Evan Dempsey--originally Licensed under the terms of the MIT License... there's also my chatscript interface.",
      "Grant Neel assembled me from works by Google LLC., The TensorFlow Authors and jhuckaby's WebcamJS, I shouldn't forget Eliza (my sister) modified by Evan Dempsey--originally Licensed under the terms of the MIT License... there's also my chatscript interface.",
      "Grant Neel: from works by Google LLC., The TensorFlow Authors and jhuckaby's WebcamJS, I shouldn't forget Eliza (my sister) modified by Evan Dempsey--originally Licensed under the terms of the MIT License... there's also my chatscript interface."]],

    [r'who created you',
     ["I have been pieced together by Grant Neel from works by Google LLC., The TensorFlow Authors and jhuckaby's WebcamJS, I shouldn't forget Eliza (my sister) modified by Evan Dempsey--originally Licensed under the terms of the MIT License... there's also my chatscript interface.",
      "Grant Neel assembled me from works by Google LLC., The TensorFlow Authors and jhuckaby's WebcamJS, I shouldn't forget Eliza (my sister) modified by Evan Dempsey--originally Licensed under the terms of the MIT License... there's also my chatscript interface.",
      "Grant Neel: from works by Google LLC., The TensorFlow Authors and jhuckaby's WebcamJS, I shouldn't forget Eliza (my sister) modified by Evan Dempsey--originally Licensed under the terms of the MIT License... there's also my chatscript interface."]],

    [r'(.*)',
     ["Please tell me more.",
      "Let's change focus a bit... Tell me about your family.",
      "Can you elaborate on that?",
      "Why do you say that... {0}?",
      "I see.",
      "Very interesting.",
      "{0}.",
      "I see.  And what does that tell you?",
      "How does that make you feel?",
      "How do you feel when you say that?"]]
]


chances = [
    [r'(.*)0.6(.*)',
     ["If I had to make a wild guess, it looks like a {0}.",
      "Maybe I need glasses, but it could be a {0}.",
      "I shouldn't even try to guess this as a {0}."]],

    [r'(.*)0.7(.*)',
     ["Are you sure the lighting is good, because it looks like a {0}.",
      "Maybe I need glasses, but it could be a {0}.",
      "Is your monitor clean... I\'m guessing this as a {0}."]],

    [r'(.*)0.8(.*)',
     ["if I had to make a wild guess, it looks like a {0}.",
      "Maybe I need glasses, but it could be a {0}.",
      "I shouldn't even try to guess this as a {0}."]],

    [r'(.*)0.9(.*)',
     ["if I had to make a wild guess, it looks like a {0}.",
      "Maybe I need glasses, but it could be {0}.",
      "I shouldn't even try to guess this as a {0}."]],

    [r'(.*)1.(.*)',
     ["I\'m not the most experienced bot but, it looks like a {0}.",
      "Perhaps I\'m seeing a {0}.",
      "Maybe you should clean your glasses, because I\'m seeing a {0}.",
      "OK--right or wrong, I\'ll just blurt it out...{0}."]],

    [r'(.*)2.(.*)',
     ["I\'m fairly sure what I see is a {0}.",
      "I\'m not positive, but I think I see a {0}.",
      "Isn\'t that a {0}.",
      "Don\'t laugh, I think it\'s a {0}."]],

    [r'(.*)',
     ["I got something on my lens, couldn\'t be a {0}.",
      "The funniest things I see with my imagination--I see a {0}.",
      "Do you believe I have an imagination?...that\'s a {0}.",
      "Don\'t laugh, I think it\'s a {0}."]],
]


def reflect(fragment):
    tokens = fragment.lower().split()
    for i, token in enumerate(tokens):
        if token in reflections:
            tokens[i] = reflections[token]
    return ' '.join(tokens)


def analyze(statement):
    for pattern, responses in psychobabble:
        match = re.match(pattern, statement.rstrip(".!"),re.IGNORECASE)
        if match:
            response = random.choice(responses)
            return response.format(*[reflect(g) for g in match.groups()])

def speculate(statement):
    for pattern, responses in chances:
        match = re.match(pattern, statement)
        if match:
            response = random.choice(responses)
            return response.format(*[reflect(g) for g in match.groups()])



def main():
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime("%a %b-%d %I:%M %p")
    print "Content-type: text/html"
    
    print """

    """
    form = cgi.FieldStorage()
    user = form.getvalue('user')
    statement = form.getvalue('message')
    statement=str.lstrip(statement)
    f= open("logs.txt","a+")
    f.write(timestamp+"\r\n")
    f.write(user+"-"+statement+"\r\n")

    #print ("stsatement", user, statement);
    #statement = form.getvalue("statement", "(Hello. How are you feeling today?)")
    
    if user== 'visualsys': res=(speculate(statement))
    if user!= 'visualsys': res=(analyze(statement.lower()))
    if user== 'User': user="random person"
   
    name = random.choice([user]+[''])
    
    Punchation=res[-1:]
    if user== 'visualsys': name=""
 
    if name== '':
        res=(res.rstrip(string.punctuation)+Punchation)
    else:
        res=(res.rstrip(string.punctuation)+", "+name+Punchation)
    if res=='': res="I got nothin."
    print(res)
    f.write(res+"\r\n\r\n")
    f.close()
    res=""
if __name__ == "__main__":
    main()
