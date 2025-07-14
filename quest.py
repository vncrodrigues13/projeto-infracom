import random




def get_next_question(previous_one):
   curr_quest = random.randint(0, len(quests))
   while curr_quest == previous_one:
       curr_quest = random.randint(0, len(quests))
   return quests[curr_quest]




quests = [
   {
       'quest': 'Qual é a capital do Brasil?',
       'awnser': 'B',
       'options': [{'A': 'São Paulo'}, {'B': 'Brasília'}, {'C': 'Rio de Janeiro'}, {'D': 'Salvador'}]
   },
   {
       'quest': 'Qual é o elemento químico representado por H?',
       'awnser': 'A',
       'options': [{'A': 'Hidrogênio'}, {'B': 'Hélio'}, {'C': 'Hidroxila'}, {'D': 'Hematita'}]
   },
   {
       'quest': 'Quem escreveu "Dom Casmurro"?',
       'awnser': 'C',
       'options': [{'A': 'José de Alencar'}, {'B': 'Carlos Drummond'}, {'C': 'Machado de Assis'},
                   {'D': 'Clarice Lispector'}]
   },
   {
       'quest': 'Qual planeta é o terceiro a partir do Sol?',
       'awnser': 'D',
       'options': [{'A': 'Vênus'}, {'B': 'Marte'}, {'C': 'Mercúrio'}, {'D': 'Terra'}]
   },
   {
       'quest': 'Em que continente fica o Egito?',
       'awnser': 'A',
       'options': [{'A': 'África'}, {'B': 'Ásia'}, {'C': 'Europa'}, {'D': 'América'}]
   },
   {
       'quest': 'Qual é o maior oceano do mundo?',
       'awnser': 'B',
       'options': [{'A': 'Atlântico'}, {'B': 'Pacífico'}, {'C': 'Índico'}, {'D': 'Ártico'}]
   },
   {
       'quest': 'Quanto é 9 x 7?',
       'awnser': 'C',
       'options': [{'A': '56'}, {'B': '72'}, {'C': '63'}, {'D': '67'}]
   },
   {
       'quest': 'Qual destes é um mamífero?',
       'awnser': 'A',
       'options': [{'A': 'Golfinho'}, {'B': 'Pinguim'}, {'C': 'Tubarão'}, {'D': 'Camarão'}]
   },
   {
       'quest': 'Quem foi o primeiro homem a pisar na Lua?',
       'awnser': 'D',
       'options': [{'A': 'Buzz Aldrin'}, {'B': 'Yuri Gagarin'}, {'C': 'Michael Collins'}, {'D': 'Neil Armstrong'}]
   },
   {
       'quest': 'Qual língua é falada no Japão?',
       'awnser': 'B',
       'options': [{'A': 'Chinês'}, {'B': 'Japonês'}, {'C': 'Coreano'}, {'D': 'Tailandês'}]
   }
]

