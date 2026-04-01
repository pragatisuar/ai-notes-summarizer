import streamlit as st
import re

def summarize_text(text):
    sentences = text.split('.')
    sentences = [s.strip() for s in sentences if s.strip()]
    return '. '.join(sentences[:3])

def extract_keywords(text):
    words = re.findall(r'\b\w+\b', text.lower())
    stopwords = {'the','is','and','in','to','of','a','for','on','with','as','by','an'}
    
    filtered = [word for word in words if word not in stopwords]
    
    freq = {}
    for word in filtered:
        freq[word] = freq.get(word, 0) + 1
    
    sorted_words = sorted(freq, key=freq.get, reverse=True)
    return sorted_words[:5]

def generate_questions(text):
    questions = []
    
    if "is" in text:
        questions.append("What is the main concept discussed?")
    if "because" in text:
        questions.append("Why is this concept important?")
    
    questions.append("Explain the topic in your own words.")
    
    return questions


# UI starts here
st.title("AI Study Notes Processor")

text = st.text_area("Paste your notes here:")

if st.button("Generate", key="generate_btn"):
    summary = summarize_text(text)
    keywords = extract_keywords(text)
    questions = generate_questions(text)

    st.subheader("Summary")
    st.write(summary)

    st.subheader("Keywords")
    st.write(", ".join(keywords))

    st.subheader("Questions")
    for q in questions:
        st.write("- " + q)

    # ✅ Proper download
    output = f"Summary:\n{summary}\n\nKeywords:\n{', '.join(keywords)}\n\nQuestions:\n"
    for q in questions:
        output += f"- {q}\n"

    st.download_button(
        label="Download Results",
        data=output,
        file_name="study_notes.txt",
        mime="text/plain"
    )