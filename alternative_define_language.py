def define_language(self, secret):
    self.secret = secret

    for letter in secret:
        for j, listt in enumerate(list_of_keys):
            if letter in listt:
                language = j
                if language > 6:
                    return language
                break
    return language
