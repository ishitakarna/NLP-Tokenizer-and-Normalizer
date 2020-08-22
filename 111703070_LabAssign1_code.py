import datetime
import re
    
months = {
    "January":"01",
    "February":"02",
    "March":"03",
    "April":"04",
    "May":"05",
    "June":"06",
    "July":"07",
    "August":"08",
    "September":"09",
    "October":"10",
    "November":"11",
    "December":"12"
}

contractions = { 
"ain't": "am not",
"aren't": "are not",
"can't": "cannot",
"can't've": "cannot have",
"'cause": "because",
"could've": "could have",
"couldn't": "could not",
"couldn't've": "could not have",
"didn't": "did not",
"doesn't": "does not",
"don't": "do not",
"hadn't": "had not",
"hadn't've": "had not have",
"hasn't": "has not",
"haven't": "have not",
"he'd": "he would",
"he'd've": "he would have",
"he'll": "he will",
"he'll've": "he will have",
"he's": "he is",
"how'd": "how did",
"how'd'y": "how do you",
"how'll": "how will",
"how's": "how is",
"i'd": "I would",
"i'd've": "I would have",
"i'll": "I will",
"i'll've": "I will have",
"i'm": "I am",
"i've": "I have",
"isn't": "is not",
"it's": "it is",
"it'd": "it would",
"it'd've": "it would have",
"it'll": "it will",
"it'll've": "it will have",
"it's": "it is",
"let's": "let us",
"ma'am": "madam",
"mayn't": "may not",
"might've": "might have",
"mightn't": "might not",
"mightn't've": "might not have",
"must've": "must have",
"mustn't": "must not",
"mustn't've": "must not have",
"needn't": "need not",
"needn't've": "need not have",
"o'clock": "of the clock",
"oughtn't": "ought not",
"oughtn't've": "ought not have",
"shan't": "shall not",
"sha'n't": "shall not",
"shan't've": "shall not have",
"she'd": "she would",
"she'd've": "she would have",
"she'll": "she will",
"she'll've": "she will have",
"she's": "she is",
"should've": "should have",
"shouldn't": "should not",
"shouldn't've": "should not have",
"so've": "so have",
"so's": "so as",
"that'd": "that would",
"that'd've": "that would have",
"that's": "that is",
"there'd": "there would",
"there'd've": "there would have",
"there's": "there is",
"they'd": "they would",
"they'd've": "they would have",
"they'll": "they will",
"they'll've": "they will have",
"they're": "they are",
"they've": "they have",
"to've": "to have",
"wasn't": "was not",
"we'd": "we would",
"we'd've": "we would have",
"we'll": "we will",
"we'll've": "we will have",
"we're": "we are",
"we've": "we have",
"weren't": "were not",
"what'll": "what will",
"what'll've": "what will have",
"what're": "what are",
"what's": "what is",
"what've": "what have",
"when's": "when is",
"when've": "when have",
"where'd": "where did",
"where's": "where is",
"where've": "where have",
"who'll": "who shall / who will",
"who'll've": "who will have",
"who's": "who is",
"who've": "who have",
"why's": "why is",
"why've": "why have",
"will've": "will have",
"won't": "will not",
"won't've": "will not have",
"would've": "would have",
"wouldn't": "would not",
"wouldn't've": "would not have",
"y'all": "you all",
"y'all'd": "you all would",
"y'all'd've": "you all would have",
"y'all're": "you all are",
"y'all've": "you all have",
"you'd": "you would",
"you'd've": "you would have",
"you'll": "you will",
"you'll've": "you will have",
"you're": "you are",
"you've": "you have"
}

emojis = [":@", ":-@",
">:o",
">:0",
"D:<",
"D:",
"D8",
"D;",
"D=",
"Dx",
">.<",
">_<",
"d:<",
"d:",
"d8",
"d;",
"d=",
"dx",
"v.v",
":/",
":\"",
"=/",
"=\"",
">:/",
">:\"",
":-/",
":-\"",
":)",
"(:",
";)",
";(",
"(;",
");",
":-)",
":3",
":d",
":D",
"xd",
":')",
"^_^",
"^.^",
":]",
":}",
":p",
":b",
"=p",
"=b",
":-p",
":-b",
"=)",
":(",
"):",
":'(",
":c",
":-(",
"</3",
":[",
":{",
"T.T",
"o_o",
"O_O",
"0_o",
"o_0",
"0_O",
"O_0",
"o.o",
"O.O",
"0.o",
"o.0",
":o",
":-o",
"<3",
":p",
":b",
"=p",
"=b",
":-p",
":-b",
":$"
]

timezones = [{'value': 'Dateline Standard Time', 'abbr': 'DST', 'utc': ['Etc/GMT+12']}, {'value': 'UTC-11', 'abbr': 'U', 'utc': ['Etc/GMT+11', 'Pacific/Midway', 'Pacific/Niue', 'Pacific/Pago_Pago']}, {'value': 'Hawaiian Standard Time', 'abbr': 'HST', 'utc': ['Etc/GMT+10', 'Pacific/Honolulu', 'Pacific/Johnston', 'Pacific/Rarotonga', 'Pacific/Tahiti']}, {'value': 'Alaskan Standard Time', 'abbr': 'AKDT', 'utc': ['America/Anchorage', 'America/Juneau', 'America/Nome', 'America/Sitka', 'America/Yakutat']}, {'value': 'Pacific Standard Time (Mexico)', 'abbr': 'PDT', 'utc': ['America/Santa_Isabel']}, {'value': 'Pacific Daylight Time', 'abbr': 'PDT', 'utc': ['America/Dawson', 'America/Los_Angeles', 'America/Tijuana', 'America/Vancouver', 'America/Whitehorse']}, {'value': 'Pacific Standard Time', 'abbr': 'PST', 'utc': ['America/Dawson', 'America/Los_Angeles', 'America/Tijuana', 'America/Vancouver', 'America/Whitehorse', 'PST8PDT']}, {'value': 'US Mountain Standard Time', 'abbr': 'UMST', 'utc': ['America/Creston', 'America/Dawson_Creek', 'America/Hermosillo', 'America/Phoenix', 'Etc/GMT+7']}, {'value': 'Mountain Standard Time (Mexico)', 'abbr': 'MDT', 'utc': ['America/Chihuahua', 'America/Mazatlan']}, {'value': 'Mountain Standard Time', 'abbr': 'MDT', 'utc': ['America/Boise', 'America/Cambridge_Bay', 'America/Denver', 'America/Edmonton', 'America/Inuvik', 'America/Ojinaga', 'America/Yellowknife', 'MST7MDT']}, {'value': 'Central America Standard Time', 'abbr': 'CAST', 'utc': ['America/Belize', 'America/Costa_Rica', 'America/El_Salvador', 'America/Guatemala', 'America/Managua', 'America/Tegucigalpa', 'Etc/GMT+6', 'Pacific/Galapagos']}, {'value': 'Central Standard Time', 'abbr': 'CDT', 'utc': ['America/Chicago', 'America/Indiana/Knox', 'America/Indiana/Tell_City', 'America/Matamoros', 'America/Menominee', 'America/North_Dakota/Beulah', 'America/North_Dakota/Center', 'America/North_Dakota/New_Salem', 'America/Rainy_River', 'America/Rankin_Inlet', 'America/Resolute', 'America/Winnipeg', 'CST6CDT']}, {'value': 'Central Standard Time (Mexico)', 'abbr': 'CDT', 'utc': ['America/Bahia_Banderas', 'America/Cancun', 'America/Merida', 'America/Mexico_City', 'America/Monterrey']}, {'value': 'Canada Central Standard Time', 'abbr': 'CCST', 'utc': ['America/Regina', 'America/Swift_Current']}, {'value': 'SA Pacific Standard Time', 'abbr': 'SPST', 'utc': ['America/Bogota', 'America/Cayman', 'America/Coral_Harbour', 'America/Eirunepe', 'America/Guayaquil', 'America/Jamaica', 'America/Lima', 'America/Panama', 'America/Rio_Branco', 'Etc/GMT+5']}, {'value': 'Eastern Standard Time', 'abbr': 'EDT', 'utc': ['America/Detroit', 'America/Havana', 'America/Indiana/Petersburg', 'America/Indiana/Vincennes', 'America/Indiana/Winamac', 'America/Iqaluit', 'America/Kentucky/Monticello', 'America/Louisville', 'America/Montreal', 'America/Nassau', 'America/New_York', 'America/Nipigon', 'America/Pangnirtung', 'America/Port-au-Prince', 'America/Thunder_Bay', 'America/Toronto', 'EST5EDT']}, {'value': 'US Eastern Standard Time', 'abbr': 'UEDT', 'utc': ['America/Indiana/Marengo', 'America/Indiana/Vevay', 'America/Indianapolis']}, {'value': 'Venezuela Standard Time', 'abbr': 'VST', 'utc': ['America/Caracas']}, {'value': 'Paraguay Standard Time', 'abbr': 'PYT', 'utc': ['America/Asuncion']}, {'value': 'Atlantic Standard Time', 'abbr': 'ADT', 'utc': ['America/Glace_Bay', 'America/Goose_Bay', 'America/Halifax', 'America/Moncton', 'America/Thule', 'Atlantic/Bermuda']}, {'value': 'Central Brazilian Standard Time', 'abbr': 'CBST', 'utc': ['America/Campo_Grande', 'America/Cuiaba']}, {'value': 'SA Western Standard Time', 'abbr': 'SWST', 'utc': ['America/Anguilla', 'America/Antigua', 'America/Aruba', 'America/Barbados', 'America/Blanc-Sablon', 'America/Boa_Vista', 'America/Curacao', 'America/Dominica', 'America/Grand_Turk', 'America/Grenada', 'America/Guadeloupe', 'America/Guyana', 'America/Kralendijk', 'America/La_Paz', 'America/Lower_Princes', 'America/Manaus', 'America/Marigot', 'America/Martinique', 'America/Montserrat', 'America/Port_of_Spain', 'America/Porto_Velho', 'America/Puerto_Rico', 'America/Santo_Domingo', 'America/St_Barthelemy', 'America/St_Kitts', 'America/St_Lucia', 'America/St_Thomas', 'America/St_Vincent', 'America/Tortola', 'Etc/GMT+4']}, {'value': 'Pacific SA Standard Time', 'abbr': 'PSST', 'utc': ['America/Santiago', 'Antarctica/Palmer']}, {'value': 'Newfoundland Standard Time', 'abbr': 'NDT', 'utc': ['America/St_Johns']}, {'value': 'E. South America Standard Time', 'abbr': 'ESAST', 'utc': ['America/Sao_Paulo']}, {'value': 'Argentina Standard Time', 'abbr': 'AST', 'utc': ['America/Argentina/La_Rioja', 'America/Argentina/Rio_Gallegos', 'America/Argentina/Salta', 'America/Argentina/San_Juan', 'America/Argentina/San_Luis', 'America/Argentina/Tucuman', 'America/Argentina/Ushuaia', 'America/Buenos_Aires', 'America/Catamarca', 'America/Cordoba', 'America/Jujuy', 'America/Mendoza']}, {'value': 'SA Eastern Standard Time', 'abbr': 'SEST', 'utc': ['America/Araguaina', 'America/Belem', 'America/Cayenne', 'America/Fortaleza', 'America/Maceio', 'America/Paramaribo', 'America/Recife', 'America/Santarem', 'Antarctica/Rothera', 'Atlantic/Stanley', 'Etc/GMT+3']}, {'value': 'Greenland Standard Time', 'abbr': 'GDT', 'utc': ['America/Godthab']}, {'value': 'Montevideo Standard Time', 'abbr': 'MST', 'utc': ['America/Montevideo']}, {'value': 'Bahia Standard Time', 'abbr': 'BST', 'utc': ['America/Bahia']}, {'value': 'UTC-02', 'abbr': 'U', 'utc': ['America/Noronha', 'Atlantic/South_Georgia', 'Etc/GMT+2']}, {'value': 'Mid-Atlantic Standard Time', 'abbr': 'MDT', 'utc': []}, {'value': 'Azores Standard Time', 'abbr': 'ADT', 'utc': ['America/Scoresbysund', 'Atlantic/Azores']}, {'value': 'Cape Verde Standard Time', 'abbr': 'CVST', 'utc': ['Atlantic/Cape_Verde', 'Etc/GMT+1']}, {'value': 'Morocco Standard Time', 'abbr': 'MDT', 'utc': ['Africa/Casablanca', 'Africa/El_Aaiun']}, {'value': 'UTC', 'abbr': 'UTC', 'utc': ['America/Danmarkshavn', 'Etc/GMT']}, {'value': 'GMT Standard Time', 'abbr': 'GMT', 'utc': ['Europe/Isle_of_Man', 'Europe/Guernsey', 'Europe/Jersey', 'Europe/London']}, {'value': 'British Summer Time', 'abbr': 'BST', 'utc': ['Europe/Isle_of_Man', 'Europe/Guernsey', 'Europe/Jersey', 'Europe/London']}, {'value': 'GMT Standard Time', 'abbr': 'GDT', 'utc': ['Atlantic/Canary', 'Atlantic/Faeroe', 'Atlantic/Madeira', 'Europe/Dublin', 'Europe/Lisbon']}, {'value': 'Greenwich Standard Time', 'abbr': 'GST', 'utc': ['Africa/Abidjan', 'Africa/Accra', 'Africa/Bamako', 'Africa/Banjul', 'Africa/Bissau', 'Africa/Conakry', 'Africa/Dakar', 'Africa/Freetown', 'Africa/Lome', 'Africa/Monrovia', 'Africa/Nouakchott', 'Africa/Ouagadougou', 'Africa/Sao_Tome', 'Atlantic/Reykjavik', 'Atlantic/St_Helena']}, {'value': 'W. Europe Standard Time', 'abbr': 'WEDT', 'utc': ['Arctic/Longyearbyen', 'Europe/Amsterdam', 'Europe/Andorra', 'Europe/Berlin', 'Europe/Busingen', 'Europe/Gibraltar', 'Europe/Luxembourg', 'Europe/Malta', 'Europe/Monaco', 'Europe/Oslo', 'Europe/Rome', 'Europe/San_Marino', 'Europe/Stockholm', 'Europe/Vaduz', 'Europe/Vatican', 'Europe/Vienna', 'Europe/Zurich']}, {'value': 'Central Europe Standard Time', 'abbr': 'CEDT', 'utc': ['Europe/Belgrade', 'Europe/Bratislava', 'Europe/Budapest', 'Europe/Ljubljana', 'Europe/Podgorica', 'Europe/Prague', 'Europe/Tirane']}, {'value': 'Romance Standard Time', 'abbr': 'RDT', 'utc': ['Africa/Ceuta', 'Europe/Brussels', 'Europe/Copenhagen', 'Europe/Madrid', 'Europe/Paris']}, {'value': 'Central European Standard Time', 'abbr': 'CEDT', 'utc': ['Europe/Sarajevo', 'Europe/Skopje', 'Europe/Warsaw', 'Europe/Zagreb']}, {'value': 'W. Central Africa Standard Time', 'abbr': 'WCAST', 'utc': ['Africa/Algiers', 'Africa/Bangui', 'Africa/Brazzaville', 'Africa/Douala', 'Africa/Kinshasa', 'Africa/Lagos', 'Africa/Libreville', 'Africa/Luanda', 'Africa/Malabo', 'Africa/Ndjamena', 'Africa/Niamey', 'Africa/Porto-Novo', 'Africa/Tunis', 'Etc/GMT-1']}, {'value': 'Namibia Standard Time', 'abbr': 'NST', 'utc': ['Africa/Windhoek']}, {'value': 'GTB Standard Time', 'abbr': 'GDT', 'utc': ['Asia/Nicosia', 'Europe/Athens', 'Europe/Bucharest', 'Europe/Chisinau']}, {'value': 'Middle East Standard Time', 'abbr': 'MEDT', 'utc': ['Asia/Beirut']}, {'value': 'Egypt Standard Time', 'abbr': 'EST', 'utc': ['Africa/Cairo']}, {'value': 'Syria Standard Time', 'abbr': 'SDT', 'utc': ['Asia/Damascus']}, {'value': 'E. Europe Standard Time', 'abbr': 'EEDT', 'utc': ['Asia/Nicosia', 'Europe/Athens', 'Europe/Bucharest', 'Europe/Chisinau', 'Europe/Helsinki', 'Europe/Kiev', 'Europe/Mariehamn', 'Europe/Nicosia', 'Europe/Riga', 'Europe/Sofia', 'Europe/Tallinn', 'Europe/Uzhgorod', 'Europe/Vilnius', 'Europe/Zaporozhye']}, {'value': 'South Africa Standard Time', 'abbr': 'SAST', 'utc': ['Africa/Blantyre', 'Africa/Bujumbura', 'Africa/Gaborone', 'Africa/Harare', 'Africa/Johannesburg', 'Africa/Kigali', 'Africa/Lubumbashi', 'Africa/Lusaka', 'Africa/Maputo', 'Africa/Maseru', 'Africa/Mbabane', 'Etc/GMT-2']}, {'value': 'FLE Standard Time', 'abbr': 'FDT', 'utc': ['Europe/Helsinki', 'Europe/Kiev', 'Europe/Mariehamn', 'Europe/Riga', 'Europe/Sofia', 'Europe/Tallinn', 'Europe/Uzhgorod', 'Europe/Vilnius', 'Europe/Zaporozhye']}, {'value': 'Turkey Standard Time', 'abbr': 'TDT', 'utc': ['Europe/Istanbul']}, {'value': 'Israel Standard Time', 'abbr': 'JDT', 'utc': ['Asia/Jerusalem']}, {'value': 'Libya Standard Time', 'abbr': 'LST', 'utc': ['Africa/Tripoli']}, {'value': 'Jordan Standard Time', 'abbr': 'JST', 'utc': ['Asia/Amman']}, {'value': 'Arabic Standard Time', 'abbr': 'AST', 'utc': ['Asia/Baghdad']}, {'value': 'Kaliningrad Standard Time', 'abbr': 'KST', 'utc': ['Europe/Kaliningrad']}, {'value': 'Arab Standard Time', 'abbr': 'AST', 'utc': ['Asia/Aden', 'Asia/Bahrain', 'Asia/Kuwait', 'Asia/Qatar', 'Asia/Riyadh']}, {'value': 'E. Africa Standard Time', 'abbr': 'EAST', 'utc': ['Africa/Addis_Ababa', 'Africa/Asmera', 'Africa/Dar_es_Salaam', 'Africa/Djibouti', 'Africa/Juba', 'Africa/Kampala', 'Africa/Khartoum', 'Africa/Mogadishu', 'Africa/Nairobi', 'Antarctica/Syowa', 'Etc/GMT-3', 'Indian/Antananarivo', 'Indian/Comoro', 'Indian/Mayotte']}, {'value': 'Moscow Standard Time', 'abbr': 'MSK', 'utc': ['Europe/Kirov', 'Europe/Moscow', 'Europe/Simferopol', 'Europe/Volgograd', 'Europe/Minsk']}, {'value': 'Samara Time', 'abbr': 'SAMT', 'utc': ['Europe/Astrakhan', 'Europe/Samara', 'Europe/Ulyanovsk']}, {'value': 'Iran Standard Time', 'abbr': 'IDT', 'utc': ['Asia/Tehran']}, {'value': 'Arabian Standard Time', 'abbr': 'AST', 'utc': ['Asia/Dubai', 'Asia/Muscat', 'Etc/GMT-4']}, {'value': 'Azerbaijan Standard Time', 'abbr': 'ADT', 'utc': ['Asia/Baku']}, {'value': 'Mauritius Standard Time', 'abbr': 'MST', 'utc': ['Indian/Mahe', 'Indian/Mauritius', 'Indian/Reunion']}, {'value': 'Georgian Standard Time', 'abbr': 'GET', 'utc': ['Asia/Tbilisi']}, {'value': 'Caucasus Standard Time', 'abbr': 'CST', 'utc': ['Asia/Yerevan']}, {'value': 'Afghanistan Standard Time', 'abbr': 'AST', 'utc': ['Asia/Kabul']}, {'value': 'West Asia Standard Time', 'abbr': 'WAST', 'utc': ['Antarctica/Mawson', 'Asia/Aqtau', 'Asia/Aqtobe', 'Asia/Ashgabat', 'Asia/Dushanbe', 'Asia/Oral', 'Asia/Samarkand', 'Asia/Tashkent', 'Etc/GMT-5', 'Indian/Kerguelen', 'Indian/Maldives']}, {'value': 'Yekaterinburg Time', 'abbr': 'YEKT', 'utc': ['Asia/Yekaterinburg']}, {'value': 'Pakistan Standard Time', 'abbr': 'PKT', 'utc': ['Asia/Karachi']}, {'value': 'Indian Standard Time', 'abbr': 'IST', 'utc': ['Asia/Kolkata']}, {'value': 'Sri Lanka Standard Time', 'abbr': 'SLST', 'utc': ['Asia/Colombo']}, {'value': 'Nepal Standard Time', 'abbr': 'NST', 'utc': ['Asia/Kathmandu']}, {'value': 'Central Asia Standard Time', 'abbr': 'CAST', 'utc': ['Antarctica/Vostok', 'Asia/Almaty', 'Asia/Bishkek', 'Asia/Qyzylorda', 'Asia/Urumqi', 'Etc/GMT-6', 'Indian/Chagos']}, {'value': 'Bangladesh Standard Time', 'abbr': 'BST', 'utc': ['Asia/Dhaka', 'Asia/Thimphu']}, {'value': 'Myanmar Standard Time', 'abbr': 'MST', 'utc': ['Asia/Rangoon', 'Indian/Cocos']}, {'value': 'SE Asia Standard Time', 'abbr': 'SAST', 'utc': ['Antarctica/Davis', 'Asia/Bangkok', 'Asia/Hovd', 'Asia/Jakarta', 'Asia/Phnom_Penh', 'Asia/Pontianak', 'Asia/Saigon', 'Asia/Vientiane', 'Etc/GMT-7', 'Indian/Christmas']}, {'value': 'N. Central Asia Standard Time', 'abbr': 'NCAST', 'utc': ['Asia/Novokuznetsk', 'Asia/Novosibirsk', 'Asia/Omsk']}, {'value': 'China Standard Time', 'abbr': 'CST', 'utc': ['Asia/Hong_Kong', 'Asia/Macau', 'Asia/Shanghai']}, {'value': 'North Asia Standard Time', 'abbr': 'NAST', 'utc': ['Asia/Krasnoyarsk']}, {'value': 'Singapore Standard Time', 'abbr': 'MPST', 'utc': ['Asia/Brunei', 'Asia/Kuala_Lumpur', 'Asia/Kuching', 'Asia/Makassar', 'Asia/Manila', 'Asia/Singapore', 'Etc/GMT-8']}, {'value': 'W. Australia Standard Time', 'abbr': 'WAST', 'utc': ['Antarctica/Casey', 'Australia/Perth']}, {'value': 'Taipei Standard Time', 'abbr': 'TST', 'utc': ['Asia/Taipei']}, {'value': 'Ulaanbaatar Standard Time', 'abbr': 'UST', 'utc': ['Asia/Choibalsan', 'Asia/Ulaanbaatar']}, {'value': 'North Asia East Standard Time', 'abbr': 'NAEST', 'utc': ['Asia/Irkutsk']}, {'value': 'Japan Standard Time', 'abbr': 'JST', 'utc': ['Asia/Dili', 'Asia/Jayapura', 'Asia/Tokyo', 'Etc/GMT-9', 'Pacific/Palau']}, {'value': 'Korea Standard Time', 'abbr': 'KST', 'utc': ['Asia/Pyongyang', 'Asia/Seoul']}, {'value': 'Cen. Australia Standard Time', 'abbr': 'CAST', 'utc': ['Australia/Adelaide', 'Australia/Broken_Hill']}, {'value': 'AUS Central Standard Time', 'abbr': 'ACST', 'utc': ['Australia/Darwin']}, {'value': 'E. Australia Standard Time', 'abbr': 'EAST', 'utc': ['Australia/Brisbane', 'Australia/Lindeman']}, {'value': 'AUS Eastern Standard Time', 'abbr': 'AEST', 'utc': ['Australia/Melbourne', 'Australia/Sydney']}, {'value': 'West Pacific Standard Time', 'abbr': 'WPST', 'utc': ['Antarctica/DumontDUrville', 'Etc/GMT-10', 'Pacific/Guam', 'Pacific/Port_Moresby', 'Pacific/Saipan', 'Pacific/Truk']}, {'value': 'Tasmania Standard Time', 'abbr': 'TST', 'utc': ['Australia/Currie', 'Australia/Hobart']}, {'value': 'Yakutsk Standard Time', 'abbr': 'YST', 'utc': ['Asia/Chita', 'Asia/Khandyga', 'Asia/Yakutsk']}, {'value': 'Central Pacific Standard Time', 'abbr': 'CPST', 'utc': ['Antarctica/Macquarie', 'Etc/GMT-11', 'Pacific/Efate', 'Pacific/Guadalcanal', 'Pacific/Kosrae', 'Pacific/Noumea', 'Pacific/Ponape']}, {'value': 'Vladivostok Standard Time', 'abbr': 'VST', 'utc': ['Asia/Sakhalin', 'Asia/Ust-Nera', 'Asia/Vladivostok']}, {'value': 'New Zealand Standard Time', 'abbr': 'NZST', 'utc': ['Antarctica/McMurdo', 'Pacific/Auckland']}, {'value': 'UTC+12', 'abbr': 'U', 'utc': ['Etc/GMT-12', 'Pacific/Funafuti', 'Pacific/Kwajalein', 'Pacific/Majuro', 'Pacific/Nauru', 'Pacific/Tarawa', 'Pacific/Wake', 'Pacific/Wallis']}, {'value': 'Fiji Standard Time', 'abbr': 'FST', 'utc': ['Pacific/Fiji']}, {'value': 'Magadan Standard Time', 'abbr': 'MST', 'utc': ['Asia/Anadyr', 'Asia/Kamchatka', 'Asia/Magadan', 'Asia/Srednekolymsk']}, {'value': 'Kamchatka Standard Time', 'abbr': 'KDT', 'utc': ['Asia/Kamchatka']}, {'value': 'Tonga Standard Time', 'abbr': 'TST', 'utc': ['Etc/GMT-13', 'Pacific/Enderbury', 'Pacific/Fakaofo', 'Pacific/Tongatapu']}, {'value': 'Samoa Standard Time', 'abbr': 'SST', 'utc': ['Pacific/Apia']}]

#indian standard time
def isTimezoneName(name):
    for timezone in timezones:
        if(timezone["value"] == name):
            return True
    return False

#indian standard time -> ist
# ist -> ist
def getTimezone(name):
    modified = name[:-1]
    for timezone in timezones:
        if(timezone["value"] == name):
            return timezone["abbr"]
        elif(timezone["abbr"] == name or timezone["abbr"] == modified):
            return name
    return False

#ist is a timezone or not 
def isTimezoneAbbr(abbr):
    modified = abbr[:-1]
    for timezone in timezones:
        if(timezone["abbr"] == abbr or timezone["abbr"] == modified):
            return True
    return False

def isTimezoneAbbrOrig(abbr):
    for timezone in timezones:
        if(timezone["abbr"] == abbr):
            return True
    return False

def isNumberinWord(word):
    for letter in word:
        if(letter.isdigit()):
            return True
    return False

def isDate(word):
    prefix = "CF:D:"
    formatList = [
                  '%d.%m.%y', '%d.%m.%Y',
                  '%d/%m/%y', '%d/%m/%Y',
                  '%d-%m-%y','%d-%m-%Y',
                  '%m.%d.%y', '%m.%d.%Y',
                  '%m/%d/%y', '%m/%d/%Y',
                  '%m-%d-%y','%m-%d-%Y',
                  '%y.%m.%d', '%Y.%m.%d',
                  '%y/%m/%d', '%Y/%m/%d',
                  '%y-%m-%d', '%Y-%m-%d',
                 ]
    
    for fmt in formatList:
        try:
            val = datetime.datetime.strptime(word,fmt)
            date = str(val).split()
            return str(prefix+date[0])
        except ValueError:
            pass
    return None

#checks if it is a time
def isTimeFormat(word):
    formatList = [
                  "%I:%M %p",
                    "%I:%M",
                    "%I %p",
                    "%I:%M:%S %p",
                    "%I:%M:%S"
                 ]
    
    for fmt in formatList:
        try:
            datetime.datetime.strptime(word,fmt)
            return True
        except ValueError:
            pass
    return False

#I = hour, M = min, S = sec, p = AM/PM 
def isTime(word):
    prefix = "CF:T:"
    formatList = [
                  "%I:%M %p",
                    "%I:%M",
                    "%I %p",
                    "%I:%M:%S %p",
                    "%I:%M:%S"
                 ]
    
    for fmt in formatList:
        try:
            in_time = datetime.datetime.strptime(word,fmt)
            out_time = datetime.datetime.strftime(in_time, "%H:%M")
            return str(prefix+out_time)
        except ValueError:
            pass
    return None

#14-07- == -07-14
def reverseDate(date):
    tempDate = ""
    i = len(date) - 1
    stack = []
    while i >= 0:
        if(date[i] == "-"):
            while(len(stack) != 0):
                tempDate += stack.pop()
            tempDate += date[i]
        else:
            stack.append(date[i])
        i = i - 1
    while(len(stack) != 0):
        tempDate += stack.pop()
    return tempDate
        
def convertDate(dateRec):
    date = isDate(dateRec)
    if(date == None):
        prefix = "CF:D:"
        if(len(dateRec) == 2):
            date = prefix+"????-"+dateRec
        elif(len(dateRec) == 6):
            date = prefix+"????"+ reverseDate(dateRec)
        else:
            date = prefix+ reverseDate(dateRec)
    if(date == "CF:D:"):
        return None
    return date

def isFinalDate(date):
    if(date.startswith("CF:D:")):
        return True
    else:
        return False
    
def isUrl(word):
    urlRegex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))" 
    if(re.findall(urlRegex, word)):
        return True
    else:
        return False
    
def isEmoji(word):
    for emoji in emojis:
        if(word == emoji):
            return True
    return False
    
def containsClitic(word):
    tempList = []
    contraction = ""
    if word.lower() in contractions:
        contraction =  contractions[word.lower()]
        if(word.isupper()):
            contraction = contraction.upper()
        elif(word[0].isupper()):
            contraction = contraction[0].upper() + contraction[1:]
    if(len(contraction) != 0):
        tempList = contraction.split()
    return tempList

def containsPunc(word):
    tempList = []
    positions = re.findall("[\.!?:,;\'\"\)\(\]-]", word)
    if(word.startswith("CF:T:")):
        tempList.append(word)
        return tempList
    for pos in positions:
        tempStr = ""
        i = 0
        for letter in word:
            i += 1
            if(letter != pos):
                tempStr += letter 
            else:
                if(letter == "'"):
                    idx = word.index(letter)
                    #apostrophe should be last letter of word and before apostrophe there should be s
                    if(idx == len(word) - 1 and (idx - 1) >= 0 and word[idx-1] == "s"):
                        tempList.append(tempStr)
                        tempList.append("'s")
                        word = word[idx+1:]
                    elif(idx+1 < len(word) and word[idx+1] == "s" and (idx+2 == len(word) or word[idx+2].isalpha() == False)):
                        if(len(tempStr) != 0):
                            tempList.append(tempStr)
                        tempStr = "'s"
                        tempList.append(tempStr)
                        word = word[idx+2:]
                    else:
                        if(len(tempStr) != 0):
                            tempList.append(tempStr)
                        tempList.append(pos)
                        word = word[i:]
                    
                elif(len(tempStr) != 0):
                    tempList.append(tempStr)
                    tempList.append(pos)
                    word = word[i:]
                
                elif(letter == pos and len(tempStr) == 0):
                    tempList.append(pos)
                    word = word[i:]
                break
    if(len(word) != 0):
        tempList.append(word)
    return tempList

filePath = "111703070_Assgn1Dataset-1.txt"

try:
    with open(filePath, 'r') as fp:
        tweets = fp.readlines()
except IOError as e:
    print("Couldn't open or read file (%s)." % e)
    

tokens = []
for tweet in tweets :
    
    words = tweet.split()
    
    #TIME
    wordIndex = 0
    while (wordIndex < len(words)) :
        if(wordIndex + 1 < len(words) and (words[wordIndex+1] == "o'clock" or words[wordIndex+1] == "O'Clock")):
            if(isTimeFormat(words[wordIndex] + " am")):
                words[wordIndex+1] = "am"
                
        #7:00:00 || 7:00|| 7 && AM||PM && IST||Indian Standard Time||any word after it
        if(wordIndex+1 < len(words)  and
            (words[wordIndex+1] == "AM" or words[wordIndex+1] == "PM" or
            words[wordIndex+1] == "am" or words[wordIndex+1] == "pm")
           and isTimeFormat(words[wordIndex]+" " + words[wordIndex+1]) and wordIndex+2 < len(words)):
                time = isTime(words[wordIndex]+" "+words[wordIndex+1])
                if(isTimezoneAbbr(words[wordIndex+2])):
                    if(isTimezoneAbbrOrig(words[wordIndex+2])):
                        time += ":" + getTimezone(words[wordIndex+2])
                        words.pop(wordIndex) #IST
                        words.pop(wordIndex) #am/pm
                        words.pop(wordIndex) #number
                        words.insert(wordIndex, time)
                    else:
                        punc = words[wordIndex+2][-1]
                        time += ":" + getTimezone(words[wordIndex+2][:-1])
                        words.pop(wordIndex) #IST.
                        words.pop(wordIndex)
                        words.pop(wordIndex)
                        words.insert(wordIndex, time)
                        words.insert(wordIndex+1, punc)
                else:
                    tempStr = words[wordIndex+2] #indian
                    j = wordIndex+3 #standard
                    countWords = 1
                    puncFlag = 0
                    while(j < len(words)):
                        if(re.findall("[\.!?:,;\'\"\)\(\]-]$", words[j])):
                            puncFlag = 1
                            punc = words[j][-1]
                            tempStr += " " + words[j][:-1]
                        else:
                            tempStr += " " + words[j]
                        countWords += 1
                        if(words[j] == "Time" or words[j] == "time" or words[j][:-1] == "Time" or words[j][:-1] == "time"):
                            break
                        j += 1
                    if(isTimezoneName(tempStr)):
                        time += ":" + getTimezone(tempStr)
                        while(countWords > 0):
                            words.pop(wordIndex)
                            countWords -= 1
                        words.pop(wordIndex) #am or pm
                        words.pop(wordIndex) #number
                        words.insert(wordIndex, time)
                        if(puncFlag == 1):
                            words.insert(wordIndex+1, punc)
                    else:
                        time = isTime(words[wordIndex]+" "+words[wordIndex+1])
                        words.pop(wordIndex)
                        words.pop(wordIndex)
                        words.insert(wordIndex, time)
            
        #7:00:00 || 7:00  IST || 7:00 IST.
        elif(isTimeFormat(words[wordIndex]) and 
           wordIndex+1 < len(words) and isTimezoneAbbr(words[wordIndex+1])):
            time = isTime(words[wordIndex])
            if(isTimezoneAbbrOrig(words[wordIndex+1])):
                time += ":" + getTimezone(words[wordIndex+1])
                words.pop(wordIndex)
                words.pop(wordIndex)
                words.insert(wordIndex, time)
            else:
                #IST.
                punc = words[wordIndex+1][-1]
                time += ":" + getTimezone(words[wordIndex+1][:-1])
                words.pop(wordIndex)
                words.pop(wordIndex)
                words.insert(wordIndex, time)
                words.insert(wordIndex+1, punc)
            
        # 7:00 Indian standard time || 7:00 Indian standard time.
        elif(isTimeFormat(words[wordIndex]) and wordIndex+1 < len(words) and 
             (words[wordIndex+1] != "AM" or words[wordIndex+1] != "PM" or
            words[wordIndex+1] != "am" or words[wordIndex+1] != "pm")):
            time = isTime(words[wordIndex])
            tempStr = words[wordIndex+1] #indian
            j = wordIndex+2 #standard
            countWords = 1
            puncFlag = 0
            while(j < len(words)):
                if(re.findall("[\.!?:,;\'\"\)\(\]-]$", words[j])):
                    puncFlag = 1
                    punc = words[j][-1]
                    tempStr += " " + words[j][:-1]
                else:
                    tempStr += " " + words[j]
                countWords += 1
                if(words[j] == "Time" or words[j] == "time" or words[j][:-1] == "Time" or words[j][:-1] == "time"):
                    break
                j += 1
            if(isTimezoneName(tempStr)):
                time += ":" + getTimezone(tempStr)
                while(countWords > 0):
                    words.pop(wordIndex)
                    countWords -= 1
                words.pop(wordIndex) #number
                words.insert(wordIndex, time)
                if(puncFlag == 1):
                    words.insert(wordIndex+1, punc)
            else:
                time = isTime(words[wordIndex])
                words.pop(wordIndex)
                words.insert(wordIndex, time)
        
        #7:00:00 || 7:00|| 7 AM||PM
        elif(wordIndex+1 < len(words)  and
            (words[wordIndex+1] == "AM" or words[wordIndex+1] == "PM" or
            words[wordIndex+1] == "am" or words[wordIndex+1] == "pm")
            and isTimeFormat(words[wordIndex]+" " + words[wordIndex+1])):
            time = isTime(words[wordIndex]+" "+words[wordIndex+1])
            words.pop(wordIndex)
            words.pop(wordIndex)
            words.insert(wordIndex, time)
        #7:00:00 || 7:00 || 7:00.
        elif(isTimeFormat(words[wordIndex]) or isTimeFormat(words[wordIndex][:-1])):
            if(isTimeFormat(words[wordIndex])):
                time = isTime(words[wordIndex])
                words.pop(wordIndex)
                words.insert(wordIndex, time)
            else:
                punc = words[wordIndex][-1]
                time = isTime(words[wordIndex][:-1])
                words.pop(wordIndex)
                words.insert(wordIndex, time)
                words.insert(wordIndex+1, punc)
        
        wordIndex += 1
    
    #CLITIC
    wordIndex = 0
    while (wordIndex < len(words)) :
        tempList = containsClitic(words[wordIndex])
        if(len(tempList) > 1):
            words.pop(wordIndex)
            words[wordIndex:wordIndex] = tempList
            wordIndex += len(tempList) - 1
        wordIndex += 1
     
    #PUNCTUATION
    wordIndex = 0
    while wordIndex < len(words) :
        if(isUrl(words[wordIndex]) == False and isEmoji(words[wordIndex]) == False and isEmoji(words[wordIndex].lower()) == False and isEmoji(words[wordIndex][:-1]) == False and isEmoji(words[wordIndex][:-1].lower()) == False):
            tempList = containsPunc(words[wordIndex])
            if(len(tempList) > 1):
                words.pop(wordIndex)
                words[wordIndex:wordIndex] = tempList
                wordIndex += len(tempList) - 1
        wordIndex += 1
        
    
    #DATE
    wordIndex = 0
    while wordIndex < len(words) :
        finalDate = ""
        if(wordIndex+1 < len(words) and words[wordIndex+1] == "'" and words[wordIndex] in months):
            month = months[words[wordIndex]]
            finalDate += month
            if(wordIndex+2 < len(words) and isNumberinWord(words[wordIndex+2])):
                finalDate += "-"
                for letter in words[wordIndex+2]:
                    if(letter.isdigit()):
                        finalDate += letter
            date = convertDate(finalDate)
            words.pop(wordIndex)
            words.pop(wordIndex)
            words.pop(wordIndex)
            words.insert(wordIndex, date)
        elif(words[wordIndex] in months):
            month = months[words[wordIndex]]
            if(wordIndex-1 >= 0 and isNumberinWord(words[wordIndex-1]) and isFinalDate(words[wordIndex-1]) == False):
                for letter in words[wordIndex-1]:
                    if(letter.isdigit()):
                        finalDate += letter
                finalDate += "-" + month + "-"
                if(wordIndex+1 < len(words)):
                    if(re.findall("[\.!?:,;\'\"\)\(\]-]", words[wordIndex+1])):
                        if(wordIndex+2 < len(words)):
                            for letter in words[wordIndex+2]:
                                if(letter.isdigit()):
                                    finalDate += letter
                        date = convertDate(finalDate)
                        words.pop(wordIndex-1)
                        words.pop(wordIndex-1)
                        words.pop(wordIndex-1)
                        words.pop(wordIndex-1)
                        words.insert(wordIndex-1, date)
                    else:
                        lengthNum = 0
                        isPureNumber = 0
                        for letter in words[wordIndex+1]:
                            if(letter.isdigit()):
                                finalDate += letter
                                lengthNum += 1
                                isPureNumber = 1
                            else:
                                isPureNumber = 0
                                break
                        date = convertDate(finalDate)
                        if((lengthNum == 2 or lengthNum == 4) and isPureNumber == 1):
                            words.pop(wordIndex-1)
                            words.pop(wordIndex-1)
                            words.pop(wordIndex-1)
                            words.insert(wordIndex-1, date)
                        else:
                            words.pop(wordIndex-1)
                            words.pop(wordIndex-1)
                            words.insert(wordIndex-1, date)
                        
                else:
                    date = convertDate(finalDate)
                    words.pop(wordIndex-1)
                    words.pop(wordIndex-1)
                    words.insert(wordIndex-1, date)
            elif(wordIndex+1 < len(words) and isNumberinWord(words[wordIndex+1])):
                finalDate = month +"-"
                for letter in words[wordIndex+1]:
                    if(letter.isdigit()):
                        finalDate += letter
                date = convertDate(finalDate)
                words.pop(wordIndex)
                words.pop(wordIndex)
                words.insert(wordIndex, date)
            else:
                finalDate = month
                date = convertDate(finalDate)
                words[wordIndex] = date
        wordIndex += 1
    
    
    tokens.append(words)
#print(tokens)

outputFile = "outputSpyder.txt"

try:
    with open(outputFile, 'w') as fp:
       i = 0
       while i < len(tweets) :
            fp.write(tweets[i])
            if(i == len(tweets)-1):
                fp.write("\n")
            fp.write(str(len(tokens[i])))
            fp.write("\n")
            tokenCount = 0
            while tokenCount < len(tokens[i]):
                if(i == len(tweets)-1 and tokenCount == len(tokens[i]) -1):
                     temp = tokens[i][tokenCount]
                     fp.write(temp)
                     break
                temp = tokens[i][tokenCount] + "\n"
                fp.write(temp)
                tokenCount += 1
            i += 1
except IOError as e:
    print("Couldn't open or write to file (%s)." % e)
    
    



