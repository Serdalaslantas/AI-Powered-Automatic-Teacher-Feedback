import os
import openai
from openai import OpenAI
import textract
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from docx import Document
from PyPDF2 import PdfReader
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'docx','rtf','odt'}
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

OPENAI_API_KEY = os.getenv("SECRET_KEY")  # Replace with your OpenAI API key

# User Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    is_teacher = db.Column(db.Boolean, default=False)

# Article Model
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    filename = db.Column(db.String(150), nullable=False)
    feedback = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def allowed_file(filename):
    """Check if the uploaded file is in an allowed format."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def extract_text_from_file(filepath):
    """Extract text from the uploaded file based on its format."""
    extension = filepath.rsplit('.', 1)[1].lower()

    if extension == 'txt':
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read()

    elif extension == 'docx':
        doc = Document(filepath)
        return '\n'.join([para.text for para in doc.paragraphs])

    elif extension == 'pdf':
        reader = PdfReader(filepath)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        return text
    
    elif extension in ['rtf', 'odt']:
        try:
            # Use textract to handle RTF and ODT files
            text = textract.process(filepath).decode('utf-8')
            return text
        except Exception as e:
            return f"Dosya işlenirken hata oluştu: {str(e)}"
    else:
         # Use textract to handle other file formats (e.g., .odt, .rtf)
        return textract.process(filepath).decode('utf-8')

def generate_ai_feedback(article_content):
    """Generate AI feedback using the OpenAI API."""
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an assistant that excels in constructive feedback for the given student essay. Your reply should be in the main language used in the essay."},
                {"role": "user", "content": f"{article_content}"}
            ],
            max_tokens=500
        )
        feedback = response.choices[0].message.content.strip()
        return feedback
    except Exception as e:
        return f"Geribildirim oluşturulurken hata oluştu: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Giriş Başarısız. Lütfen kullanıcı adı ve şifrenizi kontrol edin.', 'danger')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'], method='pbkdf2:sha256')
        is_teacher = request.form.get('is_teacher') == 'on'
        new_user = User(username=username, password=password, is_teacher=is_teacher)
        db.session.add(new_user)
        db.session.commit()
        flash('Hesap başarıyla oluşturuldu!', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_teacher:
        articles = Article.query.all()
    else:
        articles = Article.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', articles=articles)

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        title = request.form['title']
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Extract text from the uploaded file
            article_content = extract_text_from_file(filepath)

            # Generate feedback using the AI model
            feedback = generate_ai_feedback(article_content)

            # Save the article and feedback to the database
            new_article = Article(title=title, filename=filename, feedback=feedback, user_id=current_user.id)
            db.session.add(new_article)
            db.session.commit()
            flash('Makale yüklendi ve geribildirim başarıyla oluşturuldu!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Dosya formatı desteklenmiyor.', 'danger')
    return render_template('upload.html')

@app.route('/article/<int:id>', methods=['GET', 'POST'])
@login_required
def article(id):
    article = Article.query.get_or_404(id)
    if request.method == 'POST' and current_user.is_teacher:
        article.feedback = request.form['feedback']
        db.session.commit()
        flash('Geribildirim başarıyla güncellendi!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('article.html', article=article)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
@login_required
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    with app.app_context():
        db.create_all()
    app.run(debug=True)
