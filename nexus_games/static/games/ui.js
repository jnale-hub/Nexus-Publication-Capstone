// ui.js

// Function to show the final message when the game is over
export function showFinalMessage(message) {
    const finalMessage = document.getElementById("final-message");
    finalMessage.classList.remove("d-none");
    finalMessage.classList.add("d-block");
    finalMessage.textContent = message;

    setTimeout(() => {
        finalMessage.style.opacity = "1";
    }, 10);
}

// Function that shows the section on the menu
export function showSection(sectionTitle) {
    const menuTitle = document.getElementById("menu-title");
    const gameSection = document.getElementById("game");
    const statsSection = document.getElementById("stats");
    const settingsSection = document.getElementById("settings");
    const helpSection = document.getElementById("help");

    const divTitle = document.getElementById("div-title");

    divTitle.style.display = "block";

    document.querySelectorAll(".wordle-menu button").forEach(button => {
        if (button.title.toLowerCase() === sectionTitle.toLowerCase()) {
            button.classList.add("active");
        } else {
            button.classList.remove("active");
        }
    });


    // Show/hide the respective div sections based on the selected button
    switch (sectionTitle) {
        case "Stats":
            statsSection.style.display = "block";
            settingsSection.style.display = "none";
            helpSection.style.display = "none";
            gameSection.style.display = "none";
            break;
        case "Settings":
            statsSection.style.display = "none";
            settingsSection.style.display = "block";
            helpSection.style.display = "none";
            gameSection.style.display = "none";
            break;
        case "Help":
            statsSection.style.display = "none";
            settingsSection.style.display = "none";
            helpSection.style.display = "block";
            gameSection.style.display = "none";
            break;
        default:
            // If the default case is reached, hide all sections except the game section
            statsSection.style.display = "none";
            settingsSection.style.display = "none";
            helpSection.style.display = "none";
            gameSection.style.display = "block";
            document.getElementById("stats-button").classList.remove("active");
            document.getElementById("settings-button").classList.remove("active");
            document.getElementById("help-button").classList.remove("active");
            divTitle.style.display = "none";
    }

    menuTitle.textContent = sectionTitle;
}

// Function to trigger the confetti animation when the user wins
export function triggerConfetti() {
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
        clock: 50,
    };

    const confetti = new ConfettiGenerator(confettiSettings);
    confetti.render();

    setTimeout(() => {
        confetti.clear();
    }, 5000);
}

// Create the function that will change the keybord
export function shadeKeyBoard(letter, color) {
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

const messageQueue = [];
let isShowingMessage = false;
let isKeyPressed = false;

// Function to show a message on the screen
export function showMessage(message) {
    // Add the message to the queue
    messageQueue.push(message);

    // If a message is already being shown or a key is pressed, return
    if (isShowingMessage || isKeyPressed) {
        return;
    }

    // Function to show the next message in the queue
    function showNextMessage() {
        // If there are no more messages in the queue, return
        if (messageQueue.length === 0) {
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
    }

    // Show the next message in the queue
    showNextMessage();

    isShowingMessage = true;
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

export function showWinModal() {
    const winModal = new bootstrap.Modal(document.getElementById("win-modal"));
    winModal.show();
}

// Function to show the lose modal and display the correct word
export function showLoseModal(rightGuessString) {
    const loseModal = new bootstrap.Modal(document.getElementById("lose-modal"));
    const rightWordElement = document.getElementById("right-word");
    rightWordElement.textContent = rightGuessString;
    loseModal.show();
}

export const animateCSS = (element, animation, prefix = "animate__") =>
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

