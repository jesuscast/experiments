rawFile = open("./latest/data_dump.csv")
raw = rawFile.read()
rawFile.close()

listData = [ n.split("|") for n in raw.split("\n") ][:-1]
amperages = [ n[8] for n in listData ]
timestamps = [ n[2] for n in listData ]
