#!/bin/bash
here="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

result="$here/result.out"
if [ ! -z "$1" ]; then 
	result="$1"
fi 

policy=("GradualRelease" "TightRelease" "AccordingToPolicy" "Crypto"   "ForgetfulAtkSingle" "DynamicNoninterference")
mkdir -p "$here/result"
echo -e "Policy (total): \t(PASS,  FAIL,  N/A) "
for p in ${policy[*]}; 
do 
    grep -E "\| *$p" "$result" > "$here/result/$p.out"
    total=$(cat "$here/result/$p.out" | wc -l)
    pass=$(grep -E " - " "$here/result/$p.out" | wc -l)
    fail=$(grep -E " X " "$here/result/$p.out" | wc -l)
    na=$(grep -E " N/A " "$here/result/$p.out" | wc -l)
    echo -e "$p (${total//[[:blank:]]/}): \t\t\t\t (${pass//[[:blank:]]/},  ${fail//[[:blank:]]/},  ${na//[[:blank:]]/})"
    rm -f "$here/result/$p.out"
done
rm -rf "$here/result"
