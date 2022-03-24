file=open("gram.txt","r")
gr=file.read()
gr=gr.split("\n")
var=gr[0].split(",")
alpha=gr[1].split(",")
gr.pop(0)
gr.pop(0)
for i in range(0,len(gr)):
    gr[i]=gr[i].split("-->")
