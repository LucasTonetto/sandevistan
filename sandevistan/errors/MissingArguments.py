class MissingArguments(Exception):

    def __init__(self, number_of_arguments_expected, number_of_arguments_given):

        super().__init__(f'{number_of_arguments_given} arguments given. {number_of_arguments_expected} arguments expected!')
