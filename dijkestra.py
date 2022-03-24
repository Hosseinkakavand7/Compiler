graph=[]
print("Enter in this format \nV1,V2,Weigh")
while True:
    a=str(input())
    if a=="end":
        break
    a=a.split(",")
    graph.append({"V1":a[0],"V2":a[1],"Weigh":int(a[2]),"Number:":len(graph)})
a=input("Enter The V for start")
V=[]
for i in range(0,len(graph)):
    if graph[i]["V1"] not in V:
        V.append(graph[i]["V1"])
    if graph[i]["V2"] not in V:
        V.append(graph[i]["V2"])
i=1
S=[]
S.append(str(a))
while i <len(V):

    i+=1