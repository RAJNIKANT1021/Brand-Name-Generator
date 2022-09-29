import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
import random
membership=""
# reading the csv file
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

#tokenization of characters in the string
tokenizer.fit_on_texts(data)

#assigning index to the characters
char_to_index=tokenizer.word_index
index_to_char= dict ((v, k) for k, v in char_to_index.items())
print(index_to_char)

#splits a line into string
names=data.splitlines()

#converting tokens of text corpus into a sequence of integers
tokenizer.texts_to_sequences(names[0])


def name_to_seq(name):
  return[tokenizer.texts_to_sequences(c)[0][0] for c in name]

def seq_to_name(seq):
  return '\n'.join([index_to_char[i] for i in seq if i!=0])


#predict the next character by sequential modelling
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

# *****************MODEL starts from here*******************


# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Embedding, Conv1D, MaxPool1D,LSTM
# from tensorflow.keras.layers import Bidirectional, Dense
# model=Sequential([
#     Embedding(num_chars,8,input_length=max_len-1),
#     Conv1D(64,5,strides=1,activation='tanh',padding='causal'),
#     MaxPool1D(2),
#     LSTM(32),
#     Dense(num_chars,activation='softmax')
#   ])
# model.compile(
#     loss='sparse_categorical_crossentropy',
#     optimizer='adam',
#     metrics=['accuracy']
# )
# model.summary(),
# h=model.fit(
#     x_train,y_train,
#     validation_data=(x_test,y_test),
#     epochs=100, verbose=2,
#     callbacks=[
#         tf.keras.callbacks.EarlyStopping(monitor='val_accuracy',patience=12)
#     ]
# )
# import os.path
# model.save('C:\Users\HP\Desktop\BrandName\Trainedat90%.h5')
# epochs_ran=len(h.history['loss'])
# plt.plot(range(0,epochs_ran),h.history['val_accuracy'],label='validation')
# plt.plot(range(0,epochs_ran),h.history['accuracy'],label='train')
# plt.legend()
# plt.show()


# *****************MODEL ends here*******************



# This model is saved using 
# import os.path
# model.save('C:\Users\HP\Desktop\BrandName\Trainedat90%.h5')
# as Trainedat90% in the format .h5


from tensorflow.keras.models import load_model

#loading the saved model
new_model=load_model(r'Trainedat90%.h5')

new_model


#function to generate names using keras, sequence and padded sequences
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


