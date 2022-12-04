from random import randint
import random
import math

INT_MAX = 2147483647

#Binary only have 1 and 0
V=1
#population size of 8
POP_SIZE = 8

#x and y are between -2 and 2.
START=-2
END=2
#the crossover probability of 0.7
CROSS_PROP=0.7
#mutation probability of 0.01
MUTATION_PROP=0.01
#total number of generation as 200
GENERATION_NUM=200
#Table of GNOME
table=[]
# Structure of a GNOME
class individual:
    def __init__(self,x_str,y_str,x_dec,y_dec,x,y,fit):
        self.x_string=x_str
        self.y_string=y_str
        self.decoded_x = x_dec
        self.decoded_y = y_dec
        self.x=x
        self.y=y
        self.fitness = fit 
        self.percentages_fitness=0
    def __lt__(self, other):
        return self.fitness < other.fitness
    def __gt__(self, other):
        return self.fitness > other.fitness

# Function to find a random number between 0 or 1
def findRandom():
    # Generate the random number
    num = random.randint(0, 1)
    # Return the generated number
    return num
#Funtion that generate random string of binary number with size
def generateBinaryString(N):
    # Stores the empty string
    S = ""
    # Iterate over the range [0, N - 1]
    for i in range(N):
        # Store the random number
        x = findRandom()
        # Append it to the string
        S += str(x)
    # Print the resulting string
    return S
#Funtion that convert string of binary to interger
def convertToInt(val_string):
  return (int(val_string,2))
#Funtion that make x and y always in range from -2 to 2
def convertInRange(value):
  diff_of_range=START-END;
  diff_of_range_binary=math.pow(2,POP_SIZE)-1
  ratio=diff_of_range/diff_of_range_binary
  return value*ratio-START
def createRandomGnome():
  #Get random number
  x_binary= generateBinaryString(POP_SIZE)
  y_binary= generateBinaryString(POP_SIZE)
  x_int= convertToInt(x_binary)
  y_int= convertToInt(y_binary)
  
  #Making sure it is in range from -2 to 2
  new_x_int=convertInRange(x_int)
  new_y_int=convertInRange(y_int)
  
  #Formula given
  side1=-(math.pow(new_x_int,2))-(math.pow(new_y_int+1,2))
  side2=-(math.pow(new_x_int,2))-(math.pow(new_y_int,2))
  side2_2=new_x_int-math.pow(new_x_int,3)-math.pow(new_y_int,3)
  fit=(math.pow((1-new_x_int),2)*(math.pow(math.e,side1)))-(side2_2)*(math.pow(math.e,side2))
  #Pass to the Object to append to the table
  gnome_pair=individual(x_binary,y_binary,x_int,y_int,new_x_int,new_y_int,fit)
  return gnome_pair

def caculateGnome(table):
  for i in range(POP_SIZE):
    
    x_binary= table[i].x_string
    y_binary= table[i].y_string
    x_int= convertToInt(x_binary)
    y_int= convertToInt(y_binary)
    
    #Making sure it is in range from -2 to 2
    new_x_int=convertInRange(x_int)
    new_y_int=convertInRange(y_int)
    
    #Formula given
    side1=-(math.pow(new_x_int,2))-(math.pow(new_y_int+1,2))
    side2=-(math.pow(new_x_int,2))-(math.pow(new_y_int,2))
    side2_2=new_x_int-math.pow(new_x_int,3)-math.pow(new_y_int,3)
    fit=(math.pow((1-new_x_int),2)*(math.pow(math.e,side1)))-(side2_2)*(math.pow(math.e,side2))
    #Pass to the Object to append to the table
    table[i]=individual(x_binary,y_binary,x_int,y_int,new_x_int,new_y_int,fit)
  

#Funtion that get percentages from the object
def addPercentOfFit(table,min_fitness):
  #Check the min_fitness
  total=0
  #SHIFTING F TO ALL POSITIVE
  if min_fitness<0:
    for i in range(POP_SIZE):
       total+=table[i].fitness+1
    # print('TOTAL ',total)
    for i in range(POP_SIZE):
      # print('TABLE FITNESS + 1 ',table[i].fitness+1)
      table[i].percentages_fitness=round(((table[i].fitness+1)/total)*100,2)
      # print('GNOME',i,': ',table[i].percentages_fitness)
  else:
    for i in range(POP_SIZE):
      total+=table[i].fitness
      # print('TABLE FITNESS',table[i].fitness)
    for i in range(POP_SIZE):
      table[i].percentages_fitness=round((table[i].fitness/total)*100,2)
      # print('GNOME',i,': ',table[i].percentages_fitness)

#Random wheel selection  function
def random_wheel_selection(table_gnome):
  new_array=[]
  #Search through the list of wheel
  for i in range(POP_SIZE):
    number_selection=random.uniform(0,100)
    temp_total_percentage=0
    for gnome in table_gnome:
      if number_selection>=temp_total_percentage and number_selection<=gnome.percentages_fitness+temp_total_percentage:
        #Add the number to the total percentage in have it to be selected
        new_array.append(gnome)
        break;
      else:
        temp_total_percentage+=gnome.percentages_fitness
    # print('NEW GNOME',i,': ',new_array[i].percentages_fitness)
  return new_array

#CROSS OVER OPERATION
def crossOver(table1,table2):
  # print('###############BEFORE################')
  for i in range(POP_SIZE):
    # print('TABLE1 index',i,': xString ',table1[i].x_string)
    # print('TABLE1 index',i,': yString ',table1[i].y_string)
    # print('TABLE2 index',i,': xString ',table2[i].x_string)
    # print('TABLE2 index',i,': yString ',table2[i].y_string)
    if (0<=random.uniform(0,1)<=0.7):
      #Randomly choosing the break point
      break_point=random.randint(1,POP_SIZE-1)
      temp_string_x=""
      temp_string_y=""
      list_string_table1_x=list(table1[i].x_string)
      list_string_table1_y=list(table1[i].y_string)
      list_string_table2_x=list(table2[i].x_string)
      list_string_table2_y=list(table2[i].y_string)
      #Start crossover
      for j in range(break_point,POP_SIZE):
        temp_string_x=list_string_table1_x[j]
        temp_string_y=list_string_table1_y[j]
        list_string_table1_x[j]= list_string_table2_x[j]
        list_string_table1_y[j]= list_string_table2_y[j]
        list_string_table2_x[j]=temp_string_x
        list_string_table2_y[j]=temp_string_y
      table1[i].x_string=''.join(list_string_table1_x)
      table1[i].y_string=''.join(list_string_table1_y)
      table2[i].x_string=''.join(list_string_table2_x)
      table2[i].y_string=''.join(list_string_table2_y)
        
      # print('###############AFTER################')
      # print('TABLE1 index',i,': xString ',table1[i].x_string)
      # print('TABLE1 index',i,': yString ',table1[i].y_string)
      # print('TABLE2 index',i,': xString ',table2[i].x_string)
      # print('TABLE2 index',i,': yString ',table2[i].y_string)
      # print('TABLE2 index',i,': ',table1[i].percentages_fitness)
    # else:
    #   print('No Cross')

#MUTATION OPERATION
def mutation(table1):
  for i in range(POP_SIZE):
    if (0<=random.uniform(0,100)<=1):
      list_string_table1_x=list(table1[i].x_string)
      list_string_table1_y=list(table1[i].y_string)
      point = random.randint(0,7)
      if(len(list_string_table1_x[point])==0): 
        list_string_table1_x[point]="1"
      else:
        list_string_table1_x[point]="0"
      if(len(list_string_table1_y[point])==0): 
        list_string_table1_y[point]="1"
      else:
        list_string_table1_y[point]="0"
    # else:
    #   print('No Mutation')
  

def optimizedFunction():
  #FIRST GENERATION
  min_fitness=float('inf')
  for i in range(POP_SIZE):
    table.append(createRandomGnome())
    #Finding the min fitness
    if table[i].fitness<min_fitness:
      min_fitness=table[i].fitness
  addPercentOfFit(table,min_fitness)
  print('####### FIRST GENERATION #########')
  for i in range(POP_SIZE):
    print('Final X_string index',i,':  ',table[i].x_string)
    print('Fianl Y_string  index',i,': ',table[i].y_string)
    print('Final X_Decoded index',i,':  ',table[i].decoded_x)
    print('Fianl Y_Decoded  index',i,': ',table[i].decoded_y)
    print('Final Fitness ',i,': ',table[i].fitness)
    print('Final Fitness Percentage',i,': ',table[i].percentages_fitness)
    print('\n')
  #LATER GENERATION
  for _ in range(GENERATION_NUM):
    caculateGnome(table)
    addPercentOfFit(table,min_fitness)
    new_table=random_wheel_selection(table)
    crossOver(table,new_table)
    mutation(table)
  print('####### LAST GENERATION #########')
  for i in range(POP_SIZE):
    print('Final X_string index',i,':  ',table[i].x_string)
    print('Fianl Y_string  index',i,': ',table[i].y_string)
    print('Final X_Decoded index',i,':  ',table[i].decoded_x)
    print('Fianl Y_Decoded  index',i,': ',table[i].decoded_y)
    print('Final Fitness ',i,': ',table[i].fitness)
    print('Final Fitness Percentage',i,': ',table[i].percentages_fitness)
    print('\n')
  
optimizedFunction()
