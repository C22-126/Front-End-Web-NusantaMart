
from flask import Flask, render_template, request
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

food = pd.read_csv('indonesian_food.csv')
fix_food = food.sort_values('foodId', ascending=True)
food_id = fix_food['foodId'].tolist()
food_nama = fix_food['Nama'].tolist()
food_tipe = fix_food['Tipe'].tolist()
food_harga = fix_food['harga'].tolist()
food_img = fix_food['img'].tolist()

food_new = pd.DataFrame({
        'foodId': food_id,
        'name': food_nama,
        'tipe': food_tipe,
        'harga': food_harga,
        'img': food_img
    })
data = food_new
data.sample(5)

tf = TfidfVectorizer()

tf.fit(data['tipe'])
tf.get_feature_names_out()

tfidf_matrix = tf.fit_transform(data['tipe'])

tfidf_matrix.todense()

pd.DataFrame(
        tfidf_matrix.todense(),
        columns=tf.get_feature_names_out(),
        index=data.name
    ).sample(22, axis=1).sample(10, axis=0)
cosine_sim = cosine_similarity(tfidf_matrix)
cosine_sim_df = pd.DataFrame(cosine_sim, index=data['name'], columns=data[['foodId', 'name', 'tipe', 'harga', 'img']])
cosine_sim_df.sample(5, axis=1).sample(10, axis=0)


def food_recommendations(name, similarity_data=cosine_sim_df, items=data[['foodId', 'name', 'tipe']], k=19):
    search = similarity_data.loc[name].to_numpy().argpartition(range(-1, -k, -1))
    closest = similarity_data.columns[search[-1:-(k + 2):-1]]
    closest = closest.drop(name, errors='ignore')
    return closest


@app.route('/')
def index():
    return render_template("home.html")


@app.route('/signup', methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template('signup.html')
    else:
        return render_template('signup.html', message='Akun Berhasil Daftar')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
   if request.method == 'POST':
       if request.form['request'] == '':
           return render_template('home.html', message='makanan tidak ditemukan')
       else:
           req = request.form['request']
           res = food_recommendations(req)
           if len(res) > 0:
               response = res
           else:
               response = 'data tidak ditemukan'
           return render_template('home.html', data=response)
   else:
       return render_template('home.html')


@app.route("/keranjang")
def keranjang():
    return render_template('keranjang.html')


@app.route("/profile")
def profile():
    return render_template('profile.html')



if __name__ == "__main__":
    app.run(debug=True)
