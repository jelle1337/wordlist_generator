import os
import datetime
import itertools
import argparse
import configparser
from shutil import copyfile
import sys
# add arguments for wordlist size
parser = argparse.ArgumentParser()
parser.add_argument('-s','--small',action='store_true')
parser.add_argument('-m','--medium',action='store_true')
parser.add_argument('-l','--large',action='store_true')
parser.add_argument('-t','--temporary',action='store_true')
parser.add_argument('-f','--flush',action='store_true')
args = parser.parse_args()
config = configparser.ConfigParser()
def flush():
    copyfile('/home/user/tools/wordlist_gen/info_templ.cfg','/home/user/tools/wordlist_gen/info.cfg')

if args.flush:
    flush()
    sys.exit()
if args.temporary:
    copyfile('/home/user/tools/wordlist_gen/info.cfg', '/tmp/info.cfg')
    copyfile('/home/user/tools/wordlist_gen/info_templ.cfg','/home/user/tools/wordlist_gen/info.cfg')
    config.read('/tmp/info.cfg')
else:
    config.read('info.cfg')
CONFIG = {
        "birthyear": config.get("information","birthyear"),
        "birthmonth": config.get("information","birthmonth"),
        "birthday": config.get("information","birthday"),
        "name": config.get("information","name"),
        "surname": config.get("information","surname"),
        "company": config.get("information","company"),
        "streetname": config.get("information","streetname"),
        "house_address_num": config.get("information","house_address_num"),
        "postal_code": config.get("information","postal_code")}

# get the current date 
date = datetime.datetime.now()
# create a list that will contain passwords
standard_password_list = ['admin','password','P@ssw0rd','P@ssword','qwerty','qwerty123','qwertyuiop']
# supply birthday information
birthyear = CONFIG["birthyear"]
birthmonth = CONFIG["birthmonth"]
birthday = CONFIG["birthday"]
# supply other information
name = CONFIG["name"]
surname = CONFIG["surname"]
company = CONFIG["company"]
streetname = CONFIG["streetname"]
house_address_num = CONFIG["house_address_num"]
postal_code = CONFIG["postal_code"]
# common number combinations + birthday and house address numbers
common_num_comb = ['123','1234','12345','123456','111','222','333','444','555','666','777','888','999',birthyear,birthmonth,birthday,str(date.year),house_address_num]
# combine list
param_list = [name,surname,company,streetname]
# get 10 years in the future and 10 years in the past
for i in range(1,10):
    past_date = date.year - i
    future_date = date.year + i
    common_num_comb.append(str(past_date))
    common_num_comb.append(str(future_date))
# special characters
special_chars = ['!','@','#','$','%','^','&','*']
# dictionary with info
param_dict = {'default':'admin',
             'default2':'password',
             'name':name,
             'surname':surname,
             'company':company,
             'streetname':streetname,
             'postal_code':postal_code}

# combine info function lowercase for instance: name=foo surname=bar result=foobar
def combine_lower(param_list):
    combine_list = []
    for item in itertools.combinations(param_list,2):
        word = ''.join(item)
        combine_list.append(word)
    return combine_list
    
# combine info function uppercase
def combine_upper(param_list):
    combine_list = []
    passwords = combine_lower(param_list)
    for password in passwords:
        upper_passwd = password[0].upper() + password[1::]
        combine_list.append(upper_passwd)
    return combine_list

# combine first letter of name to surname for example: name=foo surname=bar result=far
def combine_lower_first_letter(param_list):
    lower_combine = param_list[0][0] + param_list[1]
    return lower_combine
def combine_upper_first_letter(param_list):
    upper_combine = param_list[0][0].upper() + param_list[1]
    return upper_combine
# capitalize both letters like so: name=foo surname=bar result=FBar
def combine_both_first_letter(param_list):
    both_combine = param_list[0][0].upper() + param_list[1][0].upper() + param_list[1][1:]
    return both_combine

# the wordlist generator
def generator(param_dict,common_num_comb,standard_password_list,special_chars):
# create for loop with information    
    for x in param_dict.keys():
# checks if you supplied information        
        if param_dict[x] != '':
            try:
# adds uppercase, lowercase and reverse passwords to wordlist                
                uppercase = param_dict[x][0].upper() + param_dict[x][1::]
                lowercase = param_dict[x]
                lowercase_rev = param_dict[x][::-1]
                if lowercase_rev == lowercase:
                    pass
                uppercase_rev = lowercase_rev[0].upper() + lowercase_rev[1::]
                if uppercase_rev == uppercase:
                    pass
            
            except IndexError:
                pass
# append the words of the wordlist to a list and supply arguments for listsize            
            standard_password_list.append(lowercase)
            standard_password_list.append(uppercase)
            if args.medium or args.large:
                standard_password_list.append(lowercase_rev)
                standard_password_list.append(uppercase_rev) 
            if args.large:
                standard_password_list.append(combine_lower_first_letter(param_list))
                standard_password_list.append(combine_upper_first_letter(param_list))
                standard_password_list.append(combine_both_first_letter(param_list))
                for i in range(0,100):
                    lower_num = lowercase + str(i)
                    upper_num = uppercase + str(i)
                    standard_password_list.append(lower_num)
                    standard_password_list.append(upper_num)
        for passwd in combine_upper(param_list):
            standard_password_list.append(passwd)
        for passwd in combine_lower(param_list):
            standard_password_list.append(passwd)
# append numbers or special characters to words        
        for num in common_num_comb:
            lowercase_num = lowercase + num
            uppercase_num = uppercase + num
            if args.medium or args.large:
                lowercase_num_rev = lowercase_rev + num
                uppercase_num_rev = uppercase_rev + num
            
            standard_password_list.append(lowercase_num)
            standard_password_list.append(uppercase_num)
            if args.medium or args.large:
                standard_password_list.append(lowercase_num_rev)
                standard_password_list.append(uppercase_num_rev)
                for spec in special_chars:
                    lower_num_spec = lowercase_num + spec
                    upper_num_spec = uppercase_num + spec
                    standard_password_list.append(lower_num_spec)
                    standard_password_list.append(upper_num_spec)

        for spec in special_chars:
            lower_spec = lowercase + spec
            upper_spec = uppercase + spec
            if args.medium or args.large:
                lower_num_spec = lowercase_num + spec
                upper_num_spec = uppercase_num + spec
                standard_password_list.append(lower_spec)
                standard_password_list.append(upper_spec)
    return standard_password_list


passwords = generator(param_dict,common_num_comb,standard_password_list,special_chars)
wordlist = open("wordlist.txt","w")

count = 0
for password in passwords:
    wordlist.write('%s\n' % password)
wordlist.close()
with open("wordlist.txt","r") as f:
    for line in f.readlines():
        count += 1
print(count,'words')
f.close()
