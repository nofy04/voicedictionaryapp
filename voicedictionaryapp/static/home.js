document.addEventListener("DOMContentLoaded", () => {
  const hrs = document.querySelectorAll("hr");
  const definition = document.getElementById("definition");
  const example = document.getElementById("examplecontent");
  const partOfSpeech = document.getElementById("partofspeechcontent");
  const voiceBtn = document.getElementById("voiceinputbutton");
  const input = document.getElementById("wordinput");

  // Show <hr> lines
  if (
    (definition && definition.textContent.trim() !== "") ||
    (example && example.textContent.trim() !== "") ||
    (partOfSpeech && partOfSpeech.textContent.trim() !== "")
  ) {
    for (const hr of hrs) {
      hr.style.display = "block";
    }
  }

  // Voice input functionality
  if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();

    recognition.lang = 'en-US';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    voiceBtn.addEventListener("click", () => {
      voiceBtn.textContent = "Listening...";
      voiceBtn.disabled = true;
      recognition.start();
    });

    recognition.addEventListener("result", (event) => {
      const spokenWord = event.results[0][0].transcript;
      input.value = spokenWord;
    });

    recognition.addEventListener("end", () => {
      voiceBtn.textContent = "Voice Input";
      voiceBtn.disabled = false;
    });

  } else {
    voiceBtn.disabled = true;
    voiceBtn.textContent = "Voice Not Supported";
  }
});
