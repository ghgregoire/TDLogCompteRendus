const promptForm = document.getElementById("prompt-form");
const submitButton = document.getElementById("submit-button");
const questionButton = document.getElementById("question-button");
const messagesContainer = document.getElementById("messages-container");
const jrperronnet = document.getElementById("perronnet-button");
const lucdormieux = document.getElementById("dormieux-button")

const appendHumanMessage = (message) => {
  const humanMessageElement = document.createElement("div");
  humanMessageElement.classList.add("message", "message-human");
  humanMessageElement.innerHTML = message;
  messagesContainer.appendChild(humanMessageElement);
};

const appendAIMessage = async (messagePromise) => {
  // Add a loader to the interface
  const loaderElement = document.createElement("div");
  loaderElement.classList.add("message");
  loaderElement.innerHTML =
    "<div class='loader'><div></div><div></div><div></div>";
  messagesContainer.appendChild(loaderElement);

  // Await the answer from the server
  const messageToAppend = await messagePromise();

  // Replace the loader with the answer
  loaderElement.classList.remove("loader");
  loaderElement.innerHTML = messageToAppend;
};

const handlePrompt = async (event) => {
  event.preventDefault();
  // Parse form data in a structured object
  const data = new FormData(event.target);
  promptForm.reset();

  let url = "/prompt";
  if (questionButton.dataset.question !== undefined) {
    url = "/answer";
    data.append("question", questionButton.dataset.question);
    delete questionButton.dataset.question;
    questionButton.classList.remove("hidden");
    submitButton.innerHTML = "Message";
  }
  if (jrperronnet.dataset.question !== undefined) {
    url = "/perro2";
    data.append("question", jrperronnet.dataset.question);
    delete jrperronnet.dataset.question;
    jrperronnet.classList.remove("hidden");
    submitButton.innerHTML = "Message";
  }
  if (lucdormieux.dataset.question !== undefined) {
    url = "/dormieux2";
    data.append("question", lucdormieux.dataset.question);
    delete lucdormieux.dataset.question;
    lucdormieux.classList.remove("hidden");
    submitButton.innerHTML = "Message";
  }
  

  

  appendHumanMessage(data.get("prompt"));

  await appendAIMessage(async () => {
    const response = await fetch(url, {
      method: "POST",
      body: data,
    });
    const result = await response.json();
    return result.answer;
  });
};

promptForm.addEventListener("submit", handlePrompt);

const handleQuestionClick = async (event) => {
  appendAIMessage(async () => {
    const response = await fetch("/question", {
      method: "GET",
    });
    const result = await response.json();
    const question = result.answer;

    questionButton.dataset.question = question;
    questionButton.classList.add("hidden");
    submitButton.innerHTML = "Répondre à la question";
    return question;
  });
};

const handleQuestionClick2 = async (event) => {
  appendAIMessage(async () => {
    const response = await fetch("/perro", {
      method: "GET",
    });
    const result = await response.json();
    const question = result.answer;

    jrperronnet.dataset.question = question;
    jrperronnet.classList.add("hidden");
    submitButton.innerHTML = "Réponse de JR Perronnet";
    return question;
  });
};

const handleQuestionClick3 = async (event) => {
  appendAIMessage(async () => {
    const response = await fetch("/dormieux", {
      method: "GET",
    });
    const result = await response.json();
    const question = result.answer;

    lucdormieux.dataset.question = question;
    lucdormieux.classList.add("hidden");
    submitButton.innerHTML = "Réponse de Luc Dormieux";
    return question;
  });
};

questionButton.addEventListener("click", handleQuestionClick);
jrperronnet.addEventListener("click", handleQuestionClick2);
lucdormieux.addEventListener("click", handleQuestionClick3);
