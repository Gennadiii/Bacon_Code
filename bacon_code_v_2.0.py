class BaconCode(object):
    '''
    Class BaconCode codes and decodes text using Bacon algorithm
    Method __init__ excepts no arguments
    '''
    global list_of_keys
    global text_exception
    global language_slovar

    list_of_keys = [' 3570124689',
                    ' qwertyuiopasdfghjklzxcvbnm',
                    ' йцукенгшщзхфывапролджячсмитьбюё',
                    ' йцукенгшщзхїфівапролджячсмитьбю',
                    ' !@#$%^&*()0123456789/*-+,.:;=qwertyuiopasdfghjklzxcvbnm', 
                    ' !@#$%^&*()0123456789/*-+,.:;=йцукенгшщзхъфывапролджэячсмитьбюё', 
                    ' !@#$%^&*()0123456789/*-+,.:;=йцукенгшщзхїфівапролджєячсмитьбю',
                    ' !@#$%^&*()0123456789/*-+,.:;abcdefghijklmnopqrstuvwxyzQWERTYUIOPASDFGHJKLZXCVBNM=',
                    ' !"№%?*()0123456789/*-+,.:;йцукенгшщзхъфывапролджэячсмитьбюёЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮЁ=',
                    ' !"№%?*()0123456789/*-+,.:;йцукенгшщзхїфівапролджєячсмитьбюЙЦУКЕНГШЩЗХЇФІВАПРОЛДЖЄЯЧСМИТЬБЮ=']  

    text_exception = ',.!@#№"\';:?$%^&() /*-+0123456789'

    hint = '''
If you want to send a secret message just choose '1' and input your secret in English, Russian or Ukrainian.
Numbers and symbols are also supported.
Them I'll ask you to input a random text which can be anything.
I'll change register of letters in this text and that will be your code.
The simplier secret you encode (like without capital letters or sumbols) the fewer letters I'll need in text.
Let's see how it works:
A woman says to a man: 
HONEY, dOn't wAsTE mONEy ON jewelry. i HAvE eNouGH oF tHat. lEt'S Buy you a new laptop instead. you need it for work.
But the question is - will he understand her?
PS She really says: 'new ring' ;)
    '''

    def slovar_for_language(self):
        '''
        Returns 2 dictionaries. First one for encoder and the second one reverted for decoder. Doesn't take arguments.
        '''
        self.language_slovar_1 = {}
        self.language_slovar_2 = {}
        key = 'aaaabbbbabbaa'
        alphabet = '0123456789'
        j = 0 # Creating a dictionary from a key with alphabet as dictionaries keys
        for i in alphabet:
            self.language_slovar_1[int(i)] = key[j:j+4]
            j+=1

        self.language_slovar_2 = {self.language_slovar_1[i]: i for i in self.language_slovar_1}
        # Creating a dictionary from a key with letters as dictionaries keys
        return self.language_slovar_1, self.language_slovar_2      

    def create_key(self, language):
        '''
        This method generates ab-key, takes 1 parametr - language which decides the length of key
        '''
        global key_len # ab group length

        if language == 0:
            key_len = 4
        elif language < 4:
            key_len = 5
        elif 3 < language < 7:
            key_len = 6
        else:
            key_len = 7

        self.key = 'a' * key_len # Generate key. To 'a'*key_len add 'b' if this group exists, delete 'b' and add 'a'
        temp_list_of_keys = [self.key]
        while len(self.key) != key_len - 1 + len(list_of_keys[language]):
            self.key += 'b'
            if self.key[-key_len:] in temp_list_of_keys:
                self.key = self.key[:-1]
                self.key += 'a'
                if self.key[-key_len:] in temp_list_of_keys:
                    self.key = self.key[:-1]
            temp_list_of_keys.append(self.key[-key_len:]) # Adds key to temp list of keys

        return self.key

    def slovar(self):
        '''
        Returns 2 dictionaries. First one for encoder and the second one reverted for decoder. Doesn't take arguments.
        '''
        self.slovar_1 = {}
        self.slovar_2 = {}
        j = 0 # Creating a dictionary from a key with alphabet as dictionaries keys
        for i in list_of_keys[language]:
            self.slovar_1[i] = self.key[j:j+key_len]
            j+=1

        self.slovar_2 = {self.slovar_1[i]: i for i in self.slovar_1}
        # Creating a dictionary from a key with letters as dictionaries keys
        return self.slovar_1, self.slovar_2

    def define_language(self, secret):
        '''
        Defines which alphabet user uses.
        Takes one argument - secret, returns language.
        '''
        self.secret = secret

        spisok = []

        for letter in secret: # If secret is with capital letters
            if letter == letter.upper() and letter not in text_exception:
                flag = True
                break
            else:
                flag = False            
        if flag:
            for letter in secret:
                for j, listt in enumerate(list_of_keys[7:]):
                    if letter in listt:
                        spisok.append(j + 7)
                        break
            self.language = max(spisok)
            return self.language
        
        for letter in secret: # If secret is numbers only
            if letter in list_of_keys[0]:
                flag = True
            else:
                flag = False
                break
        if flag:
            self.language = 0
            return self.language

        for letter in reversed(secret): # If secret is basic alphabet only
            if letter not in text_exception:
                flag = True
            else:
                flag = False
                break
        if flag:
            for letter in secret:
                for j, listt in enumerate(list_of_keys[1:]):
                    if letter in listt:
                        spisok.append(j + 1)
                        break
            self.language = max(spisok)
            return self.language

        for letter in secret:
            for j, listt in enumerate(list_of_keys[4:]): # If secret is basic alphabet with symbols only
                if letter in listt:
                    spisok.append(j + 4)
                    break
        self.language = max(spisok)
        return self.language  

    def validate_text(self, text):
        '''
        Approves that text has needed amount of letters.
        Takes one argument - text and returns text.
        '''
        self.text = text

        text_list = [letter for letter in text if letter not in text_exception] # Leave only letters in text which will be coded   
        encode_key_letters = [letter for letter in encode_key if letter not in text_exception] # Leave only letters in encoded key
        while len(text_list) < len(secret)*key_len + len(encode_key_letters):
        # Inputting the text with right amount of letters; +4 needed for encoding variable language
            print('Your text is %s symbols, you need %s more letters' % (len(text_list), len(secret)*key_len+len(encode_key_letters)-len(text_list)))
            text = text + input('Input secret you want to encode: %s' % text)
            text_list = []
            text_list = [letter for letter in text if letter not in text_exception]

        return text

    def encode_key(self, language, text):
        '''
        Separates text into two parts. Encodes key into a firts one.
        Takes 2 arguments - language and text. Returns encoded key.
        '''
        self.language = language
        self.text = text

        key_language = 'aaaabbbbabbaa'
        key_alphabet = '0123456789'

        text = text.lower()
        text_list = []
        ab_group_list = []
        encoded_key = ''
        temp_text = ''
        count = 0

        for letter in text: # Cutting text into two parts
            if letter not in text_exception:
                temp_text += letter
                count += 1
                if count == 4:
                    break
            else:
                temp_text += letter

        text_list = [letter for letter in temp_text if letter not in text_exception] # Leave only letters in text which will be coded           
        
        for group in self.language_slovar_1[language]: # Create a list of ab group letters coming one by one
            for letter in group:
                ab_group_list.append(letter)

        for j in range(len(ab_group_list)): # Chenging the register in text
            if ab_group_list[j] == 'b':
                text_list[j] = text_list[j].upper()

        for j in range(len(temp_text)): # Getting the result
            if temp_text[j] not in text_exception:
                encoded_key += text_list[0]
                del(text_list[0])
            else:
                encoded_key += temp_text[j]

        return encoded_key                               

    def encoder(self, secret, text):
        '''
        Encodes secret into a text.
        Takes 2 arguments - secret, text.
        '''
        self.secret = str(secret)
        self.text = text

        text = text.lower()
        alphabet = list_of_keys[language]
        ab_group = []
        text_list = []
        ab_group_list = []
        result = ''

        text_list = [letter for letter in text if letter not in text_exception] # Leave only letters in text which will be coded   

        try:
            ab_group = [self.slovar_1[letter] for letter in secret] # Create ab_groups
        except KeyError:
            return '''Please make sure you used only one language.
And if you did - please send me next to g.mishchevskii@gmail.com
%s, %s''' % (secret, text)
        
        for group in ab_group: # Create a list of all ab group letters coming one by one
            for letter in group:
                ab_group_list.append(letter)

        for j in range(len(ab_group_list)): # Chenging the register in text
            if ab_group_list[j] == 'b':
                text_list[j] = text_list[j].upper()

        for j in range(len(text)): # Getting the result
            if text[j] not in text_exception:
                result += text_list[0]
                del(text_list[0])
            else:
                result += text[j]

        return result

    def decode_language(self, code):
        '''
        Defines which language is used in code.
        Takes one argument - code and returnes language and code without part where language encoded
        '''
        self.code = code

        raw_coded_language = ''
        coded_language = ''

        for letter in code: # Getting first 4 letters from code and remove them from code
            if letter not in text_exception:
                raw_coded_language += letter
                code = code[1:]
                if len(raw_coded_language) == 4:
                    break
            else:
                code = code[1:]

        for letter in raw_coded_language: # Transforming first 4 letters from code into ab-group
            if letter == letter.lower():
                coded_language += 'a'
            else:
                coded_language += 'b'

        language = self.language_slovar_2[coded_language] # Getting language from slovar

        return code, language

    def decoder(self, code):
        '''
        Dencodes code and returns secret.
        Takes 1 argument - code.
        '''
        self.code = code
        
        key = self.key
        alphabet = list_of_keys[language]
        clean_code_list = []
        group_code_list = []
        ab_list = []
        ab_group = []
        string = ''
        result = ''

        clean_code_list = [letter for letter in code if letter not in text_exception]
        # Making list without spaces and symbols from code

        while len(clean_code_list) >= key_len: # Deviding code list into groups of 5 and delete the rest
            group_code_list.append(clean_code_list[:key_len])
            del(clean_code_list[:key_len])

        for group in group_code_list: # Transfering letters in the code into a or b
            for letter in group:
                if letter == letter.lower():
                    ab_list.append('a')
                else:
                    ab_list.append('b')

        while len(ab_list) != 0: # Creating ab groups
            ab_group.append(ab_list[:key_len])
            del(ab_list[:key_len])

        for group in ab_group: # Making string of ab groups conteined in a list
            for letter in group:
                string += letter
          
        for j in range(len(ab_group)): # Assigning a letter from dictionary to each ab group from stringing
            try:
                result += self.slovar_2[string[:key_len]]
            except KeyError:
                return ('''Your code can\'t be decoded. Please make sure you entered the right one\
                 and if yes please send me next line to g.mishchevskii@gmail.com
%s, %s''') % (language, code)
            string = string[key_len:]

        return result

bacon = BaconCode()
bacon.slovar_for_language()

while True:
    x = input('Press enter for a hint, 1 - encode, 2 - decode, 0 - exit: ')
    if len(x) == 0:
        print(bacon.hint)
        continue
    try:
        x = int(x)
    except ValueError:
            print('Pick your number.')
    if x == 0:
        exit()
    elif x not in [1,2]:
        print('Please choose between 1, 2 or 0')
        continue
        
    if x == 1:
        secret = input('Input secret that you don\'t want anyone to know or enter to return:---------------------------- ')
        if len(secret) == 0:
            continue
        language = bacon.define_language(secret)
        bacon.create_key(language)
        bacon.slovar()

        print('You need %s letters' % (len(str(secret))*(key_len)+4))
        text = '0'
        while len(text) < 5:
            text = input('Input text that you\'ll send open or enter to return:---------------------------- ')
            if len(text) == 0:
                continue
            elif len(text) < 5:
                print('Please input more letters')
        encode_key = bacon.encode_key(language, text)
        text = bacon.validate_text(text)
        print(encode_key + bacon.encoder(secret, text[len(encode_key):]))

    elif x == 2:
        code = input('Input code:---------------------------- ')
        if len(code) == 0:
            continue
        language = bacon.decode_language(code)[1]
        bacon.create_key(language)
        bacon.slovar()
        code = bacon.decode_language(code)[0]
        print(bacon.decoder(code))
