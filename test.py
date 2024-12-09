with open ('frequency.txt', 'r', encoding='utf8') as file:
    t = file.read()
value = t.split('\n')
    
letter_count = {}

for v in value:
    for i in v:
        if i in letter_count:
            letter_count[i] += 1
        else:
            letter_count[i] = 1

most_common_letter = list(dict(sorted(letter_count.items(), key=lambda item: item[1], reverse=True)))
most_common_letter= most_common_letter[:6]

def mots_valides(liste_mots, lettres):
    

print(mots_valides(value, most_common_letter))

