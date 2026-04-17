VALID_SUBURBS = [
    'Auckland',
    'Wellington',
    'Christchurch',
    'Hamilton',
    'Tauranga',
    'Dunedin',
    'Queen Street',
    'Lambton Quay',
    'Colombo Street',
    'Ponsonby',
    'Mount Eden',
    'Parnell',
    'Takapuna',
    'Grey Lynn',
    'Balmoral',
    'Te Aro',
    'Karori',
    'Northland',
    'Manukau',
    'Waitakere',
]


def validate_address(address: str) -> dict:
    """
    Validate an address against mock NZ suburbs.
    Returns dict with status and message.
    """
    if not address or len(address.strip()) < 3:
        return {'status': 'invalid', 'message': 'Address too short'}

    address_upper = address.upper()

    for suburb in VALID_SUBURBS:
        if suburb.upper() in address_upper:
            return {'status': 'valid', 'message': f'Address contains valid suburb: {suburb}'}

    return {'status': 'invalid', 'message': 'Address does not contain a recognized NZ suburb'}
