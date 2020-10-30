import torch, os, gdown
from flask import Flask, render_template, request, send_from_directory, make_response, jsonify
from pipelines import pipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

app = Flask(__name__)
if os.path.isfile('./models/quant-t5-base.pt'):
    pass
else:
    print('Downloading models...')
    if not os.path.isdir('models'): os.mkdir('models')
    url1 = 'https://drive.google.com/uc?id=1FoI1dH1h6inmmjsJRWpKd6qyScQo-7fU'
    url2 = 'https://drive.google.com/uc?id=1XfWd2qMJLonwa88uUCOfQkDvd9IPIpOF'
    output1 = "models/qa-qg-t5-small.pt"
    output2 = "models/quant-t5-base.pt"
    gdown.download(url1, output1, quiet=True)
    gdown.download(url2, output2, quiet=True)
    print('Models downloaded..')

device = 'cpu'
print("Device used:", device)
print('Loading models....')
t5_base = torch.load('models/quant-t5-base.pt', map_location=device) # summarizer, text_similarity
t5_small_qa_qg = torch.load('models/qa-qg-t5-small.pt', map_location=device) # questions answer generation
Tokenizer1 = AutoTokenizer.from_pretrained("t5-base" )
Tokenizer2 = AutoTokenizer.from_pretrained("valhalla/t5-small-qa-qg-hl" )
question_generator = pipeline("question-generation", model=t5_small_qa_qg, tokenizer=Tokenizer2, 
ans_model=t5_small_qa_qg, ans_tokenizer=Tokenizer2, use_cuda=device)

print('Done!!')
org_answers = None

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

# summarize text
def get_summary(text):
    try:
        text = "summarize: "+text
        tokenized_text = Tokenizer1.encode(text, return_tensors="pt")
        summary_ids = t5_base.generate(tokenized_text, num_beams=4, no_repeat_ngram_size=2,
        min_length=30,max_length=1000, early_stopping=True)

        output = Tokenizer1.decode(summary_ids[0], skip_special_tokens=True)
    except :
        print('Error.....')   
    return output

# questions and answers
def get_questions(text):
    result = question_generator(text)
    return result

# compare answers by user and model
def comapare_answers(pred_answer):
    correct = 0
    for i in range(len(org_answers)):
        try:
            org_answers[i] = "mrpc sentence1: "+org_answers[i] # model answer
            pred_answer[i] = ". sentence2: "+pred_answer[i] # user answer
            tokenized_text = Tokenizer1.encode(org_answers[i]+pred_answer[i], return_tensors="pt")
            summary_ids = t5_base.generate(tokenized_text)
            output = Tokenizer1.decode(summary_ids[0], skip_special_tokens=True)
            if output == 'equivalent':
                correct+=1
        except:
            continue        
    return correct

@app.route('/', methods=['GET', 'POST'])
# home page
def home():
    return render_template('index.html')

@app.route("/generate/summarize", methods=["POST"])
def summarize():
    print('Generating SUmmary.....')
    req = request.get_json()
    summary = get_summary(req['input_text'])
    res = make_response(jsonify({"my_summary": capitilize_text(summary)}), 200)
    return res

@app.route("/generate/thequestions", methods=["POST"])
def thequestions():
    global org_answers
    req = request.get_json()
    print('Generating SUmmary.....')
    text = get_summary(req['input_text'])
    print('Generating questions.....')
    question_answers = get_questions(text)
    print(question_answers)
    questions = [a['question'] for a in question_answers if len(a['question']) < 70]
    org_answers = [a['answer'] for a in question_answers]
    res = make_response(jsonify({"my_questions": questions}), 200)
    return res

@app.route('/verifyquestions/verifcation', methods=["POST"])
def verifcation():
    print('Verifying answers.......')
    pred_answers = request.get_json()
    print(pred_answers['predicted_answers'])
    correct_ans = comapare_answers(pred_answers['predicted_answers'])
    print('Answers verified.......')
    correct_ans = 'You answered {} questions correctly!!'.format(correct_ans)
    my_response = make_response(jsonify({"num_of_correct": correct_ans}), 200)
    return my_response

@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run()