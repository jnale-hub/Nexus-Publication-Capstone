import { WORDS } from "/static/games/words.js";

// Assign the number of guesses
const NUMBER_OF_GUESSES = 6;
const WORD_LENGTH = 5;
let guessesRemaining = NUMBER_OF_GUESSES;
let currentGuess = [];
let nextLetter = 0;

// Set a random word to be guessed
let rightGuessString = WORDS[Math.floor(Math.random() * WORDS.length)];
console.log(rightGuessString);

// Create the board by the constant number of word length and guesses
function initBoard() {
  const board = document.getElementById("game-board");

  // Loop on the number of guesses to make the boxes row
  for (let i = 0; i < NUMBER_OF_GUESSES; i++) {
    const row = document.createElement("div");
    row.className = "letter-row";

    // Set the boxes on the row to 5
    for (let j = 0; j < WORD_LENGTH; j++) {
      const box = document.createElement("div");
      box.className = "letter-box";
      row.appendChild(box);
    }

    board.appendChild(row);
  }
}

// Create the function tht will change the keybord if it used, etc.
function shadeKeyBoard(letter, color) {
  const elements = document.getElementsByClassName("keyboard-button");

  for (const elem of elements) {
    if (elem.textContent === letter) {
      const oldColor = elem.style.backgroundColor;
      if (oldColor === "green" || (oldColor === "goldenrod" && color !== "green")) {
        return;
      }

      elem.style.backgroundColor = color;
      elem.style.color = "white";
      break;
    }
  }
}

function deleteLetter() {
  const row = document.getElementsByClassName("letter-row")[NUMBER_OF_GUESSES - guessesRemaining];
  const box = row.children[nextLetter - 1];
  box.textContent = "";
  box.classList.remove("filled-box");
  currentGuess.pop();
  nextLetter -= 1;
}

document.addEventListener("DOMContentLoaded", function() {
  // Add the click event listener to the final-message element
  const finalMessageElement = document.getElementById("final-message");
  finalMessageElement.addEventListener("click", toggleModal);

  document.getElementById("surrender").addEventListener("click", () => {
    guessesRemaining = 0;
    showFinalMessage("You Lost 😥");
    showMessage(`The right word was: "${rightGuessString}"`);
  });
});


function toggleModal() {
  const messageElement = document.getElementById("final-message");
  const isWinMessage = messageElement.textContent.includes("You Win!");

  if (isWinMessage) {
    showWinModal();
  } else {
    showLoseModal(rightGuessString);
  }
}

// Keep track of queued messages
const messageQueue = [];
let isShowingMessage = false;
let isKeyPressed = false;

function showMessage(message) {
  // Add the message to the queue
  messageQueue.push(message);

  // If a message is already being shown, return
  if (isShowingMessage) {
    return;
  }

  // Show the next message in the queue
  showNextMessage();
}

function showNextMessage() {
  // If there are no more messages in the queue, return
  if (messageQueue.length === 0 || isKeyPressed) {
    isShowingMessage = false;
    return;
  }

  // Get the next message from the queue
  const message = messageQueue.shift();

  // Update the message element with the new message
  const messageElement = document.getElementById("message");
  messageElement.textContent = message;
  messageElement.classList.remove("modal-fade-out");
  messageElement.classList.add("modal-fade-in");
  messageElement.style.display = "block";

  setTimeout(() => {
    messageElement.classList.remove("modal-fade-in");
    messageElement.classList.add("modal-fade-out");

    setTimeout(() => {
      messageElement.style.display = "none";
      // Show the next message in the queue
      showNextMessage();
    }, 300);
  }, 1500); // Adjust the delay as per your preference

  isShowingMessage = true;
}

// Function to show the final message
function showFinalMessage(message) {
  const finalMessage = document.getElementById("final-message");
  finalMessage.classList.remove("d-none");
  finalMessage.classList.add("d-block");
  finalMessage.textContent = message;

  setTimeout(() => {
    finalMessage.style.opacity = "1";
  }, 10);
}

// Add an event listener for keydown event to stop showing messages
document.addEventListener("keydown", () => {
  isKeyPressed = true;
  // Clear the message queue and hide the message element
  messageQueue.length = 0;
  const messageElement = document.getElementById("message");
  messageElement.style.display = "none";
});

// Reset the isKeyPressed flag on keyup event
document.addEventListener("keyup", () => {
  isKeyPressed = false;
});

// Modify the checkGuess function
function checkGuess() {
  const row = document.getElementsByClassName("letter-row")[NUMBER_OF_GUESSES - guessesRemaining];
  const guessString = currentGuess.join("");
  const rightGuess = Array.from(rightGuessString);

  if (guessString.length !== WORD_LENGTH) {
    showMessage("Not enough letters!");
    return;
  }

  if (!WORDS.includes(guessString)) {
    showMessage("Word not in list!");
    return;
  }

  const letterColor = Array(5).fill("darkgray");

  // Check green
  for (let i = 0; i < WORD_LENGTH; i++) {
    if (rightGuess[i] === currentGuess[i]) {
      letterColor[i] = "green";
      rightGuess[i] = "#";
    }
  }

  // Check yellow
  for (let i = 0; i < WORD_LENGTH; i++) {
    if (letterColor[i] === "green") continue;

    for (let j = 0; j < WORD_LENGTH; j++) {
      if (rightGuess[j] === currentGuess[i]) {
        letterColor[i] = "goldenrod";
        rightGuess[j] = "#";
      }
    }
  }

  for (let i = 0; i < WORD_LENGTH; i++) {
    const box = row.children[i];
    const delay = 250 * i;
    setTimeout(() => {
      animateCSS(box, "flipInX");
      box.style.backgroundColor = letterColor[i];
      box.style.borderColor = letterColor[i];
      box.style.color = "white";
      shadeKeyBoard(guessString.charAt(i), letterColor[i]);
    }, delay);
  }

  if (guessString === rightGuessString) {
    // Show the win modal and update points
    updatePoints();
    showFinalMessage("You Win! 🏆");
    triggerConfetti();
    setTimeout(() => {
      showWinModal();
    }, 2000);
    return;
  } else {
    guessesRemaining -= 1;
    currentGuess = [];
    nextLetter = 0;

    if (guessesRemaining === 0) {
      showFinalMessage("You Lost 😥");
      showMessage("You've run out of guesses! Game over!");
      showMessage(`The right word was: "${rightGuessString}"`);
    }
  }
}

// Function to show the win modal
// ... Your existing JavaScript code ...

// Function to show the win modal and trigger the confetti animation
function showWinModal() {
  const winModal = new bootstrap.Modal(document.getElementById("win-modal"));
  winModal.show();
}

// Function to trigger the confetti animation
function triggerConfetti() {
  const confettiSettings = {
    target: "confetti-canvas",
    max: 80,
    size: 2,
    animate: true,
    props: ["circle", "square", "triangle", "line"],
    colors: [
      [165, 104, 246],
      [230, 61, 135],
      [0, 199, 228],
      [253, 214, 126],
    ],
    clock: 25,
  };

  const confetti = new ConfettiGenerator(confettiSettings);
  confetti.render();
}

function showLoseModal(rightGuessString) {
  const loseModal = new bootstrap.Modal(document.getElementById("lose-modal"));
  const rightWordElement = document.getElementById("right-word");
  rightWordElement.textContent = rightGuessString;
  loseModal.show();
}

// Add event listener for restart button in modal
document.querySelectorAll("#restart-button").forEach(button => {
  button.addEventListener("click", () => {
    // Reload the page to restart the game
    location.reload();
  });
});


// Function to update points
function updatePoints() {
  fetch("/update-points/", {
    method: "POST",
  })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        const newPoints = parseInt(data.points);
        const pointsElements = document.querySelectorAll("#points-num");
        pointsElements.forEach(element => {
          element.textContent = newPoints;
        });
        console.log("Points updated successfully");
      } else {
        console.log("Failed to update points");
      }
    })
    .catch(error => {
      console.log("An error occurred while updating points:", error);
    });
}

function insertLetter(pressedKey) {
  if (nextLetter === 5) {
    return;
  }

  pressedKey = pressedKey.toLowerCase();

  const isLetter = /^[a-z]$/i.test(pressedKey);
  
  if (!isLetter) {
    return; // Ignore non-letter keys
  }

  const row = document.getElementsByClassName("letter-row")[NUMBER_OF_GUESSES - guessesRemaining];
  const box = row.children[nextLetter];
  animateCSS(box, "pulse");
  box.textContent = pressedKey;
  box.classList.add("filled-box");
  currentGuess.push(pressedKey);
  nextLetter += 1;
}

const animateCSS = (element, animation, prefix = "animate__") =>
  new Promise((resolve, reject) => {
    const animationName = `${prefix}${animation}`;
    const node = element;
    node.style.setProperty("--animate-duration", "0.3s");

    node.classList.add(`${prefix}animated`, animationName);

    function handleAnimationEnd(event) {
      event.stopPropagation();
      node.classList.remove(`${prefix}animated`, animationName);
      resolve("Animation ended");
    }

    node.addEventListener("animationend", handleAnimationEnd, { once: true });
  });

document.addEventListener("keyup", (e) => {
  if (guessesRemaining === 0) {
    return;
  }

  const pressedKey = String(e.key);

  if (pressedKey === "Backspace" && nextLetter !== 0) {
    deleteLetter();
    return;
  }

  if (pressedKey === "Enter") {
    checkGuess();
    return;
  }

  const found = pressedKey.match(/[a-z]/gi);

  if (!found || found.length > 1) {
    return;
  } else {
    insertLetter(pressedKey);
  }
});

document.getElementById("keyboard-cont").addEventListener("click", (e) => {
  const target = e.target;

  if (!target.classList.contains("keyboard-button")) {
    return;
  }

  let key = target.textContent;

  if (key === "Del") {
    key = "Backspace";
  }

  document.dispatchEvent(new KeyboardEvent("keyup", { key }));
});

initBoard();
