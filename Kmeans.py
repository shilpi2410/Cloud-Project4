
from copy import deepcopy
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
plt.rcParams['figure.figsize'] = (16, 9)
plt.style.use('ggplot')


app = Flask(__name__)


@app.route('/')
def index():
   df = pd.read_csv('Students.csv', encoding='latin1')

   col1 = request.form['col1']
   col2 = request.form['col2']
   
   # df[col1] = pd.to_numeric(df[col1], errors='coerce')
   # df[col2] = pd.to_numeric(df[col2], errors='coerce')
   # df.dropna()
   f1 = df[col1].values
   f2 = df[col2].values

   X = np.array(list(zip(f1, f2)))

   plt.rcParams['figure.figsize'] = (16, 9)
   kmeans = KMeans(int(request.form['nclusters']))
   kmeans = kmeans.fit(X)
   
   labels = kmeans.predict(X)
   
   centroids = kmeans.cluster_centers_

   points = kmeans.labels_

   for i in range(len(X)):
       print("coordinate:", X[i], "label:", labels[i])

   c1 = np.where(points == 1)[0]
   c2 = np.where(points == 2)[0]
   c3 = np.where(points == 0)[0]

   colors = ['#2C3E50','#0E6251', '#C0392B', '#F0B27A', '#7D6608']
   plt.figure()
  
   for i, col in zip(range(5), colors):
       groups = kmeans.labels_ == i
       centroid = kmeans.cluster_centers_[i]

       plt.plot(X[groups, 0], X[groups, 1], 'w', markerfacecolor=col, marker='.')
       plt.plot(centroid[0], centroid[1], '*', markerfacecolor=col, markeredgecolor='k', markersize=6)
   plt.title('kmeans')
   plt.grid(True)
   plt.savefig('static/test5.png')
   return render_template('scatter.html')
     return render_template('index.html')



