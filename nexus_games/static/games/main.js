// main.js

import { initBoard, abortGame, rightGuessString, updateStats } from "./game.js"
import { showFinalMessage, showLoseModal, showWinModal, showSection, showMessage } from "./ui.js"

document.addEventListener("DOMContentLoaded", function () {

  const menuButtons = document.querySelectorAll(".wordle-menu button");

  // Event listener to surrender and abort the game
  document.getElementById("surrender").addEventListener("click", () => {
    const messageElement = document.getElementById("final-message");
    const isWinMessage = messageElement.textContent.includes("You Won!");

    if (!isWinMessage) {
      abortGame();
      showFinalMessage("You Lost 😥");
      showMessage(`The right word was: "${rightGuessString}"`);
      updateStats(false);
    } else {
      showMessage(`You already won the game! Dumbass!`);
    }
  });

  document.getElementById("final-message").addEventListener("click", () => {
    const messageElement = document.getElementById("final-message");
    const isWinMessage = messageElement.textContent.includes("You Won!");

    if (isWinMessage) {
      showWinModal();
    } else {
      showLoseModal(rightGuessString);
    }
  });

  // Handle clicks on menu buttons
  menuButtons.forEach(button => {
    button.addEventListener("click", () => {
      const sectionTitle = button.title;
      showSection(sectionTitle);
    });
  });

  document.getElementById("apply-settings").addEventListener("click", () => {
    applySettings();
  });

  document.getElementById("close-button").addEventListener("click", () => {
    showSection("Game");
  });

  // Event listener for restart button in modal
  document.querySelectorAll("#restart-button").forEach((button) => {
    button.addEventListener("click", () => {
      // Reload the page to restart the game
      location.reload();
    });
  });

});

// Initialize the game board
initBoard();