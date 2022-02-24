import dns
import datetime
import time
from datetime import date
import calendar
from dns import query
x = input()

rootList = ['198.41.0.4', '199.9.14.201', '192.33.4.12', '199.7.91.13', '192.203.230.10', '192.5.5.241', '192.112.36.4', '198.97.190.53', '192.36.148.17', '192.58.128.30', '193.0.14.129', '199.7.83.42', '202.12.27.33']
def mydig(x, ip):
    # print(start)
    domain = dns.name.from_text(x)
    # print(ip)
    request = dns.message.make_query(domain, dns.rdatatype.A)
    data = dns.query.udp(request, ip, timeout=20)
    # print(data)
    if dns.rcode.from_flags(data.flags, data.ednsflags) != dns.rcode.NOERROR:
        return ("Warning: DNS ERROR")
    if data.answer != [] and "CNAME" not in data.answer[0].to_text():
        return data.answer[0].to_text()
        # This return statement prints the resource record. It still needs to be parsed to obtain an IP address.
    #CNAME case handled here
    elif data.answer != [] and "CNAME" in data.answer[0].to_text():
        new_domain = data.answer[0].to_text().split()[-1]
        edit_cname = mydig(new_domain, rootList[0]).split()
        edit_cname[0] = x + "."
        # return mydig(new_domain, rootList[0])
        return " ".join(edit_cname)
    # Handling cases where there is an additional section
    elif data.additional != []:
        for i in range(len(data.additional)):
            if ":" not in data.additional[i].to_text().split()[-1]:
                new_IP2 = data.additional[i].to_text().split()[-1]
                break
        return mydig(x, new_IP2)
    elif data.authority != []:
        new_domain = data.authority[0].to_text().split()[-1]
        new_IP = mydig(new_domain, rootList[0]).split()[-1]
        return mydig(x, new_IP)
    else:
        raise Exception



now = datetime.datetime.now()
current_time = now.strftime("%H:%M:%S")
day_of_week = now.strftime('%A')
month = now.strftime("%B")
day = now.strftime("%d")


# for i in range(10):
#    start = time.time()
#    mydig("wikipedia.org", rootList[0])
#    end = time.time()
#        # print(end)
#    query_time = int(round((end - start) * 1000))
#    print(query_time)

start = time.time()
answer = mydig(x, rootList[0]).split('\n')[0]
end = time.time()
query_time = int(round((end - start) * 1000))
print('QUESTION SECTION: \n' + x + '.   IN A\n\nANSWER SECTION: \n' + mydig(x, rootList[0]).split('\n')[0] + "\n\nQuery time: " + str(query_time) + " msec" + "\nWHEN: " + day_of_week + " " + month + " " + day + " " + current_time + " EST 2022")