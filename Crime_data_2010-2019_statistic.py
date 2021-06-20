import pandas as pd
import numpy as np
import datetime as dt
from matplotlib import pyplot as plt
import glob

def setparameters():
    pd.set_option("display.max_rows", 200)
    pd.set_option("display.max_columns", 100)
    pd.set_option("display.max_colwidth", 200)
    pd.set_option('display.expand_frame_repr', False)

setparameters()


path = r'./data'
filenames = glob.glob(path + "/*.zip")


dfs = list()
for filename in filenames:
    df = pd.read_csv(filename, compression='zip', sep=',', parse_dates=['DATE OCC', 'Date Rptd'])    
    dfs.append(df)
crime_data = pd.concat(dfs, axis=0, ignore_index=True)


# Is there any relation between number of victims and their gender?
filter_gender=crime_data['Vict Sex'].isin(['F', 'M'])
crime_data_m1=crime_data.loc[filter_gender]
victims_by_sex=crime_data_m1[['year', 'Vict Sex']].pivot_table(index=['Vict Sex'], columns=['year'], aggfunc=len)
print(victims_by_sex)


fig = plt.figure() 
ax = fig.add_subplot(111)
df1=crime_data_m1[crime_data_m1['Vict Sex']=='F']['year']
df2=crime_data_m1[crime_data_m1['Vict Sex']=='M']['year']
ax.hist([df1, df2], label=("Female", "Male"))
ax.legend()
plt.show()

print("We can see that the number of male victims is hihger than female ones.")

# However it is reasonably to say that not only gender but also age can influence the probability of becoming a victim. Let's check this.
age_bins=[0, 18, 30, 55, 70, 99]
crime_data['Age by bins']=pd.cut(crime_data['Vict Age'], bins=age_bins)

filter_age=crime_data['Vict Age']>0
crime_data_m3=crime_data.loc[filter_gender & filter_age]  
print(crime_data_m3.groupby(['Age by bins','Vict Sex'])['DR_NO'].count())

crime_data_m3[['Age by bins','Vict Sex']].pivot_table(index='Age by bins', columns='Vict Sex', aggfunc=len).plot()
crime_data_m3[['Age by bins','Vict Sex']].pivot_table(index='Age by bins', columns='Vict Sex', aggfunc=len).plot(kind='bar')
plt.show()

print("It is an fact interesting that under 30 women are more likely to become victims than men. After 30 trend is chnaging conversely")

# Is there any relation between number of victims and their origin?
ethnic_dec={'H':'Hispanic/Latin/Mexican', 'W':'White', 'B':'Black', 'A':'Other Asian', 'O':'Other', 'X':None, 'K':'Korean', 'I':'American Indian/Alaskan Native',\
                    'J':'Japanese', 'F':'Filipino', 'C':'Chinese', 'P':'Pacific Islander', 'V':'Vietnamese', 'U':'Hawaiian', 'G':'Guamanian', 'D': 'Cambodian', 'S': 'Samoan',\
                    'Z':'Asian Indian', 'L': 'Laotian', '-':None} 
crime_data['Vict Descent_full']=crime_data['Vict Descent'].map(ethnic_dec)
crime_data_m2=crime_data.dropna(axis='index', how='any', subset=['Vict Descent_full']) 
print(crime_data_m2['Vict Descent_full'].value_counts())
print("The trend for recent years is that Hispanics suffer more from crimes than others. It can be partly explained by uncontrolled migration from this region to the USA")


# What are the top 10 crimes in LA?
print(crime_data['Crm Cd Desc'].value_counts().head(10))
crime_data['Crm Cd Desc'].value_counts().head(10).plot(kind='pie')
plt.show()

# What are the top 10 crimes in LA in correlation with gender?
print(crime_data[crime_data['Vict Sex']=='F']['Crm Cd Desc'].value_counts().head(10))
print(crime_data[crime_data['Vict Sex']=='M']['Crm Cd Desc'].value_counts().head(10))
print(crime_data_m1.groupby(['Vict Sex','Crm Cd Desc'])['DR_NO'].count().sort_values(ascending=False).head(10))


#What are the safiest and unsafiest area in LA?
top_unsafe=crime_data.groupby('AREA NAME')['DR_NO'].count().sort_values(ascending=False).head(5)
top_unsafe.plot(kind='bar', color='red')
plt.show()
top_safe=crime_data.groupby('AREA NAME')['DR_NO'].count().sort_values(ascending=False).tail(5)
top_safe.plot(kind='bar', color='green')
plt.show()


