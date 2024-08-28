# Function to separate the hours of the string hh:mm-hh:mm
import unicodedata
def separateHours(hours):
    """This function transforms string hh:mm-hh:mm to float
        In: string Out: float, float"""
    if hours == '-' :
        return
    split = hours.split("-")

    for i in range(len(split)):
        split[i] = split[i].replace(":00", "")
        if split[i][0] == "0":
            split[i] = split[i][1:]

    return float(split[0]), float(split[1]) # Example hours: 8:00-9:00, output: 8.0, 9.0

# Function to eliminate the acents and signs of punctuation in the data frame
def remove_accents(input_str):
    if isinstance(input_str, str):  # Verifica si el valor es una cadena
        nfkd_form = unicodedata.normalize('NFKD', input_str)
        return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])
    return input_str  # Devuelve el valor tal cual si no es una cadena