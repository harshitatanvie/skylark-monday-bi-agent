from typing import Union, Optional

def parse_currency(val: Union[str, int, float, None]) -> Optional[float]:
    if val is None:
        return None
    if isinstance(val, (int, float)):
        return float(val) if not (isinstance(val, float) and (val != val)) else None
    
    s = str(val).strip()
    if not s or s.lower() in ("null", "none", "n/a", "-", ""):
        return None
    
    # Check for Lakhs / Cr modifiers in string
    mult = 1.0
    s_upper = s.upper()
    if "CR" in s_upper or "CRORE" in s_upper:
        mult = 10_00_000.0 * 10  # 1 Cr = 1,00,00,000 = 10,000,000
    elif "LAKH" in s_upper or "L" in s_upper and not s_upper.startswith("L"):
        mult = 1_00_000.0  # 1 Lakh = 100,000
    
    # Strip symbols
    clean_str = ""
    for char in s:
        if char.isdigit() or char in (".", "-"):
            clean_str += char
    
    if not clean_str or clean_str == "-":
        return None
    
    try:
        val_float = float(clean_str) * mult
        return val_float
    except ValueError:
        return None

def format_inr(val: Optional[float], compact: bool = True) -> str:
    if val is None or val != val:
        return "₹0"
    
    abs_val = abs(val)
    sign = "-" if val < 0 else ""
    
    if compact:
        if abs_val >= 1_00_00_000:  # 1 Crore
            cr_val = abs_val / 1_00_00_000
            return f"{sign}₹{cr_val:.2f} Cr"
        elif abs_val >= 1_00_000:  # 1 Lakh
            lakh_val = abs_val / 1_00_000
            return f"{sign}₹{lakh_val:.2f} L"
        elif abs_val >= 1000:
            return f"{sign}₹{abs_val:,.0f}"
        else:
            return f"{sign}₹{abs_val:.0f}"
    
    return f"{sign}₹{val:,.2f}"
