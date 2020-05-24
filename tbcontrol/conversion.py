def discrete_coeffs_neg_to_pos(numer, denom):
    """Convert the coefficients of a transfer function from negative to positive powers of z
    
    numer and denom must be lists of coefficients of negative powers of z, in descending powers of z
    
    convert from
    
              -1       -2            -n
    b  +  b  z   + b  z  + ... + b  z    numer = [b0, b1, b2, ...]
     0     1        2             n
    ------------------------------
              -1       -2            -m
    a  +  a  z   + a  z  + ... + a  z    denom = [a0, b1, b2, ...]
     0     1        2             m

    to 

        k        k-1        k-2
    b  z  +  b  z    +  b  z    + ...
     0        1         2
    -------------------------------
        k        k-1        k-2
    a  z  +  a  z     + a  z    + ...  
     0        1          2

    """
    
    n = len(numer)
    m = len(denom)
    
    k = max(m, n)
    
    return list(numer) + [0]*(k - n), list(denom) + [0]*(k - m)


def discrete_coeffs_pos_to_neg(numer, denom):
    """Convert the coefficients of a transfer function from positive to negative powers of z
    
    numer and denom must be lists of coefficients of negative powers of z, in descending powers of z
    
    convert from
    
        m        m-1        m-2
    b  z  +  b  z    +  b  z    + ...      numer = [b0, b1, b2, ...]
     0        1          2 
    -------------------------
        n        n-1       n-2
    a  z  +  a  z   + a  z      + ...      denom = [a0, b1, b2, ...]
     0        1        2


   to 

              -1       -2            -n
    b  +  b  z   + b  z  + ... + b  z  
     0     1        2             n
    ------------------------------
              -1       -2            -m
    a  +  a  z   + a  z  + ... + a  z  
     0     1        2             m

    """

    n = len(numer)
    m = len(denom)
    
    k = max(m, n)
    
    return [0]*(k - n) + list(numer), [0]*(k - m) + list(denom) 

