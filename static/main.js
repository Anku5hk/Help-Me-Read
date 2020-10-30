var pred_answers = [];
var questions = new Array();
var captionEl1 = $('#caption1');;
var captionEl2 = $('#caption2');; 
// var captionEl3 = $('#caption3');; 

var captionLength = 0;
var caption = '';
var t = 1;

document.getElementById('input_textbox').addEventListener("keypress", function (event) {
  if (event.key == "Enter"){
    event.preventDefault();
    testErasingEffect(captionEl2);
    setTimeout(function (){
      next(t++);
    }, 2000);
  } 
});

$(document).ready(function() {
  setInterval ('cursorAnimation()', 600);
  captionEl1 = $('#caption1');
  captionEl2 = $('#caption2');
  // captionEl3 = $('#caption3');
});

function select_answer(){
  var ans = document.getElementById("input_textbox");
  console.log(ans.value)
  pred_answers.push(ans.value);  // predicted answers
  ans.value = " ";
}

function next(a){
  if(a < questions.length){
      setTimeout(function (){
          testTypingEffect(questions[a], captionEl2);
      }, 1000);
      select_answer();
  }
  else{
      // verify button
      document.getElementById("input_textbox").hidden = true;
      setTimeout(function (){
        testTypingEffect("Press Evaluate.", captionEl2);
       }, 1000);
    setTimeout(function (){
      document.getElementById("evaluate_btn").hidden = false;
     }, 1000);
     
  }
}

function testTypingEffect(text, captionEL) {
  caption = text
  type(captionEL);
}

function type(captionEl) {
  captionEl.html(caption.substr(0, captionLength++));
  if(captionLength < caption.length+1) {
      setTimeout(function (){
          type(captionEl);
      }, 30);
  } else {
      captionLength = 0;
      caption = '';
  }
}

function testErasingEffect(captionEl) {
  caption = captionEl.html();
  captionLength = caption.length;
  if (captionLength>0) {
      erase(captionEl);
  } else {
      $('#caption').html("You didn't write anything, but that's ok!");
      setTimeout(function (){
          testErasingEffect(captionEl);
      }, 1000);
  }
}

function erase(captionEl) {
  captionEl.html(caption.substr(0, captionLength--));
  if(captionLength >= 0) {
      setTimeout(function (){
          erase(captionEl);
      }, 30);
  } else {
      captionLength = 0;
      caption = '';
  }   
}

function cursorAnimation() {
      $('#cursor1').animate({
          opacity: 0
      }, 'fast', 'swing').animate({
          opacity: 2
      }, 'fast', 'swing');

      $('#cursor2').animate({
          opacity: 0
      }, 'fast', 'swing').animate({
          opacity: 2
      }, 'fast', 'swing');

      $('#cursor3').animate({
          opacity: 0
      }, 'fast', 'swing').animate({
          opacity: 2
      }, 'fast', 'swing');
}

function auto_scroll(){
  var interval_id =setInterval(function(){
    window.scrollBy(0,500);
  },100);
  setTimeout(() => {
    clearInterval(interval_id)
  }, 1000);

}


function Summarize(){
  document.getElementById('loading').hidden = false;
  document.getElementById('qa_div').className = 'd-none';
  let text = document.getElementById("input_area").value;
  var entry = {
    input_text: text,
  };

  fetch(`${window.origin}/generate/summarize`, {
      method: "POST",
      credentials: "include",
      body: JSON.stringify(entry),
      cache: "no-cache",
      headers: new Headers({
        "content-type": "application/json"
      })
    })
    .then(function(response) {
      if (response.status !== 200) {
        console.log(`Looks like there was a problem. Status code: ${response.status}`);
        return;
      }
      response.json().then(function(data) {
        document.getElementById('loading').hidden = true;
        auto_scroll();
        document.getElementById('sum_div').className = 'd-inline-block';
        console.log(data.my_summary)
        setTimeout(function (){
          testTypingEffect(data.my_summary, captionEl1);
          }, 1000);
  
      });
    })
    .catch(function(error) {
      console.log("Fetch error: " + error);
  });

}

function Generate_questions(){
  document.getElementById('loading').hidden = false;
  document.getElementById('sum_div').className = 'd-none';
  let text = document.getElementById("input_area").value;
  var entry = {
    input_text: text,
    };
  
    fetch(`${window.origin}/generate/thequestions`, {
        method: "POST",
        credentials: "include",
        body: JSON.stringify(entry),
        cache: "no-cache",
        headers: new Headers({
          "content-type": "application/json"
        })
      })
      .then(function(response) {
        if (response.status !== 200) {
          console.log(`Looks like there was a problem. Status code: ${response.status}`);
          return;
        }
        response.json().then(function(data) {   
          data.my_questions.forEach((item) => {
              questions.push(item);
          }); 
          console.log(questions)
          document.getElementById('loading').hidden = true;
          document.getElementById('qa_div').className = 'd-inline-block';
          document.getElementById('label3').hidden = false;
          document.getElementById("input_textbox").hidden = false;

          setTimeout(function (){
          testTypingEffect(questions[0], captionEl2);
          }, 1000);
        });
      })
      .catch(function(error) {
        console.log("Fetch error: " + error);
    });
  
}  

function Verify_answers(){
  testErasingEffect(captionEl2);
  document.getElementById('loading').hidden = false;
  document.getElementById("evaluate_btn").hidden = true;
  document.getElementById('label3').hidden = true;
  var entry = {
    predicted_answers: pred_answers,
  };

  fetch(`${window.origin}/verifyquestions/verifcation`, {
      method: "POST",
      credentials: "include",
      body: JSON.stringify(entry),
      cache: "no-cache",
      headers: new Headers({
        "content-type": "application/json"
      })
    })
    .then(function(response) {
      if (response.status !== 200) {
        console.log(`Looks like there was a problem. Status code: ${response.status}`);
        return;
      }
      response.json().then(function(data) {
        document.getElementById('loading').hidden = true;
        console.log(data.num_of_correct)
        setTimeout(function (){
          testTypingEffect(data.num_of_correct, captionEl2);
          }, 1000);
      });
    })
    .catch(function(error) {
      console.log("Fetch error: " + error);
  });

}
