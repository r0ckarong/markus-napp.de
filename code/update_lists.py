import subprocess

"""Should list the types of things to check"""

#
# whitelist = ["whitelist",
#              "02c3953435a03bc4e50ad0a5f41f0329",
#              "/etc/pihole/whitelist.txt"]
#
# blacklist = ["blacklist",
#              "36140c95bc105ee13cdc672baa940ab0",
#              "/etc/pihole/blacklist.txt"]
#
# wildcard = ["wildcards",
#             "d136976b382029f7043883bd0f024f07",
#             "/etc/dnsmasq.d/03-pihole-wildcard.conf"]
#
# auditlog = ["auditlog",
#             "127a6725da4b10b8ea3bf0c3699df47e",
#             "/etc/pihole/auditlog.list"]


### Testing
whitelist = ["whitelist",
             "02c3953435a03bc4e50ad0a5f41f0329",
             "/tmp/whitelist.txt"]

blacklist = ["blacklist",
             "36140c95bc105ee13cdc672baa940ab0",
             "/tmp/blacklist.txt"]

wildcard = ["wildcards",
            "d136976b382029f7043883bd0f024f07",
            "/tmp/03-pihole-wildcard.conf"]

auditlog = ["auditlog",
            "127a6725da4b10b8ea3bf0c3699df47e",
            "/tmp/auditlog.list"]


typelist = [whitelist, blacklist, wildcard, auditlog]

listcount=len(typelist)

count=0

while count < listcount:
    listfile = subprocess.Popen(['gist', '-r', typelist[count][1]], bufsize=2,
                                stdout=subprocess.PIPE)

    f = open("/tmp/" + typelist[count][0] + ".tmp", 'w')

    for line in iter(listfile.stdout.readline, ''):
        #print line
        f.write(line)

    f.close()

    filename = "/tmp/" + typelist[count][0] + ".diff"
    print "Filename is " + filename

    diff = subprocess.Popen(['diff',filename,typelist[count][2]], bufsize=2, stdout=subprocess.PIPE)
    diffy = open(filename, 'w')
    for diffline in iter(diff.stdout.readline, ''):
        print diffline
        diffy.write(diffline)

    diffy.close()

    count += 1
