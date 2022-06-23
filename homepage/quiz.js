console.log("Hello")
const quizFormElement = document.querySelector("#quizForm");

quizFormElement.addEventListener("submit", (submitEvent) => {
    submitEvent.preventDefault();

    const formData = new FormData(submitEvent.target);
    const answer = formData.get("answer");

    if (answer == "2") {
        alert(`Your answer is ${answer}, well done!`);

    } else {
        document.querySelector("#answer").value = "";
        alert(`Your answer is ${answer}, and that is incorrect...`);
    }
})