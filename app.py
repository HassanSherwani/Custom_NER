
# importing key modules

from flask import Flask,url_for,render_template,request
### Load for spacy
from spacy.lang.en import English
from spacy.pipeline import EntityRuler
import spacy
from spacy import displacy
from spacy.matcher import Matcher
from spacy.tokens import Span
import re
import string
nlp = spacy.load('en_core_web_sm')
nlp = English()
ruler = EntityRuler(nlp, overwrite_ents=True)


HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem">{}</div>"""

from flaskext.markdown import Markdown

app = Flask(__name__)
Markdown(app)


# def analyze_text(text):
# 	return nlp(text)

@app.route('/')
def index():
	# raw_text = "Bill Gates is An American Computer Scientist since 1986"
	# docx = nlp(raw_text)
	# html = displacy.render(docx,style="ent")
	# html = html.replace("\n\n","\n")
	# result = HTML_WRAPPER.format(html)

	return render_template('index.html')


@app.route('/extract',methods=["GET","POST"])
def extract():
	if request.method == 'POST':
		raw_text = request.form['rawtext']
		patterns = [{"label": "BUYER", "pattern": "Sarfraz"},
					{"label": "SELLER", "pattern": "Kapil"}]

		ruler.add_patterns(patterns)
		nlp.add_pipe(ruler)
		docx = nlp(raw_text)
		html = displacy.render(docx,style="ent")
		html = html.replace("\n\n","\n")
		result = HTML_WRAPPER.format(html)

	return render_template('result.html',rawtext=raw_text,result=result)


@app.route('/previewer')
def previewer():
	return render_template('previewer.html')

@app.route('/preview',methods=["GET","POST"])
def preview():
	if request.method == 'POST':
		newtext = request.form['newtext']
		result = newtext

	return render_template('preview.html',newtext=newtext,result=result)


if __name__ == '__main__':
	app.run(debug=True)