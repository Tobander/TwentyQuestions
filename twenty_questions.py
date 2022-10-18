import textwrap
import openai
import re
from time import time,sleep
from uuid import uuid4
from random import seed, sample

# Funktion, um Files zu öffnen
def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

# Funktion, um Files zu speichern
def save_file(content, filepath):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)
        
# API Key für OpenAI
openai.api_key = open_file('openaiapikey.txt')

# Funktion, um GPT-3 aufzurufen
def gpt3_completion(prompt, engine='text-davinci-002', temp=1.2, top_p=1.0, tokens=100, freq_pen=0.0, pres_pen=0.0, stop=['\n']):
    max_retry = 5
    retry = 0
    while True:
        try:
            response = openai.Completion.create(
                engine=engine,
                prompt=prompt,
                temperature=temp,
                max_tokens=tokens,
                top_p=top_p,
                frequency_penalty=freq_pen,
                presence_penalty=pres_pen,
                stop=stop)
            text = response['choices'][0]['text'].strip()
            text = re.sub('\s+', ' ', text)
            filename = '%s_gpt3.txt' % time()
            with open('gpt3_logs/%s' % filename, 'w') as outfile:
                outfile.write('PROMPT:\n\n' + prompt + '\n\n==========\n\nRESPONSE:\n\n' + text)
            return text
        except Exception as oops:
            retry += 1
            if retry >= max_retry:
                return "GPT3 error: %s" % oops
            print('Error communicating with OpenAI:', oops)
            sleep(1)
       
# Main Function
if __name__ == '__main__':
    # ToDo choose difficulty
    
    # Random Number
    seed()
    # Einlesen in kommagetrennte Liste
    seed_words = open_file('common_words.txt').splitlines()
    # Wähle 10 random Wörter aus
    sampling = sample(seed_words, 10)
    prompt = str(uuid4())
    for s in sampling:
        prompt = prompt + '\nPick a random word: %s' % s
    prompt = prompt + '\nPick a random word:'
    secret_word = gpt3_completion(prompt)
    #print('DEBUG: %s' % secret_word)
    questions_remaining = 20
    print('I have picked my secret word. Ask your first question... (questions remaining: %s)' % questions_remaining)
    while True:
        question = input('Question: (%s): ' % questions_remaining)
        prompt = open_file('prompt_valid.txt').replace('<<QUESTION>>', question)
        is_valid = gpt3_completion(prompt, temp=0.0)
        if is_valid == 'False':
            print('That is not a valid question!')
        elif is_valid == 'True':
            prompt = open_file('prompt_answer.txt').replace('<<SECRET>>', secret_word).replace('<<QUESTION>>', question)
            answer = gpt3_completion(prompt)
            # Wenn Antwort richtig, Spiel exit, ansonsten, wieder Answer ausgeben
            if answer == 'Correct':
                print('Congrats!')
                exit(0)      
            print('Answer: %s' % answer)
                
        else:
            print('Sorry, GPT-3 is confused')
            continue
        
        questions_remaining = questions_remaining - 1
        if questions_remaining <= 0:
            print('Game Over! The correct answer was: %s' % secret_word)
            exit(0)
            
            
            
            
            
            
            
            