// Seleciona os elementos principais do chatbot
const abrirTryx = document.getElementById("abrirTryx");
const fecharTryx = document.getElementById("fecharTryx");
const tryxChatBox = document.getElementById("tryxChatBox");
const tryxMessages = document.getElementById("tryxMessages");
const tryxInput = document.getElementById("tryxInput");
const enviarTryx = document.getElementById("enviarTryx");

// Abre o chatbot
abrirTryx.addEventListener("click", () => {
    tryxChatBox.classList.add("ativo");
});

// Fecha o chatbot
fecharTryx.addEventListener("click", () => {
    tryxChatBox.classList.remove("ativo");
});

// Envia mensagem ao clicar no botão
enviarTryx.addEventListener("click", enviarMensagem);

// Envia mensagem apertando Enter
tryxInput.addEventListener("keypress", (evento) => {
    if (evento.key === "Enter") {
        enviarMensagem();
    }
});

// Função principal para enviar a mensagem
function enviarMensagem() {
    const mensagem = tryxInput.value.trim();

    if (mensagem === "") {
        return;
    }

    adicionarMensagemUsuario(mensagem);
    tryxInput.value = "";

    setTimeout(() => {
        const resposta = gerarRespostaTryx(mensagem);
        adicionarMensagemBot(resposta);
    }, 700);
}

// Função usada pelos botões de sugestão
function enviarSugestao(texto) {
    tryxInput.value = texto;
    enviarMensagem();
}

// Adiciona mensagem do usuário na tela
function adicionarMensagemUsuario(texto) {
    const mensagem = document.createElement("div");
    mensagem.classList.add("tryx-message", "tryx-user");

    mensagem.innerHTML = `<p>${texto}</p>`;

    tryxMessages.appendChild(mensagem);
    rolarParaFinal();
}

// Adiciona mensagem da TRYX na tela
function adicionarMensagemBot(texto) {
    const mensagem = document.createElement("div");
    mensagem.classList.add("tryx-message", "tryx-bot");

    mensagem.innerHTML = `<p>${texto}</p>`;

    tryxMessages.appendChild(mensagem);
    rolarParaFinal();
}

// Mantém o chat sempre no final
function rolarParaFinal() {
    tryxMessages.scrollTop = tryxMessages.scrollHeight;
}

// Gera respostas simples da TRYX com base no texto do usuário
function gerarRespostaTryx(mensagem) {
    const texto = mensagem.toLowerCase();

    if (
        texto.includes("gás") ||
        texto.includes("gas") ||
        texto.includes("vazamento") ||
        texto.includes("cheiro") ||
        texto.includes("alerta")
    ) {
        return `
            Entendi. Se você recebeu um alerta ou sente cheiro de gás, mantenha a calma.
            Abra portas e janelas, evite acender luzes ou ligar aparelhos elétricos,
            afaste-se do local e acione o suporte ou emergência se necessário.
            A SENTRYX ajuda no monitoramento, mas a segurança física vem sempre em primeiro lugar.
        `;
    }

    if (
        texto.includes("offline") ||
        texto.includes("wi-fi") ||
        texto.includes("wifi") ||
        texto.includes("conexão") ||
        texto.includes("internet")
    ) {
        return `
            Vamos verificar a conexão do seu sensor. Confirme se o Wi-Fi está funcionando,
            se o dispositivo está ligado e se ele está dentro do alcance do roteador.
            Depois, tente reiniciar o sensor e aguarde alguns segundos para ele reconectar.
        `;
    }

    if (
        texto.includes("instalar") ||
        texto.includes("instalação") ||
        texto.includes("configurar") ||
        texto.includes("sensor")
    ) {
        return `
            Para instalar o sensor SENTRYX, escolha um local próximo ao ambiente monitorado,
            conecte o dispositivo à energia, configure a rede Wi-Fi e faça um teste de funcionamento.
            Também posso te direcionar para o guia completo de instalação.
        `;
    }

    if (
        texto.includes("bateria") ||
        texto.includes("pilha") ||
        texto.includes("energia")
    ) {
        return `
            Se o sensor estiver com baixa energia, verifique a fonte de alimentação ou a bateria,
            dependendo do modelo utilizado. Recomendo manter o dispositivo sempre ativo
            para garantir o monitoramento contínuo do ambiente.
        `;
    }

    if (
        texto.includes("documentação") ||
        texto.includes("manual") ||
        texto.includes("garantia") ||
        texto.includes("termos")
    ) {
        return `
            Você pode acessar a central de documentos da SENTRYX para consultar manuais,
            garantia, termos de uso e especificações técnicas do dispositivo.
        `;
    }

    if (
        texto.includes("humano") ||
        texto.includes("atendente") ||
        texto.includes("suporte") ||
        texto.includes("whatsapp") ||
        texto.includes("email") ||
        texto.includes("e-mail")
    ) {
        return `
            Claro! Posso te encaminhar para nosso suporte humano.
            Você pode entrar em contato pelo WhatsApp ou enviar um e-mail para nossa equipe técnica.
        `;
    }

    if (
        texto.includes("oi") ||
        texto.includes("olá") ||
        texto.includes("ola") ||
        texto.includes("bom dia") ||
        texto.includes("boa tarde") ||
        texto.includes("boa noite")
    ) {
        return `
            Olá! Eu sou a TRYX, assistente inteligente da SENTRYX.
            Me diga o que você precisa: alerta de gás, instalação, sensor offline,
            documentação ou suporte humano.
        `;
    }

    return `
        Entendi sua dúvida. No momento, posso te ajudar com alertas de gás,
        instalação do sensor, conexão Wi-Fi, documentação e contato com suporte humano.
        Pode me explicar com mais detalhes o que está acontecendo?
    `;
}