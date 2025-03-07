# Place for imports
import re
import string
import random
import secrets
# /Place for imports

def convert_base(
    number: str,
    from_base: int,
    to_base: int,
    precision: int = 10
) -> str:
    """
    Converts a number from one base to another, supporting fractional numbers.

    Parameters:
        number (str): The number to convert (as a string).
        from_base (int): The base of the input number (2-36).
        to_base (int): The target base to convert to (2-36).
        precision (int): Maximum number of digits in the fractional part.

    Returns:
        str: The converted number in the target base.
    """
    characters = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    if not (2 <= from_base <= 36) or not (2 <= to_base <= 36):
        raise ValueError("Bases must be between 2 and 36")

    number = str(number)
    if '.' in number:
        integer_part, fractional_part = number.split('.')
        if not integer_part and not fractional_part:
            raise ValueError("Invalid number format")
    else:
        integer_part = number
        fractional_part = ''

    symbol_map = {char.upper(): idx for idx, char in enumerate(characters[:from_base])}

    def validate_part(part, part_name):
        for char in part:
            if char.upper() not in symbol_map:
                raise ValueError(f"Invalid character '{char}' in {part_name} for base {from_base}")

    validate_part(integer_part, 'integer part')
    validate_part(fractional_part, 'fractional part')

    decimal_int = 0
    for i, char in enumerate(reversed(integer_part)):
        decimal_int += symbol_map[char.upper()] * (from_base ** i)

    decimal_frac = 0.0
    for i, char in enumerate(fractional_part, 1):
        decimal_frac += symbol_map[char.upper()] * (from_base ** -i)

    total_decimal = decimal_int + decimal_frac

    value_map = {idx: char for idx, char in enumerate(characters[:to_base])}

    converted_int = []
    integer = int(total_decimal)
    if integer == 0:
        converted_int = ['0']
    else:
        while integer > 0:
            converted_int.append(value_map[integer % to_base])
            integer = integer // to_base
    converted_int = ''.join(reversed(converted_int)) or '0'

    converted_frac = []
    fractional = total_decimal - int(total_decimal)
    for _ in range(precision):
        if not fractional:
            break
        fractional *= to_base
        digit = int(fractional)
        converted_frac.append(value_map[digit])
        fractional -= digit

    result = converted_int
    if converted_frac:
        result += '.' + ''.join(converted_frac)

    return result

def gcd_lcm(a: int, b: int) -> tuple[int, int]:
    """
    Calculates the Greatest Common Divisor (GCD) and Least Common Multiple (LCM)
    of two integers using the Euclidean algorithm.

    Parameters:
        a (int): First integer
        b (int): Second integer

    Returns:
        tuple[int, int]: A tuple containing (GCD, LCM)

    Raises:
        ValueError: If either number is not a positive integer
        ZeroDivisionError: If either number is zero
    """
    if not isinstance(a, int) or not isinstance(b, int):
        raise ValueError("Both numbers must be integers")
    if a <= 0 or b <= 0:
        raise ValueError("Both numbers must be positive")
    
    def gcd(x: int, y: int) -> int:
        while y:
            x, y = y, x % y
        return x

    def lcm(x: int, y: int) -> int:
        return abs(x * y) // gcd(x, y)

    return gcd(a, b), lcm(a, b)

def validate_email(email: str) -> tuple[bool, str]:
    """
    Validates an email address and returns a normalized version.
    
    Parameters:
        email (str): The email address to validate
        
    Returns:
        tuple[bool, str]: A tuple containing (is_valid, normalized_email)
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    email = email.strip().lower()
    
    is_valid = bool(re.match(pattern, email))
    
    return is_valid, email

def generate_password(
    length: int = 16,
    use_uppercase: bool = True,
    use_lowercase: bool = True,
    use_digits: bool = True,
    use_special: bool = True
) -> str:
    """
    Generates a secure random password with specified characteristics.
    
    Parameters:
        length (int): Length of the password (default: 16)
        use_uppercase (bool): Include uppercase letters (default: True)
        use_lowercase (bool): Include lowercase letters (default: True)
        use_digits (bool): Include digits (default: True)
        use_special (bool): Include special characters (default: True)
        
    Returns:
        str: Generated password
        
    Raises:
        ValueError: If length < 4 or no character types are selected
    """
    if length < 4:
        raise ValueError("Password length must be at least 4 characters")
        
    if not any([use_uppercase, use_lowercase, use_digits, use_special]):
        raise ValueError("At least one character type must be selected")
    
    chars = ''
    if use_uppercase:
        chars += string.ascii_uppercase
    if use_lowercase:
        chars += string.ascii_lowercase
    if use_digits:
        chars += string.digits
    if use_special:
        chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    password = []
    if use_uppercase:
        password.append(secrets.choice(string.ascii_uppercase))
    if use_lowercase:
        password.append(secrets.choice(string.ascii_lowercase))
    if use_digits:
        password.append(secrets.choice(string.digits))
    if use_special:
        password.append(secrets.choice("!@#$%^&*()_+-=[]{}|;:,.<>?"))
        
    while len(password) < length:
        password.append(secrets.choice(chars))
        
    random.shuffle(password)
    return ''.join(password)

def levenshtein_distance(s1: str, s2: str) -> int:
    """
    Calculates the Levenshtein (edit) distance between two strings.
    
    Parameters:
        s1 (str): First string
        s2 (str): Second string
        
    Returns:
        int: The minimum number of single-character edits needed to change s1 into s2
    """
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    
    if len(s2) == 0:
        return len(s1)
    
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]

def compress_string(text: str) -> str:
    """
    Compresses a string using run-length encoding.
    
    Parameters:
        text (str): The string to compress
        
    Returns:
        str: The compressed string
        
    'AABBBCCCC' -> 'A2B3C4'
    """
    if not text:
        return ""
        
    compressed = []
    count = 1
    current = text[0]
    
    for char in text[1:]:
        if char == current:
            count += 1
        else:
            compressed.append(f"{current}{count}")
            current = char
            count = 1
            
    compressed.append(f"{current}{count}")
    compressed_str = "".join(compressed)
    
    return compressed_str if len(compressed_str) < len(text) else text

def is_prime(n: int) -> bool:
    """
    Checks if a number is prime using optimized trial division.
    
    Parameters:
        n (int): The number to check
        
    Returns:
        bool: True if the number is prime, False otherwise
        
    Raises:
        ValueError: If the input is less than 2
    """
    if not isinstance(n, int):
        raise ValueError("Input must be an integer")
    if n < 2:
        raise ValueError("Numbers less than 2 are not prime")
    if n == 2:
        return True
    if n % 2 == 0:
        return False
        
    for i in range(3, int(n ** 0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

def generate_permutations(text: str) -> list[str]:
    """
    Generates all possible permutations of a string.
    
    Parameters:
        text (str): The string to generate permutations for
        
    Returns:
        list[str]: List of all possible permutations
        
    Warning:
        The number of permutations grows factorially with string length.
        Use with caution on long strings.
    """
    if len(text) <= 1:
        return [text]
        
    perms = []
    for i, char in enumerate(text):
        # Get all permutations of string without current char
        sub_perms = generate_permutations(text[:i] + text[i+1:])
        # Add current char to beginning of each sub-permutation
        perms.extend([char + p for p in sub_perms])
        
    return perms

def calculate_statistics(numbers: list[float | int]) -> dict[str, float | int | list]:
    """
    Calculates basic statistical measures for a sequence of numbers.
    
    Parameters:
        numbers (list[float | int]): List of numbers to analyze
        
    Returns:
        dict[str, float | int | list]: Dictionary containing:
            - mean: arithmetic mean of the numbers
            - median: middle value of sorted numbers
            - mode: most frequent value(s)
            - range: difference between max and min values
            - variance: variance of the numbers
            - std_dev: standard deviation
            
    Raises:
        ValueError: If the input list is empty
    """
    if not numbers:
        raise ValueError("Input list cannot be empty")
        
    # Calculate mean
    n = len(numbers)
    mean = sum(numbers) / n
    
    # Calculate median
    sorted_nums = sorted(numbers)
    if n % 2 == 0:
        median = (sorted_nums[n//2 - 1] + sorted_nums[n//2]) / 2
    else:
        median = sorted_nums[n//2]
    
    # Calculate mode
    freq = {}
    for num in numbers:
        freq[num] = freq.get(num, 0) + 1
    max_freq = max(freq.values())
    mode = [num for num, count in freq.items() if count == max_freq]
    
    # Calculate range
    range_val = max(numbers) - min(numbers)
    
    # Calculate variance and standard deviation
    variance = sum((x - mean) ** 2 for x in numbers) / n
    std_dev = variance ** 0.5
    
    return {
        'mean': mean,
        'median': median,
        'mode': mode,
        'range': range_val,
        'variance': variance,
        'std_dev': std_dev
    }

