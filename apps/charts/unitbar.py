#-*-coding:utf-8 -*-，

def strDict(sourcelist,resultlist):

	a_active= []
	for a in sourcelist:
		a_active.append({"name": a, "value": 0})


	for ai in a_active:
		for ab in resultlist:
			if ai["name"] == ab["name"]:
				ai["name"] = ab["name"]
				ai["value"] = ab["value"]
				continue
			else:
				pass
	return a_active

