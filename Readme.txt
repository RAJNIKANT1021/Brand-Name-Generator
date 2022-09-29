How to run Brand Name Generator on PC


Steps:

1)Copy all the files on your PC desktop in a folder named as "Brand Name"
2)Install all the libraries using the code "pip install -r requirements.txt" on your shell.
3)Copy the path of the current "Brand Name" folder.
4)Open app2.py on VSCode or any editor and change the 26th line, "df=pd.read_csv(r'62fdbb2cc8ccc_Brand_name_generator_Data__1_.csv')" to "df=pd.read_csv(r'{Copied path of Brand Name folder}\62fdbb2cc8ccc_Brand_name_generator_Data__1_.csv')"
5)Open brand.py on VSCode or any editor and change the 8th line, "df=pd.read_csv(r'62fdbb2cc8ccc_Brand_name_generator_Data__1_.csv')" to "df=pd.read_csv(r'{Copied path of Brand Name folder}\62fdbb2cc8ccc_Brand_name_generator_Data__1_.csv')"
6)Change the 69th line, "new_model=load_model(r'Trainedat90%.h5')" to "new_model=load_model(r'{Copied path of brand name}\Trainedat90%.h5')" in the same brand.py
7)Run app2.py