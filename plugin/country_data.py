
import requests

country_info = {
    'AF': ('Afghanistan', '🇦🇫'), 'AL': ('Albania', '🇦🇱'), 'DZ': ('Algeria', '🇩🇿'), 'AS': ('American Samoa', '🇦🇸'),
    'AD': ('Andorra', '🇦🇩'), 'AO': ('Angola', '🇦🇴'), 'AI': ('Anguilla', '🇦🇮'), 'AQ': ('Antarctica', '🇦🇶'),
    'AG': ('Antigua and Barbuda', '🇦🇬'), 'AR': ('Argentina', '🇦🇷'), 'AM': ('Armenia', '🇦🇲'), 'AW': ('Aruba', '🇦🇼'),
    'AU': ('Australia', '🇦🇺'), 'AT': ('Austria', '🇦🇹'), 'AZ': ('Azerbaijan', '🇦🇿'), 'BS': ('Bahamas', '🇧🇸'),
    'BH': ('Bahrain', '🇧🇭'), 'BD': ('Bangladesh', '🇧🇩'), 'BB': ('Barbados', '🇧🇧'), 'BY': ('Belarus', '🇧🇾'),
    'BE': ('Belgium', '🇧🇪'), 'BZ': ('Belize', '🇧🇿'), 'BJ': ('Benin', '🇧🇯'), 'BM': ('Bermuda', '🇧🇲'),
    'BT': ('Bhutan', '🇧🇹'), 'BO': ('Bolivia', '🇧🇴'), 'BA': ('Bosnia and Herzegovina', '🇧🇦'), 'BW': ('Botswana', '🇧🇼'),
    'BV': ('Bouvet Island', '🇧🇻'), 'BR': ('Brazil', '🇧🇷'), 'IO': ('British Indian Ocean Territory', '🇮🇴'),
    'BN': ('Brunei Darussalam', '🇧🇳'), 'BG': ('Bulgaria', '🇧🇬'), 'BF': ('Burkina Faso', '🇧🇫'), 'BI': ('Burundi', '🇧🇮'),
    'KH': ('Cambodia', '🇰🇭'), 'CM': ('Cameroon', '🇨🇲'), 'CA': ('Canada', '🇨🇦'), 'CV': ('Cape Verde', '🇨🇻'),
    'KY': ('Cayman Islands', '🇰🇾'), 'CF': ('Central African Republic', '🇨🇫'), 'TD': ('Chad', '🇹🇩'), 'CL': ('Chile', '🇨🇱'),
    'CN': ('China', '🇨🇳'), 'CX': ('Christmas Island', '🇨🇽'), 'CC': ('Cocos (Keeling) Islands', '🇨🇨'),
    'CO': ('Colombia', '🇨🇴'), 'KM': ('Comoros', '🇰🇲'), 'CG': ('Congo', '🇨🇬'), 'CD': ('Congo, Democratic Republic of the', '🇨🇩'),
    'CK': ('Cook Islands', '🇨🇰'), 'CR': ('Costa Rica', '🇨🇷'), 'CI': ('Côte d\'Ivoire', '🇨🇮'), 'HR': ('Croatia', '🇭🇷'),
    'CU': ('Cuba', '🇨🇺'), 'CW': ('Curaçao', '🇨🇼'), 'CY': ('Cyprus', '🇨🇾'), 'CZ': ('Czech Republic', '🇨🇿'),
    'DK': ('Denmark', '🇩🇰'), 'DJ': ('Djibouti', '🇩🇯'), 'DM': ('Dominica', '🇩🇲'), 'DO': ('Dominican Republic', '🇩🇴'),
    'EC': ('Ecuador', '🇪🇨'), 'EG': ('Egypt', '🇪🇬'), 'SV': ('El Salvador', '🇸🇻'), 'GQ': ('Equatorial Guinea', '🇬🇲'),
    'ER': ('Eritrea', '🇪🇷'), 'EE': ('Estonia', '🇪🇪'), 'SZ': ('Eswatini', '🇸🇿'), 'ET': ('Ethiopia', '🇪🇹'),
    'FK': ('Falkland Islands', '🇫🇰'), 'FO': ('Faroe Islands', '🇫🇴'), 'FJ': ('Fiji', '🇫🇯'), 'FI': ('Finland', '🇫🇮'),
    'FR': ('France', '🇫🇷'), 'GF': ('French Guiana', '🇬🇫'), 'PF': ('French Polynesia', '🇵🇫'), 'TF': ('French Southern Territories', '🇹🇫'),
    'GA': ('Gabon', '🇬🇦'), 'GM': ('Gambia', '🇬🇲'), 'GE': ('Georgia', '🇬🇪'), 'DE': ('Germany', '🇩🇪'),
    'GH': ('Ghana', '🇬🇭'), 'GI': ('Gibraltar', '🇬🇮'), 'GR': ('Greece', '🇬🇷'), 'GL': ('Greenland', '🇬🇱'),
    'GD': ('Grenada', '🇬🇩'), 'GP': ('Guadeloupe', '🇲🇫'), 'GU': ('Guam', '🇬🇺'), 'GT': ('Guatemala', '🇵🇪'),
    'GG': ('Guernsey', '🇬🇬'), 'GN': ('Guinea', '🇬🇳'), 'GW': ('Guinea-Bissau', '🇬🇼'), 'GY': ('Guyana', '🇬🇾'),
    'HT': ('Haiti', '🇭🇹'), 'HM': ('Heard Island and McDonald Islands', '🇭🇲'), 'VA': ('Holy See', '🇻🇦'),
    'HN': ('Honduras', '🇭🇳'), 'HK': ('Hong Kong', '🇭🇰'), 'HU': ('Hungary', '🇭🇺'), 'IS': ('Iceland', '🇮🇸'),
    'IN': ('India', '🇮🇳'), 'ID': ('Indonesia', '🇮🇩'), 'IR': ('Iran', '🇮🇷'), 'IQ': ('Iraq', '🇮🇶'),
    'IE': ('Ireland', '🇮🇪'), 'IM': ('Isle of Man', '🇮🇲'), 'IL': ('Israel', '🇮🇱'), 'IT': ('Italy', '🇮🇹'),
    'JE': ('Jersey', '🇯🇪'), 'JP': ('Japan', '🇯🇵'), 'JO': ('Jordan', '🇯🇴'), 'KZ': ('Kazakhstan', '🇰🇿'),
    'KE': ('Kenya', '🇰🇪'), 'KI': ('Kiribati', '🇰🇮'), 'KP': ('Korea, Democratic People\'s Republic of', '🇰🇵'),
    'KR': ('Korea, Republic of', '🇰🇷'), 'KW': ('Kuwait', '🇰🇼'), 'KG': ('Kyrgyzstan', '🇰🇬'), 'LA': ('Lao People\'s Democratic Republic', '🇱🇦'),
    'LV': ('Latvia', '🇱🇻'), 'LB': ('Lebanon', '🇱🇧'), 'LS': ('Lesotho', '🇱🇸'), 'LR': ('Liberia', '🇱🇸'),
    'LY': ('Libya', '🇱🇾'), 'LI': ('Liechtenstein', '🇱🇮'), 'LT': ('Lithuania', '🇱🇹'), 'LU': ('Luxembourg', '🇱🇺'),
    'MO': ('Macao', '🇲🇴'), 'MG': ('Madagascar', '🇲🇬'), 'MW': ('Malawi', '🇲🇼'), 'MY': ('Malaysia', '🇲🇾'),
    'MV': ('Maldives', '🇲🇻'), 'ML': ('Mali', '🇲🇱'), 'MT': ('Malta', '🇲🇹'), 'MH': ('Marshall Islands', '🇲🇭'),
    'MQ': ('Martinique', '🇲🇶'), 'MR': ('Mauritania', '🇲🇷'), 'MU': ('Mauritius', '🇲🇺'), 'YT': ('Mayotte', '🇲🇶'),
    'MX': ('Mexico', '🇲🇽'), 'FM': ('Micronesia (Federated States of)', '🇫🇲'), 'MD': ('Moldova', '🇲🇩'),
    'MC': ('Monaco', '🇲🇨'), 'MN': ('Mongolia', '🇲🇳'), 'ME': ('Montenegro', '🇲🇪'), 'MS': ('Montserrat', '🇲🇸'),
    'MA': ('Morocco', '🇲🇦'), 'MZ': ('Mozambique', '🇲🇿'), 'MM': ('Myanmar', '🇲🇲'), 'NA': ('Namibia', '🇳🇦'),
    'NR': ('Nauru', '🇳🇷'), 'NP': ('Nepal', '🇳🇵'), 'NL': ('Netherlands', '🇳🇱'), 'NC': ('New Caledonia', '🇳🇨'),
    'NZ': ('New Zealand', '🇳🇿'), 'NI': ('Nicaragua', '🇳🇮'), 'NE': ('Niger', '🇳🇪'), 'NG': ('Nigeria', '🇳🇬'),
    'NU': ('Niue', '🇳🇺'), 'NF': ('Norfolk Island', '🇳🇫'), 'MP': ('Northern Mariana Islands', '🇲🇵'),
    'NO': ('Norway', '🇳🇴'), 'OM': ('Oman', '🇴🇲'), 'PK': ('Pakistan', '🇵🇰'), 'PW': ('Palau', '🇵🇼'),
    'PS': ('Palestine', '🇵🇸'), 'PA': ('Panama', '🇵🇦'), 'PG': ('Papua New Guinea', '🇵🇬'), 'PY': ('Paraguay', '🇵🇾'),
    'PE': ('Peru', '🇵🇪'), 'PH': ('Philippines', '🇵🇭'), 'PN': ('Pitcairn Islands', '🇵🇳'), 'PL': ('Poland', '🇵🇱'),
    'PT': ('Portugal', '🇵🇹'), 'PR': ('Puerto Rico', '🇵🇷'), 'QA': ('Qatar', '🇶🇦'), 'RE': ('Réunion', '🇷🇪'),
    'RO': ('Romania', '🇷🇴'), 'RU': ('Russian Federation', '🇷🇺'), 'RW': ('Rwanda', '🇷🇼'), 'SH': ('Saint Helena', '🇸🇭'),
    'KN': ('Saint Kitts and Nevis', '🇰🇳'), 'LC': ('Saint Lucia', '🇱🇨'), 'PM': ('Saint Pierre and Miquelon', '🇵🇲'),
    'VC': ('Saint Vincent and the Grenadines', '🇻🇨'), 'WS': ('Samoa', '🇼🇸'), 'SM': ('San Marino', '🇸🇲'),
    'ST': ('Sao Tome and Principe', '🇸🇹'), 'SA': ('Saudi Arabia', '🇸🇦'), 'SN': ('Senegal', '🇸🇳'),
    'RS': ('Serbia', '🇷🇸'), 'SC': ('Seychelles', '🇸🇨'), 'SL': ('Sierra Leone', '🇸🇱'), 'SG': ('Singapore', '🇸🇬'),
    'SX': ('Sint Maarten', '🇸🇽'), 'SK': ('Slovakia', '🇸🇰'), 'SI': ('Slovenia', '🇸🇮'), 'SB': ('Solomon Islands', '🇸🇧'),
    'SO': ('Somalia', '🇸🇴'), 'ZA': ('South Africa', '🇿🇦'), 'GS': ('South Georgia and the South Sandwich Islands', '🇬🇸'),
    'SS': ('South Sudan', '🇸🇸'), 'ES': ('Spain', '🇪🇸'), 'LK': ('Sri Lanka', '🇱🇰'), 'SD': ('Sudan', '🇸🇩'),
    'SR': ('Suriname', '🇸🇷'), 'SJ': ('Svalbard and Jan Mayen', '🇸🇯'), 'SE': ('Sweden', '🇸🇪'), 'CH': ('Switzerland', '🇨🇭'),
    'SY': ('Syrian Arab Republic', '🇸🇾'), 'TW': ('Taiwan, Province of China', '🇹🇼'), 'TJ': ('Tajikistan', '🇹🇯'),
    'TZ': ('Tanzania, United Republic of', '🇹🇿'), 'TH': ('Thailand', '🇹🇭'), 'TL': ('Timor-Leste', '🇹🇱'),
    'TG': ('Togo', '🇹🇬'), 'TK': ('Tokelau', '🇹🇰'), 'TO': ('Tonga', '🇹🇴'), 'TT': ('Trinidad and Tobago', '🇹🇹'),
    'TN': ('Tunisia', '🇹🇳'), 'TR': ('Turkey', '🇹🇷'), 'TM': ('Turkmenistan', '🇹🇲'), 'TC': ('Turks and Caicos Islands', '🇹🇨'),
    'TV': ('Tuvalu', '🇹🇻'), 'UG': ('Uganda', '🇺🇬'), 'UA': ('Ukraine', '🇺🇦'), 'AE': ('United Arab Emirates', '🇦🇪'),
    'GB': ('United Kingdom', '🇬🇧'), 'US': ('United States of America', '🇺🇸'), 'UM': ('United States Minor Outlying Islands', '🇺🇲'),
    'UY': ('Uruguay', '🇺🇾'), 'UZ': ('Uzbekistan', '🇺🇿'), 'VU': ('Vanuatu', '🇻🇺'), 'VE': ('Venezuela', '🇻🇪'),
    'VN': ('Viet Nam', '🇻🇳'), 'VG': ('Virgin Islands, British', '🇻🇬'), 'VI': ('Virgin Islands, U.S.', '🇻🇮'),
    'WF': ('Wallis and Futuna', '🇼🇫'), 'EH': ('Western Sahara', '🇪🇭'), 'YE': ('Yemen', '🇾🇪'), 'ZM': ('Zambia', '🇿🇲'),
    'ZW': ('Zimbabwe', '🇿🇼')
}


COUNTRY_CODES = {
    "ad": "Andorra", "ae": "United Arab Emirates", "af": "Afghanistan",
    "ag": "Antigua and Barbuda", "ai": "Anguilla", "al": "Albania",
    "am": "Armenia", "ao": "Angola", "aq": "Antarctica", "ar": "Argentina",
    "as": "American Samoa", "at": "Austria", "au": "Australia", "aw": "Aruba",
    "ax": "Åland Islands", "az": "Azerbaijan", "ba": "Bosnia and Herzegovina",
    "bb": "Barbados", "bd": "Bangladesh", "be": "Belgium", "bf": "Burkina Faso",
    "bg": "Bulgaria", "bh": "Bahrain", "bi": "Burundi", "bj": "Benin",
    "bl": "Saint Barthélemy", "bm": "Bermuda", "bn": "Brunei Darussalam",
    "bo": "Bolivia", "bq": "Bonaire, Sint Eustatius and Saba", "br": "Brazil",
    "bs": "Bahamas", "bt": "Bhutan", "bv": "Bouvet Island", "bw": "Botswana",
    "by": "Belarus", "bz": "Belize", "ca": "Canada", "cc": "Cocos (Keeling) Islands",
    "cd": "Congo, Democratic Republic of the", "cf": "Central African Republic",
    "cg": "Congo", "ch": "Switzerland", "ci": "Côte d'Ivoire", "ck": "Cook Islands",
    "cl": "Chile", "cm": "Cameroon", "cn": "China", "co": "Colombia",
    "cr": "Costa Rica", "cu": "Cuba", "cv": "Cabo Verde", "cw": "Curaçao",
    "cx": "Christmas Island", "cy": "Cyprus", "cz": "Czechia", "de": "Germany",
    "dj": "Djibouti", "dk": "Denmark", "dm": "Dominica", "do": "Dominican Republic",
    "dz": "Algeria", "ec": "Ecuador", "ee": "Estonia", "eg": "Egypt",
    "eh": "Western Sahara", "er": "Eritrea", "es": "Spain", "et": "Ethiopia",
    "fi": "Finland", "fj": "Fiji", "fm": "Micronesia", "fo": "Faroe Islands",
    "fr": "France", "ga": "Gabon", "gb": "United Kingdom", "gd": "Grenada",
    "ge": "Georgia", "gf": "French Guiana", "gg": "Guernsey", "gh": "Ghana",
    "gi": "Gibraltar", "gl": "Greenland", "gm": "Gambia", "gn": "Guinea",
    "gp": "Guadeloupe", "gq": "Equatorial Guinea", "gr": "Greece", "gt": "Guatemala",
    "gu": "Guam", "gw": "Guinea-Bissau", "gy": "Guyana", "hk": "Hong Kong",
    "hm": "Heard Island and McDonald Islands", "hn": "Honduras", "hr": "Croatia",
    "ht": "Haiti", "hu": "Hungary", "id": "Indonesia", "ie": "Ireland", "il": "Israel",
    "im": "Isle of Man", "in": "India", "io": "British Indian Ocean Territory", "iq": "Iraq",
    "ir": "Iran", "is": "Iceland", "it": "Italy", "je": "Jersey", "jm": "Jamaica",
    "jn": "Jinmen", "jo": "Jordan", "jp": "Japan", "ke": "Kenya", "kg": "Kyrgyzstan",
    "kh": "Cambodia", "ki": "Kiribati", "km": "Comoros", "kn": "Saint Kitts and Nevis",
    "kp": "North Korea", "kr": "South Korea", "kw": "Kuwait", "ky": "Cayman Islands",
    "kz": "Kazakhstan", "la": "Lao People's Democratic Republic", "lb": "Lebanon",
    "lc": "Saint Lucia", "li": "Liechtenstein", "lk": "Sri Lanka", "lr": "Liberia",
    "ls": "Lesotho", "lt": "Lithuania", "lu": "Luxembourg", "lv": "Latvia", "ly": "Libya",
    "ma": "Morocco", "mc": "Monaco", "md": "Moldova", "me": "Montenegro",
    "mf": "Saint Martin", "mg": "Madagascar", "mh": "Marshall Islands", "mk": "North Macedonia",
    "ml": "Mali", "mm": "Myanmar", "mn": "Mongolia", "mo": "Macao", "mp": "Northern Mariana Islands",
    "mq": "Martinique", "mr": "Mauritania", "ms": "Montserrat", "mt": "Malta", "mu": "Mauritius",
    "mv": "Maldives", "mw": "Malawi", "mx": "Mexico", "my": "Malaysia", "mz": "Mozambique",
    "na": "Namibia", "nc": "New Caledonia", "ne": "Niger", "nf": "Norfolk Island",
    "ng": "Nigeria", "ni": "Nicaragua", "nl": "Netherlands", "no": "Norway", "np": "Nepal",
    "nr": "Nauru", "nu": "Niue", "nz": "New Zealand", "om": "Oman", "pa": "Panama",
    "pe": "Peru", "pf": "French Polynesia", "pg": "Papua New Guinea", "ph": "Philippines",
    "pk": "Pakistan", "pl": "Poland", "pm": "Saint Pierre and Miquelon", "pn": "Pitcairn",
    "pr": "Puerto Rico", "pt": "Portugal", "pw": "Palau", "py": "Paraguay", "qa": "Qatar",
    "re": "Réunion", "ro": "Romania", "rs": "Serbia", "ru": "Russia", "rw": "Rwanda",
    "sa": "Saudi Arabia", "sb": "Solomon Islands", "sc": "Seychelles", "sd": "Sudan",
    "se": "Sweden", "sg": "Singapore", "sh": "Saint Helena", "si": "Slovenia",
    "sj": "Svalbard and Jan Mayen", "sk": "Slovakia", "sl": "Sierra Leone", "sm": "San Marino",
    "sn": "Senegal", "so": "Somalia", "sr": "Suriname", "ss": "South Sudan",
    "st": "São Tomé and Príncipe", "sv": "El Salvador", "sx": "Sint Maarten",
    "sy": "Syria", "sz": "Eswatini", "tc": "Turks and Caicos Islands", "td": "Chad",
    "tf": "French Southern Territories", "tg": "Togo", "th": "Thailand", "tj": "Tajikistan",
    "tk": "Tokelau", "tl": "Timor-Leste", "tm": "Turkmenistan", "tn": "Tunisia",
    "to": "Tonga", "tr": "Turkey", "tt": "Trinidad and Tobago", "tv": "Tuvalu",
    "tz": "Tanzania", "ua": "Ukraine", "ug": "Uganda", "um": "United States Minor Outlying Islands",
    "us": "United States", "uy": "Uruguay", "uz": "Uzbekistan", "va": "Vatican City",
    "vc": "Saint Vincent and the Grenadines", "ve": "Venezuela", "vg": "British Virgin Islands",
    "vi": "U.S. Virgin Islands", "vn": "Vietnam", "vu": "Vanuatu", "wf": "Wallis and Futuna",
    "ws": "Samoa", "xk": "Kosovo", "ye": "Yemen", "yt": "Mayotte", "za": "South Africa",
    "zm": "Zambia", "zw": "Zimbabwe"
}

FAKER_LOCALES = {
    "ad": "en_US", "ae": "en_AE", "af": "en_AF", "ag": "en_US", "ai": "en_US", "al": "en_US",
    "am": "en_AM", "ao": "en_AO", "aq": "en_US", "ar": "es_AR", "as": "en_US", "at": "de_AT",
    "au": "en_AU", "aw": "en_US", "ax": "sv_SE", "az": "en_AZ", "ba": "en_BA", "bb": "en_US",
    "bd": "en_BD", "be": "nl_BE", "bf": "fr_BF", "bg": "bg_BG", "bh": "en_BH", "bi": "fr_BI",
    "bj": "fr_BJ", "bl": "fr_BL", "bm": "en_US", "bn": "en_BN", "bo": "es_BO", "bq": "en_US",
    "br": "pt_BR", "bs": "en_US", "bt": "en_IN", "bv": "en_US", "bw": "en_BW", "by": "be_BY",
    "bz": "en_BZ", "ca": "en_CA", "cc": "en_AU", "cd": "fr_CD", "cf": "fr_CF", "cg": "fr_CG",
    "ch": "de_CH", "ci": "fr_CI", "ck": "en_CK", "cl": "es_CL", "cm": "en_CM", "cn": "zh_CN",
    "co": "es_CO", "cr": "es_CR", "cu": "es_CU", "cv": "pt_CV", "cw": "en_US", "cx": "en_AU",
    "cy": "en_CY", "cz": "cs_CZ", "de": "de_DE", "dj": "fr_DJ", "dk": "da_DK", "dm": "en_US",
    "do": "es_DO", "dz": "fr_DZ", "ec": "es_EC", "ee": "et_EE", "eg": "ar_EG", "eh": "es_EH",
    "er": "en_ER", "es": "es_ES", "et": "en_ET", "fi": "fi_FI", "fj": "en_FJ", "fm": "en_US",
    "fo": "en_FO", "fr": "fr_FR", "ga": "fr_GA", "gb": "en_GB", "gd": "en_US", "ge": "en_GE",
    "gf": "fr_GF", "gg": "en_GB", "gh": "en_GH", "gi": "en_GI", "gl": "da_GL", "gm": "en_GM",
    "gn": "fr_GN", "gp": "fr_GP", "gq": "es_GQ", "gr": "el_GR", "gt": "es_GT", "gu": "en_US",
    "gw": "pt_GW", "gy": "en_GY", "hk": "zh_HK", "hm": "en_US", "hn": "es_HN", "hr": "hr_HR",
    "ht": "fr_HT", "hu": "hu_HU", "id": "id_ID", "ie": "en_IE", "il": "en_IL", "im": "en_GB",
    "in": "en_IN", "io": "en_US", "iq": "ar_IQ", "ir": "fa_IR", "is": "is_IS", "it": "it_IT",
    "je": "en_GB", "jm": "en_JM", "jn": "zh_TW", "jo": "ar_JO", "jp": "ja_JP", "ke": "en_KE",
    "kg": "en_KG", "kh": "km_KH", "ki": "en_KI", "km": "fr_KM", "kn": "en_US", "kp": "ko_KP",
    "kr": "ko_KR", "kw": "en_KW", "ky": "en_KY", "kz": "kk_KZ", "la": "en_LA", "lb": "ar_LB",
    "lc": "en_LC", "li": "de_LI", "lk": "si_LK", "lr": "en_LR", "ls": "en_LS", "lt": "lt_LT",
    "lu": "lb_LU", "lv": "lv_LV", "ly": "ar_LY", "ma": "ar_MA", "mc": "fr_MC", "md": "ro_MD",
    "me": "en_ME", "mf": "fr_MF", "mg": "fr_MG", "mh": "en_MH", "mk": "mk_MK", "ml": "fr_ML",
    "mm": "my_MM", "mn": "mn_MN", "mo": "zh_MO", "mp": "en_US", "mq": "fr_MQ", "mr": "ar_MR",
    "ms": "en_US", "mt": "en_MT", "mu": "en_MU", "mv": "en_MV", "mw": "en_MW", "mx": "es_MX",
    "my": "ms_MY", "mz": "pt_MZ", "na": "en_NA", "nc": "fr_NC", "ne": "fr_NE", "nf": "en_AU",
    "ng": "en_NG", "ni": "es_NI", "nl": "nl_NL", "no": "no_NO", "np": "ne_NP", "nr": "en_NR",
    "nu": "en_NU", "nz": "en_NZ", "om": "en_OM", "pa": "es_PA", "pe": "es_PE", "pf": "fr_PF",
    "pg": "en_PG", "ph": "en_PH", "pk": "en_PK", "pl": "pl_PL", "pm": "fr_PM", "pn": "en_PN",
    "pr": "en_US", "pt": "pt_PT", "pw": "en_PW", "py": "es_PY", "qa": "ar_QA", "re": "fr_RE",
    "ro": "ro_RO", "rs": "sr_RS", "ru": "ru_RU", "rw": "en_RW", "sa": "ar_SA", "sb": "en_SB",
    "sc": "en_SC", "sd": "ar_SD", "se": "sv_SE", "sg": "en_SG", "sh": "en_SH", "si": "sl_SI",
    "sj": "no_SJ", "sk": "sk_SK", "sl": "en_SL", "sm": "it_SM", "sn": "fr_SN", "so": "en_SO",
    "sr": "nl_SR", "ss": "en_SS", "st": "pt_ST", "sv": "es_SV", "sx": "en_SX", "sy": "ar_SY",
    "sz": "en_SZ", "tc": "en_TC", "td": "fr_TD", "tf": "en_US", "tg": "fr_TG", "th": "th_TH",
    "tj": "tg_TJ", "tk": "en_TK", "tl": "pt_TL", "tm": "en_TM", "tn": "ar_TN", "to": "en_TO",
    "tr": "tr_TR", "tt": "en_TT", "tv": "en_TV", "tz": "en_TZ", "ua": "uk_UA", "ug": "en_UG",
    "um": "en_US", "us": "en_US", "uy": "es_UY", "uz": "en_UZ", "va": "it_VA", "vc": "en_VC",
    "ve": "es_VE", "vg": "en_VG", "vi": "en_VI", "vn": "vi_VN", "vu": "en_VU", "wf": "fr_WF",
    "ws": "en_WS", "xk": "en_XK", "ye": "ar_YE", "yt": "fr_YT", "za": "en_ZA", "zm": "en_ZM",
    "zw": "en_ZW"
}