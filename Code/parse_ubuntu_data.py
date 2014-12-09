import csv
import re
import sys

def parse_emoticons(emoticons):
    obj = {}

    for emo in emoticons:
        join_symbols = []

        for symbol in emoticons[emo]:
            pattern = re.escape(symbol)
            join_symbols.append(pattern)

        obj[emo] = "|".join(join_symbols)

    return obj

def clean_string(raw):
    try:
        string = raw.encode('utf-8').replace('\n', '').replace('\r', '')
    except Exception as inst:
        string = raw.replace('\n', '').replace('\r', '')

    return string

def parse_data(filename, emoticons):
    emos = parse_emoticons(emoticons)

    file_in = filename + ".txt"
    file_out = filename + ".tsv"

    with open(file_in,'rb') as txt, open(file_out, 'wb') as tsv:
        tsv = csv.writer(tsv, delimiter="\t", lineterminator='\n')

        for row in txt:
            # regular expression
            match_timestamp = re.match('^(\[[^\]]*\]){1}', row)
            match_username = re.search('<[^>]*>', row)
            match_message = re.split('^((\[[^\]]*\]){1}[ ]{1}(<[^>]*>){1}[ ]{1}){1}', row)

            if match_timestamp and match_username and len(match_message) == 5:
                timestamp = match_timestamp.group(0)
                username = match_username.group(0)
                message = clean_string(match_message[4])

                # regular expression for emoticon
                label = "none"

                for emo in emos:
                    match_emo = re.search(emos[emo], message)

                    if match_emo:
                        label = emo
                        break

                label = "[" + label + "]"
                row_tsv = [label, timestamp, username, message]
                try:
                    tsv.writerow(row_tsv)
                except Exception as inst:
                    print "There is an error when writing tsv file"
                    sys.exit()

filename = [
"2006-05-27-#ubuntu",
"2006-06-01-#ubuntu",
"2007-04-20-#ubuntu",
"2007-04-21-#ubuntu",
"2007-04-22-#ubuntu",
"2007-10-19-#ubuntu",
"2007-10-20-#ubuntu",
"2007-10-21-#ubuntu",
"2008-04-25-#ubuntu",
"2008-04-26-#ubuntu",
]

emoticons = {
        'positive': [
            ":)",
            ":-)", ":)", ":D", ":o)", ":]", ":3", ":c)", ":>", "=]", "8)",
            "=)", ":}", ":^)",
            ":-D", "8-D", "8D", "x-D", "xD", "X-D", "XD", "=-D", "=D", "=-3", "=3",
            "B^D",
            ":-))",
            ":'-)", ":')",
            ":*", ":^*", "( '}{' )",
            ";-)", ";)", "*-)", "*)", ";-]", ";]", ";D", ";^)", ":-",
            ">:P", ":-P", ":P", "X-P", "x-p", "xp", "XP", ":-p", ":p", "=p", ":-P",
            ":P", ":p", ":-p", ":-b", ":b", "d:"
            ],
        'negative' : [
            ":(", ":'(",
            ">:[", ":-(", ":(",  ":-c", ":c", ":-<", ":<", ":-[", ":[", ":{",
            ";(",
            ":-||", ":@ >:(",
            ":'-(", ":'(",
            "D:<", "D:", "D8", "D;", "D=", "DX", "v.v", "D-':",
            ">:\\", ">:/", ":-/", ":-.", ":/", ":\\", "=/", "=\\", ":L", "=L", ":S", ">.<",
            ":$",
            ">:)", ">;)", ">:-)",
            ]
        }

for f in filename:
    parse_data(f, emoticons)





