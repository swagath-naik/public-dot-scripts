#! /bin/bash
# This script is used for logging to College Lan/Wifi captive profile and it refreshes login after a given specified time. 
# VARS
###########################################################
port="1000"		# change port if needed
sleep_secs=1200		# change refresh time if needed
user_name=""		# set username
pass_word=""		# set password
###########################################################
ip_gateway="$(route -n | grep 'UG[ \t]' | awk '{print $2}')"
ip_addrs="$(ip -4 a  | grep inet | cut -d' ' -f 6 | cut -d'/' -f1)"
url_site="http://$ip_gateway:$port"


# LOGIN
magic="$(curl -v --silent $url_site/login? 2>&1 | grep magic | cut -d' ' -f14 | cut -d'"' -f2)"
keep_alive="$(curl -v --silent -d "username=$user_name&password=$pass_word&magic=$magic&4Tredir=$url_site/login?" -X POST $url_site 2>&1 | grep Location | cut -d' ' -f3)"
ret=$?
if [ $ret -eq 0 ]; then
	tput setaf 11;echo "Logging in as : $user_name"
fi
tput setaf 11; echo "LOGIN : $(date)"
tput setaf 11; echo "IPv4-list: $ip_addrs" | tr ' ' '\n'
tput setaf 11; echo "Gateway: $ip_gateway"

# LOGOUT TRAP
trap 'curl -s -o /dev/null $url_site/logout? && tput setaf 11; echo -e "\nLOGOUT : $(date)" && exit' SIGHUP
trap 'curl -s -o /dev/null $url_site/logout? && tput setaf 11; echo -e "\nLOGOUT : $(date)" && exit' SIGINT
trap 'curl -s -o /dev/null $url_site/logout? && tput setaf 11; echo -e "\nLOGOUT : $(date)" && exit' SIGKILL
trap 'curl -s -o /dev/null $url_site/logout? && tput setaf 11; echo -e "\nLOGOUT : $(date)" && exit' SIGTERM

# LOOP
while true
do
	tput setaf 10; echo "$keep_alive"
	tput setaf 10; echo "Refresh every $sleep_secs seconds"
	curl -s -o /dev/null "${keep_alive[@]%$'\r'}"
	ret=$?
	if [ $ret -ne 0 ]; then
		tput setaf 1; echo "LOGIN FAIL : $(date)"
        	exit 1
	fi
	sleep $sleep_secs
done


