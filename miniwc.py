import sys

def wc(filename):
   wordcount=0
   the_file=open(filename,"r")
   lines=len(the_file.readlines())
   with open(filename,"r") as file:
      for line in file:
         wordcount += len(line.split())
   size=sys.getsizeof(the_file)
   return lines,wordcount,size,filename
   the_file.close()

if __name__ == "__main__":
    
    filewc = (sys.argv[1])

    

print(wc(filewc))

#print(press enter to exit)

