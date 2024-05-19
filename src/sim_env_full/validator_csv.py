# Version 1.02 | Encoding UFT-8
# Created by: Jesper Hammer
# Date: 05-05-2024

class ValidatorCSV:
    """
    Validates content of csv file against corresponding schema file\n
    List of class methods:\n
    - Validate: validates content of csv file against corresponding schema file\n
    """

    def __init__(self) -> None:
        pass

    @staticmethod
    def validate(file, sch_file) -> bool:
        """
        Validates content of csv file against corresponding schema file\n
        \n
        ------------
        PARAMETERS\n
        file:\n
        Takes name of input file of type STRING\n
        File must be of type CSV\n
        sch_file:\n
        Takes name of schema file of type STRING\n
        File must be of type CSV\n
        \n
        ------------
        RETURNS\n
        Returns result of validation\n
        Return type is BOOL\n
        \n
        """

        reader = []
        sch = []
        delim = ','
        return_val = bool(False)

        with open(file,'r') as file:
            for line in file:
                reader.append(line.rstrip('\n').rstrip('\r').split(delim))

        with open(sch_file,'r') as file:
            for line in file:
                sch.append(line.rstrip('\n').rstrip('\r').split(delim))

        #Generates list of validation rules based on schema
        for i in range(len(sch[0])):
            if str(sch[0][i]) == "str":
                sch[0][i] = str("str")
            if str(sch[0][i]) == "int":
                sch[0][i] = int(1)
            if str(sch[0][i]) == "float":
                sch[0][i] = float(0.1)

        #Validates csv against validation rules
        for i in range(len(reader)):
            for j in range(len(reader[i])):
                try:
                    reader[i][j] == int(reader[i][j])
                except ValueError:
                    pass
                
                if type(reader[i][j]) == type(sch[0][j]):
                    return_val = bool(True)
                elif type(reader[i][j]) != type(sch[0][j]):
                    return_val = bool(False)
                    break
        return return_val