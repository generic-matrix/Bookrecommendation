import pandas as pd
import neattext.functions as nfx
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity,linear_kernel
from pathlib import Path
from flask import Flask, request, jsonify
import json
from flask_cors import CORS
import base64


from pathlib import Path

class RecommendBooks:
  def __init__(self):
    #create a dataframe 
    dirname = Path.cwd().as_posix()
    df = pd.read_csv(dirname+'/dataset/final_book_dataset_kaggle2.csv')

    #drop duplicates from the course_title column
    df = df.drop_duplicates(subset=['title'])
    # clean_title column to string from course_title
    df['clean_title'] = df['title'].astype(str)
    # clean_title remove stopwords
    df['clean_title'] = df['clean_title'].apply(nfx.remove_stopwords)
    # clean_title remove special characters
    df['clean_title'] = df['clean_title'].apply(nfx.remove_special_characters)

    # create CountVectorizer
    countvect = CountVectorizer()
    cv_mat = countvect.fit_transform(df['clean_title'])

    # create CV words
    df_cv_words = pd.DataFrame(cv_mat.todense(),columns=countvect.get_feature_names())
    self.df = df
    self.cosine_sim_mat = cosine_similarity(cv_mat)
    print("Data loaded Successfully")

  def autocomplete(self,query):
    result = self.df.loc[self.df['clean_title'].str.contains(query, case=False)]
    data = []
    index = 0
    for obj in result["title"][0:5]:
      data.append({
          "key":index,
          "value":obj
      })
      index = index + 1
    return data
  
  def recommend_books(self,title,numrec = 10):
    print(title)
    course_index = pd.Series( self.df.index, index=self.df['title']).drop_duplicates()
    if title in course_index:
      index = course_index[title]
      scores = list(enumerate(self.cosine_sim_mat [index]))
      sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
      selected_course_index = [i[0] for i in sorted_scores[1:]]
      selected_course_score = [i[1] for i in sorted_scores[1:]]
      rec_df = self.df.iloc[selected_course_index]
      rec_df['Similarity_Score'] = selected_course_score
      final_recommended_courses = rec_df[['title', 'Similarity_Score', 'link']]
      result = final_recommended_courses.head(numrec).to_json(orient ='index')
      parsed = json.loads(result)
      return {"error":None,"data":parsed}
    else:
      return {"error": "course with title name "+title+" not found"}


app = Flask(__name__)
CORS(app)
recommendation = RecommendBooks()



@app.route("/recommend", methods=["GET"])
def recommend():
    query = request.args.get("query")
    if query is None:
        return jsonify({'error' : 'Malformed Request'})
    else:
        #Introduction Financial Modeling
        return recommendation.recommend_books(base64.b64decode(query).decode("utf-8"),20)

@app.route("/autocomplete", methods=["GET"])
def autocomplete():
    query = request.args.get("query")
    if query is None:
        return jsonify({'error' : 'Malformed Request'})
    else:
        return jsonify(recommendation.autocomplete(query))
    


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5001,debug=True)

