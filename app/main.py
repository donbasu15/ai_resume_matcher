import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from src.preprocessing import extract_text_from_file, clean_text, advanced_text_preprocessing
from src.matcher import match_resume
from src.skills_database import get_all_skills
import logging
import traceback

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'pdf', 'docx'}
UPLOAD_FOLDER = 'uploads'

# Create upload folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def index():
    """Main route for file upload and analysis."""
    if request.method == "POST":
        try:
            # Validate form data
            if 'resume' not in request.files:
                flash('No resume file uploaded', 'danger')
                return redirect(request.url)
            
            if 'job_description' not in request.form:
                flash('No job description provided', 'danger')
                return redirect(request.url)
            
            resume_file = request.files['resume']
            jd_text = request.form['job_description'].strip()
            
            # Validate file
            if resume_file.filename == '':
                flash('No file selected', 'warning')
                return redirect(request.url)
            
            if not allowed_file(resume_file.filename):
                flash('Invalid file type. Please upload PDF or DOCX files only.', 'danger')
                return redirect(request.url)
            
            # Validate job description
            if len(jd_text) < 50:
                flash('Job description is too short. Please provide more details.', 'warning')
                return redirect(request.url)
            
            # Process files
            logger.info(f"Processing resume: {resume_file.filename}")
            
            # Extract text from resume
            resume_text = extract_text_from_file(resume_file, resume_file.filename)
            
            if not resume_text.strip():
                flash('Could not extract text from the resume. Please check the file format.', 'danger')
                return redirect(request.url)
            
            # Clean and preprocess text
            resume_text = advanced_text_preprocessing(resume_text)
            jd_text = advanced_text_preprocessing(jd_text)
            
            logger.info("Text extraction and preprocessing completed")
            
            # Perform matching analysis
            skills_list = get_all_skills()
            result = match_resume(resume_text, jd_text, skills_list)
            
            logger.info(f"Analysis completed. Overall score: {result.get('overall_match_score', 0)}")
            
            return render_template("result.html", result=result)
            
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            logger.error(traceback.format_exc())
            flash('An error occurred while processing your request. Please try again.', 'danger')
            return redirect(request.url)
    
    return render_template("index.html")

@app.route("/api/analyze", methods=["POST"])
def api_analyze():
    """API endpoint for programmatic access."""
    try:
        # Check if request contains files
        if 'resume' not in request.files or 'job_description' not in request.form:
            return jsonify({'error': 'Missing resume file or job description'}), 400
        
        resume_file = request.files['resume']
        jd_text = request.form['job_description']
        
        # Validate inputs
        if not allowed_file(resume_file.filename):
            return jsonify({'error': 'Invalid file type'}), 400
        
        # Process request
        resume_text = extract_text_from_file(resume_file, resume_file.filename)
        resume_text = advanced_text_preprocessing(resume_text)
        jd_text = advanced_text_preprocessing(jd_text)
        
        skills_list = get_all_skills()
        result = match_resume(resume_text, jd_text, skills_list)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"API Error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route("/health")
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'message': 'AI Resume Matcher is running'})

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error."""
    flash('File is too large. Please upload a file smaller than 16MB.', 'danger')
    return redirect(url_for('index'))

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors."""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {str(e)}")
    return render_template('500.html'), 500

# Template filters for better formatting
@app.template_filter('format_percentage')
def format_percentage(value):
    """Format number as percentage."""
    try:
        return f"{float(value):.1f}%"
    except (ValueError, TypeError):
        return "0.0%"

@app.template_filter('format_list')
def format_list(items, max_items=5):
    """Format list with maximum items."""
    if not items:
        return []
    return items[:max_items]

if __name__ == "__main__":
    # Check if required models are available
    try:
        import spacy
        nlp = spacy.load("en_core_web_sm")
        logger.info("SpaCy model loaded successfully")
    except OSError:
        logger.warning("SpaCy English model not found. Please install: python -m spacy download en_core_web_sm")
    except Exception as e:
        logger.warning(f"SpaCy model loading failed: {e}")
    
    # Start the application
    logger.info("Starting AI Resume Matcher application...")
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
