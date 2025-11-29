# AI-Powered Resume & Job Description Matcher

## Overview

A sophisticated ML/NLP-based system that analyzes resumes and job descriptions using advanced artificial intelligence to provide comprehensive matching insights.


##  Enhanced Tech Stack

### Backend & AI/ML

- **Python 3.8+** - Core programming language
- **Flask** - Web framework with enhanced error handling
- **Sentence Transformers** - BERT-based semantic embeddings (`all-MiniLM-L6-v2`)
- **spaCy** - Advanced NLP processing with `en_core_web_sm`
- **scikit-learn** - TF-IDF fallback and additional ML utilities
- **NLTK** - Text preprocessing and tokenization
- **FuzzyWuzzy** - Intelligent skill matching with Levenshtein distance

### File Processing

- **PyMuPDF (fitz)** - PDF text extraction
- **python-docx** - DOCX document processing
- **Advanced text preprocessing** - Lemmatization, stopword removal, entity recognition

### Frontend & UI

- **Bootstrap 5** - Modern responsive design framework
- **Font Awesome 6** - Professional iconography
- **Custom CSS** - Enhanced animations and user experience
- **Vanilla JavaScript** - Interactive features and file handling

### Development & Deployment

- **Comprehensive logging** - Application monitoring and debugging
- **Error handling** - Graceful failure management with user feedback
- **API endpoints** - RESTful API for programmatic access
- **Health checks** - System monitoring capabilities

### Automated Setup (Recommended)

```bash
# Clone the repository
git clone https://github.com/donbasu15/ai_resume_matcher
cd resume_job_matcher

# Run the setup script
./setup.sh

# Start the application
source venv/bin/activate
python app/main.py
```

### Manual Setup

```bash
# 1. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 3. Download NLP models
python -m spacy download en_core_web_sm

# 4. Create necessary directories
mkdir -p uploads logs data/models

# 5. Start the application
python app/main.py
```

## Usage

### Web Interface

1. **Open your browser** and navigate to `http://localhost:5000`
2. **Upload your resume** (PDF or DOCX format)
3. **Paste the job description** you're interested in
4. **Click "Analyze Match"** and get comprehensive insights

### API Usage

```bash
# Programmatic analysis via REST API
curl -X POST http://localhost:5000/api/analyze \
  -F "resume=@path/to/resume.pdf" \
  -F "job_description=Your job description text here"
```

## 📈 Analysis Results

### What You Get

- **Overall Match Score**: Weighted composite score (0-100%)
- **Component Breakdown**: Individual scores for skills, experience, content similarity
- **Skills Analysis**:
  - ✅ Matching skills with categories
  - ❌ Missing skills with priority levels
  - 📊 Skills distribution by category
- **Experience Analysis**: Years match, seniority level alignment
- **Improvement Suggestions**: Prioritized actionable recommendations
- **Keyword Optimization**: Density analysis and strategic recommendations

### Sample Output

```json
{
  "overall_match_score": 78.5,
  "component_scores": {
    "skill_match": 85.2,
    "experience_match": 72.1,
    "semantic_similarity": 76.8,
    "section_scores": {...}
  },
  "common_skills": ["python", "machine learning", "sql"],
  "missing_skills": ["aws", "docker", "kubernetes"],
  "improvement_suggestions": [
    {
      "type": "critical_skills",
      "title": "Critical Skills Missing",
      "description": "Add cloud skills: AWS, Docker",
      "priority": "high"
    }
  ]
}
```

## Configuration

### Environment Variables

```bash
export FLASK_ENV=development  # or production
export SECRET_KEY=your-secret-key-here
export MAX_FILE_SIZE=16777216  # 16MB in bytes
export UPLOAD_FOLDER=uploads
```

### Model Configuration

- **Sentence Transformer Model**: `all-MiniLM-L6-v2` (384 dimensions)
- **spaCy Model**: `en_core_web_sm` (English language)
- **Skill Database**: 500+ curated technical and soft skills
- **File Support**: PDF (PyMuPDF), DOCX (python-docx)

## 🚀 Deployment Options

### Local Development

```bash
python app/main.py
# Access: http://localhost:5000
```

### Production Deployment

#### Docker (Recommended)

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_sm
COPY . .
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app.main:app"]
```

#### Cloud Platforms

- **Heroku**: Ready for deployment with Procfile
- **AWS/GCP**: Compatible with standard Python hosting
- **Docker**: Containerized deployment support

## 🧪 Testing

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest tests/ -v --cov=src/

# Test API endpoints
curl http://localhost:5000/health
```

### Development Setup

```bash
git clone <repository-url>
cd resume_job_matcher
./setup.sh
source venv/bin/activate

# Install development dependencies
pip install -r requirements-dev.txt

# Run in development mode
export FLASK_ENV=development
python app/main.py
```

### Code Structure

```
resume_job_matcher/
├── app/
│   ├── main.py              # Flask application
│   ├── static/              # CSS, JS, assets
│   └── templates/           # HTML templates
├── src/
│   ├── embedding.py         # Semantic similarity
│   ├── extractor.py         # Skill/experience extraction
│   ├── matcher.py           # Core matching algorithm
│   ├── preprocessing.py     # Text processing
│   └── skills_database.py   # Skills repository
├── data/                    # Data files
├── notebooks/               # Jupyter notebooks
├── tests/                   # Test suite
├── requirements.txt         # Dependencies
├── setup.sh                # Setup script
└── README.md               # Documentation
```


```bash
python -m spacy download en_core_web_sm
```


---

bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python app/main.py

```

```
