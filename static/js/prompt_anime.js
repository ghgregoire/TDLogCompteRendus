const meetingScenario = [
    {
        bot: "bot1",
        avatar: "/static/images/bot1_avatar.png",
        message: "Dans mon entreprise précédente, les réunions d'équipe étaient monotones. Chacun rendait compte de ses avancées au manager pendant que les autres étaient ailleurs. Nous avons décidé de changer cela en faisant tourner le rôle d'animateur chaque semaine.",
    },
    {
        bot: "bot2",
        avatar: "/static/images/bot2_avatar.png",
        message: "Ce changement a apporté de nombreux bénéfices. Les responsabilités étaient partagées, les animations étaient variées et adaptées à chacun. Cela a favorisé une meilleure collaboration et une écoute accrue au sein de l'équipe.",
    },
    {
        bot: "bot3",
        avatar: "/static/images/bot3_avatar.png",
        message: "La réunion d'équipe est ainsi devenue un véritable moment d'échange et de partage pour tout le groupe, favorisant un esprit d'équipe renforcé. Ce modèle a permis à chacun de s'impliquer activement dans les discussions et les décisions prises.",
    }
];
function displayScenario(scenario) {
    const chatContainer = document.getElementById('chat-container');

    scenario.forEach((entry, index) => {
        setTimeout(() => {
            const messageDiv = document.createElement('div');
            messageDiv.classList.add('chat-message');

            const avatarImg = document.createElement('img');
            avatarImg.src = entry.avatar;
            avatarImg.alt = `${entry.bot} avatar`;
            avatarImg.classList.add('chat-avatar');

            const textDiv = document.createElement('div');
            textDiv.classList.add('chat-text');
            textDiv.innerHTML = `<strong>${entry.bot}:</strong> ${entry.message}`;

            messageDiv.appendChild(avatarImg);
            messageDiv.appendChild(textDiv);
            chatContainer.appendChild(messageDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }, index * 3000); // Affiche chaque message avec un délai de 3 secondes
    });
}

// Appeler la fonction pour lancer le scénario
window.onload = () => {
    displayScenario(meetingScenario);
};