// Exemple de script JavaScript pour animer une réunion sur un site web

const meetingScenario = [
    {
        bot: "bot1",
        avatar: "/static/images/bot1_avatar.png",
        message: "Bonjour ! Je vais vous présenter la réunion. Elle portait sur la gestion des parcs éoliens et les caractéristiques liées à leur puissance."
    },
    {
        bot: "bot2",
        avatar: "static/images/bot2_avatar.png",
        message: "Bonjour, je suis Pierre-Emmanuel Vos. Je tiens à m'excuser pour une erreur concernant le site Acrocéan. Nous avons des données météo depuis 2015, ce qui a permis aux industriels de proposer des projets adaptés."
    },
    {
        bot: "bot3",
        avatar: "static/images/bot3_avatar.png",
        message: "Pourquoi ces informations n'ont-elles pas été communiquées plus tôt ?"
    },
    {
        bot: "bot4",
        avatar: "static/images/bot4_avatar.png",
        message: "Les industriels ont avancé malgré tout, en partie grâce aux subventions."
    },
    {
        bot: "bot2",
        avatar: "static/images/bot2_avatar.png",
        message: "Je vais clarifier cela. Les données étaient disponibles via une bouée entre 2015 et 2017. De plus, la loi Essoc garantit un cahier des charges précis pour les projets, avec des objectifs de puissance clairement définis."
    },
    {
        bot: "bot3",
        avatar: "static/images/bot3_avatar.png",
        message: "Selon vous, les caractéristiques des éoliennes peuvent-elles être adaptées pour atteindre un chiffre cible ?"
    },
    {
        bot: "bot2",
        avatar: "static/images/bot2_avatar.png",
        message: "Oui, mais uniquement en termes de nombre d'éoliennes. Si la puissance unitaire des éoliennes augmente, il en faudra moins pour atteindre la puissance globale définie."
    },
    {
        bot: "bot5",
        avatar: "static/images/bot5_avatar.png",
        message: "Dans le cadre de ce débat, on parle d'un parc précis, avec une puissance totale fixe."
    },
    {
        bot: "bot3",
        avatar: "static/images/bot3_avatar.png",
        message: "Donc, si le vent est faible, il faudra peut-être augmenter le nombre d'éoliennes ?"
    },
    {
        bot: "bot5",
        avatar: "static/images/bot5_avatar.png",
        message: "Non, ce n'est pas la puissance du vent qui détermine le nombre d'éoliennes, mais leur puissance unitaire. Par exemple, pour un parc de 1000 mégawatts avec des éoliennes de 20 mégawatts, il faudra 50 éoliennes."
    }
];

// Fonction pour afficher les messages dans un chat simulé
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
