// game.js

import { WORDS } from "/static/games/words.js";
import { showFinalMessage, showWinModal, triggerConfetti, shadeKeyBoard, showMessage, animateCSS } from "./ui.js"

// Assign the number of guesses, word length, and other variables
let NUMBER_OF_GUESSES = 6;
let WORD_LENGTH = 5;
let guessesRemaining = NUMBER_OF_GUESSES;
let currentGuess = [];

// Set a random word to be guessed
export let rightGuessString = WORDS[Math.floor(Math.random() * WORDS.length)];
console.log(rightGuessString);

// Function to initialize the game board based on the word length and number of guesses
export function initBoard() {

  const board = document.getElementById("game-board");

  // Loop on the number of guesses to make the boxes row
  for (let i = 0; i < NUMBER_OF_GUESSES; i++) {
    const row = document.createElement("div");
    row.className = "letter-row";

    // Set the boxes on the row based on the new word length
    for (let j = 0; j < WORD_LENGTH; j++) {
      const box = document.createElement("div");
      box.className = "letter-box";
      row.appendChild(box);
    }

    board.appendChild(row);
  }

  if (!WORDS || !Array.isArray(WORDS) || WORDS.length === 0) {
    showMessage("Error: No words available. Please check the word list.");
    return;
  }

}

export function abortGame() {
  guessesRemaining = 0;
  return;
}

// Function to check the user's guess and update the game board accordingly
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
    showFinalMessage("You Won! 🏆");
    triggerConfetti();
    setTimeout(() => {
      showWinModal();
    }, 2000);
    return;
  } else {
    guessesRemaining -= 1;
    currentGuess = [];

    if (guessesRemaining === 0) {
      showFinalMessage("You Lost 😥");
      showMessage("You've run out of guesses! Game over!");
      showMessage(`The right word was: "${rightGuessString}"`);
    }
  }
}

// Function to delete a letter from the current guess
function deleteLetter() {
  const row = document.getElementsByClassName("letter-row")[NUMBER_OF_GUESSES - guessesRemaining];
  const box = row.children[currentGuess.length - 1];
  box.textContent = "";
  box.classList.remove("filled-box");
  currentGuess.pop();
}

// Function to insert a letter into the current guess
function insertLetter(pressedKey) {
  if (currentGuess.length === WORD_LENGTH) {
    return;
  }

  pressedKey = pressedKey.toLowerCase();

  const isLetter = /^[a-z]$/i.test(pressedKey);

  if (!isLetter) {
    return; // Ignore non-letter keys
  }

  const row = document.getElementsByClassName("letter-row")[NUMBER_OF_GUESSES - guessesRemaining];
  const box = row.children[currentGuess.length];
  animateCSS(box, "pulse");
  box.textContent = pressedKey;
  box.classList.add("filled-box");
  currentGuess.push(pressedKey);
}

// Function to update the player's points after winning a game
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
        console.log("Failed to update points. Server responded with:", data);
      }
    })
    .catch(error => {
      console.log("An error occurred while updating points:", error);
    });
}

document.addEventListener("DOMContentLoaded", function () {

  // Function to handle keyboard input
  document.addEventListener("keyup", (e) => {
    if (guessesRemaining === 0) {
      return;
    }

    const pressedKey = String(e.key);

    if (pressedKey === "Backspace" && currentGuess.length !== 0) {
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

  // Handle clicks on the virtual keyboard
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

});

function applySettings() {
  const wordLengthSelect = document.getElementById("word-length");
  const guessesInput = document.getElementById("guesses");

  // Get the selected word length and number of guesses
  const wordLength = parseInt(wordLengthSelect.value);
  const guesses = parseInt(guessesInput.value);

  // Apply the settings to the game
  setWordLength(wordLength);
  setNumberOfGuesses(guesses);

  // Close the settings section
  showSection("Close");
}

function setWordLength(wordLength) {
  WORD_LENGTH = wordLength;
  location.reload(); // Re-initialize the game board with the new word length
}

function setNumberOfGuesses(guesses) {
  NUMBER_OF_GUESSES = guesses;
}