"""
=============================================================
  RESUME MATCHING ENGINE — 
=============================================================
  Name     : Aman Singh (M.Tech AI - A023144825024)
  Libraries: Python standard library ONLY
  
  =============================================================
"""

import math
import re
from collections import defaultdict

# ─────────────────────────────────────────────────────────
#  PHASE 1 — DATA PREPARATION
# ─────────────────────────────────────────────────────────

# SKILL_ALIASES — copied EXACTLY from the hackathon problem sheet.
# DO NOT modify, add, or remove any entry.
SKILL_ALIASES = {
    # Languages
    "python":               "python",
    "pyhton":               "python",
    "java":                 "java",
    "javascript":           "javascript",
    "javascrpit":           "javascript",
    "js":                   "javascript",
    "typescript":           "typescript",
    "typescrpit":           "typescript",
    "c++":                  "cpp",
    "cpp":                  "cpp",
    "r":                    "r",
    "kotlin":               "kotlin",

    # ML / Data
    "machinelearning":      "machine_learning",
    "machine learning":     "machine_learning",
    "ml":                   "machine_learning",
    "sklearn":              "machine_learning",
    "deeplearning":         "deep_learning",
    "deep learning":        "deep_learning",
    "deep-learning":        "deep_learning",
    "tensorflow":           "tensorflow",
    "pytorch":              "pytorch",
    "keras":                "keras",
    "nlp":                  "nlp",
    "bert":                 "bert",
    "xgboost":              "xgboost",
    "feature engineering":  "feature_engineering",
    "statistics":           "statistics",
    "stats":                "statistics",
    "regression":           "regression",
    "clustering":           "clustering",
    "data-viz":             "data_visualization",
    "data visualization":   "data_visualization",
    "data viz":             "data_visualization",
    "matplotlib":           "data_visualization",
    "tableau":              "data_visualization",
    "power-bi":             "data_visualization",
    "power bi":             "data_visualization",
    "powerbi":              "data_visualization",
    "pandas":               "pandas",
    "numpy":                "numpy",

    # Web — Frontend
    "react":                "react",
    "reacts":               "react",
    "reactjs":              "react",
    "vue":                  "vue",
    "vue.js":               "vue",
    "vuejs":                "vue",
    "redux":                "redux",
    "tailwind":             "tailwind",
    "html/css":             "html_css",
    "html css":             "html_css",
    "html":                 "html_css",
    "css":                  "html_css",
    "jest":                 "jest",
    "graphql":              "graphql",

    # Web — Backend
    "node.js":              "nodejs",
    "nodejs":               "nodejs",
    "node js":              "nodejs",
    "flask":                "flask",
    "spring boot":          "spring_boot",
    "springboot":           "spring_boot",
    "rest api":             "rest_api",
    "rest":                 "rest_api",
    "restapi":              "rest_api",
    "microservices":        "microservices",

    # Databases
    "sql":                  "sql",
    "mysql":                "mysql",
    "mysq":                 "mysql",
    "postgresql":           "postgresql",
    "postgres":             "postgresql",
    "mongodb":              "mongodb",
    "redis":                "redis",

    # DevOps / Cloud
    "docker":               "docker",
    "kubernetes":           "kubernetes",
    "kubernates":           "kubernetes",
    "k8s":                  "kubernetes",
    "ci/cd":                "ci_cd",
    "cicd":                 "ci_cd",
    "ci cd":                "ci_cd",
    "aws":                  "aws",

    # Mobile
    "android":              "android",
    "firebase":             "firebase",

    # CS Fundamentals
    "algorithms":           "algorithms",
    "algoritms":            "algorithms",
    "data structure":       "data_structures",
    "data structures":      "data_structures",
    "competitive programming": "competitive_programming",

    # Design
    "ui/ux":                "ui_ux",
    "ui ux":                "ui_ux",
    "figma":                "figma",
}

# ── 10 Resumes — EXACT data from the hackathon problem sheet ──
RESUMES = [
    {
        "name":   "Arjun Sharma",
        "skills": "Pyhton, MachineLearning, SQL, pandas, numpy, Deep-learning"
    },
    {
        "name":   "Priya Nair",
        "skills": "JavaScrpit, Reacts, Node.JS, MongoDb, REST api, HTML/CSS"
    },
    {
        "name":   "Rahul Gupta",
        "skills": "Java, Spring Boot, MySql, Microservices, Docker, kubernates"
    },
    {
        "name":   "Sneha Patel",
        "skills": "Python, TensorFlow, Keras, NLP, BERT, data-viz, matplotlib"
    },
    {
        "name":   "Vikram Singh",
        "skills": "C++, Algoritms, Data Structure, competitive programming, python"
    },
    {
        "name":   "Ananya Krishnan",
        "skills": "javascript, vue.js, python, flask, PostgreSQL, AWS, CI/CD"
    },
    {
        "name":   "Karan Mehta",
        "skills": "Python, Sklearn, XGboost, feature engineering, SQL, tableau"
    },
    {
        "name":   "Deepika Rao",
        "skills": "Java, Android, Kotlin, Firebase, REST, UI/UX, figma"
    },
    {
        "name":   "Aditya Kumar",
        "skills": "Reactjs, TypeScrpit, GraphQL, redux, tailwind, nodejs, jest"
    },
    {
        "name":   "Meera Iyer",
        "skills": "python, R, statistics, ML, regression, clustering, Power-BI"
    },
]

# ── 3 Job Descriptions — EXACT data from the hackathon problem sheet ──
# JD skills = Required Skills + Preferred Skills combined
JOB_DESCRIPTIONS = [
    {
        "id":    "JD-1",
        "title": "Kakao (ML Engineer)",
        # Required: Python, Machine Learning, Deep Learning, TensorFlow, PyTorch, SQL, Data Visualization
        # Preferred: NLP, BERT, Feature Engineering, Statistics
        "skills": "Python, Machine Learning, Deep Learning, TensorFlow, PyTorch, SQL, Data Visualization, NLP, BERT, Feature Engineering, Statistics"
    },
    {
        "id":    "JD-2",
        "title": "Naver (Backend Engineer)",
        # Required: Java, Spring Boot, MySQL, PostgreSQL, Microservices, Docker, Kubernetes
        # Preferred: REST API, CI/CD, Redis
        "skills": "Java, Spring Boot, MySQL, PostgreSQL, Microservices, Docker, Kubernetes, REST API, CI/CD, Redis"
    },
    {
        "id":    "JD-3",
        "title": "Line (Frontend Engineer)",
        # Required: JavaScript, React, Vue, TypeScript, REST API, HTML/CSS
        # Preferred: Node.js, GraphQL, Redux, Jest, AWS
        "skills": "JavaScript, React, Vue, TypeScript, REST API, HTML/CSS, Node.js, GraphQL, Redux, Jest, AWS"
    },
]


# ─────────────────────────────────────────────────────────
#  PHASE 2 — SKILL NORMALIZATION
# ─────────────────────────────────────────────────────────

def normalize_skills(raw_skills_str: str, debug: bool = False) -> list:
    """
    Normalize a raw comma-separated skills string to canonical skill names.

    Steps:
    1. Split on commas
    2. Lowercase + strip whitespace each token
    3. Try to match each token against SKILL_ALIASES (exact key match)
       - Aliases are sorted longest-first so multi-word phrases like
         "feature engineering", "spring boot", "competitive programming"
         are matched before any shorter sub-key could shadow them.
         (In practice every token here is a single comma-separated chunk
          so multi-word phrases arrive as a single token already.)
    4. Discard tokens with no alias match
    5. Remove duplicates (preserve first-seen order for dedup, return sorted)

    Returns a sorted list of canonical skill names.
    """
    # Step 1 & 2: split on commas, lowercase, strip whitespace
    tokens = [t.strip().lower() for t in raw_skills_str.split(",")]

    canonical = []
    removed   = []

    # Sort alias keys longest-first so multi-word keys match before
    # shorter ones (e.g. "feature engineering" before "feature")
    sorted_alias_keys = sorted(SKILL_ALIASES.keys(), key=lambda k: -len(k))

    for token in tokens:
        if not token:          # skip empty strings from trailing commas etc.
            continue
        matched = False
        for alias_key in sorted_alias_keys:
            if token == alias_key:
                canonical.append(SKILL_ALIASES[alias_key])
                matched = True
                break
        if not matched:
            removed.append(token)

    # Step 5: remove duplicates, keep first occurrence, then sort
    seen   = set()
    deduped = []
    for skill in canonical:
        if skill not in seen:
            seen.add(skill)
            deduped.append(skill)

    result = sorted(deduped)

    if debug:
        print(f"  Raw tokens  : {tokens}")
        print(f"  Normalized  : {result}")
        print(f"  Removed     : {removed}")

    return result


# ─────────────────────────────────────────────────────────
#  PHASE 3 — VOCABULARY CONSTRUCTION
# ─────────────────────────────────────────────────────────

def build_vocabulary(normalized_resumes: list) -> list:
    """
    Build a sorted, deduplicated vocabulary from all resume skills.
    JD skills are NOT used for vocabulary construction.
    """
    vocab_set = set()
    for resume in normalized_resumes:
        for skill in resume["normalized_skills"]:
            vocab_set.add(skill)
    vocab = sorted(vocab_set)
    return vocab


# ─────────────────────────────────────────────────────────
#  PHASE 4 — TF-IDF IMPLEMENTATION
# ─────────────────────────────────────────────────────────

def compute_tf(skill: str, skill_list: list) -> float:
    """
    TF(skill, resume) = count(skill in resume) / len(resume_skills)
    Since duplicates are removed, count is always 1 if skill exists.
    TF = 1 / N   where N = total unique skills in resume.
    """
    N = len(skill_list)
    if N == 0:
        return 0.0
    count = 1 if skill in skill_list else 0
    return count / N


def compute_idf(skill: str, all_resumes_skills: list, total_docs: int = 10) -> float:
    """
    IDF(skill) = ln(total_docs / df(skill))
    df(skill)  = number of resumes containing the skill
    No smoothing applied.
    If df = 0, return 0 (skill appears in no document — shouldn't happen
    since vocab is built from resume skills, but guard anyway).
    """
    df = sum(1 for skills in all_resumes_skills if skill in skills)
    if df == 0:
        return 0.0
    return math.log(total_docs / df)


def compute_tfidf_vectors(normalized_resumes: list, vocab: list) -> dict:
    """
    Compute TF-IDF vector for every resume over the shared vocabulary.
    Returns dict: { candidate_name -> [tfidf_val_for_each_vocab_skill] }
    """
    all_skills_lists = [r["normalized_skills"] for r in normalized_resumes]
    total_docs = len(normalized_resumes)

    # Pre-compute IDF for every vocab skill
    idf_table = {}
    for skill in vocab:
        idf_table[skill] = compute_idf(skill, all_skills_lists, total_docs)

    # DF table for display
    df_table = {}
    for skill in vocab:
        df_table[skill] = sum(1 for sl in all_skills_lists if skill in sl)

    # Compute TF-IDF vectors
    vectors = {}
    for resume in normalized_resumes:
        name        = resume["name"]
        skill_list  = resume["normalized_skills"]
        vector      = []
        for skill in vocab:
            tf    = compute_tf(skill, skill_list)
            idf   = idf_table[skill]
            tfidf = tf * idf
            vector.append(tfidf)
        vectors[name] = vector

    return vectors, idf_table, df_table


# ─────────────────────────────────────────────────────────
#  PHASE 5 — JD BINARY VECTORS
# ─────────────────────────────────────────────────────────

def build_jd_vector(jd_skills: list, vocab: list) -> list:
    """
    Build a binary vector for a JD over the shared vocabulary.
    1 if skill in JD, 0 otherwise.
    """
    return [1 if skill in jd_skills else 0 for skill in vocab]


# ─────────────────────────────────────────────────────────
#  PHASE 6 — COSINE SIMILARITY
# ─────────────────────────────────────────────────────────

def cosine_similarity(vec_a: list, vec_b: list) -> float:
    """
    Cosine(A, B) = (A · B) / (|A| × |B|)
    Implemented manually without any library.
    """
    # Dot product
    dot = sum(a * b for a, b in zip(vec_a, vec_b))

    # Norms
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot / (norm_a * norm_b)


# ─────────────────────────────────────────────────────────
#  PHASE 7 — RANKING SYSTEM
# ─────────────────────────────────────────────────────────

def rank_candidates(similarity_scores: dict, top_n: int = 3) -> list:
    """
    Rank candidates by similarity score (descending).
    Tie-break: alphabetical by candidate name.
    Returns top_n candidates as list of (name, score) tuples.
    """
    # Sort: primary = -score (descending), secondary = name (ascending)
    ranked = sorted(
        similarity_scores.items(),
        key=lambda x: (-round(x[1], 10), x[0])
    )
    return ranked[:top_n]


# ─────────────────────────────────────────────────────────
#  PHASE 9 — VALIDATION HELPERS
# ─────────────────────────────────────────────────────────

def validate_vectors(tfidf_vectors: dict, jd_vectors: dict, vocab: list):
    """Ensure all vectors have the same length as vocabulary."""
    vocab_len = len(vocab)
    print("\n── Validation ──────────────────────────────────")
    for name, vec in tfidf_vectors.items():
        assert len(vec) == vocab_len, f"Vector length mismatch for {name}!"
    print(f"  ✓ All resume TF-IDF vectors length = {vocab_len}")

    for jd_id, vec in jd_vectors.items():
        assert len(vec) == vocab_len, f"JD vector length mismatch for {jd_id}!"
    print(f"  ✓ All JD binary vectors   length = {vocab_len}")

    # Spot-check cosine of identical vectors = 1.0
    test_v = [0.1, 0.2, 0.3]
    cs = cosine_similarity(test_v, test_v)
    assert abs(cs - 1.0) < 1e-9, "Cosine self-similarity should be 1.0!"
    print("  ✓ Cosine self-similarity check passed")

    # Cosine of orthogonal vectors = 0.0
    v1, v2 = [1, 0, 0], [0, 1, 0]
    assert cosine_similarity(v1, v2) == 0.0, "Orthogonal vectors should have cosine 0"
    print("  ✓ Cosine orthogonality check passed")
    print("────────────────────────────────────────────────\n")


# ─────────────────────────────────────────────────────────
#  MAIN PIPELINE
# ─────────────────────────────────────────────────────────

def main():
    DIVIDER = "=" * 60

    # ── PHASE 2: Normalize all resumes ────────────────────
    print(f"\n{DIVIDER}")
    print("  PHASE 2 — SKILL NORMALIZATION")
    print(DIVIDER)

    normalized_resumes = []
    for resume in RESUMES:
        print(f"\nCandidate: {resume['name']}")
        norm_skills = normalize_skills(resume["skills"], debug=True)
        normalized_resumes.append({
            "name":             resume["name"],
            "normalized_skills": norm_skills,
        })

    # ── PHASE 3: Build vocabulary ──────────────────────────
    print(f"\n{DIVIDER}")
    print("  PHASE 3 — VOCABULARY CONSTRUCTION")
    print(DIVIDER)

    vocab = build_vocabulary(normalized_resumes)
    print(f"\nVocabulary ({len(vocab)} skills):")
    for i, skill in enumerate(vocab, 1):
        print(f"  {i:2d}. {skill}")

    # ── PHASE 4: TF-IDF ───────────────────────────────────
    print(f"\n{DIVIDER}")
    print("  PHASE 4 — TF-IDF COMPUTATION")
    print(DIVIDER)

    tfidf_vectors, idf_table, df_table = compute_tfidf_vectors(
        normalized_resumes, vocab
    )

    print("\nDocument Frequency Table:")
    for skill in vocab:
        print(f"  df({skill:<30}) = {df_table[skill]}")

    print("\nIDF Table:")
    for skill in vocab:
        print(f"  idf({skill:<30}) = {idf_table[skill]:.6f}")

    print("\nTF-IDF Vectors (non-zero entries only):")
    for name, vec in tfidf_vectors.items():
        print(f"\n  {name}:")
        for i, skill in enumerate(vocab):
            if vec[i] > 0:
                print(f"    {skill:<30} = {vec[i]:.6f}")

    # ── PHASE 5: JD binary vectors ─────────────────────────
    print(f"\n{DIVIDER}")
    print("  PHASE 5 — JD BINARY VECTORS")
    print(DIVIDER)

    normalized_jds    = []
    jd_vectors_dict   = {}

    for jd in JOB_DESCRIPTIONS:
        print(f"\n{jd['id']} — {jd['title']}")
        norm_skills = normalize_skills(jd["skills"], debug=True)
        jd_vec      = build_jd_vector(norm_skills, vocab)
        normalized_jds.append({
            "id":              jd["id"],
            "title":           jd["title"],
            "normalized_skills": norm_skills,
            "vector":          jd_vec,
        })
        jd_vectors_dict[jd["id"]] = jd_vec
        print(f"  Binary vector (active skills): "
              f"{[vocab[i] for i,v in enumerate(jd_vec) if v]}")

    # ── PHASE 9: Validation ────────────────────────────────
    validate_vectors(tfidf_vectors, jd_vectors_dict, vocab)

    # ── PHASE 6: Cosine similarity ─────────────────────────
    print(f"{DIVIDER}")
    print("  PHASE 6 — COSINE SIMILARITY MATRIX")
    print(DIVIDER)

    similarity_matrix = defaultdict(dict)  # {jd_id: {candidate: score}}

    for jd_info in normalized_jds:
        jd_id  = jd_info["id"]
        jd_vec = jd_info["vector"]
        print(f"\n{jd_id} — {jd_info['title']}")
        for name, res_vec in tfidf_vectors.items():
            score = cosine_similarity(res_vec, jd_vec)
            similarity_matrix[jd_id][name] = score
            print(f"  {name:<10} → {score:.6f}")

    # ── PHASE 7: Ranking ───────────────────────────────────
    print(f"\n{DIVIDER}")
    print("  PHASE 7 — FINAL RANKED OUTPUT (Top 3 per JD)")
    print(DIVIDER)

    for jd_info in normalized_jds:
        jd_id    = jd_info["id"]
        jd_title = jd_info["title"]
        scores   = similarity_matrix[jd_id]
        top3     = rank_candidates(scores, top_n=3)

        print(f"\n{jd_id} — {jd_title}")
        result_parts = [f"{name}({round(score, 2):.2f})" for name, score in top3]
        print("  " + ", ".join(result_parts))

    print(f"\n{DIVIDER}\n")


if __name__ == "__main__":
    main()