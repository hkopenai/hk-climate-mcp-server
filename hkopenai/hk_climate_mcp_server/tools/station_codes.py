from typing import Dict

def get_station_codes() -> Dict[str, str]:
    """
    Get a dictionary of station codes and their corresponding names for weather and radiation reports in Hong Kong.
    
    Returns:
        Dict mapping station codes to station names.
    """
    return {
        'CCH': 'Cheung Chau',
        'CLK': 'Chek Lap Kok',
        'EPC': 'Ping Chau',
        'HKO': 'Hong Kong Observatory',
        'HKP': 'Hong Kong Park',
        'HKS': 'Wong Chuk Hang',
        'HPV': 'Happy Valley',
        'JKB': 'Tseung Kwan O',
        'KAT': 'Kat O',
        'KLT': 'Kowloon City',
        'KP': 'Kings Park',
        'KTG': 'Kwun Tong',
        'LFS': 'Lau Fau Shan',
        'PLC': 'Tai Mei Tuk',
        'SE1': 'Kai Tak Runway Park',
        'SEK': 'Shek Kong',
        'SHA': 'Sha Tin',
        'SKG': 'Sai Kung',
        'SKW': 'Shau Kei Wan',
        'SSP': 'Sham Shui Po',
        'STK': 'Sha Tau Kok',
        'STY': 'Stanley',
        'SWH': 'Sai Wan Ho',
        'TAP': 'Tap Mun',
        'TBT': 'Tsim Bei Tsui',
        'TKL': 'Ta Kwu Ling',
        'TUN': 'Tuen Mun',
        'TW': 'Tsuen Wan Shing Mun Valley',
        'TWN': 'Tsuen Wan Ho Koon',
        'TY1': 'Tsing Yi',
        'WTS': 'Wong Tai Sin',
        'YCT': 'Tai Po',
        'YLP': 'Yuen Long Park',
        'YNF': 'Yuen Ng Fan'
    }
