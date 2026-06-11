function speak(language){

fetch('/speak/'+language)

.then(response=>response.text())

.then(text=>{

let speech =
new SpeechSynthesisUtterance();

speech.text = text;

if(language==="Telugu")
speech.lang="te-IN";

else if(language==="Hindi")
speech.lang="hi-IN";

else if(language==="Tamil")
speech.lang="ta-IN";

else
speech.lang="en-US";

window.speechSynthesis.speak(speech);

});

}