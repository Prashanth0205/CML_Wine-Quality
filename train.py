import numpy as np
import pandas as pd 
import seaborn as sns 
import matplotlib.pyplot as plt 

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

seed = 42

# Data Preparation 
df = pd.read_csv(r"wine_quality.csv")
y = df.pop("quality")

# Split the data into Train and test selections 
X_train, X_test, y_train, y_test = train_test_split(df, y, test_size=0.2, random_state=seed)

# Modelling 
regr = RandomForestClassifier(max_depth=2, random_state=seed)
regr.fit(X_train, y_train)

# Report training and test set score 
train_score = regr.score(X_train, y_train) * 100
test_score = regr.score(X_test, y_test) * 100

with open("metrics.txt", 'w') as outfile:
    outfile.write(f"Training variance explained: {train_score}")
    outfile.write(f"Test variance explained: {test_score}")

# Calculate feature importance in random forest 
importances = regr.feature_importances_
labels = df.columns
feature_df = pd.DataFrame(list(zip(labels, importances)), columns = ["feature","importance"])
feature_df = feature_df.sort_values(by='importance', ascending=False,)

# Image formatting 
axis_fs = 18
title_fs = 22 
sns.set(style="whitegrid")
ax = sns.barplot(x="importance", y="feature", data=feature_df)
ax.set_xlabel('Importance',fontsize = axis_fs) 
ax.set_ylabel('Feature', fontsize = axis_fs)#ylabel
ax.set_title('Random forest\nfeature importance', fontsize = title_fs)

plt.tight_layout()
plt.savefig("feature_importance.png",dpi=120) 
plt.close()

# Plot residuals 
y_pred = regr.predict(X_test) + np.random.normal(0,0.25,len(y_test))
y_jitter = y_test + np.random.normal(0,0.25,len(y_test))
res_df = pd.DataFrame(list(zip(y_jitter,y_pred)), columns = ["true","pred"])

ax = sns.scatterplot(x="true", y="pred",data=res_df)
ax.set_aspect('equal')
ax.set_xlabel('True wine quality',fontsize = axis_fs) 
ax.set_ylabel('Predicted wine quality', fontsize = axis_fs)#ylabel
ax.set_title('Residuals', fontsize = title_fs)

# Make it pretty- square aspect ratio
ax.plot([1, 10], [1, 10], 'black', linewidth=1)
plt.ylim((2.5,8.5))
plt.xlim((2.5,8.5))

plt.tight_layout()
plt.savefig("residuals.png",dpi=120) 