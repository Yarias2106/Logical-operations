from tkinter import Tk
from tkinter import Entry
from tkinter import Frame
from tkinter import Label
from tkinter import Button
from tkinter import Text
from tkinter import messagebox
import numpy as np
from keras.models import load_model
import pandas as pd
from sklearn.preprocessing import StandardScaler

dataset = pd.read_csv('Operaciones Logicas.csv')
X = dataset.iloc[: , 0:3].values
sc_X = StandardScaler()
sc_X.fit_transform(X)

modelo = './modelo/modelo.h5'
pesos_modelo = './modelo/pesos.h5'
rna = load_model(modelo)
rna.load_weights(pesos_modelo)

diccionario_valores={"v":5, "^" : 10 , "→" : 15}
lista2 = []

list_symbols = ['{','(','[',']','}',')'] 
LIST_KEYS = ['v','^','→','~']

SYMBOLS_REVERSE = {
    '(': ')',
    '[':']',
    '{':'}'
}

OPEN_SYMBOLS= SYMBOLS_REVERSE.keys()
CLOSURE_SYMBOLS = SYMBOLS_REVERSE.values()
#andres
def is_special_character(char):
    value =  False 
    if char in list_symbols:
       value = True 
    return value 

def is_a_closure_symbol(last_item, char):
    value =  False
    if char in CLOSURE_SYMBOLS:
        value = True
    return value

def save_expression(str, list):
    if len(str.strip()) != 0:
        list.append(str)

def is_a_open_symbol(char):
    value = False
    if char in OPEN_SYMBOLS:
        value = True
    return value

def isClauseNot(char):
    value = False
    if char == '~':
        value = True
    return value

def nextPositionisAlphabeticCharacter(idx, str):
    value = False
    if  idx + 1 < len(str):
        if(str[idx + 1].isalpha()):
            value = True
    return value

def nextPositionisOpenClosure(idx, str):
    value = False
    if  idx + 1 < len(str):
        if (is_a_open_symbol(str[idx + 1])):
            value = True
    return value

def isKey(char):
    value = False
    if char in LIST_KEYS:
        value = True 
    return value 
def is_begin_new_expression(char):
    value = False
    if char == '[':
        value = True 
    return value 
def is_ended_new_expression(char):
    
    value = False
    if char == ']':
        value = True 
    return value

 #andres   
def is_negative(string):
   char = string[0]
   if char == "~":
       a = string[1]
       b = diccionario_valores[a]
       if b == 0:
           b = 1
       else:
           b = 0
   else:    
       b = diccionario_valores[char]
   return b

def change_final_negation(negation_list, results_list):
       for j in negation_list:
        dato_cambiar = results_list[j]
        if dato_cambiar == 1:
            nuevo_dato = 0
        else:
            nuevo_dato = 1
        results_list.pop(j)
        results_list.insert(j,nuevo_dato)
       return results_list
    
def control_negatives(list_key,lista_posiciones_negacion,list_key2):   
    contador = 0
    for i in  list_key:
        if i == "~":
            lista_posiciones_negacion.append(contador)
        else:
            contador = contador + 1
            a = diccionario_valores[i]
            list_key2.append(a)
            
def obtain_result(list_resultados2):
     operacion = np.array([list_resultados2])
     x_operacion = sc_X.transform(operacion)
     operacion_pred=rna.predict(x_operacion)
      
     if operacion_pred>0.5 : 
            result = 1          
     else:
          result = 0
     list_resultados2.clear()  
     return result
    

def show_result(result):
    if result == 0:
        messagebox.showinfo("Resultado","El resultado de la operacion logica es Falso" )
    else:
        messagebox.showinfo("Resultado","El resultado de la operacion logica es Verdadero")

#andres
def descompose_string(str, list_expression, list_key):
    
    stack = []
    expression = ''
    sub_expression = ''
    isOpenSymbol = False
    isBeginNewExpression = False
    position_save = -1
    idx = 0
    for char in str:
        if is_special_character(char):
            if isBeginNewExpression == True:  
                sub_expression+=char 
            size_stack = len(stack)
            if is_a_open_symbol(char):
                isOpenSymbol = True 
                stack.append(char)
                if is_begin_new_expression(char):
                   isBeginNewExpression = True 
                   sub_expression+=char
            elif is_a_closure_symbol(size_stack -1 ,char):
                save_expression(expression, list_expression)
                expression = ''
                isOpenSymbol = False
                if is_ended_new_expression(char):
                    print('finished')
                    isBeginNewExpression = False
                    save_expression(sub_expression, list_expression)    
                    sub_expression= ''
                if len(stack) > 0:
                    stack.pop()
            else: 
                return False
        elif isBeginNewExpression == True:
            sub_expression+=char
        elif isOpenSymbol == True:
            if isBeginNewExpression == False:
                expression+=char
        elif isKey(char):
            if isBeginNewExpression == False: 
                #remove identation
                if isClauseNot(char):
                    if (nextPositionisOpenClosure(idx, str) == True):
                        list_key.append(char)
                    elif(nextPositionisAlphabeticCharacter(idx, str) == True): 
                        position_save = idx + 1        
                else:
                    list_key.append(char)
        else:
            if isBeginNewExpression == False: 
                if idx == position_save:
                    save_expression('~'+char, list_expression)          
                else:
                    save_expression(char, list_expression)
        idx +=1
    return len(stack) == 0
#andres

#Funcion para iterar resultados
def predict_iteraction(list_resultados, list_keys):
    list_resultados2 = []
    result = 1000
    for j in range (len(list_keys)):
        
     if result == 1000:
       condicional = list_keys[j]
       preposicion_1 = list_resultados[j]
       preposicion_2 = list_resultados[j+1]
      
       list_resultados2.append(preposicion_1)
       list_resultados2.append(condicional)
       list_resultados2.append(preposicion_2)
      
       result =  obtain_result(list_resultados2)  

     else:
       list_resultados2.append(result)
       list_resultados2.append(list_keys[j])
       list_resultados2.append(list_resultados[j+1])
       
       result = obtain_result(list_resultados2)
       
    return result 
    
#Funcion para saber resultados de las opearaciones basicas    
def predict(list_expression2,list_key2, lista_posiciones_negacion):
    
    list_resultados = []
    for i in range (len(list_expression2)):
      a = "" # Variable para guardar resultado de la red
      #Usamos la funcion predict de nuestra red para saber el resultado  
      dato = list_expression2[i]
      if len(dato) > 2:
       operacion = np.array([dato])
       x_operacion = sc_X.transform(operacion)
       operacion_pred=rna.predict(x_operacion)
     
       if operacion_pred>0.5 : 
            a = 1          
       else:
          a = 0
       list_resultados.append(a)
      else:
        list_resultados.append(dato[0]) 
    #Lueo de añadir resultados a una lista iteramos    
    if len(lista_posiciones_negacion) > 0: 
        
     list_resultados  = change_final_negation(lista_posiciones_negacion, list_resultados)
     return predict_iteraction(list_resultados, list_key2)
    else:
     return predict_iteraction(list_resultados, list_key2)     
    

def sub_problem(problem):
    
    test = problem
    list_expression = []
    list_key = []
    list_expression2 = []
    list_key2 = []

    if descompose_string(list(test), list_expression, list_key):
        for i in range (len(list_expression)):
            
            a = list_expression[i]
            list_1 = a.split()
            lista_aux = []
            for j in range (len(list_1)):
                #Convertimos nuestras preposiones a 1 y 0 con la funcion "is_negative"              
                b = list_1[j]
                result = is_negative(b)
                lista_aux.append(result)
                
            list_expression2.append(lista_aux)
         
        lista_posiciones_negacion = []
        control_negatives(list_key, lista_posiciones_negacion, list_key2)
       
    else:
        print('error ')
    #Mandamos a resolver el problema    
    resultado_momentaneo = predict(list_expression2, list_key2, lista_posiciones_negacion)
    return resultado_momentaneo

    
def general_problem(problem):
 test = problem
 list_expression = []
 list_key = []
 list_key2 =[]
 list_expression2= []
 if descompose_string(list(test), list_expression, list_key):
      for i in list_expression:
            char = i[0]
            if char == "[":  #preguntar si es un sub problema
               sub_problema = i [1:-1]
               sub_problema = sub_problem(sub_problema)
               list_expression2.append(sub_problema) 
            else:
                if len(i)>2: # ejercicio normal lo resolvemos
                   
                   ejercicio_normal = sub_problem(i) 
                   list_expression2.append(ejercicio_normal)
               
                else: # Preposicion normal (lo cambiamos)
                    result = is_negative(i)
                    list_expression2.append(result)
      #Controlamos las negaciones que cambian el resultado de los parentesis
      lista_posiciones_negacion = []
      control_negatives(list_key, lista_posiciones_negacion, list_key2)
  
      if len(lista_posiciones_negacion) > 0: #Si hay negativos cambiamos su valor 
          list_expression2 = change_final_negation(lista_posiciones_negacion, list_expression2)
      #Iteramos los resultados finales
      resultado_final = predict_iteraction(list_expression2, list_key2)   
 else:
       print('error ')
 show_result(resultado_final)
 
     
#Funcion para obtener el problema y los valores de las preposiciones ingresadas   
def get_text():
    valores_preposiciones = text_1.get("1.0", "end")
    problem =entry_1.get()
    lista = valores_preposiciones.split()
    for i in  lista:
        if i != "=":
           lista2.append(i) 
    for i in range(len(lista2)):
         if i%2 == 0:
             a = lista2[i]
             b = lista2[i+1]
             if b=="Verdad" or b == "verdadero" or b == "Verdadero":
                 c = 1
             else:
                 c = 0
             #Añadimos a nuestro diccionario los valores 1 y 0
             diccionario_valores [a]=c
    general_problem(problem)

raiz=Tk()
raiz.title("Operaciones Logicas.IA")
raiz.resizable(0,0)

frame= Frame(raiz, width="600", height="600",   bg ="#86E2D5")
frame.pack()

label_1= Label(frame, text="¡Bienvenido!", bd = 10, bg ="#86E2D5")
label_1.config(font=("Palatino",25))
label_1.grid(row=0,column=0)
label_2= Label(frame, text="Por favor ingrese la operación que desea resolver: ",   bg ="#86E2D5")
label_2.config(font=("Palatino",19))
label_2.grid(row=1,column=0)
entry_1 = Entry(frame, width = 40, bd = 5, font=("Palatino",14) ) 
entry_1.grid(row=1,column=1)

label_3 = Label(frame, text="Por favor ingrese el valor de las preposiciones: ", bd = 20, padx = 8,   bg ="#86E2D5") 
label_3.config(font=("Palatino",19))
label_3.grid(row=3,column=0)
text_1 = Text(frame, width=40, bd = 5, height= 20, font=("Palatino",14))
text_1.grid(row=3, column=1)

boton= Button(frame, text= "Aceptar", width=20, height = 3, command= get_text, bd = 15,  bg ="#1abc9c")
boton.grid(row = 4, column = 0)

raiz.mainloop()