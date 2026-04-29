# Prompt: Desenvolvimento de Clone Flappy Bird (Vanilla JS)

**Atue como um Desenvolvedor de Jogos Web Sênior.** O objetivo é criar uma réplica completa e funcional do jogo "Flappy Bird" utilizando exclusivamente **HTML5, CSS3 e JavaScript Puro (Vanilla JS)**.

### Requisitos Técnicos:
1. **Renderização:** Utilize a **HTML5 Canvas API**. Não utilize bibliotecas externas (como Phaser ou PixiJS).
2. **Arquitetura:** - Utilize uma estrutura baseada em Objetos ou Classes (ES6) para representar o Pássaro, os Canos e o Cenário.
   - Implemente um **Game Loop** robusto usando `requestAnimationFrame`.
3. **Persistência:** Salve o "Recorde" (High Score) no **LocalStorage**.

### Mecânicas de Jogo:
* **Física:** Implemente gravidade acumulativa e um impulso vertical instantâneo ao detectar clique ou tecla "Espaço".
* **Obstáculos:** Gerador de canos procedurais com espaçamento vertical fixo e posicionamento aleatório.
* **Colisão:** Detecção de colisão por retângulo (AABB) entre o pássaro e os canos/chão.
* **Interface (UI):** Renderize a pontuação atual no topo do canvas e crie um modal de "Game Over" em HTML/CSS sobreposto ao Canvas.

### Entrega de Código:
1. Somente um `index.html` contendo a estrutura e o CSS necessário.
2. Um código javascript deve estar na tag `<script>`.
3. O código deve ser autossuficiente e rodar apenas abrindo o arquivo no navegador.
4. Use cores sólidas ou gradientes para os gráficos (assets) para que o jogo seja funcional sem arquivos de imagem externos.

### Critérios de Qualidade:
* O jogo deve ser responsivo (ajustar o tamanho do canvas para diferentes telas).
* O código deve ser limpo, evitando variáveis globais desnecessárias e utilizando boas práticas de organização.
