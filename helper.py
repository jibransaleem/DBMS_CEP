import regex as re
import phonenumbers
def is_strong_password(password):
    if len(password) < 8:
        return False
    
    if not re.search('[A-Z]', password):
        return False
    
    if not re.search('[a-z]', password):
        return False
    
    if not re.search('[0-9]', password):
        return False
    
    if not re.search('[!@#$%^&*]', password):
        return False
    
    return True

def is_valid_name(name):
    pattern = r'^[A-Za-z ]+\d*$'
    return bool(re.fullmatch(pattern, name))

def is_valid_company(name):
    pattern = r'^[A-Za-z0-9 .&-]+$'
    return bool(re.fullmatch(pattern, name))


def validate_contact_number(number):
        region= 'PK'
        pattern = r"^\d+$"
        if not re.match(pattern, number) or len(number)>13:
            return False
        if not number.startswith("+"):
            number = f"+92{number}"
        parse_ = phonenumbers.parse(number, region)
        if phonenumbers.is_valid_number(parse_) and phonenumbers.region_code_for_number(parse_) == region:
                return True
        else:
            return False
