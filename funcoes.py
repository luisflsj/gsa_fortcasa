
def format_number(value, prefix=''):
    is_negative = value < 0
    value = abs(value)

    for unit in ['', 'mil']:
        if value < 1000:
            formatted_value = f'{value:.2f}'.replace('-', '')  # Remove o sinal de menos se presente
            return f'{prefix}{"-" if is_negative else ""}{formatted_value} {unit}'
        value /= 1000

    formatted_value = f'{value:.2f}'.replace('-', '')  # Remove o sinal de menos se presente
    return f'{prefix}{"-" if is_negative else ""}{formatted_value} milhões'