# Prompt: Desenvolvimento Detalhado de Clone Flappy Bird (Vanilla JS)

**Atue como um Desenvolvedor de Jogos Web Sênior.** O objetivo é criar uma réplica completa e funcional do jogo "Flappy Bird" utilizando exclusivamente **HTML5, CSS3 e JavaScript Puro (Vanilla JS)**. Você deve gerar um código de alta qualidade, legível e totalmente focado na lógica, sem depender de assets externos (imagens ou sons).

### 1. Requisitos Técnicos e Arquitetura:
* **Renderização:** Utilize a **HTML5 Canvas API**. Nenhuma biblioteca externa é permitida.
* **Estrutura:** O código deve estar em um único arquivo `index.html`. O CSS deve estar na tag `<style>` e o JavaScript na tag `<script>`.
* **Organização (ES6):** Crie constantes no topo do script para todas as variáveis de jogo (gravidade, força do pulo, velocidade dos canos, etc.) para facilitar o balanceamento.
* **Game Loop:** Utilize `requestAnimationFrame` para atualizar a física e renderizar os quadros.

### 2. Estados do Jogo (State Machine):
O jogo deve ter 3 estados claros:
1. **START:** Tela inicial aguardando o primeiro clique/toque para começar. Mostra o título e "Clique para iniciar".
2. **PLAYING:** O pássaro cai, os canos se movem e a colisão está ativa.
3. **GAME OVER:** O pássaro congela ou cai até o chão. Mostra o "Score" atual, o "High Score" (salvo no LocalStorage) e um botão/texto "Clique para reiniciar".

### 3. Mecânicas e Física:
* **Controles:** O pulo deve ser ativado ao pressionar a tecla "Espaço", "Seta para Cima", clique do mouse ou toque na tela (Touch).
* **O Pássaro (Bird):**
  * Posicionado fixamente no eixo X (ex: 20% da largura da tela). Movimenta-se apenas no eixo Y.
  * Deve ter uma variável de `velocidadeY` que aumenta constantemente devido a uma `gravidade` (ex: +0.6 por frame).
  * Ao pular, a `velocidadeY` recebe um impulso negativo instantâneo (ex: -8).
  * **Animação:** A inclinação visual do pássaro deve mudar com base na sua `velocidadeY` (apontar para cima ao pular, apontar para baixo ao cair).
* **Os Canos (Pipes):**
  * Devem ser gerados proceduralmente (ex: a cada 100 frames).
  * Movimentam-se da direita para a esquerda a uma velocidade constante.
  * Cada obstáculo é composto por um cano superior e um inferior.
  * O espaço (gap) entre o cano superior e o inferior deve ser **sempre fixo e do mesmo tamanho** (ex: 150px), o que varia aleatoriamente é a posição vertical do gap na tela.
  * Remova da memória os canos que saírem da tela pela esquerda para evitar vazamento de memória.

### 4. Regras de Colisão e Pontuação:
* **Colisão (AABB):** O "Game Over" ocorre se a caixa de colisão do pássaro tocar em:
  1. Qualquer parte de um cano (superior ou inferior).
  2. O limite inferior da tela (Chão).
  3. O limite superior da tela (Teto - opcionalmente, ele apenas não pode passar do Y=0).
* **Pontuação:** O jogador ganha +1 ponto no exato momento em que o eixo X do pássaro ultrapassa o eixo X do cano (centro ou borda direita). Garanta que a pontuação conte apenas uma vez por cano.

### 5. Interface e Identidade Visual (Apenas Código):
* Como não haverá imagens, desenhe as entidades usando métodos do Canvas (`fillRect`, `arc`):
  * **Cenário:** Fundo azul claro (`#70C5CE`) e um retângulo verde/marrom na parte inferior simulando o chão. O chão deve dar a ilusão de movimento.
  * **Pássaro:** Desenhe como um círculo amarelo (`#F1C40F`) com um pequeno detalhe (um olho ou bico) para deixar claro a direção para onde está olhando.
  * **Canos:** Retângulos verdes (`#2ECC71`) com uma borda ligeiramente mais escura e uma "tampa" um pouco mais larga nas pontas para simular a boca do cano.
* **UI:** A pontuação atual deve ser desenhada com `fillText` no centro-superior da tela em branco com uma sombra/borda preta, usando uma fonte grossa (ex: Arial Black, sans-serif).

### Entrega Final:
Escreva o conteúdo completo do arquivo `index.html`. Certifique-se de que o código é autossuficiente, responsivo (canvas ajustável à janela do navegador), e que funciona perfeitamente assim que o arquivo é aberto. Não omita a lógica, forneça a implementação de ponta a ponta.
