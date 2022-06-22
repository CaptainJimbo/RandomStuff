print("Caesar's cipher shifts each letter by a number of letters. If the shift takes you past the end of the alphabet, just rotate back to the front of the alphabet. In the case of a rotation by 3, w, x, y and z would map to z, a, b and c.\n")

def caesarCipher(s, k):
    # Write your code here
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    alphabet_rotated = alphabet[k%26:]+alphabet[:k%26]
    s_rotated = ''
    for i in range(len(s)):
        if alphabet.find(s[i])==-1 and alphabet.upper().find(s[i].upper())==-1:
            s_rotated += s[i]
        else:
            if s[i].isupper():
                s_rotated += alphabet_rotated[alphabet.find(s[i].lower())].upper()
            else:
                s_rotated += alphabet_rotated[alphabet.find(s[i])]
    return s_rotated

print('type message...\n')
s = input()
print('\ntype number of shift...\n')
k = int(input().strip())
print('\n')
print(caesarCipher(s, k))
print('\n')
