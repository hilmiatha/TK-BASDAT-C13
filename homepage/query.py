def cek_user(email, password):
    return f"""
        SELECT * 
        from akun
        where email = '{email}' and password = '{password}';
    """

def cek_premium(email):
    return f"""
        SELECT * 
        from premium
        where email = '{email}';
    """
    
def cek_label(email, password):
    return f"""
        SELECT * 
        from label
        where email = '{email}' and password = '{password}';
    """

def cek_podcaster(email):
    return f"""
        SELECT * 
        from podcaster
        where email = '{email}';
    """

def cek_artist(email):
    return f"""
        SELECT * 
        from artist
        where email_akun = '{email}';
    """

def cek_songwriter(email):
    return f"""
        SELECT * 
        from songwriter
        where email_akun = '{email}';
    """