import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
import random
membership=""
df=pd.read_csv(r'62fdbb2cc8ccc_Brand_name_generator_Data__1_.csv')
df.dropna(inplace=True)
df.isna().sum()

# converting column into list
a = list(df['Moleculesname'].iloc[0:10000])
  
#converting list into string and then joining it with space
data= '\n'.join(str(i) for i in a)

tokenizer=tf.keras.preprocessing.text.Tokenizer(
    filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~0123456789',
    split='\n',
)

tokenizer.fit_on_texts(data)

char_to_index=tokenizer.word_index
index_to_char= dict ((v, k) for k, v in char_to_index.items())
print(index_to_char)

names=data.splitlines()

tokenizer.texts_to_sequences(names[0])

def name_to_seq(name):
  return[tokenizer.texts_to_sequences(c)[0][0] for c in name]

def seq_to_name(seq):
  return '\n'.join([index_to_char[i] for i in seq if i!=0])

sequences=[]
for name in names:
  seq=name_to_seq(name)
  if len(seq)>=2:
     sequences=sequences+[seq[:i] for i in range(2,len(seq)+1)]

sequences[:10]

max_len=max([len(x) for x in sequences])
print(max_len)

padded_sequences=tf.keras.preprocessing.sequence.pad_sequences(
    sequences,padding='pre',
    maxlen=max_len
)
print(padded_sequences[0])
padded_sequences.shape

x,y=padded_sequences[:, :-1],padded_sequences[:,-1]
print(x.shape,y.shape)

from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.005)
print(x_train.shape,y_train.shape)
print(x_test.shape,y_test.shape)

num_chars=len(char_to_index.keys())+1
print(num_chars)

from tensorflow.keras.models import load_model
new_model=load_model(r'Trainedat90%.h5')

new_model

def generate_names(seed):
  x=len(seed)
  for i in range(0,random.randint(6,9)):
    
    seq=name_to_seq(seed)
    padded=tf.keras.preprocessing.sequence.pad_sequences([seq],padding='pre',
                                                        maxlen=max_len-1,
                                                        truncating='pre')
    pred=new_model.predict(padded)[0]
    pred_char=index_to_char[tf.argmax(pred).numpy()]
    seed=seed+pred_char
    if pred_char=='\t':
      break
    

  return seed[x:]


