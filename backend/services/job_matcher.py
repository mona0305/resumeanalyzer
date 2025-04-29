
from models.job import Job
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def match_jobs(skills, location):
    # Fetch all jobs from the database
    jobs = Job.objects.all()
    
    # Prepare data for matching
    job_titles = [job.title for job in jobs]
    job_skills = [' '.join(job.required_skills) for job in jobs]
    
    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer()
    job_skills_tfidf = vectorizer.fit_transform(job_skills)
    
    # Create a query vector for the user's skills
    user_skills_tfidf = vectorizer.transform([' '.join(skills)])
    
    # Calculate similarity
    cosine_sim = cosine_similarity(user_skills_tfidf, job_skills_tfidf)
    
    # Get top matches based on similarity
    job_matches = []
    for idx, score in enumerate(cosine_sim[0]):
        if score > 0.1:  # You can adjust the threshold
            job_matches.append({
                "title": job_titles[idx],
                "skills": jobs[idx].required_skills,
                "location": jobs[idx].location,
                "score": score
            })
    
    return job_matches
    