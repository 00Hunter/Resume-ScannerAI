from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def parse_resume(file_path):

    reader=PdfReader(file_path)

    # print(len(reader.pages))

    page=reader.pages[0]

    # print(page.extract_text())
    return page.extract_text()

def calculate_resume_score(resume_text,job_desc_text):
    """
    Compares resume text with job description text using TF-IDF and Cosine Similarity.
    
    Args:
    resume_text (str): Extracted text from the resume.
    job_desc_text (str): Text from the job description.

    Returns:
    float: Resume match percentage (0-100%).
    """
    
    # Convert text into numerical vectors
    vectorizer = TfidfVectorizer(stop_words='english')
    # resume_text=parse_resume();
    tfidf_matrix = vectorizer.fit_transform([resume_text, job_desc_text])
    
    # Compute cosine similarity between resume and job description
    similarity = cosine_similarity(tfidf_matrix)[0, 1]  # Similarity score

    return round(similarity * 100, 2)  # Convert to percentage (0-100%)


