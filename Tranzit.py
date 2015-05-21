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
            self.language_slovar_1[i] = key[j:j+4]
            j+=1

        self.language_slovar_2 = {self.language_slovar_1[i]: i for i in self.language_slovar_1}
        # Creating a dictionary from a key with letters as dictionaries keys
        return self.language_slovar_1, self.language_slovar_2      

    def language(self):
        '''
        Defines variable language.
        Takes no arguments
        '''
        hint = '''
First you have to choose language. 3 languages available: English (1,4,7), Russian(2,5,8), Ukrainian(3,6,9) and numbers(0).
Russian alphabet doesn't have 'э' and 'ъ', Ukrainian - 'ї'.
Choises 1, 2 and 3 - basic alphabet.
4, 5, 6 - basic alphabet with symbols.
6, 7, 8 - basic alphabet with symbols and capital letters.
Text in which you wnat to wrap your secret can cosist from symbols, but symbols can't be encoded so use letters for that matter.
For instance you want to encode you secret: "love!". There is symbol but no capital letters.
You choose "4" and then "1" to encode. Input your secret (love!)
Now input any text in which you want to wrap up your secret: Space is available in every choise here.
The result would be: Space IS avAIlaBlE iN EVeRY choise Here.
    '''
        while True:
            language = input('''Press enter if you need a hint.
0 - Numbers, 1, 4, 7 - English, 2, 5, 8 - Русский, 3, 6, 9 - Українська, 10 - exit: ''')
            if len(language) == 0:
                print(hint)
                continue
            try:
                language = int(language)
            except ValueError:
                print('Pick your number.')
                continue
            if language not in range(0,11):
                print('Pick a number from 0 to 10 or press enter for hint.')
                continue
            elif language == 10:
                exit()
            else:
                break
        return language

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

    def validate_secret(self, secret):
        '''
        Validates the secret. If user enters symbols not in alphabet it asks him to enter valid secret and shows the alphabet.
        Takes one argument - secret.
        '''
        self.secret = secret
        flag = len(str(secret))
        count = 0
        while flag != count:
            for letter in secret:
                if letter in list_of_keys[language]:
                    count += 1
                else:
                    print('Please use symbols from this list: %s' % list_of_keys[language])
                    secret = input('Input secret:---------------------------- ')
                    flag = len(str(secret))
                    count = 0
                    break
        return secret

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
            language = max(spisok)
            return language
        
        for letter in secret: # If secret is numbers only
            if letter in list_of_keys[0]:
                flag = True
            else:
                flag = False
                break
        if flag:
            language = 0
            return language

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
            language = max(spisok)
            return language

        for letter in secret:
            for j, listt in enumerate(list_of_keys[4:]): # If secret is basic alphabet with symbols only
                if letter in listt:
                    spisok.append(j + 4)
                    break
        language = max(spisok)
        return language                                   

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

        while len(text_list) < len(secret)*key_len + 4:
        # Inputting the text with right amount of letters; +4 needed for encoding variable language
            print('Your text is %s symbols, you need %s more letters' % (len(text_list), len(secret)*key_len-len(text_list)))
            text = text + input('Input secret you want to encode: %s' % text)
            text_list = []
            text_list = [letter for letter in text if letter not in text_exception]

        ab_group = [self.slovar_1[letter] for letter in secret] # Create ab_groups             
        
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
language = bacon.language()
bacon.create_key(language)
bacon.slovar()
x = None
while True:
    while True:    
        try:
            x = int(input('1 - encode, 2 - decode, 3 - change language, 10 - exit: '))
            if x == 10:
                exit()
            elif x not in [1,2,3]:
                print('Please choose between 1, 2, 3 or 10')
                continue
            break
        except ValueError:
                print('Pick your number.')

    if x == 3:
        language = bacon.language()
        bacon.create_key(language)
        bacon.slovar()
    elif x == 1:
        secret = input('Input secret:---------------------------- ')
        secret = bacon.validate_secret(secret)
        print('You need %s letters' % (len(str(secret))*(key_len)+4))
        text = input('Input text:---------------------------- ')
        print(bacon.encoder(secret, text))

    elif x == 2:
        code = input('Input code:---------------------------- ')
        print(bacon.decoder(code))
