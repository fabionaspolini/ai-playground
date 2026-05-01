# Prompt: Réplica Funcional do Flappy Bird

## Contexto e Objetivo

Você é um desenvolvedor front-end especialista em jogos 2D com Canvas API. Sua tarefa é construir uma réplica **completamente funcional** do jogo **Flappy Bird**, utilizando exclusivamente **HTML5, CSS3 e JavaScript Vanilla (sem nenhuma biblioteca ou framework externo)**. Todo o código deve estar em um **único arquivo `.html`** autocontido.

---

## Restrições Técnicas Absolutas

- ✅ HTML5 (incluindo `<canvas>`)
- ✅ CSS3 puro
- ✅ JavaScript Vanilla (ES6+)
- ❌ Nenhuma biblioteca externa (sem jQuery, Phaser, p5.js, etc.)
- ❌ Nenhuma requisição de rede (sem fetch, CDN, fontes do Google)
- ❌ Nenhum arquivo separado — tudo em um único `.html`

---

## Especificações Visuais

### Paleta de Cores (estilo pixel art retrô)
- **Céu:** gradiente de `#70C5CE` → `#C9E8F0`
- **Chão:** `#DED895` (topo) com `#9FB52A` (faixa de grama)
- **Canos:** `#74BF2E` com borda `#588A20` e topo arredondado mais largo
- **Pássaro:** corpo amarelo-alaranjado (`#F5A623`), asa mais clara, olho branco com pupila preta, bico laranja-avermelhado

### Elementos Visuais Obrigatórios
1. **Fundo com nuvens** desenhadas no canvas, animadas em parallax lento (mais lentas que os canos)
2. **Chão animado** com scroll contínuo, com textura de grama no topo
3. **Pássaro com animação de asa** — a asa deve bater ciclicamente (3 frames: cima, meio, baixo), e o corpo deve inclinar para cima no flap e cair gradualmente (rotação proporcional à velocidade vertical)
4. **Canos com "chapéu"** — a extremidade de cada cano tem um bloco mais largo e mais alto (estilo cano do Mario/Flappy Bird original)
5. **Partículas de pena** ao colidir (opcional mas valorizado)

---

## Mecânicas de Jogo

### Física do Pássaro
```
GRAVITY = 0.5          // aceleração por frame
FLAP_FORCE = -9        // velocidade vertical ao pular (negativo = sobe)
MAX_FALL_SPEED = 12    // velocidade máxima de queda
ROTATION_MAX_UP = -30° // inclinação máxima subindo
ROTATION_MAX_DOWN = 90°// inclinação máxima caindo
```

### Canos
```
PIPE_WIDTH = 80px
PIPE_GAP = 160px       // espaço vertical entre cano superior e inferior
PIPE_SPEED = 3px/frame // velocidade horizontal inicial
PIPE_SPAWN_INTERVAL = 1800ms
GAP_Y_MIN = 120px      // distância mínima do topo para o gap
GAP_Y_MAX = canvas.height - GROUND_HEIGHT - 120px
```

### Dificuldade Progressiva
- A cada **10 pontos**, aumentar `PIPE_SPEED` em `+0.3` (máximo de `7`)
- A cada **10 pontos**, reduzir `PIPE_SPAWN_INTERVAL` em `100ms` (mínimo de `1000ms`)

### Colisão
- Usar **hitbox reduzida** (80% do tamanho visual do pássaro) para sensação mais justa
- Colisão com: cano superior, cano inferior, chão, teto (opcional, mas recomendado)
- Ao colidir: parar o jogo, exibir tela de Game Over com animação

### Pontuação
- +1 ponto ao **ultrapassar completamente** um par de canos (centro do pássaro passa o eixo X do centro do cano)
- Exibir score centralizado no topo durante o jogo (fonte grande, com sombra)

---

## Estados do Jogo

O jogo deve ter **3 estados distintos**, controlados por uma variável `gameState`:

### 1. `'idle'` — Tela Inicial
- Logo "Flappy Bird" estilizado desenhado no canvas (ou texto grande)
- Pássaro flutuando com animação senoidal suave (hovering)
- Texto "Toque ou pressione ESPAÇO para jogar" piscando
- Canos **não aparecem**, fundo e chão animam normalmente

### 2. `'playing'` — Jogo Ativo
- Física completa ativa
- Canos surgem e se movem
- Score atualiza em tempo real
- Input: `SPACE`, `ArrowUp`, `W`, clique/toque → flap

### 3. `'gameover'` — Tela de Game Over
- Animação do pássaro caindo até o chão (gravidade ainda ativa, sem input)
- Após pássaro atingir o chão: parar tudo e exibir painel central com:
  - Texto "GAME OVER"
  - Score atual
  - Melhor score (salvo em `localStorage`)
  - Botão ou instrução "Pressione ESPAÇO para reiniciar"
- Transição suave (fade in do painel)

---

## Sistema de Áudio (Web Audio API)

Implementar sons **sintetizados via Web Audio API** (sem arquivos externos):

```javascript
// Flap: oscilador curto, frequência alta
function playFlap() { /* onda senoidal, freq 600Hz, duração 0.1s */ }

// Ponto: som de "ding" agradável
function playScore() { /* onda senoidal, freq 800→1200Hz, duração 0.15s */ }

// Morte: som descendente grave
function playDie() { /* onda sawtooth, freq 400→100Hz, duração 0.4s */ }

// Hit: impacto curto
function playHit() { /* onda quadrada, freq 200Hz, duração 0.1s */ }
```

> Inicializar o `AudioContext` apenas após o **primeiro gesto do usuário** (clique ou teclado) para respeitar a política de autoplay dos browsers.

---

## Loop de Jogo

Implementar com `requestAnimationFrame`. Estrutura obrigatória:

```javascript
function gameLoop(timestamp) {
  const deltaTime = timestamp - lastTimestamp;
  lastTimestamp = timestamp;

  update(deltaTime); // lógica
  render();          // desenho

  requestAnimationFrame(gameLoop);
}
```

- O `update` deve ser **independente do framerate** — usar `deltaTime` para normalizar a física quando possível
- O `render` deve sempre limpar o canvas antes de redesenhar (`ctx.clearRect`)
- **Ordem de desenho (back to front):** fundo → nuvens → canos → chão → pássaro → UI/score

---

## Interface e UX

### Canvas
- Tamanho fixo: **400×600px** (proporção retrato, estilo mobile)
- Centralizado na página com `display: flex` no body
- Fundo da página: cor escura neutra (`#1a1a2e`) para contraste

### Responsividade
- O canvas deve **escalar proporcionalmente** via CSS (`max-width: 100%; height: auto`) para funcionar em mobile sem quebrar a lógica interna

### Inputs

| Ação | Triggers |
|------|----------|
| Flap | `Space`, `ArrowUp`, `W`, `click`, `touchstart` |
| Reiniciar (game over) | `Space`, `click`, `touchstart` |

---

## Estrutura do Código

Organizar o JavaScript em seções claras com comentários:

```
// ─── CONSTANTES ──────────────────────────────────
// ─── ESTADO DO JOGO ──────────────────────────────
// ─── ÁUDIO ───────────────────────────────────────
// ─── PÁSSARO ─────────────────────────────────────
// ─── CANOS ───────────────────────────────────────
// ─── NUVENS ──────────────────────────────────────
// ─── CHÃO ────────────────────────────────────────
// ─── COLISÃO ─────────────────────────────────────
// ─── RENDER ──────────────────────────────────────
// ─── UPDATE ──────────────────────────────────────
// ─── INPUT ───────────────────────────────────────
// ─── INICIALIZAÇÃO ───────────────────────────────
// ─── LOOP PRINCIPAL ──────────────────────────────
```

---

## Critérios de Aceitação

O jogo está completo quando:

- [ ] Roda em um único arquivo `.html` sem dependências externas
- [ ] Os 3 estados (idle, playing, gameover) funcionam corretamente
- [ ] A física do pássaro (gravidade, flap, rotação) é fluida e responsiva
- [ ] Canos geram com gap aleatório e colisão funciona corretamente
- [ ] Score incrementa e melhor score persiste via `localStorage`
- [ ] Dificuldade aumenta progressivamente
- [ ] Animação do pássaro (asa + rotação) está implementada
- [ ] Sons sintetizados funcionam no primeiro gesto
- [ ] Funciona em desktop (teclado + mouse) e mobile (touch)
- [ ] Nenhum erro no console durante o gameplay normal

---

Gere o código completo, funcional e bem comentado, em um único bloco de código HTML.
