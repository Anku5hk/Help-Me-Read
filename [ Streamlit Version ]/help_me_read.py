import torch
import streamlit as st
from transformers import AutoTokenizer, AutoModel, AutoModelForSeq2SeqLM
from question_generation.pipelines import pipeline

device = torch.device('cuda')
tokenizer = None
model = None
question_generator = None

# load models,tokenizer
def load_models():
     global tokenizer, model, question_generator
     tokenizer = AutoTokenizer.from_pretrained("t5-small")
     model = AutoModelForSeq2SeqLM.from_pretrained("t5-small").to(device)
     question_generator = pipeline("question-generation")

# summarize text
def get_summary(text):
    text = "summarize: "+text
    tokenized_text = tokenizer.encode(text, return_tensors="pt").to(device)
    summary_ids = model.generate(tokenized_text, num_beams=4, no_repeat_ngram_size=2,min_length=30,max_length=100, early_stopping=True)
    output = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return output

# capitilize text of summary
def capitilize_text(source):
    stop, output = '.', ''
    i,j = 0, 0
    for i, w in enumerate(source):
        if w == stop:
            sen = source[j:i+1].capitalize() 
            j = i+2
            output+=sen      
    output+=source[j:].capitalize()       
    return output

# translate text
def translate_text(text,option):   
    text = "translate English to "+ option +": "+ text
    tokenized_text = tokenizer.encode(text, return_tensors="pt").to(device)
    summary_ids = model.generate(tokenized_text, num_beams=4, no_repeat_ngram_size=2,min_length=30,max_length=100, early_stopping=True)
    output = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return output

# questions and answers
def get_questions(text):
    result = question_generator(text)
    st.markdown('**Question Answers:**')
    for res in result:
        st.markdown('**'+res['question']+'**')
        st.text(res['answer']) 

def main():
    st.title('HelpMeRead')
    message = st.text_area("Enter Text: ")
    option = st.selectbox("Select language: ", ('German', 'French', 'Romanian'))
    Translate = st.button("Translate")
    Summarize = st.button("Summarize")
    QAs = st.button("QAs")
    load_models()
    if Summarize:
        result = get_summary(message)
        st.markdown('**Summary:**')
        st.write(capitilize_text(result))
    if Translate:
        result = translate_text(message, option)
        st.markdown('**Translation:**')
        st.write(result)
    if QAs:
        get_questions(message)   

if __name__ == "__main__":
    main()
