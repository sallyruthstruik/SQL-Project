fd = open("dump.sql", "w")

fd.write("create table test(")
for i in range(1000):
    fd.write("\n\t`%s` int(10),"%(i))

fd.write("\n\t`1001` int(10));")